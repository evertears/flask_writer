from flask import current_app, url_for, session, jsonify
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from datetime import datetime
from markdown import markdown
import re

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    pages = db.relationship('Page', backref='user', lazy='dynamic')
    about_me = db.Column(db.String(140))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"User({self.username})"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=True)
    dir_path = db.Column(db.String(500), nullable=True)
    path = db.Column(db.String(500), nullable=True)
    parent_id = db.Column(db.Integer(), db.ForeignKey('page.id'), nullable=True)
    child = db.relationship('Page', remote_side=[id], backref='children')
    template = db.Column(db.String(100))
    banner = db.Column(db.String(500), nullable=True)
    body = db.Column(db.String(10000000))
    tags = db.relationship('Tag', secondary=tags, lazy='subquery', 
            backref=db.backref('pages', lazy=True))
    summary = db.Column(db.String(300), nullable=True)
    sidebar = db.Column(db.String(1000), nullable=True)
    user_id = db.Column('User', db.ForeignKey('user.id'), nullable=False)
    sort = db.Column(db.Integer(), nullable=False, default=75)
    pub_date = db.Column(db.DateTime(), nullable=True)
    published = db.Column(db.Boolean(), default=False)
    edit_date = db.Column(db.DateTime(), index=True, default=datetime.utcnow)

    TEMPLATE_CHOICES = [
        ('page', 'Page'),
        ('post', 'Post'),
        ('story', 'Story'),
        ('book', 'Book'),
        ('chapter', 'Chapter'),
        ('blog', 'Blog'),
    ]

    def parent(self):
        return Page.query.filter_by(id=self.parent_id).first()

    def set_path(self):
        if self.parent_id:
            print(f"PARENT ID: {self.parent_id}")
            parent = Page.query.filter_by(id=self.parent_id).first()
            print(f"PARENT: {parent}")
            try:
                parent_path = parent.path
            except AttributeError:
                parent.set_path()
            self.path = f"{parent.path}/{self.slug}"
            self.dir_path = parent.path

        else:
            self.path = f"/{self.slug}"
            self.dir_path = "/"

    def html_body(self):
        return markdown(self.body)

    def html_sidebar(self):
        return markdown(self.sidebar)
    
    def banner_path(self):
        if not self.banner and (self.template is 'chapter' or self.template is 'post'):
            return self.parent().banner
        return self.banner

    def pub_children(self):
        return Page.query.filter_by(parent_id=self.id,published=True).order_by('sort','pub_date','title').all()

    def ancestors(self):
        ancestors = []
        parent = Page.query.filter_by(id=self.parent_id).first()
        if parent:
            ancestors.append(parent)
            for p in parent.ancestors():
                ancestors.append(p)
        return ancestors

    def descendents(self):
        descendents = []
        children = Page.query.filter_by(parent_id=self.id).all()
        for child in children:
            descendents.append(child)
            for c in child.all_children():
                descendents.append(c)
        return descendents

    def word_count(self):
        try:
            return self.words
        except:
            words = len(re.findall("[a-zA-Z]+", self.body))
            read_time = str(round(words / 200)) + " - " + str(round(words / 150)) + " mins."
            self.words = words
        return self.words

    def read_time(self):
        words = self.word_count()
        return str(round(words / 200)) + " - " + str(round(words / 150)) + " mins."

    def child_word_count(self):
        try:
            return self.child_words
        except:
            words = 0
            for child in self.children:
                words += child.word_count()
            self.child_words = words
        return self.child_words

    def child_read_time(self):
        words = self.child_word_count()
        return str(round(words / 200)) + " - " + str(round(words / 150)) + " mins."
    
    def nav_list(self):
        nav = []
        return nav

    def top_nav(force=False):
        if not 'nav' in session or not len(session['nav']) or force:
            nav = []
            top_pages = Page.query.filter_by(published=True,parent_id=0).order_by('sort','pub_date','title').all()
            for top_page in top_pages:
                page = {
                        'id': top_page.id,
                        'title': top_page.title,
                        'path': top_page.path,
                        'children': [],
                    }
                for child in top_page.pub_children():
                    kid = {
                            'id': child.id,
                            'title': child.title,
                            'path': child.path,
                            'children': [],
                        }
                    for grandchild in child.pub_children():
                        kid['children'].append({
                                'id': grandchild.id,
                                'title': grandchild.title,
                                'path': grandchild.path,
                                'children': [],
                             })
                    page['children'].append(kid)
                nav.append(page)

            session['nav'] = nav


    def __str__(self):
        return f"{self.title} ({self.path})"

    def __repr__(self):
        return f"Page({self.id}, {self.title}, {self.path})"

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75), nullable=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Tag({self.name})"

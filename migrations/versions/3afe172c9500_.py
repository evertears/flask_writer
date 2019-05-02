"""empty message

Revision ID: 3afe172c9500
Revises: bb966775ad65
Create Date: 2019-05-02 14:22:17.456079

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3afe172c9500'
down_revision = 'bb966775ad65'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('page_version',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Page', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('slug', sa.String(length=200), nullable=True),
    sa.Column('dir_path', sa.String(length=500), nullable=True),
    sa.Column('path', sa.String(length=500), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('template', sa.String(length=100), nullable=True),
    sa.Column('banner', sa.String(length=500), nullable=True),
    sa.Column('body', sa.String(length=10000000), nullable=True),
    sa.Column('summary', sa.String(length=300), nullable=True),
    sa.Column('sidebar', sa.String(length=1000), nullable=True),
    sa.Column('User', sa.Integer(), nullable=False),
    sa.Column('sort', sa.Integer(), nullable=False),
    sa.Column('pub_date', sa.DateTime(), nullable=True),
    sa.Column('published', sa.Boolean(), nullable=True),
    sa.Column('edit_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['Page'], ['page.id'], ),
    sa.ForeignKeyConstraint(['User'], ['user.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['page.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_page_version_edit_date'), 'page_version', ['edit_date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_page_version_edit_date'), table_name='page_version')
    op.drop_table('page_version')
    # ### end Alembic commands ###

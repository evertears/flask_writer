"""Add subscriber model

Revision ID: f30c4ce8ccb3
Revises: 69d100fb2b85
Create Date: 2019-05-05 06:30:37.626337

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f30c4ce8ccb3'
down_revision = '69d100fb2b85'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscriber',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('first_name', sa.String(length=75), nullable=True),
    sa.Column('last_name', sa.String(length=75), nullable=True),
    sa.Column('subscription', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subscriber')
    # ### end Alembic commands ###

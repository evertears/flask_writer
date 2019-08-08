"""Page notes

Revision ID: e4d818a01040
Revises: b6aeee8baac1
Create Date: 2019-08-08 19:26:20.594874

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4d818a01040'
down_revision = 'b6aeee8baac1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('page', sa.Column('notes', sa.Text(length=5000000), nullable=True))
    op.add_column('page_version', sa.Column('notes', sa.Text(length=5000000), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('page_version', 'notes')
    op.drop_column('page', 'notes')
    # ### end Alembic commands ###
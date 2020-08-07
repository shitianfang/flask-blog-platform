"""empty message

Revision ID: 9c1bf19bd97a
Revises: 491417b3537e
Create Date: 2020-07-07 19:11:06.762146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c1bf19bd97a'
down_revision = '491417b3537e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('crawls', schema=None) as batch_op:
        batch_op.add_column(sa.Column('urlset', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('crawls', schema=None) as batch_op:
        batch_op.drop_column('urlset')

    # ### end Alembic commands ###

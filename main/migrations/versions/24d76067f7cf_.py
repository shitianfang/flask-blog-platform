"""empty message

Revision ID: 24d76067f7cf
Revises: 87b301973f6e
Create Date: 2020-07-01 18:15:13.612442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24d76067f7cf'
down_revision = '87b301973f6e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('crawls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rrs', sa.String(length=255), nullable=True),
    sa.Column('p_home', sa.String(length=255), nullable=True),
    sa.Column('p_page', sa.String(length=225), nullable=True),
    sa.Column('p_title', sa.String(length=125), nullable=True),
    sa.Column('p_link', sa.String(length=125), nullable=True),
    sa.Column('p_body', sa.String(length=125), nullable=True),
    sa.Column('blog_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['blog_id'], ['blogs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('blogs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('platform', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blogs', schema=None) as batch_op:
        batch_op.drop_column('platform')

    op.drop_table('crawls')
    # ### end Alembic commands ###

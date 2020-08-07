"""empty message

Revision ID: c089c44a60fc
Revises: 0982f7d5be45
Create Date: 2020-07-04 01:45:34.801099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c089c44a60fc'
down_revision = '0982f7d5be45'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('crawl_id', sa.Integer(), nullable=True),
    sa.Column('complete', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['crawl_id'], ['crawls.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_tasks_name'), ['name'], unique=False)

    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_index('ix_task_name')

    op.drop_table('task')
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_column('md5')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('md5', sa.VARCHAR(length=32), nullable=True))

    op.create_table('task',
    sa.Column('id', sa.VARCHAR(length=36), nullable=False),
    sa.Column('name', sa.VARCHAR(length=128), nullable=True),
    sa.Column('crawl_id', sa.INTEGER(), nullable=True),
    sa.Column('complete', sa.BOOLEAN(), nullable=True),
    sa.CheckConstraint('complete IN (0, 1)'),
    sa.ForeignKeyConstraint(['crawl_id'], ['crawls.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.create_index('ix_task_name', ['name'], unique=False)

    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_tasks_name'))

    op.drop_table('tasks')
    # ### end Alembic commands ###
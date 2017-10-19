"""19_10_2017_17_48

Revision ID: 382bbea9042c
Revises: 
Create Date: 2017-10-19 17:48:42.402898

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '382bbea9042c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('table_key', sa.String(length=120), nullable=True),
    sa.Column('table_info', sa.Integer(), nullable=True),
    sa.Column('table_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('table', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_table_table_key'), ['table_key'], unique=True)

    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password', sa.String(length=24), nullable=True),
    sa.Column('phone', sa.String(length=12), nullable=True),
    sa.Column('fts_key', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_phone'), ['phone'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('table_id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=120), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['table_id'], ['table.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('product_name')
    )
    op.create_table('user_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('table_id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['table_id'], ['table.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user_table', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_table_table_id'), ['table_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_table_user_id'), ['user_id'], unique=True)

    op.create_table('user_table_archive',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('table_id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['table_id'], ['table.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user_table_archive', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_table_archive_table_id'), ['table_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_table_archive_user_id'), ['user_id'], unique=False)

    op.create_table('user_product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('table_id', sa.Integer(), nullable=True),
    sa.Column('count', sa.Float(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user_product', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_product_product_id'), ['product_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_product_table_id'), ['table_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_product_user_id'), ['user_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_product', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_product_user_id'))
        batch_op.drop_index(batch_op.f('ix_user_product_table_id'))
        batch_op.drop_index(batch_op.f('ix_user_product_product_id'))

    op.drop_table('user_product')
    with op.batch_alter_table('user_table_archive', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_table_archive_user_id'))
        batch_op.drop_index(batch_op.f('ix_user_table_archive_table_id'))

    op.drop_table('user_table_archive')
    with op.batch_alter_table('user_table', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_table_user_id'))
        batch_op.drop_index(batch_op.f('ix_user_table_table_id'))

    op.drop_table('user_table')
    op.drop_table('products')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_phone'))

    op.drop_table('user')
    with op.batch_alter_table('table', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_table_table_key'))

    op.drop_table('table')
    # ### end Alembic commands ###
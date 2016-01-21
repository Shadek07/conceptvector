"""empty message

Revision ID: 1cdb6a14c9f6
Revises: 21dc0327953b
Create Date: 2016-01-20 22:31:56.657913

"""

# revision identifiers, used by Alembic.
revision = '1cdb6a14c9f6'
down_revision = '21dc0327953b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('admin', sa.Boolean(), nullable=False))
    op.add_column('users', sa.Column('registered_on', sa.DateTime(), nullable=False))
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('users', 'registered_on')
    op.drop_column('users', 'admin')
    ### end Alembic commands ###

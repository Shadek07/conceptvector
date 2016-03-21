"""empty message

Revision ID: c80991840b24
Revises: 8f85bc5a934c
Create Date: 2016-03-20 08:40:11.691862

"""

# revision identifiers, used by Alembic.
revision = 'c80991840b24'
down_revision = '8f85bc5a934c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('articles', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.BIGINT())
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               type_=sa.String(length=255),
               existing_nullable=False)
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(),
               type_=sa.String(length=255),
               existing_nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    op.alter_column('users', 'email',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    op.alter_column('articles', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.INTEGER())
    ### end Alembic commands ###

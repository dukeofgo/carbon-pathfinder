"""init existing models

Revision ID: 7282e3b8e986
Revises: 
Create Date: 2024-11-16 01:33:56.539407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7282e3b8e986'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('status', sa.Enum('SUPERUSER', 'ADMIN', 'USER', name='userstatus'), nullable=False),
    sa.Column('registered_date', sa.Date(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_borrower', sa.Boolean(), nullable=False),
    sa.Column('is_member', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('author', sa.String(length=64), nullable=False),
    sa.Column('isbn', sa.String(length=13), nullable=False),
    sa.Column('edition', sa.String(length=64), nullable=True),
    sa.Column('publisher', sa.String(length=64), nullable=True),
    sa.Column('publish_date', sa.String(length=64), nullable=True),
    sa.Column('publish_place', sa.String(length=64), nullable=True),
    sa.Column('number_of_pages', sa.String(), nullable=True),
    sa.Column('description', sa.String(length=1024), nullable=True),
    sa.Column('language', sa.String(length=32), nullable=True),
    sa.Column('lccn', sa.String(length=64), nullable=True),
    sa.Column('subtitle', sa.String(length=1024), nullable=True),
    sa.Column('subjects', sa.String(length=256), nullable=True),
    sa.Column('cover_image', sa.LargeBinary(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('added_date', sa.Date(), nullable=False),
    sa.Column('borrowed_date', sa.Date(), nullable=True),
    sa.Column('returned_date', sa.Date(), nullable=True),
    sa.Column('is_borrowed', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('books')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###

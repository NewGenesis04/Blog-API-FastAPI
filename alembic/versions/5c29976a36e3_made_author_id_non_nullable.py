"""Made author_id non-nullable

Revision ID: 5c29976a36e3
Revises: bd477f4e39ef
Create Date: 2024-12-20 00:31:00.171344

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '5c29976a36e3'
down_revision: Union[str, None] = 'bd477f4e39ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_blogs_created_at', table_name='blogs')
    op.drop_index('ix_blogs_id', table_name='blogs')
    op.drop_index('ix_blogs_published', table_name='blogs')
    op.drop_index('ix_blogs_published_at', table_name='blogs')
    op.drop_table('blogs')
    op.drop_index('email', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('email', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('password', mysql.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('email', 'users', ['email'], unique=True)
    op.create_table('blogs',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('content', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('created_at', mysql.DATETIME(), nullable=True),
    sa.Column('published_at', mysql.DATETIME(), nullable=True),
    sa.Column('published', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('author_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], name='blogs_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_blogs_published_at', 'blogs', ['published_at'], unique=False)
    op.create_index('ix_blogs_published', 'blogs', ['published'], unique=False)
    op.create_index('ix_blogs_id', 'blogs', ['id'], unique=False)
    op.create_index('ix_blogs_created_at', 'blogs', ['created_at'], unique=False)
    # ### end Alembic commands ###

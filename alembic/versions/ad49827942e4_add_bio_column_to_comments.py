"""Add bio column to comments

Revision ID: ad49827942e4
Revises: 23deb906a509
Create Date: 2025-02-03 00:58:20.084300

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'ad49827942e4'
down_revision: Union[str, None] = '23deb906a509'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('bio', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blogs',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('content', mysql.TEXT(), nullable=False),
    sa.Column('created_at', mysql.DATETIME(), nullable=True),
    sa.Column('published_at', mysql.DATETIME(), nullable=True),
    sa.Column('published', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('author_id', mysql.INTEGER(), autoincrement=False, nullable=False),
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
    op.create_index('ix_blogs_author_id', 'blogs', ['author_id'], unique=False)
    op.create_table('follows',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('follower_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('followed_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', mysql.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['users.id'], name='follows_ibfk_2'),
    sa.ForeignKeyConstraint(['follower_id'], ['users.id'], name='follows_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_follows_id', 'follows', ['id'], unique=False)
    op.create_index('ix_follows_created_at', 'follows', ['created_at'], unique=False)
    op.create_table('users',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('email', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('password', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('role', mysql.VARCHAR(length=255), server_default=sa.text("'reader'"), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('email', 'users', ['email'], unique=True)
    op.create_table('comments',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('author_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('blog_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('content', mysql.TEXT(), nullable=False),
    sa.Column('created_at', mysql.DATETIME(), server_default=sa.text('(now())'), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], name='comments_ibfk_1', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['blog_id'], ['blogs.id'], name='comments_ibfk_2', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_comments_id', 'comments', ['id'], unique=False)
    op.create_index('ix_comments_created_at', 'comments', ['created_at'], unique=False)
    op.create_index('ix_comments_blog_id', 'comments', ['blog_id'], unique=False)
    op.create_index('ix_comments_author_id', 'comments', ['author_id'], unique=False)
    # ### end Alembic commands ###

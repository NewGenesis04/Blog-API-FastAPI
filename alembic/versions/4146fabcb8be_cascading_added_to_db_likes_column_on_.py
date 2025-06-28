"""Cascading added to db, Likes column on parent table removed

Revision ID: 4146fabcb8be
Revises: af20e3160e27
Create Date: 2025-06-28 01:19:41.059094

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '4146fabcb8be'
down_revision: Union[str, None] = 'af20e3160e27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table('comments') as batch_op:
        batch_op.drop_column('likes')

    with op.batch_alter_table('blogs') as batch_op:
        batch_op.drop_column('likes')
    # === blog_likes ===
    with op.batch_alter_table('blog_likes') as batch_op:
        batch_op.drop_constraint('blog_likes_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('blog_likes_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(
            'blog_likes_ibfk_1',
            'blogs',
            ['blog_id'],
            ['id'],
            ondelete='CASCADE'
        )
        batch_op.create_foreign_key(
            'blog_likes_ibfk_2',
            'users',
            ['user_id'],
            ['id'],
            ondelete='CASCADE'
        )

    # === blogs ===
    with op.batch_alter_table('blogs') as batch_op:
        batch_op.drop_constraint('blogs_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(
            'blogs_ibfk_1',
            'users',
            ['author_id'],
            ['id'],
            ondelete='CASCADE'
        )

    # === comments ===
    with op.batch_alter_table('comments') as batch_op:
        batch_op.drop_constraint('comments_ibfk_1', type_='foreignkey')  # author_id
        batch_op.drop_constraint('comments_ibfk_2', type_='foreignkey')  # blog_id
        batch_op.create_foreign_key(
            'comments_ibfk_1',
            'users',
            ['author_id'],
            ['id'],
            ondelete='CASCADE'
        )
        batch_op.create_foreign_key(
            'comments_ibfk_2',
            'blogs',
            ['blog_id'],
            ['id'],
            ondelete='CASCADE'
        )

    # === comment_likes ===
    with op.batch_alter_table('comment_likes') as batch_op:
        batch_op.drop_constraint('comment_likes_ibfk_1', type_='foreignkey')  # comment_id
        batch_op.drop_constraint('comment_likes_ibfk_2', type_='foreignkey')  # user_id
        batch_op.create_foreign_key(
            'comment_likes_ibfk_1',
            'comments',
            ['comment_id'],
            ['id'],
            ondelete='CASCADE'
        )
        batch_op.create_foreign_key(
            'comment_likes_ibfk_2',
            'users',
            ['user_id'],
            ['id'],
            ondelete='CASCADE'
        )

    # === follows ===
    with op.batch_alter_table('follows') as batch_op:
        batch_op.drop_constraint('follows_ibfk_1', type_='foreignkey')  # follower_id
        batch_op.drop_constraint('follows_ibfk_2', type_='foreignkey')  # followed_id
        batch_op.create_foreign_key(
            'follows_ibfk_1',
            'users',
            ['follower_id'],
            ['id'],
            ondelete='CASCADE'
        )
        batch_op.create_foreign_key(
            'follows_ibfk_2',
            'users',
            ['followed_id'],
            ['id'],
            ondelete='CASCADE'
        )


def downgrade():
    with op.batch_alter_table('comments') as batch_op:
        batch_op.add_column(sa.Column('likes', sa.Integer(), nullable=False))

    with op.batch_alter_table('blogs') as batch_op:
        batch_op.add_column(sa.Column('likes', sa.Integer(), nullable=False))
    # === blog_likes ===
    with op.batch_alter_table('blog_likes') as batch_op:
        batch_op.drop_constraint('blog_likes_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('blog_likes_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(
            'blog_likes_ibfk_1',
            'blogs',
            ['blog_id'],
            ['id']
        )
        batch_op.create_foreign_key(
            'blog_likes_ibfk_2',
            'users',
            ['user_id'],
            ['id']
        )

    # === blogs ===
    with op.batch_alter_table('blogs') as batch_op:
        batch_op.drop_constraint('blogs_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(
            'blogs_ibfk_1',
            'users',
            ['author_id'],
            ['id']
        )

    # === comments ===
    with op.batch_alter_table('comments') as batch_op:
        batch_op.drop_constraint('comments_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('comments_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(
            'comments_ibfk_1',
            'users',
            ['author_id'],
            ['id']
        )
        batch_op.create_foreign_key(
            'comments_ibfk_2',
            'blogs',
            ['blog_id'],
            ['id']
        )

    # === comment_likes ===
    with op.batch_alter_table('comment_likes') as batch_op:
        batch_op.drop_constraint('comment_likes_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('comment_likes_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(
            'comment_likes_ibfk_1',
            'comments',
            ['comment_id'],
            ['id']
        )
        batch_op.create_foreign_key(
            'comment_likes_ibfk_2',
            'users',
            ['user_id'],
            ['id']
        )

    # === follows ===
    with op.batch_alter_table('follows') as batch_op:
        batch_op.drop_constraint('follows_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('follows_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(
            'follows_ibfk_1',
            'users',
            ['follower_id'],
            ['id']
        )
        batch_op.create_foreign_key(
            'follows_ibfk_2',
            'users',
            ['followed_id'],
            ['id']
        )
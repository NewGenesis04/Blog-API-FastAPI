"""Made default for role == author

Revision ID: b66d7ec6d817
Revises: d0fe81dc8e60
Create Date: 2024-12-20 22:38:14.118213

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'b66d7ec6d817'
down_revision: Union[str, None] = 'd0fe81dc8e60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Update the default value of the 'role' column to 'author'
    op.alter_column('users', 'role',
                    existing_type=sa.String(length=255),
                    server_default='author',
                    existing_nullable=False)


def downgrade() -> None:
    # Revert the default value of the 'role' column to 'view'
    op.alter_column('users', 'role',
                    existing_type=sa.String(length=255),
                    server_default='view',
                    existing_nullable=False)

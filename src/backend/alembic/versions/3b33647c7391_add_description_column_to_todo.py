"""add description column to todo

Revision ID: 3b33647c7391
Revises: d475f6465fd4
Create Date: 2026-02-14 20:13:10.548629

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3b33647c7391'
down_revision = 'd475f6465fd4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema: add 'description' column to 'todo' table."""
    op.add_column('todo', sa.Column('description', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema: remove 'description' column from 'todo' table."""
    op.drop_column('todo', 'description')

"""Add Dynamic Legal Custom Pages Table

Revision ID: 002_add_custom_pages
Revises: 001_initial_schema
Create Date: 2026-06-14 02:15:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '002_add_custom_pages'
down_revision: Union[str, None] = '001_initial_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('custom_pages',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('slug', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_custom_pages_id'), 'custom_pages', ['id'], unique=False)
    op.create_index(op.f('ix_custom_pages_slug'), 'custom_pages', ['slug'], unique=True)

def downgrade() -> None:
    op.drop_index(op.f('ix_custom_pages_slug'), table_name='custom_pages')
    op.drop_index(op.f('ix_custom_pages_id'), table_name='custom_pages')
    op.drop_table('custom_pages')
  

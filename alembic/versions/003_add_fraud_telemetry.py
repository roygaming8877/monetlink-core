"""Add Anti-Fraud Telemetry and Link Views

Revision ID: 003_add_fraud_telemetry
Revises: 002_add_custom_pages
Create Date: 2026-06-14 02:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '003_add_fraud_telemetry'
down_revision: Union[str, None] = '002_add_custom_pages'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('link_views',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('link_id', sa.String(), nullable=False),
        sa.Column('ip_address', sa.String(), nullable=False),
        sa.Column('country', sa.String(), server_default='Global', nullable=False),
        sa.Column('payout_credited', sa.Float(), server_default='0.0', nullable=False),
        
        # Security Metrics
        sa.Column('fingerprint', sa.String(), nullable=True),
        sa.Column('is_valid', sa.Boolean(), server_default='true', nullable=False),
        
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['link_id'], ['links.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_link_views_ip_address'), 'link_views', ['ip_address'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_link_views_ip_address'), table_name='link_views')
    op.drop_table('link_views')
  

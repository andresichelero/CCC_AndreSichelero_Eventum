"""Ajusta default das datas de inscrição para timezone-aware

Revision ID: ajuste_default_datas_inscricao
Revises: eea580de11f0
Create Date: 2025-10-15 23:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime, timezone

# revision identifiers, used by Alembic.
revision = 'ajuste_default_datas_inscricao'
down_revision = "eea580de11f0"
branch_labels = None
depends_on = None


def upgrade():
    now_utc = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S+00')
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.alter_column('inscription_start_date', server_default=sa.text(f"'{now_utc}'"))
        batch_op.alter_column('inscription_end_date', server_default=sa.text(f"'{now_utc}'"))


def downgrade():
    # Remove o default timezone-aware e volta para sem timezone
    now_naive = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.alter_column('inscription_start_date', server_default=sa.text(f"'{now_naive}'"))
        batch_op.alter_column('inscription_end_date', server_default=sa.text(f"'{now_naive}'"))

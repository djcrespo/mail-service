"""update max length to cotizacion attribute in cotizacion model

Revision ID: 3a9a111b9847
Revises: b866d38c22f6
Create Date: 2024-05-24 09:21:03.824077

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '3a9a111b9847'
down_revision: Union[str, None] = 'b866d38c22f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cotizaciones', sa.Column('cotizacion', sa.String(length=500), nullable=True))
    op.drop_index('ix_cotizaciones_message', table_name='cotizaciones')
    op.create_index(op.f('ix_cotizaciones_cotizacion'), 'cotizaciones', ['cotizacion'], unique=False)
    op.drop_column('cotizaciones', 'message')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cotizaciones', sa.Column('message', mysql.VARCHAR(length=255), nullable=True))
    op.drop_index(op.f('ix_cotizaciones_cotizacion'), table_name='cotizaciones')
    op.create_index('ix_cotizaciones_message', 'cotizaciones', ['message'], unique=True)
    op.drop_column('cotizaciones', 'cotizacion')
    # ### end Alembic commands ###

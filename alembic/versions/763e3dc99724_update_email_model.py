"""update email model

Revision ID: 763e3dc99724
Revises: 702ea3c412b7
Create Date: 2024-05-22 10:28:12.672198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '763e3dc99724'
down_revision: Union[str, None] = '702ea3c412b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cotizaciones', sa.Column('person_id', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'cotizaciones', ['person_id'])
    op.create_foreign_key(None, 'cotizaciones', 'persons', ['person_id'], ['id'])
    op.drop_index('ix_emails_message', table_name='emails')
    op.create_index(op.f('ix_emails_message'), 'emails', ['message'], unique=False)
    op.drop_constraint('emails_cotizacion_ibfk_1', 'emails_cotizacion', type_='foreignkey')
    op.drop_column('emails_cotizacion', 'person_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('emails_cotizacion', sa.Column('person_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('emails_cotizacion_ibfk_1', 'emails_cotizacion', 'persons', ['person_id'], ['id'])
    op.drop_index(op.f('ix_emails_message'), table_name='emails')
    op.create_index('ix_emails_message', 'emails', ['message'], unique=True)
    op.drop_constraint(None, 'cotizaciones', type_='foreignkey')
    op.drop_constraint(None, 'cotizaciones', type_='unique')
    op.drop_column('cotizaciones', 'person_id')
    # ### end Alembic commands ###

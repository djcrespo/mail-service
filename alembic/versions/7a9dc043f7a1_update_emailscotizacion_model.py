"""update emailsCotizacion model

Revision ID: 7a9dc043f7a1
Revises: 763e3dc99724
Create Date: 2024-05-22 10:30:48.832498

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a9dc043f7a1'
down_revision: Union[str, None] = '763e3dc99724'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('emails_cotizacion', sa.Column('person_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'emails_cotizacion', 'persons', ['person_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'emails_cotizacion', type_='foreignkey')
    op.drop_column('emails_cotizacion', 'person_id')
    # ### end Alembic commands ###
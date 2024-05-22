"""Update income table

Revision ID: 49fe4cb71216
Revises: 7fbab4daf456
Create Date: 2024-05-14 23:07:52.743241

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49fe4cb71216'
down_revision: Union[str, None] = '7fbab4daf456'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('incomes', sa.Column('price', sa.Integer(), nullable=False))
    op.drop_column('incomes', 'ptice')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('incomes', sa.Column('ptice', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('incomes', 'price')
    # ### end Alembic commands ###
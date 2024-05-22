"""Add forien key

Revision ID: 7fbab4daf456
Revises: 7724d4eb86c9
Create Date: 2024-05-09 23:57:38.652763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7fbab4daf456'
down_revision: Union[str, None] = '7724d4eb86c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('incomes', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'incomes', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'incomes', type_='foreignkey')
    op.drop_column('incomes', 'user_id')
    # ### end Alembic commands ###
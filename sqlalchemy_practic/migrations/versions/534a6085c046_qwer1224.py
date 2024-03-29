"""qwer1224

Revision ID: 534a6085c046
Revises: 39d927cc05fb
Create Date: 2024-02-24 17:44:21.624232

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '534a6085c046'
down_revision: Union[str, None] = '39d927cc05fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_group_group_id_key', 'user_group', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('user_group_group_id_key', 'user_group', ['group_id'])
    # ### end Alembic commands ###

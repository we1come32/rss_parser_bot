"""Adding autoincrement where it needed

Revision ID: 07123387ce3c
Revises: 09a92ace3196
Create Date: 2023-11-13 13:03:28.695387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07123387ce3c'
down_revision: Union[str, None] = '09a92ace3196'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

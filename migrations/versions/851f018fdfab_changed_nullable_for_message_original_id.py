"""Changed nullable for Message.original_id

Revision ID: 851f018fdfab
Revises: 8876e798292a
Create Date: 2023-11-15 12:50:23.355013

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '851f018fdfab'
down_revision: Union[str, None] = '8876e798292a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('messages', 'original_id',
               existing_type=sa.BIGINT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('messages', 'original_id',
               existing_type=sa.BIGINT(),
               nullable=False)
    # ### end Alembic commands ###
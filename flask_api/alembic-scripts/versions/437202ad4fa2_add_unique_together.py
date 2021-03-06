"""Add unique together

Revision ID: 437202ad4fa2
Revises: d9c39fbb39fb
Create Date: 2022-05-27 16:17:54.997611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '437202ad4fa2'
down_revision = 'd9c39fbb39fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq__price_history__ticker_name', 'price_history', type_='unique')
    op.create_unique_constraint('_ticker_day_uc', 'price_history', ['ticker_name', 'trading_day'])
    op.create_unique_constraint(op.f('uq__price_history__id'), 'price_history', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq__price_history__id'), 'price_history', type_='unique')
    op.drop_constraint('_ticker_day_uc', 'price_history', type_='unique')
    op.create_unique_constraint('uq__price_history__ticker_name', 'price_history', ['ticker_name'])
    # ### end Alembic commands ###

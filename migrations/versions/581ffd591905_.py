"""empty message

Revision ID: 581ffd591905
Revises: 947417f980dc
Create Date: 2022-02-07 16:50:19.501569

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float


# revision identifiers, used by Alembic.
revision = '581ffd591905'
down_revision = '947417f980dc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('people', Column('default_tags', String(120), index=True, nullable=True, default=None))


def downgrade():
    op.drop_column('people', 'default_tags')

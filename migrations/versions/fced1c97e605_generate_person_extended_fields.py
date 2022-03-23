"""generate person extended fields

Revision ID: fced1c97e605
Revises: 581ffd591905
Create Date: 2022-03-09 17:57:41.987573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fced1c97e605'
down_revision = '581ffd591905'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('people', sa.Column('nationality', sa.String(20), index=True, nullable=True, default=None))
    op.add_column('people', sa.Column('birthplace', sa.String(3), index=True, nullable=True, default=None))
    op.add_column('people', sa.Column('birthdate', sa.Date(), index=True, nullable=True, default=None))
    op.add_column('people', sa.Column('ethnicity', sa.String(15), index=True, nullable=True, default=None))
    op.add_column('people', sa.Column('hair_color', sa.String(10), index=True, nullable=True, default=None))
    op.add_column('people', sa.Column('cupsize', sa.String(10), index=True, nullable=True, default=None))


def downgrade():
    op.drop_column('people', 'nationality')
    op.drop_column('people', 'birthplace')
    op.drop_column('people', 'birthdate')
    op.drop_column('people', 'ethnicity')
    op.drop_column('people', 'hair_color')
    op.drop_column('people', 'cupsize')

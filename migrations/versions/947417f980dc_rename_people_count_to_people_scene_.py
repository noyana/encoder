"""rename people.count to people.scene_count

Revision ID: 947417f980dc
Revises: 672a1399dccf
Create Date: 2022-01-21 12:38:05.764695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '947417f980dc'
down_revision = '672a1399dccf'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('people', 'count', new_column_name='scene_count')


def downgrade():
    op.alter_column('people', 'scene_count', new_column_name='count')

"""trying to get alembic working

Revision ID: fd6e84d09380
Revises: 29f4e3d1dd6f
Create Date: 2017-05-19 10:42:16.129583

"""

# revision identifiers, used by Alembic.
revision = 'fd6e84d09380'
down_revision = '29f4e3d1dd6f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
            'products',
            sa.Column('id', sa.INTEGER, primary_key=True),
            sa.Column('raw', sa.JSON),
            sa.Column('name', sa.Text),
            sa.Column('description', sa.Text),
            sa.Column('brand', sa.Text),
            sa.Column('price', sa.DECIMAL),
            sa.Column('avgrating', sa.DECIMAL),
            sa.Column('model', sa.Text),
            sa.Column('rating_count', sa.Integer),
            sa.Column('good_rating', sa.Text),
            sa.Column('bad_rating', sa.Text)
            )
    pass


def downgrade():
    op.drop_table('products')
    pass

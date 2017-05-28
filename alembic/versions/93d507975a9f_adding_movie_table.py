"""Adding movie table

Revision ID: 93d507975a9f
Revises: 2fa633188da0
Create Date: 2017-05-28 11:23:06.341646

"""

# revision identifiers, used by Alembic.
revision = '93d507975a9f'
down_revision = '2fa633188da0'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
            'movies',
            sa.Column('id', sa.INTEGER),
            sa.Column('imdb_id', sa.String(length=10), primary_key=True),

            sa.Column('name', sa.Text),
            sa.Column('plot_outline', sa.Text),
            sa.Column('release_date_string', sa.String(length=12)),
            sa.Column('avgrating', sa.DECIMAL),
            sa.Column('certification', sa.String(length=1)),
            sa.Column('actors', sa.JSON),
            sa.Column('runtime_seconds', sa.Integer),
            sa.Column('directors', sa.JSON),
            sa.Column('poster_url', sa.Text)
            )
    pass


def downgrade():
    op.drop_table('movies')
    pass

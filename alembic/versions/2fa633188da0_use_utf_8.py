"""use utf-8

Revision ID: 2fa633188da0
Revises: fd6e84d09380
Create Date: 2017-05-19 11:34:46.011512

"""

# revision identifiers, used by Alembic.
revision = '2fa633188da0'
down_revision = 'fd6e84d09380'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    conn = op.get_bind()
    conn.execute(sa.sql.text('ALTER table products CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci'))
    pass


def downgrade():
    pass

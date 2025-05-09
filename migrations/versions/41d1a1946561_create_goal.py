"""create goal

Revision ID: 41d1a1946561
Revises: 3464ae9cce7c
Create Date: 2025-05-06 22:04:53.157232

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41d1a1946561'
down_revision = '3464ae9cce7c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('goal', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('goal', schema=None) as batch_op:
        batch_op.drop_column('title')

    # ### end Alembic commands ###

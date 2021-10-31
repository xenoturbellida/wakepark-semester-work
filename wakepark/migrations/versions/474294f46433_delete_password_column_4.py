"""delete password column 4

Revision ID: 474294f46433
Revises: 56df39970859
Create Date: 2021-10-31 20:25:59.828548

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '474294f46433'
down_revision = '56df39970859'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    # ### end Alembic commands ###

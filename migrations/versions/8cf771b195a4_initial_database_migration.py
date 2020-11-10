"""initial database migration

Revision ID: 8cf771b195a4
Revises: 
Create Date: 2020-11-09 18:45:26.924269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cf771b195a4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('forecast',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(length=255), nullable=True),
    sa.Column('state', sa.String(length=255), nullable=True),
    sa.Column('country', sa.String(length=255), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('rain_probability', sa.Float(), nullable=True),
    sa.Column('rain_precipitation', sa.Float(), nullable=True),
    sa.Column('max_temp', sa.Float(), nullable=True),
    sa.Column('min_temp', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('forecast')
    # ### end Alembic commands ###
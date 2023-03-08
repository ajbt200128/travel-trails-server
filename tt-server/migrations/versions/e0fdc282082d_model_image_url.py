"""Model image url

Revision ID: e0fdc282082d
Revises: 4a1036e508b6
Create Date: 2023-03-04 15:59:32.661019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0fdc282082d'
down_revision = '4a1036e508b6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('location', sa.Column('model_image_url', sa.String(length=1024), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('location', 'model_image_url')
    # ### end Alembic commands ###
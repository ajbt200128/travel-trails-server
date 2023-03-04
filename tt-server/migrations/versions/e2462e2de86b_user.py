"""User

Revision ID: e2462e2de86b
Revises: f5fb61a752f0
Create Date: 2023-03-01 17:00:33.111117

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2462e2de86b'
down_revision = 'f5fb61a752f0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('profile_picture', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('username')
    )
    op.create_table('user_visit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.Column('time_visited', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], ),
    sa.ForeignKeyConstraint(['username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_visit')
    op.drop_table('user')
    # ### end Alembic commands ###

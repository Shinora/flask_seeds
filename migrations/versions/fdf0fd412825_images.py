"""images

Revision ID: fdf0fd412825
Revises: 
Create Date: 2020-04-21 23:43:06.136353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdf0fd412825'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('plant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=300), nullable=True),
    sa.Column('description', sa.String(length=5000), nullable=True),
    sa.Column('author', sa.String(length=64), nullable=True),
    sa.Column('image_file', sa.String(length=20), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plant_description'), 'plant', ['description'], unique=False)
    op.create_index(op.f('ix_plant_name'), 'plant', ['name'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('image_file', sa.String(length=20), nullable=False),
    sa.Column('date_creation', sa.DateTime(), nullable=True),
    sa.Column('reputation', sa.Integer(), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_date_creation'), 'user', ['date_creation'], unique=False)
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_reputation'), 'user', ['reputation'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_reputation'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_index(op.f('ix_user_date_creation'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_plant_name'), table_name='plant')
    op.drop_index(op.f('ix_plant_description'), table_name='plant')
    op.drop_table('plant')
    # ### end Alembic commands ###

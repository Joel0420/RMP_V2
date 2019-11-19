"""empty message

Revision ID: f32de056272d
Revises: 
Create Date: 2019-11-19 14:51:09.189349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f32de056272d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=300), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_course_description'), 'course', ['description'], unique=False)
    op.create_index(op.f('ix_course_name'), 'course', ['name'], unique=False)
    op.create_table('professor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('last_name', sa.String(length=64), nullable=True),
    sa.Column('average_rating', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_professor_average_rating'), 'professor', ['average_rating'], unique=False)
    op.create_index(op.f('ix_professor_first_name'), 'professor', ['first_name'], unique=False)
    op.create_index(op.f('ix_professor_last_name'), 'professor', ['last_name'], unique=False)
    op.create_table('rating',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('section',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('semester', sa.String(length=64), nullable=True),
    sa.Column('year', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_section_semester'), 'section', ['semester'], unique=False)
    op.create_index(op.f('ix_section_year'), 'section', ['year'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('last_name', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_first_name'), 'user', ['first_name'], unique=False)
    op.create_index(op.f('ix_user_last_name'), 'user', ['last_name'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_last_name'), table_name='user')
    op.drop_index(op.f('ix_user_first_name'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_section_year'), table_name='section')
    op.drop_index(op.f('ix_section_semester'), table_name='section')
    op.drop_table('section')
    op.drop_table('rating')
    op.drop_index(op.f('ix_professor_last_name'), table_name='professor')
    op.drop_index(op.f('ix_professor_first_name'), table_name='professor')
    op.drop_index(op.f('ix_professor_average_rating'), table_name='professor')
    op.drop_table('professor')
    op.drop_index(op.f('ix_course_name'), table_name='course')
    op.drop_index(op.f('ix_course_description'), table_name='course')
    op.drop_table('course')
    # ### end Alembic commands ###
"""Agregar columna estado a cuotasgc

Revision ID: aea891c3650a
Revises: 3dbb19c5622a
Create Date: 2024-12-02 05:19:02.975988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aea891c3650a'
down_revision = '3dbb19c5622a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cuotasgc', schema=None) as batch_op:
        batch_op.add_column(sa.Column('estado', sa.String(length=20), nullable=True))
        batch_op.drop_column('telefono')
        batch_op.drop_column('rut')
        batch_op.drop_column('nombre')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cuotasgc', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nombre', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('rut', sa.VARCHAR(length=12), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('telefono', sa.VARCHAR(length=15), autoincrement=False, nullable=True))
        batch_op.drop_column('estado')

    # ### end Alembic commands ###

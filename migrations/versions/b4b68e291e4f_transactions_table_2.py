"""Transactions table 2

Revision ID: b4b68e291e4f
Revises: 903f92cce344
Create Date: 2024-02-03 17:33:10.586645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4b68e291e4f'
down_revision = '903f92cce344'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('issue_date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('return_date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('expected_return_date', sa.DateTime(), nullable=False))
        batch_op.drop_column('transaction_type')
        batch_op.drop_column('transaction_date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('transaction_date', sa.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('transaction_type', sa.VARCHAR(length=10), nullable=False))
        batch_op.drop_column('expected_return_date')
        batch_op.drop_column('return_date')
        batch_op.drop_column('issue_date')

    # ### end Alembic commands ###

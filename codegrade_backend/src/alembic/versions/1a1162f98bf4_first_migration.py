"""First migration

Revision ID: 1a1162f98bf4
Revises: 
Create Date: 2025-03-03 00:15:12.838694

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '1a1162f98bf4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('session',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('external_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_session_external_id'), 'session', ['external_id'], unique=True)
    op.create_table('exercise',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('external_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('session_id', sa.Uuid(), nullable=False),
    sa.Column('question', sqlmodel.sql.sqltypes.AutoString(length=10000), nullable=False),
    sa.Column('instructions', sqlmodel.sql.sqltypes.AutoString(length=10000), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['session.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('session_id', 'external_id', name='session_id_unique_together_with_external_id')
    )
    op.create_index(op.f('ix_exercise_external_id'), 'exercise', ['external_id'], unique=False)
    op.create_table('group',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('external_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('session_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['session_id'], ['session.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('session_id', 'external_id', name='session_id_unique_together_with_external_id')
    )
    op.create_index(op.f('ix_group_external_id'), 'group', ['external_id'], unique=False)
    op.create_table('evaluationflag',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('exercise_id', sa.Uuid(), nullable=False),
    sa.Column('flag', sa.Enum('execution', 'compilation', 'code_quality', name='evaluationflagenum'), nullable=False),
    sa.Column('score_percentage', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercise.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('testcase',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('external_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('exercise_id', sa.Uuid(), nullable=False),
    sa.Column('test_input', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('expected_output', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('score_percentage', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercise.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('exercise_id', 'external_id', name='exercise_id_unique_together_with_external_id')
    )
    op.create_index(op.f('ix_testcase_external_id'), 'testcase', ['external_id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('external_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('fullname', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('session_id', sa.Uuid(), nullable=False),
    sa.Column('group_id', sa.Uuid(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.ForeignKeyConstraint(['session_id'], ['session.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('session_id', 'external_id', name='session_id_unique_together_with_external_id')
    )
    op.create_index(op.f('ix_user_external_id'), 'user', ['external_id'], unique=False)
    op.create_table('submission',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('session_id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=True),
    sa.Column('group_id', sa.Uuid(), nullable=True),
    sa.Column('status', sa.Enum('QUEUED', 'GRADING', 'GRADED', 'FAILED', name='submissionstatus'), nullable=False),
    sa.Column('overrall_total', sa.Float(), nullable=True),
    sa.Column('reviewed', sa.Boolean(), nullable=False),
    sa.Column('auto_generated_feedback', sqlmodel.sql.sqltypes.AutoString(length=5000), nullable=False),
    sa.Column('manual_feedback', sqlmodel.sql.sqltypes.AutoString(length=5000), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.ForeignKeyConstraint(['session_id'], ['session.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('exercisesubmission',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('submission_id', sa.Uuid(), nullable=False),
    sa.Column('exercise_id', sa.Uuid(), nullable=False),
    sa.Column('graded', sa.Boolean(), nullable=False),
    sa.Column('total_score', sa.Float(), nullable=True),
    sa.Column('auto_generated_feedback', sqlmodel.sql.sqltypes.AutoString(length=5000), nullable=False),
    sa.Column('manual_feedback', sqlmodel.sql.sqltypes.AutoString(length=5000), nullable=False),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercise.id'], ),
    sa.ForeignKeyConstraint(['submission_id'], ['submission.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('evaluationflagresult',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('submission_id', sa.Uuid(), nullable=False),
    sa.Column('evaluation_flag_id', sa.Uuid(), nullable=False),
    sa.Column('passed', sa.Boolean(), nullable=False),
    sa.Column('score', sa.Float(), nullable=False),
    sa.Column('adjusted', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['evaluation_flag_id'], ['evaluationflag.id'], ),
    sa.ForeignKeyConstraint(['submission_id'], ['exercisesubmission.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('testcaseresult',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('submission_id', sa.Uuid(), nullable=False),
    sa.Column('test_case_id', sa.Uuid(), nullable=False),
    sa.Column('passed', sa.Boolean(), nullable=False),
    sa.Column('score', sa.Float(), nullable=False),
    sa.Column('exit_code', sa.Integer(), nullable=False),
    sa.Column('std_out', sqlmodel.sql.sqltypes.AutoString(length=1000), nullable=False),
    sa.Column('adjusted', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['submission_id'], ['exercisesubmission.id'], ),
    sa.ForeignKeyConstraint(['test_case_id'], ['testcase.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('testcaseresult')
    op.drop_table('evaluationflagresult')
    op.drop_table('exercisesubmission')
    op.drop_table('submission')
    op.drop_index(op.f('ix_user_external_id'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_testcase_external_id'), table_name='testcase')
    op.drop_table('testcase')
    op.drop_table('evaluationflag')
    op.drop_index(op.f('ix_group_external_id'), table_name='group')
    op.drop_table('group')
    op.drop_index(op.f('ix_exercise_external_id'), table_name='exercise')
    op.drop_table('exercise')
    op.drop_index(op.f('ix_session_external_id'), table_name='session')
    op.drop_table('session')
    # ### end Alembic commands ###

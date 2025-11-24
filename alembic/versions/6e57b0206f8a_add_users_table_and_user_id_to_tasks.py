"""add users table and user_id to tasks

Revision ID: 6e57b0206f8a
Revises: 00a5f5e30912
Create Date: 2025-11-21 12:08:42.248423

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from fastapi_users_db_sqlalchemy.generics import GUID

# revision identifiers, used by Alembic.
revision: str = '6e57b0206f8a'
down_revision: Union[str, Sequence[str], None] = '00a5f5e30912'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Create users table
    op.create_table(
        'users',
        sa.Column('id', GUID(), primary_key=True, nullable=False),
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('hashed_password', sa.String(length=1024), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_superuser', sa.Boolean(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # 2. Add nullable user_id to tasks first (cannot be NOT NULL yet)
    op.add_column('tasks', sa.Column(
        'user_id', sa.UUID(as_uuid=True), nullable=True))
    op.create_index(op.f('ix_tasks_user_id'), 'tasks',
                    ['user_id'], unique=False)

    # 3. Insert system user and fetch id
    connection = op.get_bind()
    result = connection.execute(sa.text("""
        INSERT INTO users (id, email, hashed_password, is_active, is_superuser, is_verified)
        VALUES (gen_random_uuid(), 'system@local', 'placeholder', TRUE, FALSE, FALSE)
        RETURNING id;
    """))
    default_user_id = result.fetchone()[0]

    # 4. Update all existing tasks with this default user_id
    connection.execute(sa.text(f"""
        UPDATE tasks SET user_id = '{default_user_id}';
    """))

    # 5. Now enforce NOT NULL
    op.alter_column('tasks', 'user_id', nullable=False)

    # 6. Add foreign key
    op.create_foreign_key(
        "fk_tasks_user_id",
        "tasks", "users",
        ["user_id"], ["id"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop FK first
    op.drop_constraint("fk_tasks_user_id", "tasks", type_="foreignkey")

    # Drop index and column user_id
    op.drop_index(op.f('ix_tasks_user_id'), table_name='tasks')
    op.drop_column('tasks', 'user_id')

    # Drop users table
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')

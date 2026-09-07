from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "add_resume_profile"
down_revision: Union[str, Sequence[str], None] = "7aee27353390"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "candidates",
        sa.Column(
            "structured_profile",
            sa.JSON(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "candidates",
        "structured_profile",
    )
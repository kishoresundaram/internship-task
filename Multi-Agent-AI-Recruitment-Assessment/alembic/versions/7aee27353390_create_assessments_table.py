"""create assessments table

Revision ID: 7aee27353390
Revises: 9ec565cca090
Create Date: 2026-09-07 12:53:11.303909

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7aee27353390"
down_revision: Union[str, Sequence[str], None] = "9ec565cca090"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create assessments table."""

    op.create_table(
        "assessments",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "candidate_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "job_description_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
        ),

        sa.Column(
            "technical_score",
            sa.Float(),
            nullable=True,
        ),

        sa.Column(
            "qa_score",
            sa.Float(),
            nullable=True,
        ),

        sa.Column(
            "coding_score",
            sa.Float(),
            nullable=True,
        ),

        sa.Column(
            "communication_score",
            sa.Float(),
            nullable=True,
        ),

        sa.Column(
            "overall_score",
            sa.Float(),
            nullable=True,
        ),

        sa.Column(
            "recommendation",
            sa.Text(),
            nullable=True,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["candidate_id"],
            ["candidates.id"],
        ),

        sa.ForeignKeyConstraint(
            ["job_description_id"],
            ["job_descriptions.id"],
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_assessments_id"),
        "assessments",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_assessments_candidate_id"),
        "assessments",
        ["candidate_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_assessments_job_description_id"),
        "assessments",
        ["job_description_id"],
        unique=False,
    )


def downgrade() -> None:
    """Drop assessments table."""

    op.drop_index(
        op.f("ix_assessments_job_description_id"),
        table_name="assessments",
    )

    op.drop_index(
        op.f("ix_assessments_candidate_id"),
        table_name="assessments",
    )

    op.drop_index(
        op.f("ix_assessments_id"),
        table_name="assessments",
    )

    op.drop_table("assessments")
"""modify

Revision ID: 8e857f9e502a
Revises: 3ce56626f723
Create Date: 2025-01-02 16:02:41.867686

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8e857f9e502a"
down_revision: Union[str, None] = "3ce56626f723"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, comment="PK"),
        sa.Column("title", sa.String(length=256), nullable=True, comment="제목"),
        sa.Column("content", sa.String(), nullable=True, comment="내용"),
        sa.Column("owner_id", sa.Integer(), nullable=True, comment="작성자"),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
            comment="생성일시",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
            comment="수정일시",
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True, comment="삭제일시"),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        comment="게시판",
    )
    op.create_index(op.f("ix_posts_id"), "posts", ["id"], unique=False)
    op.create_index(op.f("ix_posts_title"), "posts", ["title"], unique=False)
    op.add_column(
        "users",
        sa.Column(
            "hashed_password",
            sa.String(length=256),
            nullable=False,
            comment="해시된 비밀번호",
        ),
    )
    op.add_column(
        "users", sa.Column("is_active", sa.Boolean(), nullable=True, comment="탈퇴여부")
    )
    op.drop_column("users", "password")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column(
            "password",
            sa.VARCHAR(length=256),
            autoincrement=False,
            nullable=False,
            comment="비밀번호",
        ),
    )
    op.drop_column("users", "is_active")
    op.drop_column("users", "hashed_password")
    op.drop_index(op.f("ix_posts_title"), table_name="posts")
    op.drop_index(op.f("ix_posts_id"), table_name="posts")
    op.drop_table("posts")
    # ### end Alembic commands ###

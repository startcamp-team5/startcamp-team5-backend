from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class BoardCategory(Base):
    __tablename__ = "board_categories"
    __table_args__ = (
        CheckConstraint(
            "is_active IN (0, 1)",
            name="ck_board_categories_is_active",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    code: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    display_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    is_active: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
    )


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = (
        CheckConstraint(
            "length(trim(title)) BETWEEN 1 AND 100",
            name="ck_posts_title_length",
        ),
        CheckConstraint(
            "length(trim(content)) BETWEEN 1 AND 5000",
            name="ck_posts_content_length",
        ),
        CheckConstraint(
            "length(edit_password) BETWEEN 4 AND 20",
            name="ck_posts_password_length",
        ),
        CheckConstraint("view_count >= 0", name="ck_posts_view_count"),
        CheckConstraint(
            "is_deleted IN (0, 1)",
            name="ck_posts_is_deleted",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    board_category_id: Mapped[int] = mapped_column(
        ForeignKey("board_categories.id", ondelete="RESTRICT"),
        nullable=False,
    )
    local_content_id: Mapped[int | None] = mapped_column(
        ForeignKey("local_contents.id", ondelete="SET NULL"),
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    edit_password: Mapped[str] = mapped_column(String(20), nullable=False)
    author_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="익명",
    )
    view_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    is_deleted: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime)
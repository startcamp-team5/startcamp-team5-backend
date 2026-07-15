from datetime import datetime

from colorama import init
from pydantic import config
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

class Comment(Base):
    __tablename__ = "comments"
    __table_args__ = (
        CheckConstraint(
            f"length(trim(content)) BETWEEN 1 AND 1000",
            name="ck_comments_content_length",
        ),
        CheckConstraint(
            f"length(edit_password) BETWEEN 4 AND 16",
            name="ck_comments_password_length",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    author_name: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="익명",
    )
    edit_password: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
    )
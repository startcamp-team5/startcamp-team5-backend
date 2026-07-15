from datetime import date, datetime

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Region(Base):
    __tablename__ = "regions"
    __table_args__ = (
        CheckConstraint(
            "is_active IN (0, 1)",
            name="ck_regions_is_active",
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
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
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
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
    )


class ContentCategory(Base):
    __tablename__ = "content_categories"
    __table_args__ = (
        CheckConstraint(
            "is_active IN (0, 1)",
            name="ck_content_categories_is_active",
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
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
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


class DataSource(Base):
    __tablename__ = "data_sources"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    provider: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    source_url: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    license_name: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    kogl_type: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    commercial_use_allowed: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    modification_allowed: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    collected_at: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
    )


class LocalContent(Base):
    __tablename__ = "local_contents"
    __table_args__ = (
        UniqueConstraint(
            "source_id",
            "external_id",
            name="uq_local_contents_source_external",
        ),
        CheckConstraint(
            "latitude IS NULL OR latitude BETWEEN -90 AND 90",
            name="ck_local_contents_latitude",
        ),
        CheckConstraint(
            "longitude IS NULL OR longitude BETWEEN -180 AND 180",
            name="ck_local_contents_longitude",
        ),
        CheckConstraint(
            "is_active IN (0, 1)",
            name="ck_local_contents_is_active",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    region_id: Mapped[int] = mapped_column(
        ForeignKey("regions.id", ondelete="RESTRICT"),
        nullable=False,
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("content_categories.id", ondelete="RESTRICT"),
        nullable=False,
    )
    source_id: Mapped[int | None] = mapped_column(
        ForeignKey("data_sources.id", ondelete="SET NULL"),
        nullable=True,
    )

    external_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    title: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    detail_address: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    postal_code: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    homepage_url: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    thumbnail_url: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    start_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )
    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    opening_hours: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    closed_days: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    fee_info: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    parking_info: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    map_level: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    raw_json: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    search_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
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
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
    )
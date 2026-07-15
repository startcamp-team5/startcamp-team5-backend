from datetime import date
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    message: str | None = None
    data: T | None = None


class LocationListItem(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
    )

    location_id: int = Field(
        serialization_alias="locationId",
    )
    name: str
    category: str
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    thumbnail_url: str | None = Field(
        default=None,
        serialization_alias="thumbnailUrl",
    )


class LocationPageData(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
    )

    items: list[LocationListItem]
    page: int
    size: int
    total_elements: int = Field(
        serialization_alias="totalElements",
    )
    total_pages: int = Field(
        serialization_alias="totalPages",
    )


class LocationDetailData(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
    )

    location_id: int = Field(
        serialization_alias="locationId",
    )
    name: str
    category: str

    summary: str | None = None
    description: str | None = None

    address: str | None = None
    detail_address: str | None = Field(
        default=None,
        serialization_alias="detailAddress",
    )
    postal_code: str | None = Field(
        default=None,
        serialization_alias="postalCode",
    )

    latitude: float | None = None
    longitude: float | None = None

    phone: str | None = None
    homepage_url: str | None = Field(
        default=None,
        serialization_alias="homepageUrl",
    )
    thumbnail_url: str | None = Field(
        default=None,
        serialization_alias="thumbnailUrl",
    )

    start_date: date | None = Field(
        default=None,
        serialization_alias="startDate",
    )
    end_date: date | None = Field(
        default=None,
        serialization_alias="endDate",
    )

    opening_hours: str | None = Field(
        default=None,
        serialization_alias="openingHours",
    )
    closed_days: str | None = Field(
        default=None,
        serialization_alias="closedDays",
    )
    fee_info: str | None = Field(
        default=None,
        serialization_alias="feeInfo",
    )
    parking_info: str | None = Field(
        default=None,
        serialization_alias="parkingInfo",
    )


class LocationMapItem(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
    )

    location_id: int = Field(
        serialization_alias="locationId",
    )
    name: str
    category: str
    address: str | None = None
    latitude: float
    longitude: float
    thumbnail_url: str | None = Field(
        default=None,
        serialization_alias="thumbnailUrl",
    )
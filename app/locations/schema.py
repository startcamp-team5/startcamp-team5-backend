from typing import Generic, TypeVar

from pydantic import BaseModel, Field, ConfigDict


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: T


# 목록 조회용
class LocationListItem(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
    )

    location_id: str = Field(
        serialization_alias="locationId"
    )

    name: str

    category: str

    address: str | None = None

    latitude: float | None = None

    longitude: float | None = None

    thumbnail_url: str | None = Field(
        default=None,
        serialization_alias="thumbnailUrl"
    )


class LocationPageResponse(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
    )

    items: list[LocationListItem]

    page: int

    size: int

    total_elements: int = Field(
        serialization_alias="totalElements"
    )

    total_pages: int = Field(
        serialization_alias="totalPages"
    )


# 상세 조회용
class LocationDetailResponse(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
    )


    location_id: str = Field(
        serialization_alias="locationId"
    )

    name: str

    category: str


    summary: str | None = None

    description: str | None = None


    address: str | None = None


    latitude: float | None = None

    longitude: float | None = None


    phone: str | None = None


    homepage_url: str | None = Field(
        default=None,
        serialization_alias="homepageUrl"
    )


    thumbnail_url: str | None = Field(
        default=None,
        serialization_alias="thumbnailUrl"
    )



# 지도용
class LocationMapResponse(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
    )


    location_id: str = Field(
        serialization_alias="locationId"
    )

    name: str

    category: str

    latitude: float

    longitude: float
import math

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.locations.repository import LocationRepository
from app.locations.schema import (
    LocationDetailData,
    LocationListItem,
    LocationMapItem,
    LocationPageData,
)


class LocationService:
    def __init__(self, db: Session) -> None:
        self.repository = LocationRepository(db)

    def get_locations(
        self,
        category: str | None,
        keyword: str | None,
        page: int,
        size: int,
    ) -> LocationPageData:
        normalized_category = self._normalize_category(category)
        normalized_keyword = self._normalize_keyword(keyword)

        self._validate_category(normalized_category)

        rows, total = self.repository.find_all(
            category=normalized_category,
            keyword=normalized_keyword,
            page=page,
            size=size,
        )

        items = [
            LocationListItem(
                location_id=location.id,
                name=location.title,
                category=category_code,
                address=location.address,
                latitude=location.latitude,
                longitude=location.longitude,
                thumbnail_url=location.thumbnail_url,
            )
            for location, category_code in rows
        ]

        total_pages = (
            math.ceil(total / size)
            if total > 0
            else 0
        )

        return LocationPageData(
            items=items,
            page=page,
            size=size,
            total_elements=total,
            total_pages=total_pages,
        )

    def get_location(
        self,
        location_id: int,
    ) -> LocationDetailData:
        result = self.repository.find_detail_by_id(
            location_id
        )

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "errorCode": "LOCATION_NOT_FOUND",
                    "message": "지역정보를 찾을 수 없습니다.",
                },
            )

        location, category_code = result

        return LocationDetailData(
            location_id=location.id,
            name=location.title,
            category=category_code,
            summary=location.summary,
            description=location.description,
            address=location.address,
            detail_address=location.detail_address,
            postal_code=location.postal_code,
            latitude=location.latitude,
            longitude=location.longitude,
            phone=location.phone,
            homepage_url=location.homepage_url,
            thumbnail_url=location.thumbnail_url,
            start_date=location.start_date,
            end_date=location.end_date,
            opening_hours=location.opening_hours,
            closed_days=location.closed_days,
            fee_info=location.fee_info,
            parking_info=location.parking_info,
        )

    def get_map_locations(
        self,
        category: str | None,
        keyword: str | None,
    ) -> list[LocationMapItem]:
        normalized_category = self._normalize_category(category)
        normalized_keyword = self._normalize_keyword(keyword)

        self._validate_category(normalized_category)

        rows = self.repository.find_map_items(
            category=normalized_category,
            keyword=normalized_keyword,
        )

        return [
            LocationMapItem(
                location_id=location.id,
                name=location.title,
                category=category_code,
                address=location.address,
                latitude=location.latitude,
                longitude=location.longitude,
                thumbnail_url=location.thumbnail_url,
            )
            for location, category_code in rows
            if (
                location.latitude is not None
                and location.longitude is not None
            )
        ]

    def _validate_category(
        self,
        category: str | None,
    ) -> None:
        if category is None:
            return

        category_entity = self.repository.find_category_by_code(
            category
        )

        if category_entity is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "errorCode": "INVALID_CATEGORY",
                    "message": "지원하지 않는 카테고리입니다.",
                },
            )

    @staticmethod
    def _normalize_category(
        category: str | None,
    ) -> str | None:
        if category is None:
            return None

        normalized = category.strip().upper()

        return normalized or None

    @staticmethod
    def _normalize_keyword(
        keyword: str | None,
    ) -> str | None:
        if keyword is None:
            return None

        normalized = keyword.strip()

        return normalized or None
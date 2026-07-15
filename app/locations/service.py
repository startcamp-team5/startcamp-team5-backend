import math

from sqlalchemy.orm import Session

from fastapi import HTTPException

from app.locations.repository import (
    LocationRepository
)

from app.locations.schema import (
    LocationListItem,
    LocationPageResponse,
    LocationDetailResponse,
    LocationMapResponse
)



class LocationService:


    def __init__(
        self,
        db: Session
    ):

        self.repository = LocationRepository(db)



    # 목록

    def get_locations(
        self,
        category,
        keyword,
        page,
        size
    ):


        rows, total = (
            self.repository.find_all(
                category,
                keyword,
                page,
                size
            )
        )



        items = []


        for location, category_code in rows:

            items.append(

                LocationListItem(

                    location_id=
                    location.external_id,

                    name=
                    location.title,

                    category=
                    category_code,

                    address=
                    location.address,

                    latitude=
                    location.latitude,

                    longitude=
                    location.longitude,

                    thumbnail_url=
                    location.thumbnail_url

                )

            )



        return LocationPageResponse(

            items=items,

            page=page,

            size=size,

            total_elements=total,

            total_pages=
            math.ceil(total / size)

        )



    # 상세

    def get_location(
        self,
        external_id: str
    ):


        result = (
            self.repository
            .find_by_external_id(
                external_id
            )
        )


        if result is None:

            raise HTTPException(
                404,
                "지역정보 없음"
            )



        location, category = result



        return LocationDetailResponse(

            location_id=
            location.external_id,

            name=
            location.title,

            category=
            category,

            summary=
            location.summary,

            description=
            location.description,

            address=
            location.address,

            latitude=
            location.latitude,

            longitude=
            location.longitude,

            phone=
            location.phone,

            homepage_url=
            location.homepage_url,

            thumbnail_url=
            location.thumbnail_url

        )



    # 지도

    def get_map_locations(
        self,
        category
    ):


        rows = (
            self.repository
            .find_map_data(category)
        )



        return [

            LocationMapResponse(

                location_id=
                location.external_id,

                name=
                location.title,

                category=
                category_code,

                latitude=
                location.latitude,

                longitude=
                location.longitude

            )

            for location, category_code in rows

        ]
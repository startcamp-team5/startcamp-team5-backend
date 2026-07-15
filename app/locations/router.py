from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.locations.schema import (
    ApiResponse,
    LocationDetailData,
    LocationMapItem,
    LocationPageData,
)
from app.locations.service import LocationService


router = APIRouter(
    prefix="/locations",
    tags=["지역 정보"],
)

DbSession = Annotated[
    Session,
    Depends(get_db),
]


@router.get(
    "",
    response_model=ApiResponse[LocationPageData],
    response_model_by_alias=True,
    summary="지역정보 목록 조회",
)
def get_locations(
    db: DbSession,
    category: str | None = Query(
        default=None,
        description="콘텐츠 카테고리 코드",
        examples=["TOURIST_SPOT"],
    ),
    keyword: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
        description="장소명·주소·설명 검색어",
    ),
    page: int = Query(
        default=1,
        ge=1,
        description="페이지 번호",
    ),
    size: int = Query(
        default=20,
        ge=1,
        le=100,
        description="페이지 크기",
    ),
) -> ApiResponse[LocationPageData]:
    data = LocationService(db).get_locations(
        category=category,
        keyword=keyword,
        page=page,
        size=size,
    )

    return ApiResponse(
        success=True,
        message="지역정보 목록을 조회했습니다.",
        data=data,
    )


@router.get(
    "/map",
    response_model=ApiResponse[list[LocationMapItem]],
    response_model_by_alias=True,
    summary="지도 데이터 조회",
)
def get_map_locations(
    db: DbSession,
    category: str | None = Query(
        default=None,
        description="지도에 표시할 카테고리 코드",
        examples=["RESTAURANT"],
    ),
    keyword: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
        description="장소명·주소 검색어",
    ),
) -> ApiResponse[list[LocationMapItem]]:
    data = LocationService(db).get_map_locations(
        category=category,
        keyword=keyword,
    )

    return ApiResponse(
        success=True,
        message="지도 데이터를 조회했습니다.",
        data=data,
    )


@router.get(
    "/{location_id}",
    response_model=ApiResponse[LocationDetailData],
    response_model_by_alias=True,
    summary="지역정보 상세 조회",
)
def get_location(
    db: DbSession,
    location_id: int = Path(
        gt=0,
        description="local_contents 테이블의 내부 ID",
    ),
) -> ApiResponse[LocationDetailData]:
    data = LocationService(db).get_location(
        location_id
    )

    return ApiResponse(
        success=True,
        message="지역정보를 조회했습니다.",
        data=data,
    )
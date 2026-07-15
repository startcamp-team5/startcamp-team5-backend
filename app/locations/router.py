from fastapi import (
    APIRouter,
    Depends,
    Query,
    Path,
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.locations.service import LocationService

from app.locations.schema import (
    ApiResponse,
    LocationPageResponse,
    LocationDetailResponse,
    LocationMapResponse,
)


router = APIRouter(
    prefix="/locations",
    tags=["지역 정보 API"],
)


# --------------------------------------------------
# 1. 지역정보 목록 조회
# --------------------------------------------------

@router.get(
    "",
    response_model=ApiResponse[LocationPageResponse],
    summary="지역정보 목록 조회",
    description="""
    구미/경북 지역의 관광지, 맛집 등 지역 콘텐츠 목록을 조회합니다.

    - 카테고리별 조회 가능
    - 장소명 및 주소 기반 검색 가능
    - 페이지 단위 조회 지원

    사용 목적:
    - 지역정보 목록 화면
    - 검색 결과 화면
    - 관광지/맛집 리스트 표시
    """,
    response_description="조회된 지역정보 목록",
)
def get_locations(

    category: str | None = Query(
        default=None,
        title="카테고리",
        description="""
        조회할 콘텐츠 카테고리 코드

        예:
        - TOURIST_SPOT : 관광지
        - RESTAURANT : 음식점
        - CULTURAL_FACILITY : 문화시설
        """,
        examples=[
            "TOURIST_SPOT"
        ],
    ),


    keyword: str | None = Query(
        default=None,
        title="검색어",
        description="""
        장소명, 주소, 설명에서 검색할 키워드

        예:
        금오산
        """,
        examples=[
            "금오산"
        ],
    ),


    page: int = Query(
        default=1,
        ge=1,
        title="페이지 번호",
        description="""
        조회할 페이지 번호

        기본값:
        1
        """,
        examples=[
            1
        ],
    ),


    size: int = Query(
        default=20,
        ge=1,
        le=100,
        title="페이지 크기",
        description="""
        한 페이지에 조회할 데이터 개수

        최대:
        100개
        """,
        examples=[
            20
        ],
    ),


    db: Session = Depends(get_db),

):


    data = LocationService(db).get_locations(

        category,

        keyword,

        page,

        size

    )


    return ApiResponse(

        success=True,

        message="지역정보 목록 조회 성공",

        data=data

    )



# --------------------------------------------------
# 2. 지도 데이터 조회
# --------------------------------------------------

@router.get(
    "/map",
    response_model=ApiResponse[list[LocationMapResponse]],

    summary="지도 마커 데이터 조회",

    description="""
    지도 화면에 표시할 지역정보 좌표 데이터를 조회합니다.

    반환 데이터는 지도 Marker 표시를 위한 최소 정보만 제공합니다.

    포함 정보:
    - 지역 ID
    - 장소명
    - 카테고리
    - 위도(latitude)
    - 경도(longitude)

    좌표(latitude, longitude)가 존재하는 데이터만 반환합니다.
    """,

    response_description="지도 표시용 지역정보 좌표 목록",
)
def get_map_locations(


    category: str | None = Query(

        default=None,

        title="카테고리",

        description="""
        지도에서 표시할 지역정보 카테고리

        예:
        RESTAURANT
        TOURIST_SPOT
        """,

        examples=[
            "RESTAURANT"
        ],

    ),


    db: Session = Depends(get_db),

):


    data = LocationService(db).get_map_locations(

        category

    )


    return ApiResponse(

        success=True,

        message="지도 데이터 조회 성공",

        data=data

    )



# --------------------------------------------------
# 3. 지역정보 상세 조회
# --------------------------------------------------

@router.get(
    "/{external_id}",

    response_model=ApiResponse[LocationDetailResponse],

    summary="지역정보 상세 조회",

    description="""
    특정 지역정보의 상세 내용을 조회합니다.

    요청 ID는 내부 DB PK가 아닌
    공공데이터 원본 식별자인 external_id를 사용합니다.

    예:
    /api/locations/126016

    조회 가능 정보:
    - 장소명
    - 카테고리
    - 설명
    - 주소
    - 위치 좌표
    - 홈페이지
    - 이미지 정보
    """,

    response_description="지역정보 상세 데이터",

)
def get_location(


    external_id: str = Path(

        title="지역정보 ID",

        description="""
        공공데이터 원본 식별자

        local_contents.external_id 값

        예:
        126016
        """,

        examples=[
            "126016"
        ],

    ),


    db: Session = Depends(get_db),


):


    data = LocationService(db).get_location(

        external_id

    )


    return ApiResponse(

        success=True,

        message="지역정보 상세 조회 성공",

        data=data

    )
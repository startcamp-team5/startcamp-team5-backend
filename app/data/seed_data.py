import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.init_db import create_tables
from app.locations.model import (
    ContentCategory,
    DataSource,
    LocalContent,
    Region,
)
from app.posts.model import BoardCategory


DATA_DIR = Path(__file__).resolve().parent
JSON_PATTERN = "구미_경북권_*.json"


CONTENT_CATEGORIES = [
    ("TOURIST_SPOT", "관광지"),
    ("CULTURAL_FACILITY", "문화시설"),
    ("FESTIVAL_EVENT", "축제·공연"),
    ("TRAVEL_COURSE", "여행 코스"),
    ("LEISURE_SPORTS", "레포츠"),
    ("ACCOMMODATION", "숙박"),
    ("SHOPPING", "쇼핑"),
    ("RESTAURANT", "음식점"),
]


BOARD_CATEGORIES = [
    ("FREE", "자유게시판"),
    ("QUESTION", "질문"),
    ("REVIEW", "방문 후기"),
    ("RECOMMENDATION", "장소 추천"),
    ("FESTIVAL", "축제·행사"),
    ("RESTAURANT", "맛집 정보"),
]


CONTENT_TYPE_MAPPING = {
    "관광지": "TOURIST_SPOT",
    "문화시설": "CULTURAL_FACILITY",
    "축제공연행사": "FESTIVAL_EVENT",
    "축제·공연": "FESTIVAL_EVENT",
    "축제": "FESTIVAL_EVENT",
    "여행코스": "TRAVEL_COURSE",
    "레포츠": "LEISURE_SPORTS",
    "숙박": "ACCOMMODATION",
    "쇼핑": "SHOPPING",
    "음식점": "RESTAURANT",
    "맛집": "RESTAURANT",
}


def normalize_text(value: Any) -> str | None:
    """빈 문자열을 None으로 변환하고 문자열 앞뒤 공백을 제거한다."""
    if value is None:
        return None

    text = str(value).strip()

    if not text:
        return None

    return text


def parse_float(value: Any) -> float | None:
    """문자열 또는 숫자를 float로 변환한다."""
    text = normalize_text(value)

    if text is None:
        return None

    try:
        return float(text)
    except (TypeError, ValueError):
        return None


def parse_datetime(value: Any) -> datetime | None:
    """
    공공데이터의 날짜·시간 문자열을 datetime으로 변환한다.

    예:
    20230831114818
    20260616113921
    """
    text = normalize_text(value)

    if text is None:
        return None

    formats = (
        "%Y%m%d%H%M%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y%m%d",
        "%Y-%m-%d",
    )

    for date_format in formats:
        try:
            return datetime.strptime(text, date_format)
        except ValueError:
            continue

    return None


def parse_date(value: Any) -> date | None:
    """축제 시작일·종료일 등을 date로 변환한다."""
    parsed = parse_datetime(value)

    if parsed is None:
        return None

    return parsed.date()


def load_json_file(json_path: Path) -> dict[str, Any]:
    """JSON 파일을 UTF-8 BOM까지 고려하여 읽는다."""
    with json_path.open("r", encoding="utf-8-sig") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError(
            f"{json_path.name}: 최상위 JSON은 객체 형식이어야 합니다."
        )

    return data


def extract_items(
    json_path: Path,
    data: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    최상위 items 배열을 추출하고 total 값과 실제 개수를 비교한다.
    """
    items = data.get("items", [])

    if not isinstance(items, list):
        raise ValueError(
            f"{json_path.name}: items가 배열 형식이 아닙니다."
        )

    valid_items = [
        item
        for item in items
        if isinstance(item, dict)
    ]

    declared_total = data.get("total")

    if declared_total is not None:
        try:
            expected_total = int(declared_total)

            if expected_total != len(valid_items):
                print(
                    f"[경고] {json_path.name}: "
                    f"total={expected_total}, "
                    f"실제 items={len(valid_items)}"
                )
        except (TypeError, ValueError):
            print(
                f"[경고] {json_path.name}: "
                f"total 값이 숫자가 아닙니다: {declared_total}"
            )

    return valid_items


def resolve_category_code(
    content_type: str | None,
    file_name: str,
) -> str:
    """
    JSON 최상위 contentType을 우선 사용하고,
    값이 없으면 파일명으로 카테고리를 판별한다.
    """
    normalized_content_type = (
        content_type.replace(" ", "")
        if content_type
        else ""
    )

    if normalized_content_type in CONTENT_TYPE_MAPPING:
        return CONTENT_TYPE_MAPPING[normalized_content_type]

    normalized_file_name = file_name.replace(" ", "")

    for keyword, category_code in CONTENT_TYPE_MAPPING.items():
        if keyword in normalized_file_name:
            return category_code

    raise ValueError(
        f"카테고리를 결정할 수 없습니다. "
        f"contentType={content_type}, file={file_name}"
    )


def get_or_create_region(
    db: Session,
    region_name: str | None,
) -> Region:
    region_code = "GUMI_GYEONGBUK"
    resolved_name = region_name or "구미 경북권"

    region = db.scalar(
        select(Region).where(Region.code == region_code)
    )

    if region is not None:
        if region.name != resolved_name:
            region.name = resolved_name

        return region

    region = Region(
        code=region_code,
        name=resolved_name,
        description="구미 및 경상북도 지역 공공데이터 권역",
        is_active=1,
    )

    db.add(region)
    db.flush()

    return region


def seed_content_categories(
    db: Session,
) -> dict[str, ContentCategory]:
    categories: dict[str, ContentCategory] = {}

    for display_order, (code, name) in enumerate(
        CONTENT_CATEGORIES,
        start=1,
    ):
        category = db.scalar(
            select(ContentCategory).where(
                ContentCategory.code == code
            )
        )

        if category is None:
            category = ContentCategory(
                code=code,
                name=name,
                display_order=display_order,
                is_active=1,
            )

            db.add(category)
            db.flush()

        categories[code] = category

    return categories


def seed_board_categories(db: Session) -> None:
    for display_order, (code, name) in enumerate(
        BOARD_CATEGORIES,
        start=1,
    ):
        category = db.scalar(
            select(BoardCategory).where(
                BoardCategory.code == code
            )
        )

        if category is None:
            db.add(
                BoardCategory(
                    code=code,
                    name=name,
                    display_order=display_order,
                    is_active=1,
                )
            )


def get_or_create_data_source(
    db: Session,
    json_path: Path,
    content_type: str,
    content_type_id: str | None,
) -> DataSource:
    """
    JSON 파일별로 data_sources를 생성한다.

    예:
    구미_경북권_관광지.json
    구미_경북권_음식점.json
    """
    source_name = json_path.stem

    source = db.scalar(
        select(DataSource).where(
            DataSource.name == source_name
        )
    )

    description = (
        f"contentType={content_type}, "
        f"contentTypeId={content_type_id or '없음'}"
    )

    if source is not None:
        source.provider = "한국관광공사 관광정보"
        source.description = description

        return source

    source = DataSource(
        name=source_name,
        provider="한국관광공사 관광정보",
        source_url=None,
        license_name="공공데이터 라이선스 확인 필요",
        kogl_type=None,
        commercial_use_allowed=None,
        modification_allowed=None,
        collected_at=date.today(),
        description=description,
    )

    db.add(source)
    db.flush()

    return source


def build_search_text(
    item: dict[str, Any],
    content_type: str,
    region_name: str,
) -> str:
    """
    검색 및 챗봇에서 활용할 통합 문자열을 만든다.
    """
    values = [
        item.get("title"),
        content_type,
        region_name,
        item.get("addr1"),
        item.get("addr2"),
        item.get("tel"),
        item.get("cat1"),
        item.get("cat2"),
        item.get("cat3"),
        item.get("sigungucode"),
        item.get("lDongRegnCd"),
        item.get("lDongSignguCd"),
    ]

    return " ".join(
        str(value).strip()
        for value in values
        if normalize_text(value) is not None
    )


def build_summary(
    item: dict[str, Any],
    content_type: str,
) -> str | None:
    """
    목록용 간단한 설명을 생성한다.
    JSON에 overview가 없으므로 주소와 유형을 조합한다.
    """
    title = normalize_text(item.get("title"))
    address = normalize_text(item.get("addr1"))

    if title and address:
        return f"{content_type} · {address}"

    if title:
        return f"{content_type} 정보"

    return None


def find_existing_content(
    db: Session,
    source_id: int,
    external_id: str | None,
    title: str,
    address: str | None,
) -> LocalContent | None:
    """
    contentid가 있으면 source_id + external_id로 검색한다.

    contentid가 없는 경우에는 제목과 주소 조합으로 임시 중복 검사를 한다.
    """
    if external_id is not None:
        return db.scalar(
            select(LocalContent).where(
                LocalContent.source_id == source_id,
                LocalContent.external_id == external_id,
            )
        )

    query = select(LocalContent).where(
        LocalContent.source_id == source_id,
        LocalContent.title == title,
    )

    if address is not None:
        query = query.where(LocalContent.address == address)

    return db.scalar(query)


def upsert_local_content(
    db: Session,
    item: dict[str, Any],
    region: Region,
    category: ContentCategory,
    source: DataSource,
    content_type: str,
) -> str:
    title = normalize_text(item.get("title"))

    if title is None:
        return "skipped"

    external_id = normalize_text(item.get("contentid"))
    address = normalize_text(item.get("addr1"))

    existing = find_existing_content(
        db=db,
        source_id=source.id,
        external_id=external_id,
        title=title,
        address=address,
    )

    raw_created_at = parse_datetime(item.get("createdtime"))
    raw_updated_at = parse_datetime(item.get("modifiedtime"))

    values = {
        "region_id": region.id,
        "category_id": category.id,
        "source_id": source.id,
        "external_id": external_id,
        "title": title,
        "summary": build_summary(item, content_type),
        "description": None,
        "address": address,
        "detail_address": normalize_text(item.get("addr2")),
        "postal_code": normalize_text(item.get("zipcode")),

        # 한국관광공사 데이터 기준:
        # mapx = 경도, mapy = 위도
        "latitude": parse_float(item.get("mapy")),
        "longitude": parse_float(item.get("mapx")),

        "phone": normalize_text(item.get("tel")),
        "homepage_url": None,
        "thumbnail_url": (
            normalize_text(item.get("firstimage"))
            or normalize_text(item.get("firstimage2"))
        ),

        # 관광지 등 일반 콘텐츠에는 날짜가 없으므로 기본 None
        "start_date": parse_date(
            item.get("eventstartdate")
            or item.get("startdate")
        ),
        "end_date": parse_date(
            item.get("eventenddate")
            or item.get("enddate")
        ),

        "opening_hours": normalize_text(
            item.get("usetime")
            or item.get("opentime")
        ),
        "closed_days": normalize_text(
            item.get("restdate")
        ),
        "fee_info": normalize_text(
            item.get("usefee")
        ),
        "parking_info": normalize_text(
            item.get("parking")
        ),

        "map_level": (
            int(item["mlevel"])
            if normalize_text(item.get("mlevel"))
            and str(item["mlevel"]).isdigit()
            else None
        ),

        "raw_json": json.dumps(
            item,
            ensure_ascii=False,
        ),
        "search_text": build_search_text(
            item=item,
            content_type=content_type,
            region_name=region.name,
        ),
        "is_active": 1,
    }

    if existing is not None:
        for field_name, value in values.items():
            setattr(existing, field_name, value)

        if raw_updated_at is not None:
            existing.updated_at = raw_updated_at

        return "updated"

    content = LocalContent(**values)

    if raw_created_at is not None:
        content.created_at = raw_created_at

    if raw_updated_at is not None:
        content.updated_at = raw_updated_at

    db.add(content)

    return "inserted"


def process_json_file(
    db: Session,
    json_path: Path,
    categories: dict[str, ContentCategory],
) -> dict[str, int]:
    data = load_json_file(json_path)

    region_name = normalize_text(data.get("region")) or "구미 경북권"
    content_type = normalize_text(data.get("contentType"))

    if content_type is None:
        raise ValueError(
            f"{json_path.name}: contentType이 없습니다."
        )

    content_type_id = normalize_text(data.get("contentTypeId"))

    category_code = resolve_category_code(
        content_type=content_type,
        file_name=json_path.name,
    )
    category = categories[category_code]

    region = get_or_create_region(
        db=db,
        region_name=region_name,
    )

    source = get_or_create_data_source(
        db=db,
        json_path=json_path,
        content_type=content_type,
        content_type_id=content_type_id,
    )

    items = extract_items(
        json_path=json_path,
        data=data,
    )

    result_count = {
        "inserted": 0,
        "updated": 0,
        "skipped": 0,
    }

    for item in items:
        result = upsert_local_content(
            db=db,
            item=item,
            region=region,
            category=category,
            source=source,
            content_type=content_type,
        )

        result_count[result] += 1

    print(
        f"[처리 완료] {json_path.name} "
        f"({content_type}, contentTypeId={content_type_id}) "
        f"- 추가 {result_count['inserted']}건, "
        f"수정 {result_count['updated']}건, "
        f"제외 {result_count['skipped']}건"
    )

    return result_count


def seed_database() -> None:

    json_files = sorted(DATA_DIR.glob(JSON_PATTERN))

    if not json_files:
        raise FileNotFoundError(
            f"JSON 파일을 찾을 수 없습니다.\n"
            f"경로: {DATA_DIR}\n"
            f"패턴: {JSON_PATTERN}"
        )


    total_inserted = 0
    total_updated = 0
    total_skipped = 0


    with SessionLocal() as db:

        try:

            categories = seed_content_categories(db)

            seed_board_categories(db)

            db.flush()


            for json_path in json_files:

                result = process_json_file(
                    db=db,
                    json_path=json_path,
                    categories=categories,
                )

                total_inserted += result["inserted"]
                total_updated += result["updated"]
                total_skipped += result["skipped"]


            db.commit()


        except Exception:

            db.rollback()

            raise

    print()
    print("========== 전체 적재 결과 ==========")
    print(f"대상 JSON 파일: {len(json_files)}개")
    print(f"추가: {total_inserted}건")
    print(f"수정: {total_updated}건")
    print(f"제외: {total_skipped}건")
    print("===================================")


if __name__ == "__main__":
    seed_database()
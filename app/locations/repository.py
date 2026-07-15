from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.locations.model import ContentCategory, LocalContent


class LocationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def find_category_by_code(
        self,
        category_code: str,
    ) -> ContentCategory | None:
        statement = select(ContentCategory).where(
            ContentCategory.code == category_code,
            ContentCategory.is_active == 1,
        )

        return self.db.scalar(statement)

    def find_all(
        self,
        category: str | None,
        keyword: str | None,
        page: int,
        size: int,
    ) -> tuple[list[tuple[LocalContent, str]], int]:
        filters = [
            LocalContent.is_active == 1,
            ContentCategory.is_active == 1,
        ]

        if category is not None:
            filters.append(
                ContentCategory.code == category
            )

        if keyword is not None:
            search_keyword = f"%{keyword.strip()}%"

            filters.append(
                or_(
                    LocalContent.title.like(search_keyword),
                    LocalContent.address.like(search_keyword),
                    LocalContent.description.like(search_keyword),
                    LocalContent.search_text.like(search_keyword),
                )
            )

        list_statement = (
            select(
                LocalContent,
                ContentCategory.code,
            )
            .join(
                ContentCategory,
                ContentCategory.id == LocalContent.category_id,
            )
            .where(*filters)
            .order_by(
                LocalContent.title.asc(),
                LocalContent.id.asc(),
            )
            .offset((page - 1) * size)
            .limit(size)
        )

        count_statement = (
            select(func.count(LocalContent.id))
            .select_from(LocalContent)
            .join(
                ContentCategory,
                ContentCategory.id == LocalContent.category_id,
            )
            .where(*filters)
        )

        rows = self.db.execute(list_statement).all()
        total = self.db.scalar(count_statement) or 0

        return [
            (row[0], row[1])
            for row in rows
        ], total

    def find_detail_by_id(
        self,
        location_id: int,
    ) -> tuple[LocalContent, str] | None:
        statement = (
            select(
                LocalContent,
                ContentCategory.code,
            )
            .join(
                ContentCategory,
                ContentCategory.id == LocalContent.category_id,
            )
            .where(
                LocalContent.id == location_id,
                LocalContent.is_active == 1,
                ContentCategory.is_active == 1,
            )
        )

        row = self.db.execute(statement).first()

        if row is None:
            return None

        return row[0], row[1]

    def find_map_items(
        self,
        category: str | None,
        keyword: str | None,
    ) -> list[tuple[LocalContent, str]]:
        filters = [
            LocalContent.is_active == 1,
            ContentCategory.is_active == 1,
            LocalContent.latitude.is_not(None),
            LocalContent.longitude.is_not(None),
        ]

        if category is not None:
            filters.append(
                ContentCategory.code == category
            )

        if keyword is not None:
            search_keyword = f"%{keyword.strip()}%"

            filters.append(
                or_(
                    LocalContent.title.like(search_keyword),
                    LocalContent.address.like(search_keyword),
                    LocalContent.search_text.like(search_keyword),
                )
            )

        statement = (
            select(
                LocalContent,
                ContentCategory.code,
            )
            .join(
                ContentCategory,
                ContentCategory.id == LocalContent.category_id,
            )
            .where(*filters)
            .order_by(
                LocalContent.title.asc(),
                LocalContent.id.asc(),
            )
        )

        rows = self.db.execute(statement).all()

        return [
            (row[0], row[1])
            for row in rows
        ]
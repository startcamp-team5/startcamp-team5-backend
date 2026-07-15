from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session


from app.locations.model import (
    LocalContent,
    ContentCategory
)



class LocationRepository:


    def __init__(
        self,
        db: Session
    ):
        self.db = db



    # 목록 조회

    def find_all(
        self,
        category: str | None,
        keyword: str | None,
        page: int,
        size: int
    ):


        conditions = [
            LocalContent.is_active == 1
        ]



        if category:

            conditions.append(
                ContentCategory.code == category
            )


        if keyword:

            keyword = f"%{keyword}%"

            conditions.append(
                or_(
                    LocalContent.title.like(keyword),
                    LocalContent.address.like(keyword)
                )
            )



        query = (
            select(
                LocalContent,
                ContentCategory.code
            )
            .join(
                ContentCategory,
                ContentCategory.id
                ==
                LocalContent.category_id
            )
            .where(
                *conditions
            )
            .offset(
                (page-1)*size
            )
            .limit(size)
        )


        count_query = (
            select(
                func.count(LocalContent.id)
            )
            .join(
                ContentCategory,
                ContentCategory.id
                ==
                LocalContent.category_id
            )
            .where(
                *conditions
            )
        )



        result = self.db.execute(query).all()

        total = self.db.scalar(
            count_query
        )


        return result, total or 0



    # 상세 조회

    def find_by_external_id(
        self,
        external_id: str
    ):


        query = (
            select(
                LocalContent,
                ContentCategory.code
            )
            .join(
                ContentCategory,
                ContentCategory.id
                ==
                LocalContent.category_id
            )
            .where(
                LocalContent.external_id
                ==
                external_id
            )
        )


        return self.db.execute(
            query
        ).first()



    # 지도 조회

    def find_map_data(
        self,
        category: str | None
    ):


        conditions = [

            LocalContent.latitude.is_not(None),

            LocalContent.longitude.is_not(None)

        ]


        if category:

            conditions.append(
                ContentCategory.code
                ==
                category
            )


        query = (

            select(
                LocalContent,
                ContentCategory.code
            )

            .join(
                ContentCategory,
                ContentCategory.id
                ==
                LocalContent.category_id
            )

            .where(
                *conditions
            )

        )


        return self.db.execute(
            query
        ).all()
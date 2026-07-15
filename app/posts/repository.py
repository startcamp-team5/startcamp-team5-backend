from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.locations.model import LocalContent
from app.posts.model import BoardCategory, Post


class PostRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def find_category_by_code(
        self,
        category_code: str,
    ) -> BoardCategory | None:
        statement = select(BoardCategory).where(
            BoardCategory.code == category_code,
            BoardCategory.is_active == 1,
        )

        return self.db.scalar(statement)

    def find_local_content_by_id(
        self,
        local_content_id: int,
    ) -> LocalContent | None:
        statement = select(LocalContent).where(
            LocalContent.id == local_content_id,
            LocalContent.is_active == 1,
        )

        return self.db.scalar(statement)

    def save(self, post: Post) -> Post:
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)

        return post

    def find_by_id(
        self,
        post_id: int,
    ) -> Post | None:
        statement = select(Post).where(
            Post.id == post_id,
            Post.is_deleted == 0,
        )

        return self.db.scalar(statement)

    def find_detail_by_id(
        self,
        post_id: int,
    ) -> tuple[Post, str] | None:
        statement = (
            select(
                Post,
                BoardCategory.code,
            )
            .join(
                BoardCategory,
                Post.board_category_id == BoardCategory.id,
            )
            .where(
                Post.id == post_id,
                Post.is_deleted == 0,
            )
        )

        row = self.db.execute(statement).first()

        if row is None:
            return None

        return row[0], row[1]

    def find_all(
        self,
        category: str | None,
        keyword: str | None,
        page: int,
        size: int,
    ) -> tuple[list[tuple[Post, str]], int]:
        filters = [Post.is_deleted == 0]

        if category:
            filters.append(BoardCategory.code == category)

        if keyword:
            search_keyword = f"%{keyword.strip()}%"

            filters.append(
                or_(
                    Post.title.like(search_keyword),
                    Post.content.like(search_keyword),
                )
            )

        list_statement = (
            select(
                Post,
                BoardCategory.code,
            )
            .join(
                BoardCategory,
                Post.board_category_id == BoardCategory.id,
            )
            .where(*filters)
            .order_by(Post.created_at.desc())
            .offset((page - 1) * size)
            .limit(size)
        )

        count_statement = (
            select(func.count(Post.id))
            .select_from(Post)
            .join(
                BoardCategory,
                Post.board_category_id == BoardCategory.id,
            )
            .where(*filters)
        )

        rows = self.db.execute(list_statement).all()
        total = self.db.scalar(count_statement) or 0

        return [(row[0], row[1]) for row in rows], total

    def increase_view_count(self, post: Post) -> Post:
        post.view_count += 1

        self.db.commit()
        self.db.refresh(post)

        return post

    def update(
        self,
        post: Post,
        title: str,
        content: str,
    ) -> Post:
        post.title = title
        post.content = content

        self.db.commit()
        self.db.refresh(post)

        return post

    def soft_delete(self, post: Post) -> None:
        from datetime import datetime

        post.is_deleted = 1
        post.deleted_at = datetime.now()
        post.updated_at = datetime.now()

        self.db.commit()
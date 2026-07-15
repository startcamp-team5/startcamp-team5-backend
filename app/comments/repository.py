from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.comments.model import Comment

class CommentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def save(self, comment: Comment) -> Comment:
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def find_by_id(self, comment_id: int) -> Comment | None:
        statement = select(Comment).where(Comment.id == comment_id)
        return self.db.scalar(statement)

    def find_by_post_id(
        self,
        post_id: int,
        page: int = 1,
        size: int = 20,
    ) -> tuple[list[Comment], int]:
        list_stmt = (
            select(Comment)
            .where(Comment.post_id == post_id)
            .order_by(Comment.created_at.asc())
            .offset((page - 1) * size)
            .limit(size)
        )

        count_stmt = (
            select(func.count(Comment.id))
            .where(Comment.post_id == post_id)
        )

        rows = self.db.execute(list_stmt).scalars().all()
        total = self.db.scalar(count_stmt) or 0

        return rows, total

    def delete(self, comment: Comment) -> None:
        self.db.delete(comment)
        self.db.commit()

    def update(self, comment: Comment, content: str) -> Comment:
        comment.content = content
        self.db.commit()
        self.db.refresh(comment)
        return comment
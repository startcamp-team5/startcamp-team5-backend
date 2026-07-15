from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.comments.model import Comment
from app.comments.repository import CommentRepository
from app.comments.schema import CommentCreateData, CommentCreateRequest, CommentUpdateRequest
from app.posts.repository import PostRepository


class CommentService:
    def __init__(self, db: Session) -> None:
        self.comment_repo = CommentRepository(db)
        self.post_repo = PostRepository(db)

    def create_comment(
        self,
        post_id: int,
        request: CommentCreateRequest,
    ) -> CommentCreateData:
        post = self.post_repo.find_by_id(post_id)
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="게시글을 찾을 수 없습니다.",
            )

        comment = Comment(
            post_id=post_id,
            content=request.content,
            author_name=request.author_name,
            edit_password=request.edit_password,
        )

        saved = self.comment_repo.save(comment)

        return CommentCreateData(comment_id=saved.id)

    def list_comments(
        self,
        post_id: int,
        page: int = 1,
        size: int = 20,
    ) -> tuple[list[Comment], int]:
        post = self.post_repo.find_by_id(post_id)
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="게시글을 찾을 수 없습니다.",
            )

        return self.comment_repo.find_by_post_id(post_id=post_id, page=page, size=size)

    def delete_comment(self, comment_id: int, edit_password: str) -> None:
        comment = self.comment_repo.find_by_id(comment_id)
        if comment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="댓글을 찾을 수 없습니다.",
            )

        if comment.edit_password != edit_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="비밀번호가 일치하지 않습니다.",
            )

        self.comment_repo.delete(comment)

    def update_comment(self, comment_id: int, request: CommentUpdateRequest) -> None:
        comment = self.comment_repo.find_by_id(comment_id)
        if comment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="댓글을 찾을 수 없습니다.")
        if comment.edit_password != request.edit_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="비밀번호가 일치하지 않습니다.")
        self.comment_repo.update(comment=comment, content=request.content)
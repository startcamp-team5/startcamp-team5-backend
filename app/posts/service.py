import math

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.posts.model import Post
from app.posts.repository import PostRepository
from app.posts.schema import (
    PostCreateData,
    PostCreateRequest,
    PostDeleteRequest,
    PostDetailData,
    PostListItem,
    PostPageData,
    PostUpdateRequest,
)


class PostService:
    def __init__(self, db: Session) -> None:
        self.repository = PostRepository(db)

    def get_posts(
        self,
        category: str | None,
        keyword: str | None,
        page: int,
        size: int,
    ) -> PostPageData:
        normalized_category = (
            category.strip().upper()
            if category
            else None
        )

        rows, total = self.repository.find_all(
            category=normalized_category,
            keyword=keyword,
            page=page,
            size=size,
        )

        items = [
            PostListItem(
                post_id=post.id,
                local_content_id=post.local_content_id,
                category=category_code,
                title=post.title,
                author_name=post.author_name,
                view_count=post.view_count,
                created_at=post.created_at,
            )
            for post, category_code in rows
        ]

        total_pages = math.ceil(total / size) if total > 0 else 0

        return PostPageData(
            items=items,
            page=page,
            size=size,
            total_elements=total,
            total_pages=total_pages,
        )

    def get_post(
        self,
        post_id: int,
    ) -> PostDetailData:
        result = self.repository.find_detail_by_id(post_id)

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="게시글을 찾을 수 없습니다.",
            )

        post, category_code = result

        post = self.repository.increase_view_count(post)

        return PostDetailData(
            post_id=post.id,
            local_content_id=post.local_content_id,
            category=category_code,
            title=post.title,
            content=post.content,
            author_name=post.author_name,
            view_count=post.view_count,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )

    def create_post(
        self,
        request: PostCreateRequest,
    ) -> PostCreateData:
        category_code = request.board_category_code.upper()

        board_category = self.repository.find_category_by_code(
            category_code
        )

        if board_category is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="존재하지 않는 게시판 카테고리입니다.",
            )

        if request.local_content_id is not None:
            local_content = (
                self.repository.find_local_content_by_id(
                    request.local_content_id
                )
            )

            if local_content is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="연결할 지역정보를 찾을 수 없습니다.",
                )

        post = Post(
            board_category_id=board_category.id,
            local_content_id=request.local_content_id,
            title=request.title,
            content=request.content,
            author_name=request.author_name,
            edit_password=request.edit_password,
            view_count=0,
            is_deleted=0,
        )

        saved_post = self.repository.save(post)

        return PostCreateData(
            post_id=saved_post.id,
        )

    def update_post(
        self,
        post_id: int,
        request: PostUpdateRequest,
    ) -> None:
        post = self._get_post_or_raise(post_id)

        self._validate_password(
            post=post,
            password=request.edit_password,
        )

        self.repository.update(
            post=post,
            title=request.title,
            content=request.content,
        )

    def delete_post(
        self,
        post_id: int,
        request: PostDeleteRequest,
    ) -> None:
        post = self._get_post_or_raise(post_id)

        self._validate_password(
            post=post,
            password=request.edit_password,
        )

        self.repository.soft_delete(post)

    def _get_post_or_raise(
        self,
        post_id: int,
    ) -> Post:
        post = self.repository.find_by_id(post_id)

        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="게시글을 찾을 수 없습니다.",
            )

        return post

    @staticmethod
    def _validate_password(
        post: Post,
        password: str,
    ) -> None:
        if post.edit_password != password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="비밀번호가 일치하지 않습니다.",
            )
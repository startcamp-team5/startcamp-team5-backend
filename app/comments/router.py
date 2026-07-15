import math

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.posts.schema import ApiResponse
from app.comments.schema import (
    CommentCreateRequest,
    CommentCreateData,
    CommentListItem,
    CommentPageData,
    CommentDeleteRequest,
    CommentUpdateRequest,
)

from app.comments.service import CommentService


router = APIRouter(
    prefix="/posts/{post_id}/comments",
    tags=["댓글"],
)

DbSession = Annotated[Session, Depends(get_db)]


@router.post(
    "",
    response_model=ApiResponse[CommentCreateData],
    status_code=status.HTTP_201_CREATED,
    summary="댓글 작성",
)
def create_comment(
    request: CommentCreateRequest,
    db: DbSession,
    post_id: int = Path(gt=0, description="게시글 ID"),
) -> ApiResponse[CommentCreateData]:
    data = CommentService(db).create_comment(post_id=post_id, request=request)

    return ApiResponse(
        success=True,
        message="댓글이 등록되었습니다.",
        data=data,
    )


@router.get(
    "",
    response_model=ApiResponse[CommentPageData],
    summary="댓글 목록 조회",
)
def list_comments(
    db: DbSession,
    post_id: int = Path(gt=0, description="게시글 ID"),
    page: int = Query(default=1, ge=1, description="페이지 번호"),
    size: int = Query(default=20, ge=1, le=100, description="페이지 크기"),
) -> ApiResponse[CommentPageData]:
    rows, total = CommentService(db).list_comments(post_id=post_id, page=page, size=size)

    items = [
        CommentListItem(
            comment_id=c.id,
            content=c.content,
            author_name=c.author_name,
            created_at=c.created_at,
        )
        for c in rows
    ]

    total_pages = math.ceil(total / size) if total > 0 else 0

    return ApiResponse(
        success=True,
        message="댓글 목록을 조회했습니다.",
        data=CommentPageData(
            items=items,
            page=page,
            size=size,
            total_elements=total,
            total_pages=total_pages,
        ),
    )


@router.delete(
    "/{comment_id}",
    response_model=ApiResponse[None],
    summary="댓글 삭제",
)
def delete_comment(
    db: DbSession,
    post_id: int = Path(gt=0, description="게시글 ID"),
    comment_id: int = Path(gt=0, description="댓글 ID"),
    request: CommentDeleteRequest = Body(...),
) -> ApiResponse[None]:
    CommentService(db).delete_comment(comment_id=comment_id, edit_password=request.edit_password)

    return ApiResponse(
        success=True,
        message="댓글이 삭제되었습니다.",
        data=None,
    )


@router.put(
    "/{comment_id}",
    response_model=ApiResponse[None],
    summary="댓글 수정",
)
def update_comment(
    request: CommentUpdateRequest,
    db: DbSession,
    post_id: int = Path(gt=0, description="게시글 ID"),
    comment_id: int = Path(gt=0, description="댓글 ID"),
) -> ApiResponse[None]:
    CommentService(db).update_comment(comment_id=comment_id, request=request)
    return ApiResponse(success=True, message="댓글이 수정되었습니다.", data=None)
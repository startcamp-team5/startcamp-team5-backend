from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.posts.schema import (
    ApiResponse,
    PostCreateData,
    PostCreateRequest,
    PostDeleteRequest,
    PostDetailData,
    PostPageData,
    PostUpdateRequest,
)
from app.posts.service import PostService


router = APIRouter(
    prefix="/posts",
    tags=["커뮤니티 게시글"],
)

DbSession = Annotated[Session, Depends(get_db)]


@router.get(
    "",
    response_model=ApiResponse[PostPageData],
    summary="게시글 목록 조회",
)
def get_posts(
    db: DbSession,
    category: str | None = Query(
        default=None,
        description="게시판 종류",
        examples=["REVIEW"],
    ),
    keyword: str | None = Query(
        default=None,
        description="제목 또는 내용 검색어",
    ),
    page: int = Query(
        default=1,
        ge=1,
        description="페이지 번호",
    ),
    size: int = Query(
        default=10,
        ge=1,
        le=100,
        description="페이지 크기",
    ),
) -> ApiResponse[PostPageData]:
    data = PostService(db).get_posts(
        category=category,
        keyword=keyword,
        page=page,
        size=size,
    )

    return ApiResponse(
        success=True,
        message="게시글 목록을 조회했습니다.",
        data=data,
    )


@router.get(
    "/{post_id}",
    response_model=ApiResponse[PostDetailData],
    summary="게시글 상세 조회",
)
def get_post(
    db: DbSession,
    post_id: int = Path(
        gt=0,
        description="게시글 ID",
    ),
) -> ApiResponse[PostDetailData]:
    data = PostService(db).get_post(post_id)

    return ApiResponse(
        success=True,
        message="게시글을 조회했습니다.",
        data=data,
    )


@router.post(
    "",
    response_model=ApiResponse[PostCreateData],
    status_code=status.HTTP_201_CREATED,
    summary="게시글 작성",
)
def create_post(
    request: PostCreateRequest,
    db: DbSession,
) -> ApiResponse[PostCreateData]:
    data = PostService(db).create_post(request)

    return ApiResponse(
        success=True,
        message="게시글이 등록되었습니다.",
        data=data,
    )


@router.put(
    "/{post_id}",
    response_model=ApiResponse[None],
    summary="게시글 수정",
)
def update_post(
    request: PostUpdateRequest,
    db: DbSession,
    post_id: int = Path(
        gt=0,
        description="게시글 ID",
    ),
) -> ApiResponse[None]:
    PostService(db).update_post(
        post_id=post_id,
        request=request,
    )

    return ApiResponse(
        success=True,
        message="게시글이 수정되었습니다.",
        data=None,
    )


@router.delete(
    "/{post_id}",
    response_model=ApiResponse[None],
    summary="게시글 삭제",
)
def delete_post(
    db: DbSession,
    post_id: int = Path(
        gt=0,
        description="게시글 ID",
    ),
    request: PostDeleteRequest = Body(...),
) -> ApiResponse[None]:
    PostService(db).delete_post(
        post_id=post_id,
        request=request,
    )

    return ApiResponse(
        success=True,
        message="게시글이 삭제되었습니다.",
        data=None,
    )
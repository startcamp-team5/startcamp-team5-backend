from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str | None = None
    data: T | None = None


class PostCreateRequest(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    local_content_id: int | None = Field(
        default=None,
        alias="localContentId",
        gt=0,
    )
    board_category_code: str = Field(
        alias="boardCategoryCode",
        min_length=1,
        max_length=30,
    )
    title: str = Field(
        min_length=1,
        max_length=100,
    )
    content: str = Field(
        min_length=1,
        max_length=5000,
    )
    author_name: str = Field(
        default="익명",
        alias="authorName",
        min_length=1,
        max_length=30,
    )
    edit_password: str = Field(
        alias="editPassword",
        min_length=4,
        max_length=20,
    )


class PostUpdateRequest(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    title: str = Field(
        min_length=1,
        max_length=100,
    )
    content: str = Field(
        min_length=1,
        max_length=5000,
    )
    edit_password: str = Field(
        alias="editPassword",
        min_length=4,
        max_length=20,
    )


class PostDeleteRequest(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    edit_password: str = Field(
        alias="editPassword",
        min_length=4,
        max_length=20,
    )


class PostCreateData(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
    )

    post_id: int = Field(alias="postId")


class PostListItem(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
    )

    post_id: int = Field(alias="postId")
    local_content_id: int | None = Field(
        default=None,
        alias="localContentId",
    )
    category: str
    title: str
    author_name: str = Field(alias="authorName")
    view_count: int = Field(alias="viewCount")
    created_at: datetime = Field(alias="createdAt")


class PostDetailData(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
    )

    post_id: int = Field(alias="postId")
    local_content_id: int | None = Field(
        default=None,
        alias="localContentId",
    )
    category: str
    title: str
    content: str
    author_name: str = Field(alias="authorName")
    view_count: int = Field(alias="viewCount")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class PostPageData(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
    )

    items: list[PostListItem]
    page: int
    size: int
    total_elements: int = Field(alias="totalElements")
    total_pages: int = Field(alias="totalPages")
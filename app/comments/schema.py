from datetime import datetime
from colorama import init
from pydantic import BaseModel, ConfigDict, Field, config

from app.posts.schema import ApiResponse

class CommentCreateRequest(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    content: str = Field(
        min_length=1,
        max_length=1000,
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
        max_length=16,
    )

class CommentUpdateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)
    content: str = Field(min_length=1, max_length=1000)
    edit_password: str = Field(alias="editPassword", min_length=4, max_length=16)

class CommentDeleteRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    edit_password: str = Field(alias="editPassword", min_length=4, max_length=16)

class CommentListItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True, serialize_by_alias=True)
    comment_id: int = Field(alias="commentId")
    content: str
    author_name: str = Field(alias="authorName")
    created_at: datetime = Field(alias="createdAt")

class CommentPageData(BaseModel):
    model_config = ConfigDict(populate_by_name=True, serialize_by_alias=True)
    items: list[CommentListItem]
    page: int
    size: int
    total_elements: int = Field(alias="totalElements")
    total_pages: int = Field(alias="totalPages")

class CommentCreateData(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
    )

    comment_id: int = Field(alias="commentId")
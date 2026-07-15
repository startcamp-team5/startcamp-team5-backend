from datetime import datetime

from pydantic import BaseModel, Field, constr


class PostCreate(BaseModel):
    locationId: int = Field(..., description="게시글과 연결된 지역 정보 ID")
    category: constr(min_length=1, max_length=50) = Field(..., description="게시판 종류")
    title: constr(min_length=5, max_length=100) = Field(..., description="게시글 제목")
    content: constr(min_length=10, max_length=5000) = Field(..., description="게시글 내용")
    authorName: constr(strip_whitespace=True, max_length=20) | None = Field(
        default=None,
        description="작성자 이름. 입력하지 않으면 익명으로 저장됩니다.",
    )
    editPassword: constr(min_length=4, max_length=20) = Field(..., description="수정/삭제용 비밀번호")


class PostUpdate(BaseModel):
    title: constr(min_length=5, max_length=100) | None = Field(
        default=None,
        description="수정할 제목",
    )
    content: constr(min_length=10, max_length=5000) | None = Field(
        default=None,
        description="수정할 내용",
    )
    editPassword: constr(min_length=4, max_length=20) = Field(..., description="게시글 수정용 비밀번호")


class PostDelete(BaseModel):
    editPassword: constr(min_length=4, max_length=20) = Field(..., description="게시글 삭제용 비밀번호")


class PostResponse(BaseModel):
    postId: int
    locationId: int | None
    category: str
    title: str
    content: str
    authorName: str
    viewCount: int
    createdAt: datetime
    updatedAt: datetime

    model_config = {
        "from_attributes": True,
    }

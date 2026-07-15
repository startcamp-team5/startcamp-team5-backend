import hashlib
import secrets
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.posts.model import BoardCategory, Post
from app.posts.schemas import PostCreate, PostDelete, PostUpdate

router = APIRouter(prefix="/posts", tags=["posts"])


def success_response(message: str, data: object | None = None) -> dict:
    return {
        "success": True,
        "message": message,
        "data": data if data is not None else {},
    }


def get_post_dict(post: Post) -> dict:
    return {
        "postId": post.id,
        "locationId": post.local_content_id,
        "category": post.board_category.name if post.board_category is not None else "",
        "title": post.title,
        "content": post.content,
        "authorName": post.author_name,
        "viewCount": post.view_count,
        "createdAt": post.created_at,
        "updatedAt": post.updated_at,
    }


def hash_password(password: str, salt: str | None = None) -> str:
    if salt is None:
        salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        120_000,
    )
    return f"{salt}${digest.hex()}"


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        salt, expected = hashed_password.split("$", 1)
    except ValueError:
        return False
    return secrets.compare_digest(hash_password(password, salt), hashed_password)


def get_or_create_category(db: Session, category: str) -> BoardCategory:
    category_name = category.strip()
    category_code = category_name.lower()
    category_record = (
        db.query(BoardCategory)
        .filter(BoardCategory.code == category_code)
        .one_or_none()
    )
    if category_record is not None:
        return category_record

    category_record = BoardCategory(
        code=category_code,
        name=category_name,
        description=f"{category_name} 게시글 카테고리",
    )
    db.add(category_record)
    db.commit()
    db.refresh(category_record)
    return category_record


def get_post_or_404(db: Session, post_id: int) -> Post:
    post = (
        db.query(Post)
        .filter(Post.id == post_id)
        .filter(Post.is_deleted == 0)
        .one_or_none()
    )
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다.",
        )
    return post


@router.get("")
def list_posts(
    category: str | None = None,
    keyword: str | None = None,
    page: int = 1,
    db: Session = Depends(get_db),
) -> dict:
    page = max(page, 1)
    query = db.query(Post).filter(Post.is_deleted == 0)

    if category:
        query = query.join(BoardCategory).filter(BoardCategory.code == category.strip().lower())

    if keyword:
        keyword_text = f"%{keyword.strip()}%"
        query = query.filter(
            or_(
                Post.title.ilike(keyword_text),
                Post.content.ilike(keyword_text),
            )
        )

    posts = (
        query.order_by(Post.created_at.desc())
        .offset((page - 1) * 10)
        .limit(10)
        .all()
    )

    return success_response(
        message="게시글 목록을 조회했습니다.",
        data=[get_post_dict(post) for post in posts],
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_post(
    post_in: PostCreate,
    db: Session = Depends(get_db),
) -> dict:
    board_category = get_or_create_category(db, post_in.category)
    post = Post(
        board_category_id=board_category.id,
        local_content_id=post_in.locationId,
        title=post_in.title.strip(),
        content=post_in.content.strip(),
        edit_password_hash=hash_password(post_in.editPassword),
        author_name=post_in.authorName.strip() if post_in.authorName else "익명",
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return success_response(
        message="게시글이 등록되었습니다.",
        data={"postId": post.id},
    )


@router.get("/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)) -> dict:
    post = get_post_or_404(db, post_id)
    post.view_count += 1
    db.commit()
    db.refresh(post)
    return success_response(
        message="게시글 상세 조회에 성공했습니다.",
        data=get_post_dict(post),
    )


@router.put("/{post_id}")
def update_post(
    post_id: int,
    post_in: PostUpdate,
    db: Session = Depends(get_db),
) -> dict:
    post = get_post_or_404(db, post_id)
    if not verify_password(post_in.editPassword, post.edit_password_hash):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="비밀번호가 일치하지 않습니다.",
        )

    updated = False
    if post_in.title is not None:
        post.title = post_in.title.strip()
        updated = True
    if post_in.content is not None:
        post.content = post_in.content.strip()
        updated = True
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="수정할 내용이 없습니다.",
        )

    post.updated_at = datetime.now()
    db.commit()
    return success_response(message="게시글이 수정되었습니다.")


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    delete_in: PostDelete,
    db: Session = Depends(get_db),
) -> dict:
    post = get_post_or_404(db, post_id)
    if not verify_password(delete_in.editPassword, post.edit_password_hash):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="비밀번호가 일치하지 않습니다.",
        )

    post.is_deleted = 1
    post.deleted_at = datetime.now()
    db.commit()
    return success_response(message="게시글이 삭제되었습니다.")

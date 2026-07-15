from sqlalchemy import select

from app.core.config import settings
from app.core.database import Base, SessionLocal, engine
from app.data.seed_data import seed_database
from app.locations.model import (
    ContentCategory,
    DataSource,
    LocalContent,
    Region,
)
from app.posts.model import BoardCategory, Post
from app.comments.model import Comment


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def initialize_database() -> None:
    print(f"[DB] 초기화 시작: {settings.database_url}")
    create_tables()

    with SessionLocal() as db:
        has_any_content = db.scalar(
            select(LocalContent.id).limit(1)
        )

        if has_any_content is not None:
            print("[DB] 기존 데이터가 있어 시드를 건너뜁니다.")
            return

        print("[DB] 빈 데이터베이스이므로 JSON 시드를 적재합니다.")

        try:
            seed_database()
        except FileNotFoundError as exc:
            print(f"[DB] 시드 파일을 찾을 수 없어 초기화만 진행합니다: {exc}")
        except Exception as exc:
            print(f"[DB] 시드 적재 중 오류가 발생했습니다: {exc}")
            raise

    print("[DB] 초기화 완료")

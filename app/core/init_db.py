from sqlalchemy import select

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
    create_tables()

    with SessionLocal() as db:
        has_any_content = db.scalar(
            select(LocalContent.id).limit(1)
        )

        if has_any_content is not None:
            return

        seed_database()

from app.core.database import Base, engine

# SQLAlchemy가 모든 테이블 모델을 인식하도록 반드시 import
from app.locations.model import (
    ContentCategory,
    DataSource,
    LocalContent,
    Region,
)
from app.posts.model import BoardCategory, Post


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
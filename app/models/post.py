from datetime import datetime

from sqlalchemy import DateTime, Identity, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class BlogPost(Base):
    __tablename__ = "blog_posts"

    id: Mapped[int] = mapped_column(
        "blog_post_id", Identity(), primary_key=True, index=True
    )
    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text)
    published_on: Mapped[datetime] = mapped_column(
        DateTime(), server_default=func.now()
    )

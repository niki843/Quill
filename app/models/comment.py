from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Identity, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class BlogComment(Base):
    __tablename__ = "blog_comment"

    id: Mapped[int] = mapped_column(
        "comment_id", Identity(), primary_key=True, index=True
    )
    blog_post_id: Mapped[int] = mapped_column(
        ForeignKey("blog_posts.blog_post_id"), index=True
    )
    comment: Mapped[str] = mapped_column(Text)
    commented_on: Mapped[datetime] = mapped_column(
        DateTime(), server_default=func.now()
    )

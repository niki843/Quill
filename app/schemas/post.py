from datetime import datetime

from pydantic import BaseModel, ConfigDict

class BlogPostBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class BlogPostRead(BlogPostBase):
    id: int
    title: str
    body: str
    published_on: datetime


class BlogPostTitleRead(BlogPostBase):
    id: int
    title: str
    comment_count: int

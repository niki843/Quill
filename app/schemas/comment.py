from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BlogCommentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int 
    blog_post_id: int
    comment: str
    commented_on: datetime

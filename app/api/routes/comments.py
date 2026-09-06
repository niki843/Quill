from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.comment import BlogComment
from app.schemas.comment import BlogCommentRead

router = APIRouter(prefix="/comments", tags=["comments"])

@router.get("/", response_model=List[BlogCommentRead])
async def list_comments(db: Session = Depends(get_db)): 
    return await db.scalars(select(BlogComment).order_by(BlogComment.id))

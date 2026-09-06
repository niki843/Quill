from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cache import cached
from app.db.session import get_db
from app.models.comment import BlogComment
from app.schemas.comment import BlogCommentRead

router = APIRouter(prefix="/comments", tags=["comments"])

@router.get("/", response_model=List[BlogCommentRead])
async def list_comments(offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit is capped to 100 for performance")

    result = await db.scalars(select(BlogComment).order_by(BlogComment.commented_on).offset(offset).limit(limit))
    return result.all()

@router.get("/{post_id}", response_model=List[BlogCommentRead])
@cached(ttl=15)
async def get_comments_per_post(post_id: int, offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit is capped to 100 for performance")

    result = await db.scalars(
        select(BlogComment)
        .where(BlogComment.blog_post_id == post_id)
        .order_by(BlogComment.commented_on)
        .offset(offset)
        .limit(limit)
    )
    return result.all()

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cache import cached
from app.db.session import get_db
from app.models.comment import BlogComment
from app.models.post import BlogPost
from app.schemas.post import BlogPostRead, BlogPostTitleRead

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/", response_model=List[BlogPostRead])
@cached(ttl=30)
async def list_posts(offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit is capped to 100 for performance")

    result = await db.scalars(
        select(BlogPost).order_by(BlogPost.published_on).offset(offset).limit(limit)
    )
    return result.all()

@router.get("/titles", response_model=List[BlogPostTitleRead])
@cached(ttl=30)
async def list_post_titles(offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit is capped to 100 for performance")

    comment_count = (
        select(func.count(BlogComment.id))
        .where(BlogComment.blog_post_id == BlogPost.id)
        .correlate(BlogPost)
        .scalar_subquery()
    )
    result = await db.execute(
        select(BlogPost.id, BlogPost.title, comment_count.label("comment_count"))
        .order_by(BlogPost.published_on)
        .offset(offset)
        .limit(limit)
    )
    return result.all()

@router.get("/{post_id}", response_model=List[BlogPostRead])
async def get_post_by_id(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.scalars(select(BlogPost).where(BlogPost.id == post_id))
    return result.all()

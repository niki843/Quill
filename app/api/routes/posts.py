from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cache import cached
from app.db.session import get_db
from app.models.comment import BlogComment
from app.models.post import BlogPost
from app.schemas.post import BlogPostCommentCount, BlogPostRead, BlogPostTitleRead
from app.schemas.comment import BlogCommentRead

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

@router.get("/details", response_model=List[BlogPostRead])
async def list_posts(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.scalars(select(BlogPost).where(BlogPost.id == post_id))
    return result.all()

@router.get("/titles", response_model=List[BlogPostTitleRead])
@cached(ttl=60)
async def list_post_titles(offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit is capped to 100 for performance")

    result = await db.execute(
        select(BlogPost.id, BlogPost.title).order_by(BlogPost.published_on).offset(offset).limit(limit)
    )
    return result.all()

@router.get("/{post_id}/comment-count", response_model=BlogPostCommentCount)
@cached(ttl=30)
async def get_comments_per_post_count(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(func.count(BlogComment.id)).where(BlogComment.blog_post_id == post_id)
    )
    return {"post_id": post_id, "comment_count": result.scalar_one()}

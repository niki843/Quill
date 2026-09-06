from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.post import BlogPost
from app.schemas.post import BlogPostRead, BlogPostTitleRead

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/", response_model=List[BlogPostRead])
async def list_posts(db: AsyncSession = Depends(get_db)):
    return await db.scalars(select(BlogPost).order_by(BlogPost.id))

@router.get("/titles", response_model=List[BlogPostTitleRead])
async def list_post_titles(db: AsyncSession = Depends(get_db)):
    return await db.execute(select(BlogPost.id, BlogPost.title).order_by(BlogPost.id))

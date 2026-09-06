from datetime import datetime

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.comment import BlogComment
from app.models.post import BlogPost


@pytest.fixture
async def db_engine():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest.fixture
def session_factory(db_engine):
    return async_sessionmaker(bind=db_engine, expire_on_commit=False)


@pytest.fixture
async def db_session(session_factory):
    async with session_factory() as session:
        yield session


@pytest.fixture
async def client(session_factory):
    async def override_get_db():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def seed_posts(db_session):
    posts = [
        BlogPost(title="First post", body="Body one", published_on=datetime(2024, 1, 1)),
        BlogPost(title="Second post", body="Body two", published_on=datetime(2024, 1, 2)),
        BlogPost(title="Third post", body="Body three", published_on=datetime(2024, 1, 3)),
    ]
    db_session.add_all(posts)
    await db_session.commit()
    for post in posts:
        await db_session.refresh(post)
    return posts


@pytest.fixture
async def seed_comments(db_session, seed_posts):
    first_post = seed_posts[0]
    comments = [
        BlogComment(blog_post_id=first_post.id, comment="Nice post!", commented_on=datetime(2024, 1, 1, 10)),
        BlogComment(blog_post_id=first_post.id, comment="Thanks for sharing", commented_on=datetime(2024, 1, 1, 11)),
    ]
    db_session.add_all(comments)
    await db_session.commit()
    for comment in comments:
        await db_session.refresh(comment)
    return comments

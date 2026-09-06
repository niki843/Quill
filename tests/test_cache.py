from datetime import datetime

from app.models.comment import BlogComment


async def test_comment_count_is_served_from_cache_after_first_request(client, db_session, seed_posts):
    post = seed_posts[0]

    first = await client.get(f"/api/v1/posts/{post.id}/comment-count")
    assert first.json()["comment_count"] == 0

    db_session.add(BlogComment(blog_post_id=post.id, comment="late arrival", commented_on=datetime(2024, 1, 1)))
    await db_session.commit()

    second = await client.get(f"/api/v1/posts/{post.id}/comment-count")
    assert second.json()["comment_count"] == 0, "expected the cached value, not the freshly committed comment"


async def test_comment_count_cache_is_keyed_per_post_id(client, seed_posts):
    post_a, post_b = seed_posts[0], seed_posts[1]

    response_a = await client.get(f"/api/v1/posts/{post_a.id}/comment-count")
    response_b = await client.get(f"/api/v1/posts/{post_b.id}/comment-count")

    assert response_a.json()["post_id"] == post_a.id
    assert response_b.json()["post_id"] == post_b.id


async def test_list_posts_cache_is_keyed_per_offset_and_limit(client, seed_posts):
    all_posts = await client.get("/api/v1/posts/")
    first_page = await client.get("/api/v1/posts/", params={"offset": 0, "limit": 1})

    assert len(all_posts.json()) == 3
    assert len(first_page.json()) == 1

from datetime import datetime

from app.models.comment import BlogComment


async def test_list_posts_cache_is_keyed_per_offset_and_limit(client, seed_posts):
    all_posts = await client.get("/api/v1/posts/")
    first_page = await client.get("/api/v1/posts/", params={"offset": 0, "limit": 1})

    assert len(all_posts.json()) == 3
    assert len(first_page.json()) == 1


async def test_list_post_titles_comment_count_is_served_from_cache_after_first_request(client, db_session, seed_posts):
    post = seed_posts[0]

    first = await client.get("/api/v1/posts/titles")
    by_id = {row["id"]: row["comment_count"] for row in first.json()}
    assert by_id[post.id] == 0

    db_session.add(BlogComment(blog_post_id=post.id, comment="late arrival", commented_on=datetime(2024, 1, 1)))
    await db_session.commit()

    second = await client.get("/api/v1/posts/titles")
    by_id = {row["id"]: row["comment_count"] for row in second.json()}
    assert by_id[post.id] == 0, "expected the cached value, not the freshly committed comment"

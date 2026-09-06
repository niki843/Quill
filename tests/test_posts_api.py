import pytest


async def test_list_posts_returns_all_seeded_posts(client, seed_posts):
    response = await client.get("/api/v1/posts/")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 3
    assert [post["title"] for post in body] == ["First post", "Second post", "Third post"]


async def test_list_posts_respects_offset_and_limit(client, seed_posts):
    response = await client.get("/api/v1/posts/", params={"offset": 1, "limit": 1})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "Second post"


async def test_list_posts_empty_when_no_data(client):
    response = await client.get("/api/v1/posts/")

    assert response.status_code == 200
    assert response.json() == []


async def test_list_posts_rejects_limit_over_100(client, seed_posts):
    response = await client.get("/api/v1/posts/", params={"limit": 101})

    assert response.status_code == 400
    assert "capped" in response.json()["detail"]


async def test_list_post_titles_returns_id_and_title_only(client, seed_posts):
    response = await client.get("/api/v1/posts/titles")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 3
    assert set(body[0].keys()) == {"id", "title"}


async def test_list_post_titles_rejects_limit_over_100(client, seed_posts):
    response = await client.get("/api/v1/posts/titles", params={"limit": 101})

    assert response.status_code == 400


async def test_get_post_details_by_id(client, seed_posts):
    target = seed_posts[1]

    response = await client.get("/api/v1/posts/details", params={"post_id": target.id})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == target.id
    assert body[0]["title"] == "Second post"


async def test_get_post_details_unknown_id_returns_empty_list(client, seed_posts):
    response = await client.get("/api/v1/posts/details", params={"post_id": 999999})

    assert response.status_code == 200
    assert response.json() == []


async def test_get_post_details_requires_post_id(client):
    response = await client.get("/api/v1/posts/details")

    assert response.status_code == 422


async def test_comment_count_reflects_number_of_comments(client, seed_comments, seed_posts):
    post_with_comments = seed_posts[0]

    response = await client.get(f"/api/v1/posts/{post_with_comments.id}/comment-count")

    assert response.status_code == 200
    assert response.json() == {"post_id": post_with_comments.id, "comment_count": 2}


async def test_comment_count_is_zero_for_post_without_comments(client, seed_posts):
    post_without_comments = seed_posts[2]

    response = await client.get(f"/api/v1/posts/{post_without_comments.id}/comment-count")

    assert response.status_code == 200
    assert response.json() == {"post_id": post_without_comments.id, "comment_count": 0}


async def test_comment_count_for_nonexistent_post_is_zero_not_404(client):
    response = await client.get("/api/v1/posts/999999/comment-count")

    assert response.status_code == 200
    assert response.json()["comment_count"] == 0

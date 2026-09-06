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


async def test_list_post_titles_returns_id_title_and_comment_count(client, seed_posts):
    response = await client.get("/api/v1/posts/titles")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 3
    assert set(body[0].keys()) == {"id", "title", "comment_count"}


async def test_list_post_titles_includes_comment_count_per_post(client, seed_comments, seed_posts):
    post_with_comments = seed_posts[0]
    post_without_comments = seed_posts[2]

    response = await client.get("/api/v1/posts/titles")

    assert response.status_code == 200
    by_id = {post["id"]: post["comment_count"] for post in response.json()}
    assert by_id[post_with_comments.id] == 2
    assert by_id[post_without_comments.id] == 0


async def test_list_post_titles_rejects_limit_over_100(client, seed_posts):
    response = await client.get("/api/v1/posts/titles", params={"limit": 101})

    assert response.status_code == 400


async def test_get_post_by_id(client, seed_posts):
    target = seed_posts[1]

    response = await client.get(f"/api/v1/posts/{target.id}")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == target.id
    assert body[0]["title"] == "Second post"


async def test_get_post_by_id_unknown_id_returns_empty_list(client, seed_posts):
    response = await client.get("/api/v1/posts/999999")

    assert response.status_code == 200
    assert response.json() == []


async def test_get_post_by_id_invalid_id_type_is_422(client):
    response = await client.get("/api/v1/posts/not-a-number")

    assert response.status_code == 422

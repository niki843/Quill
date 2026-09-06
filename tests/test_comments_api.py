async def test_list_comments_returns_all_seeded_comments(client, seed_comments):
    response = await client.get("/api/v1/comments/")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert [c["comment"] for c in body] == ["Nice post!", "Thanks for sharing"]


async def test_list_comments_respects_offset_and_limit(client, seed_comments):
    response = await client.get("/api/v1/comments/", params={"offset": 1, "limit": 1})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["comment"] == "Thanks for sharing"


async def test_list_comments_rejects_limit_over_100(client, seed_comments):
    response = await client.get("/api/v1/comments/", params={"limit": 101})

    assert response.status_code == 400
    assert "capped" in response.json()["detail"]


async def test_get_comments_per_post_filters_by_post_id(client, seed_comments, seed_posts):
    post_with_comments = seed_posts[0]
    other_post = seed_posts[1]

    response = await client.get(f"/api/v1/comments/{post_with_comments.id}")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert all(c["blog_post_id"] == post_with_comments.id for c in body)

    other_response = await client.get(f"/api/v1/comments/{other_post.id}")
    assert other_response.status_code == 200
    assert other_response.json() == []


async def test_get_comments_per_post_respects_pagination(client, seed_comments, seed_posts):
    post_with_comments = seed_posts[0]

    response = await client.get(
        f"/api/v1/comments/{post_with_comments.id}", params={"offset": 1, "limit": 1}
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["comment"] == "Thanks for sharing"


async def test_get_comments_per_post_rejects_limit_over_100(client, seed_comments, seed_posts):
    post_with_comments = seed_posts[0]

    response = await client.get(
        f"/api/v1/comments/{post_with_comments.id}", params={"limit": 101}
    )

    assert response.status_code == 400


async def test_get_comments_per_post_invalid_id_type_is_422(client):
    response = await client.get("/api/v1/comments/not-a-number")

    assert response.status_code == 422

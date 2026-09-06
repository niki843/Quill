from datetime import datetime
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from app.schemas.comment import BlogCommentRead
from app.schemas.post import BlogPostRead, BlogPostTitleRead


class FakeOrmPost:
    """Stand-in for a BlogPost ORM instance, used to test from_attributes without a DB."""

    def __init__(self, id, title, body, published_on):
        self.id = id
        self.title = title
        self.body = body
        self.published_on = published_on


class FakeOrmComment:
    def __init__(self, id, blog_post_id, comment, commented_on):
        self.id = id
        self.blog_post_id = blog_post_id
        self.comment = comment
        self.commented_on = commented_on


def test_blog_post_read_from_orm_attributes():
    orm_post = FakeOrmPost(1, "Title", "Body", datetime(2024, 1, 1))

    schema = BlogPostRead.model_validate(orm_post)

    assert schema.id == 1
    assert schema.title == "Title"
    assert schema.body == "Body"
    assert schema.published_on == datetime(2024, 1, 1)


def test_blog_post_read_missing_field_raises():
    with pytest.raises(ValidationError):
        BlogPostRead(id=1, title="Title")


def test_blog_post_title_read_from_row_like_object():
    # BlogPostTitleRead is populated from a query result row (id, title, comment_count),
    # not directly from a BlogPost ORM instance -- it has no body/published_on.
    row = SimpleNamespace(id=1, title="Title", comment_count=3)

    schema = BlogPostTitleRead.model_validate(row)

    assert schema.id == 1
    assert schema.title == "Title"
    assert schema.comment_count == 3


def test_blog_comment_read_from_orm_attributes():
    orm_comment = FakeOrmComment(1, 2, "Nice post!", datetime(2024, 1, 1, 10))

    schema = BlogCommentRead.model_validate(orm_comment)

    assert schema.id == 1
    assert schema.blog_post_id == 2
    assert schema.comment == "Nice post!"
    assert schema.commented_on == datetime(2024, 1, 1, 10)

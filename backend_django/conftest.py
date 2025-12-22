import pytest
from django.contrib.auth import get_user_model
from  blog.models import Post, Comment
from datetime import datetime

User = get_user_model()  

@pytest.fixture
def test_user(db):
    """Create a test user for account/blog tests"""
    return User.objects.create_user(username="testuser", password="testpass123")

@pytest.fixture
def logged_in_client(client, test_user):
    client.login(username="testuser", password="testpass123")
    return client

@pytest.fixture
def test_post(db, test_user):
    """Create a test post"""
    return Post.objects.create(
        title="Test Post",
        content="This is a test post",
        author=test_user,
        published=True
    )


@pytest.fixture
def test_comment(test_user, test_post, db):
    """Create a sample comment"""
    return Comment.objects.create(
        content="Test Comment",
        author=test_user,
        post=test_post
    )
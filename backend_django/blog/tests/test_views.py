import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from blog.models import Post, Comment


# ----------- POST VIEWS -----------

def test_allPosts_view(client, test_post):
    url = reverse("posts")
    response = client.get(url)
    assert response.status_code == 200
    assert "posts" in response.context
    assert test_post in response.context["posts"]

def test_postByID_view(client, test_post, test_user):
    url = reverse("postDetail", args=[test_post.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["post_detail"] == test_post

def test_get_user_posts_view(logged_in_client, test_post):
    url = reverse("userPosts")
    response = logged_in_client.get(url)
    assert response.status_code == 200
    assert test_post in response.context["posts"]

def test_create_post_view_get(logged_in_client):
    url = reverse("createPost")
    response = logged_in_client.get(url)
    assert response.status_code == 200

def test_create_post_view_post(logged_in_client):
    url = reverse("createPost")
    data = {"title": "New Post", "content": "New content"}
    response = logged_in_client.post(url, data)
    # Should redirect after success
    assert response.status_code == 302
    assert Post.objects.filter(title="New Post").exists()

def test_update_post_view(logged_in_client, test_post):
    url = reverse("editPost", args=[test_post.id])
    data = {"title": "Updated Title"}
    response = logged_in_client.post(url, data)
    test_post.refresh_from_db()
    assert response.status_code == 302
    assert test_post.title == "Updated Title"

def test_delete_post_view(logged_in_client, test_post):
    url = reverse("deletePost", args=[test_post.id])
    response = logged_in_client.post(url)
    assert response.status_code == 302
    assert not Post.objects.filter(id=test_post.id).exists()

# ----------- COMMENT VIEWS -----------

def test_get_user_comments_view(logged_in_client, test_comment):
    url = reverse("comments")
    response = logged_in_client.get(url)
    assert response.status_code == 200
    assert test_comment in response.context["comments"]

def test_create_comment_view(logged_in_client, test_post):
    url = reverse("createComment", args=[test_post.id])
    data = {"content": "Another comment"}
    response = logged_in_client.post(url, data)
    assert response.status_code == 302
    assert Comment.objects.filter(content="Another comment").exists()

def test_update_comment_view(logged_in_client, test_comment):
    url = reverse("editComment", args=[test_comment.id])
    data = {"content": "Updated comment"}
    response = logged_in_client.post(url, data)
    test_comment.refresh_from_db()
    assert response.status_code == 302
    assert test_comment.content == "Updated comment"

def test_delete_comment_view(logged_in_client, test_comment):
    url = reverse("deleteComment", args=[test_comment.id])
    response = logged_in_client.post(url)
    assert response.status_code == 302
    assert not Comment.objects.filter(id=test_comment.id).exists()

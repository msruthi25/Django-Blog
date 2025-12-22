from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from asgiref.sync import sync_to_async
from django.template.response import TemplateResponse
from backend_django.blog.models import Post, Comment
from backend_django.blog.serializers import PostSerializer, CommentSerializer

# ---------------- POSTS ----------------

@sync_to_async
def get_all_posts_query():
    return list(Post.objects.all())

@sync_to_async
def get_post(id):
    return get_object_or_404(Post, id=id)

@sync_to_async
def get_user_posts_query(user):
    return list(Post.objects.filter(author=user))

@sync_to_async
def save_post(serializer, user):
    serializer.save(author=user, published=True)

@sync_to_async
def get_post_author_username(post):
    return post.author.username

# ---------------- COMMENTS ----------------

@sync_to_async
def get_user_comments_query(user):
    return list(Comment.objects.filter(author=user))

# ---------------- VIEWS ----------------

# Home / All Posts
async def allPosts(request):
    all_posts = await get_all_posts_query()
    return TemplateResponse(request, "home.html", {"posts": all_posts})

# Render form for creating post (GET)
async def createPostView(request):
    return TemplateResponse(request, "write_post.html")

# Post Detail
async def postByID(request, id):
    post = await get_post(id)
    comments = await sync_to_async(list)(Comment.objects.filter(post=post).order_by("-created_at"))
    author_name = await get_post_author_username(post)
    return TemplateResponse(
        request,
        "post_detail.html",
        {"post_detail": post, "author_name": author_name, "comments": comments},
    )

# User Posts
@login_required(login_url="login")
async def get_user_posts(request):
    user = await sync_to_async(lambda u: u)(request.user)
    posts = await get_user_posts_query(user)
    if not posts:
        messages.warning(request, "No posts found")
    return TemplateResponse(request, "userPost.html", {"posts": posts})

@login_required(login_url="login")
async def create_post(request):
    user = await sync_to_async(lambda u: u)(request.user)
    if request.method == "POST":
        serializer = PostSerializer(data=request.POST)
        is_valid = await sync_to_async(serializer.is_valid, thread_sensitive=True)()
        if is_valid:
            await save_post(serializer, user)
            messages.success(request, "Post created successfully")
            return redirect("userPosts")
        else:
            for field, errors in serializer.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return TemplateResponse(request, "write_post.html", {"data": request.POST})
    return TemplateResponse(request, "write_post.html")

@login_required(login_url="login")
def update_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author_id != request.user.id:
        messages.error(request, "You cannot edit this post")
        return redirect("userPosts")

    if request.method == "POST":
        serializer = PostSerializer(instance=post, data=request.POST, partial=True)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Post updated successfully")
            return redirect("userPosts")
        else:
            for field, errors in serializer.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return render(request, "edit_post.html", {"post": post, "data": request.POST})
    return render(request, "edit_post.html", {"post": post})

@login_required(login_url="login")
def delete_post(request, id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    post = get_object_or_404(Post, id=id)
    if post.author_id != request.user.id:
        messages.error(request, "You are not allowed to delete this post.")
        return redirect("userPosts")
    post.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect("userPosts")

# ---------------- COMMENTS ----------------

@login_required(login_url="login")
async def get_user_comments(request):
    user = await sync_to_async(lambda u: u)(request.user)
    comments = await get_user_comments_query(user)
    if not comments:
        messages.warning(request, "No comments found")
    return TemplateResponse(request, "userComments.html", {"comments": comments})


@login_required(login_url="login")
def create_comment(request, id):
    if request.method == "POST":
        serializer = CommentSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save(author_id=request.user.id, post_id=id)
            messages.success(request, "Comment created successfully")
            return redirect("comments")
        else:
            for field, errors in serializer.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect("comments")


async def view_comment(request, id):
    comment = await sync_to_async(get_object_or_404)(Comment, id=id)
    return TemplateResponse(request, "comment_detail.html", {"comment": comment})

@login_required(login_url="login")
def update_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    if comment.author_id != request.user.id:
        messages.error(request, "You cannot edit this comment")
        return redirect("comments")
    if request.method == "POST":
        serializer = CommentSerializer(instance=comment, data=request.POST, partial=True)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Comment updated successfully")
            return redirect("comments")
        else:
            for field, errors in serializer.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect("comments")
    return redirect("comments")

@login_required(login_url="login")
def delete_comment(request, id):  #Delete comments
    comment = get_object_or_404(Comment, id=id)
    if comment.author_id != request.user.id:
        messages.error(request, "You cannot delete this comment")
        return redirect("comments")
    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted successfully")
        return redirect("comments")    
    return redirect("comments") 
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from blog.models import Post, Comment
from blog.serializers import PostSerializer,CommentSerializer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

def allPosts(request):     #Display All posts    
        all_posts = Post.objects.all()                
        return render(request, "home.html", {"posts": all_posts})
     
def postByID(request, id):
        post = get_object_or_404(Post, id=id)
        comments = Comment.objects.filter(post=post).order_by("-created_at")

        return render(
            request,
            "post_detail.html",
            {
                "post_detail": post,
                "author_name": post.author.username,
                "comments": comments,
            }

        )
def createPostView(request):        
        return render(request, "write_post.html")

#User Posts
@login_required(login_url="login")
def get_user_posts(request):  #Get all posts of Logged In Users
    posts = Post.objects.filter(author=request.user)
    if not posts.exists():
        messages.warning(request, "No posts found")
    return render(request, "userPost.html", {"posts": posts})

@login_required(login_url="login")
def create_post(request):
    if request.method == "POST":
        serializer = PostSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save(author=request.user, published=True)
            messages.success(request, "Post created successfully")
            return redirect("userPosts")
        else:
            for field, errors in serializer.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return render(request, "write_post.html", {"data": request.POST})

    return render(request, "write_post.html")

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

        
# --- COMMENTS ---

@login_required(login_url="login")
def get_user_comments(request):  #Get Comments by userId
    comments = Comment.objects.filter(author_id=request.user.id)
    if not comments.exists():
        messages.warning(request, "No comments found")
    return render(request, "userComments.html", {"comments": comments})

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
        
def view_comment(request, id):     #View User Comments 
    comment = get_object_or_404(Comment, id=id)
    return render(request, "comment_detail.html", {"comment": comment})

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

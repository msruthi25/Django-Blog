from datetime import timezone
from django.http import QueryDict
from django.shortcuts import get_object_or_404, redirect, render
from blog.models import Post, Comment
from blog.serializers import PostSerializer,CommentSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied,AuthenticationFailed
from rest_framework import status
from account.auth_utils import get_user_from_request
from account.models import User
from django.contrib import messages
from django.http import JsonResponse

class AllPosts(APIView):  #Display All posts
    def get(self,request):        
        all_posts = Post.objects.all()
        if not all_posts.exists():
            raise NotFound("No posts Found")
        serialized = PostSerializer(all_posts, many=True)          
        return render(request, "home.html", {"posts": serialized.data}, status=status.HTTP_200_OK)
     
class PostByID(APIView):
    def get(self, request, id):
        post = Post.objects.filter(id=id).first()
        if not post:
            raise NotFound("Post Not Found")
        serialized_post = PostSerializer(post)
        comments = Comment.objects.filter(post_id=post.id).order_by('-created_at')        
        return render(
            request,
            "post_detail.html",
            {
                "post_detail": serialized_post.data,
                "author_name": post.author.username,
                "comments": comments
            },
            status=status.HTTP_200_OK
        )

class createPostView(APIView):
    def get(self,request):        
        return render(request, "write_post.html")

#User Posts
def get_user_posts(request):  #Get all posts of Logged In Users
    try:
       user_id = get_user_from_request(request)
    except AuthenticationFailed as e:
        return JsonResponse({"error": str(e)}, status=401)  
    posts = Post.objects.filter(author_id=user_id)
    if not posts.exists():
        messages.warning(request, "No posts found")
    return render(request, "userPost.html", {"posts": posts})

def create_post(request):        #Create Posts
    try:
       user_id = get_user_from_request(request)
    except AuthenticationFailed as e:
        return JsonResponse({"error": str(e)}, status=401)  
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        image_url = request.POST.get("image_url")
        Post.objects.create(title=title, content=content, author_id=user_id, image_url=image_url, published=True)
        messages.success(request, "Post created successfully")
        return redirect("userPosts")
    return render(request, "write_post.html")

def view_post(request, id):   #View posts by PostID
    post = get_object_or_404(Post, id=id)
    return render(request, "post_detail.html", {"post": post})

def update_post(request, id):  #Update Posts
    try:
       user_id = get_user_from_request(request)
    except AuthenticationFailed as e:
        return JsonResponse({"error": str(e)}, status=401)  
    post = get_object_or_404(Post, id=id)
    if post.author_id != user_id:
        messages.error(request, "You cannot edit this post")
        return redirect("userPosts")
    if request.method == "POST":
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.image_url = request.POST.get("image_url")
        post.save()
        messages.success(request, "Post updated successfully")
        return redirect("userPosts")    
    return render(request, "edit_post.html", {"post": post})

def delete_post(request, id):  #Delete posts
    try:
       user_id = get_user_from_request(request)
    except AuthenticationFailed as e:
        return JsonResponse({"error": str(e)}, status=401)  
    post = get_object_or_404(Post, id=id)
    if post.author_id != user_id:
        messages.error(request, "You cannot delete this post")
        return redirect("userPosts")
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully")
        return redirect("userPosts")    
    return render(request, {"post": post})
        
# --- COMMENTS ---

def get_user_comments(request):  #Get Comments by userId
    try:
       user_id = get_user_from_request(request)
    except AuthenticationFailed as e:
        return JsonResponse({"error": str(e)}, status=401)
    comments = Comment.objects.filter(author_id=user_id)
    if not comments.exists():
        messages.warning(request, "No comments found")
    return render(request, "userComments.html", {"comments": comments})

def create_comment(request,id):  #Create Comment
    try:
       user_id = get_user_from_request(request)
    except AuthenticationFailed as e:
        return JsonResponse({"error": str(e)}, status=401)  
    if request.method == "POST":
        content = request.POST.get("content")
        Comment.objects.create(author_id=user_id, post_id=id, content=content)
        messages.success(request, "Comment created successfully")
        return redirect("comments")

def view_comment(request, id):     #View User Comments 
    comment = get_object_or_404(Comment, id=id)
    return render(request, "comment_detail.html", {"comment": comment})

def update_comment(request, id): #Update Comments
    try:
       user_id = get_user_from_request(request)
    except AuthenticationFailed as e:
        return JsonResponse({"error": str(e)}, status=401)  
    comment = get_object_or_404(Comment, id=id)
    if comment.author_id != user_id:
        messages.error(request, "You cannot edit this comment")
        return redirect("comments")
    if request.method == "POST":
        comment.content = request.POST.get("content")
        comment.save()
        messages.success(request, "Comment updated successfully")
        return redirect("comments")    
    return redirect("comments")

def delete_comment(request, id):  #Delete comments
    try:
       user_id = get_user_from_request(request)
    except AuthenticationFailed as e:
        return JsonResponse({"error": str(e)}, status=401)  
    comment = get_object_or_404(Comment, id=id)
    if comment.author_id != user_id:
        messages.error(request, "You cannot delete this comment")
        return redirect("comments")
    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted successfully")
        return redirect("comments")    
    return redirect("comments")

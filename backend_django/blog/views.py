from datetime import timezone
from blog.models import Post, Comment
from blog.serializers import PostSerializer,CommentSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
from rest_framework import status
from account.auth_utils import get_user_from_request
from account.models import User

class AllPosts(APIView):  #Display All posts
    def get(self,request):        
        all_posts = Post.objects.all()
        if not all_posts.exists():
            raise NotFound("No posts Found")
        serialized = PostSerializer(all_posts, many=True)       
        return Response(serialized.data,status=status.HTTP_200_OK)     
       
           
    
class PostByID(APIView):   #Display post by ID
    def get(self,request,id): 
        post = Post.objects.filter(id=id).first()
        if not post:
            raise NotFound("Post Not Found")
        serialized = PostSerializer(post)
        return Response(serialized.data,status=status.HTTP_200_OK)
    

        

class UserPosts(APIView):   #User Posts
    def get(self,request,id):
        user_id = get_user_from_request(request)
        post = Post.objects.filter(id=id).first()
        if not post:
            raise NotFound("Post Not Found")
        serialized = PostSerializer(post)
        return Response(serialized.data,status=status.HTTP_200_OK)
    
    def post(self,request):    
        user_id = get_user_from_request(request)
        serializer = PostSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError("Data Entered is not Valid", serializer.errors)
        serializer.save()
        return Response("Data added", status=status.HTTP_200_OK)    
    
    def put(self,request,id):
        user_id = get_user_from_request(request)
        post  = Post.objects.filter(id=id).first()       
        if not post:
            raise NotFound("Post Not Found")    
        print(user_id , post.author_id)    
        if user_id != post.author_id:
            raise PermissionDenied("You cannot edit this Post")
        serializer = PostSerializer(post,data=request.data)
        if not serializer.is_valid():
            raise ValidationError("Data Entered is Not Valid")
        serializer.save()
        return Response("Data Updated", status = status.HTTP_200_OK)
    
    def delete(self, request, id):
        user_id = get_user_from_request(request)
        post = Post.objects.filter(id=id).first()
        if not post:
            raise NotFound("No Post Found")
        if user_id != post.author_id:
            raise PermissionDenied("You cannot Delete this Post")
        post.delete()
        return Response("Post Deleted", status= status.HTTP_200_OK)
        
         


class Comments(APIView):
    def get(self, request, id):  #get all comments with user_id
        all_comment = Comment.objects.filter(author_id=id)
        if not all_comment:
            raise NotFound("Comments Not Found")
        serializer = CommentSerializer(all_comment,many=True)              
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        user_id = get_user_from_request(request)
        serializer = CommentSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)        
        serializer.save()          
        return Response({"message": "Comment Created"},status=status.HTTP_201_CREATED)
    
    def put(self, request, id):
        user_id = get_user_from_request(request)
        comment = Comment.objects.filter(id=id).first()       
        if not comment:
            raise NotFound("Comment Not Found")
        if user_id != comment.author_id:
            raise PermissionDenied("You cannot Edit this comment")
        serializer = CommentSerializer(comment, data=request.data, partial=True)  # partial=True allows partial update
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        user_id = get_user_from_request(request)
        comment = Comment.objects.filter(id=id).first()
        if not comment:
            raise NotFound("Comment Not Found")
        if user_id != comment.author_id:
            raise PermissionDenied("You cannot Delete this comment")
        comment.delete()
        return Response({"message": "Comment deleted"}, status=status.HTTP_204_NO_CONTENT)


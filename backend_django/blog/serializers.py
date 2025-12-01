from rest_framework import serializers
from blog.models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
   class Meta:
    model = Post    
    fields =['id', 'title', 'content', 'author', 'image_url', 'published', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
   class Meta:
    model = Comment    
    fields =['id', 'post',  'author','content' ,'created_at']    
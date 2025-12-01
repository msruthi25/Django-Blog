from django.db import models
from account.models import User
from datetime import datetime

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField(null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)   # FIXED
    image_url = models.TextField(blank=True)
    published = models.BooleanField(default=True)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post= models.ForeignKey(Post,on_delete=models.CASCADE,  db_column='post_id')
    author  = models.ForeignKey(User,on_delete=models.CASCADE , db_column='author_id')
    content   = models.TextField(null=True)
    created_at = models.DateTimeField(default=datetime.now())


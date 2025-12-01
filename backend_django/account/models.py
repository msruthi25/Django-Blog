from datetime import datetime
from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True)
    email =  models.EmailField(unique=True)
    password = models.CharField(null=True, max_length=128)
    created_at = models.DateTimeField(default=datetime.now())

from datetime import date, time
from unittest.util import _MAX_LENGTH
from django.db import models
from django.db.models.base import Model
from django.forms import fields
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Articles(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    author = models.CharField(max_length=20)
    picture = models.ImageField(null=True)
    pub_date = models.DateTimeField(default=timezone.now)
    cetagory = models.CharField(max_length=120,default="")
    sub_cetagory = models.CharField(max_length=120,default="")
    total_articles_length = models.IntegerField(default=0,null=True)

    def __str__(self):
        return self.title

class Contact(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    title= models.CharField(max_length=250)
    description = models.TextField()
    replay = models.TextField(default='',blank=True)
    date = models.DateTimeField(default=timezone.now)
    seen_by_manager = models.BooleanField(default=False)
    seen_by_user = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    Article = models.ForeignKey(Articles,on_delete=models.CASCADE)
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    replay_comment_text = models.JSONField(blank=True)

class ViewArticleHistory(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    Article = models.ForeignKey(Articles,on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    


class SavedArticles(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    Article = models.ForeignKey(Articles,on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
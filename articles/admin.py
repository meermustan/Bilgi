from csv import list_dialects
from django.contrib import admin
from django.db import models
from .models import Articles,Contact,Comment
from tinymce.widgets import TinyMCE
# Register your models here.
class ArticlesAdmin(admin.ModelAdmin):
   list_display = ['title','author','pub_date','cetagory','id']

   formfield_overrides = {

    models.TextField: {'widget': TinyMCE()}

   }

class ContactAdmin(admin.ModelAdmin):
   list_display = ['title','replay','date']

class CommentAdmin(admin.ModelAdmin):
   list_display = ['User','id','Article']

# class ReplayCommentAdmin(admin.ModelAdmin):
#    list_display = ['User','id','comment']

admin.site.register(Comment,CommentAdmin)
admin.site.register(Articles, ArticlesAdmin)
admin.site.register(Contact,ContactAdmin)
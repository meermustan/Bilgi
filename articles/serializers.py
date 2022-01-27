from django.db import models
from django.db.models import fields
from django.http import request
from rest_framework import serializers
from rest_framework import validators
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Articles, Comment , Contact
from django.contrib.auth.models import User

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True,required=True)

    class Meta:
        model = User
        fields = ('username','password','email','first_name','last_name')
        extra_kwargs = {
            'first_name':{'required':True},
            'last_name':{'required':True}
        }

    def create(self,validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class CommentSerializer(serializers.ModelSerializer):
    # Replay_Comment = serializers.CharField(source='replay_comment.replay_comment_text')
    User_first_name = serializers.CharField(source='User.first_name')
    User_last_name = serializers.CharField(source='User.last_name')

    class Meta:
        model = Comment
        fields = ('User_first_name','User_last_name','id','comment','create_date','User','replay_comment_text')


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('title','description','replay','date','seen_by_user','id')

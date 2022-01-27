"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('',views.apiOverview,name="apiOverview"),
    
    path('articles-list/',views.articlesList,name='allArticles'),
    path('article/<str:pk>/',views.article,name='article'),
    path('articles-list/cetagory/',views.articlesWithCetagory,name='articles_cetagory'),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-user/',views.createUser,name='create_new user'),
    path('search/<str:pk>/',views.search,name='search_articles'),
    path('saveArticlesOrHistory/',views.saveArticleOrHistory,name='save_History_or_Articles'),
    path('getSavedArticlesOrHistory/',views.getSavedArticlesOrHistory,name='get_saved_History_or_Articles'),
    path('contact/',views.contact,name='contact'),
    path('notification/',views.notification,name='notification'),
    path('save-comments/',views.saveComments,name='save_comments'),
    path('get-comments/',views.getComments,name='get_comments'),
    path('delete-comments/',views.delComment,name='del_comments'),


] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

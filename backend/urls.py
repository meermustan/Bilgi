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
from re import S
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from articles import urls
from django.views.generic import TemplateView

urlpatterns = [

    path('',TemplateView.as_view(template_name='index.html')),
    path('cetagory/',TemplateView.as_view(template_name='index.html')),
    path('articles/',TemplateView.as_view(template_name='index.html')),
    path('article/<str:id>/',TemplateView.as_view(template_name='index.html')),
    path('search/<str:content>',TemplateView.as_view(template_name='index.html')),
    path('account/',TemplateView.as_view(template_name='index.html')),
    path('account-view/',TemplateView.as_view(template_name='index.html')),
    path('account-view/saved-list/',TemplateView.as_view(template_name='index.html')),
    path('account-view/view-history/',TemplateView.as_view(template_name='index.html')),
    path('account-view/notifications/',TemplateView.as_view(template_name='index.html')),
    path('account-view/contact/',TemplateView.as_view(template_name='index.html')),
    path('account-view/about/',TemplateView.as_view(template_name='index.html')),
    path('account-view/privicy-policy/',TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('api/', include('articles.urls')),
    path('tinymce/',include('tinymce.urls')),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

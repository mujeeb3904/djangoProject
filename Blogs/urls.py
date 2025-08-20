from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_blog, name='create_blog'),
    path('', views.get_blogs, name='get_blogs'),
    path('my-blogs/', views.get_user_blogs, name='get_user_blogs'),
]

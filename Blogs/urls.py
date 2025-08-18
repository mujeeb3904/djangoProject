from django.urls import path
from . import views
from middleware.validateTokenHandler import JWTAuthenticationMiddleware

urlpatterns = [
    path("create/", JWTAuthenticationMiddleware(views.create_blog)),
]

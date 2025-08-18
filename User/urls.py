from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.get_all_users ),
    path('register/', views.register_user),
    path('login/', views.login_user,),
    path('<str:user_id>/update/', views.update_user),
    path('<str:user_id>/delete/', views.delete_user),
    path('<str:user_id>/', views.get_user),
]

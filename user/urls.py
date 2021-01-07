from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('follow/<int:following_id>', views.follow, name='follow'),
    path('un-follow/<int:following_id>', views.un_follow, name='un-follow'),
    path('edit_profile', views.edit_profile, name='edit_profile')
]
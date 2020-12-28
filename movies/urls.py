from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('<int:movie_id>', views.detail, name='detail'),
    path('prev', views.prev, name='prev'),
]
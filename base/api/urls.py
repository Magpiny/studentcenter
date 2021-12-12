from django.urls import path

from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('rooms/', views.getRooms, name="api_rooms"),
    path('topics/', views.getTopics, name="api_topics"),
]

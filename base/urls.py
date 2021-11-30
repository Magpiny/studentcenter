# url configurations for the app and not the entire project
from django.urls import path

#from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register"),

    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.user_profile, name="profile"),

    path('settings/', views.settings, name="settings"),
    path('edit_user/', views.edit_user, name="edit_user"),

    path('create_room/', views.room_create, name="create_room"),
    path('update_room/<str:pk>/', views.room_update, name="update_room"),
    path('delete_room/<str:pk>/', views.room_delete, name="delete_room"),

    path('delete_message/<str:pk>/', views.message_delete, name="delete_message"),

    # urls for our mobile views
    path('topics/', views.m_topic, name="topics"),
    path('activities/', views.m_activities, name="activities"),

]

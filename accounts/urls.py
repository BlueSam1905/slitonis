from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = "accounts"

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_post, name='create'),
    path('profile/', views.profile, name='profile'),
    path('profile/<slug:slug>/', views.other_profile, name='other_profile'),
    path('profile/<slug:slug>/follow/', views.follow, name='follow'),
    path('myposts/',views.myposts, name="myposts"),
    path("edit/<slug:slug>/", views.edit_post,name="edit"),
    path("editprofile/", views.edit_profile,name="editprofile"),
   
]


from django.urls import path
from . import views


app_name = "posts"

urlpatterns = [
    path("categories/", views.categories, name="categories"),
    path("feed/<slug:slug>/", views.feed, name = "feed"),
    path("post/<slug:slug>/", views.post, name = "post"),
    path("post/<slug:slug>/like/", views.like_post, name = "like"),
    path("search/", views.search, name="search")
]
from django.urls import path
from . import views

app_name = "actors"

urlpatterns = [
    path("", views.actor_list, name="list"),
    path("<int:actor_id>/", views.actor_detail, name="detail"),
    path("statistics/", views.statistics, name="statistics"), 
    path("movies/", views.movie_list, name="movies"),
]
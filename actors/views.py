from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count
from actors.models import Actor, Movie


def actor_list(request):
    actors_list = Actor.objects.all()

    search_query = request.GET.get("q", "").strip()
    if search_query:
        actors_list = actors_list.filter(full_name__icontains=search_query)

    sort_param = request.GET.get("sort", "name")
    if sort_param == "age":
        actors_list = actors_list.order_by("-age")
    else:
        actors_list = actors_list.order_by("full_name")

    paginator = Paginator(actors_list, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "actors": page_obj,
        "page_obj": page_obj,
        "search_query": search_query,
        "sort_param": sort_param,
    }
    return render(request, "actors/actor_list.html", context)


def actor_detail(request, actor_id):
    actor = get_object_or_404(Actor, pk=actor_id)
    movies = actor.movies.all()
    context = {
        "actor": actor,
        "movies": movies
    }
    return render(request, "actors/actor_detail.html", context)


def movie_list(request):
    movies = Movie.objects.prefetch_related("actors").all().order_by("-year")
    context = {
        "movies": movies
    }
    return render(request, "actors/movie_list.html", context)


def statistics(request):
    stats = (
        Actor.objects
        .values("role_type")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    total = Actor.objects.count()

    selected_role = request.GET.get("role")
    role_actors = []
    if selected_role:
        role_actors = Actor.objects.filter(role_type=selected_role)

    context = {
        "stats": stats,
        "total": total,
        "selected_role": selected_role,
        "role_actors": role_actors
    }
    return render(request, "actors/statistics.html", context)
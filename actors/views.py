from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, Avg
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
    # select_related здесь не нужен (нет ForeignKey), используем prefetch
    actor = get_object_or_404(Actor, pk=actor_id)
    movies = actor.movies.all()
    context = {
        "actor": actor,
        "movies": movies
    }
    return render(request, "actors/actor_detail.html", context)


def movie_list(request):
    # Используем values() для получения только нужных полей
    movies = Movie.objects.prefetch_related("actors").all().order_by("-year")
    context = {
        "movies": movies
    }
    return render(request, "actors/movie_list.html", context)


def statistics(request):
    # 1. Агрегация (aggregate) - средний возраст всех актеров
    avg_age_data = Actor.objects.aggregate(avg_age=Avg("age"))
    avg_age = round(avg_age_data["avg_age"], 1) if avg_age_data["avg_age"] else 0

    # 2. Группировка (annotate) - количество по амплуа
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
        # 3. Исключение (exclude) - берем выбранное амплуа, 
        # но исключаем неактивных актеров (is_active=False)
        role_actors = Actor.objects.filter(
            role_type=selected_role
        ).exclude(
            is_active=False
        )

    context = {
        "stats": stats,
        "total": total,
        "avg_age": avg_age,
        "selected_role": selected_role,
        "role_actors": role_actors
    }
    return render(request, "actors/statistics.html", context)
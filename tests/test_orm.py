import pytest
from django.core.paginator import Paginator
from django.db.models import Count, Max, Min, Avg
from actors.models import Actor, Movie


# --- 1. Тесты моделей (6 тестов) ---
@pytest.mark.django_db
def test_create_actor():
    actor = Actor.objects.create(
        full_name="Тест Тестов",
        age=30,
        role_type="Главная роль",
        is_active=True
    )
    assert actor.id is not None
    assert actor.full_name == "Тест Тестов"
    assert str(actor) == "Тест Тестов (Главная роль)"


@pytest.mark.django_db
def test_default_actor_status():
    actor = Actor.objects.create(
        full_name="Новичок",
        age=20,
        role_type="Эпизод"
    )
    assert actor.is_active is True


@pytest.mark.django_db
def test_create_movie():
    movie = Movie.objects.create(
        title="Тестовый фильм",
        year=2024,
        genre="Комедия"
    )
    assert movie.id is not None
    assert str(movie) == "Тестовый фильм (2024)"


@pytest.mark.django_db
def test_actor_ordering():
    Actor.objects.create(full_name="Яков", age=30, role_type="Роль")
    Actor.objects.create(full_name="Антон", age=25, role_type="Роль")
    actors = Actor.objects.all()
    assert actors[0].full_name == "Антон"


@pytest.mark.django_db
def test_movie_actor_relation():
    actor = Actor.objects.create(
        full_name="Актер",
        age=20,
        role_type="Эпизод"
    )
    movie = Movie.objects.create(
        title="Фильм",
        year=2024,
        genre="Боевик"
    )
    movie.actors.add(actor)

    assert movie.actors.count() == 1
    assert actor.movies.first().title == "Фильм"


@pytest.mark.django_db
def test_related_name_reverse_lookup():
    actor = Actor.objects.create(full_name="А", age=20, role_type="Роль")
    movie = Movie.objects.create(title="М", year=2020, genre="Ж")
    movie.actors.add(actor)
    assert actor.movies.count() == 1
    assert actor.movies.first().title == "М"


# --- 2. Тесты фильтрации и поиска (3 теста) ---
@pytest.mark.django_db
def test_filter_actors_by_name():
    Actor.objects.create(
        full_name="Джонни Депп", age=60, role_type="Роль"
    )
    Actor.objects.create(
        full_name="Скарлетт Йоханссон", age=39, role_type="Роль"
    )
    results = Actor.objects.filter(full_name__contains="Джонни")
    assert results.count() == 1
    assert results.first().full_name == "Джонни Депп"


@pytest.mark.django_db
def test_filter_actors_by_role():
    Actor.objects.create(full_name="А1", age=30, role_type="Главная роль")
    Actor.objects.create(full_name="А2", age=40, role_type="Эпизод")
    results = Actor.objects.filter(role_type="Главная роль")
    assert results.count() == 1
    assert results.first().full_name == "А1"


@pytest.mark.django_db
def test_filter_active_actors():
    Actor.objects.create(
        full_name="Свободен", age=30, role_type="Роль", is_active=True
    )
    Actor.objects.create(
        full_name="Занят", age=30, role_type="Роль", is_active=False
    )
    results = Actor.objects.filter(is_active=True)
    assert results.count() == 1
    assert results.first().full_name == "Свободен"


# --- 3. Тесты агрегации и группировки (3 теста) ---
@pytest.mark.django_db
def test_aggregate_count():
    Actor.objects.create(full_name="А1", age=20, role_type="Роль")
    Actor.objects.create(full_name="А2", age=30, role_type="Роль")
    total = Actor.objects.count()
    assert total == 2


@pytest.mark.django_db
def test_group_by_role_type():
    Actor.objects.create(full_name="А1", age=20, role_type="Главная")
    Actor.objects.create(full_name="А2", age=30, role_type="Главная")
    Actor.objects.create(full_name="А3", age=40, role_type="Эпизод")
    stats = Actor.objects.values("role_type").annotate(count=Count("id"))
    stats_dict = {item["role_type"]: item["count"] for item in stats}
    assert stats_dict["Главная"] == 2
    assert stats_dict["Эпизод"] == 1


@pytest.mark.django_db
def test_aggregate_max_min_avg():
    Actor.objects.create(full_name="А1", age=20, role_type="Роль")
    Actor.objects.create(full_name="А2", age=40, role_type="Роль")
    ages = Actor.objects.aggregate(
        max_age=Max("age"),
        min_age=Min("age"),
        avg_age=Avg("age")
    )
    assert ages["max_age"] == 40
    assert ages["min_age"] == 20
    assert ages["avg_age"] == 30.0


# --- 4. Тесты пагинации (2 теста) ---
@pytest.mark.django_db
def test_pagination():
    for i in range(5):
        Actor.objects.create(
            full_name=f"Актер {i}",
            age=20 + i,
            role_type="Роль"
        )
    actors = Actor.objects.all()
    paginator = Paginator(actors, 2)
    assert paginator.num_pages == 3
    page1 = paginator.get_page(1)
    assert len(page1.object_list) == 2


@pytest.mark.django_db
def test_pagination_invalid_page():
    Actor.objects.create(full_name="А1", age=20, role_type="Роль")
    paginator = Paginator(Actor.objects.all(), 2)
    page = paginator.get_page("abc")
    assert page.number == 1


# --- 5. Тесты сортировки (2 теста) ---
@pytest.mark.django_db
def test_ordering_by_age_desc():
    Actor.objects.create(full_name="Молодой", age=20, role_type="Роль")
    Actor.objects.create(full_name="Старый", age=60, role_type="Роль")
    actors = Actor.objects.order_by("-age")
    assert actors[0].full_name == "Старый"
    assert actors[1].full_name == "Молодой"


@pytest.mark.django_db
def test_ordering_movies_by_year():
    Movie.objects.create(title="Новый", year=2024, genre="Ж")
    Movie.objects.create(title="Старый", year=1990, genre="Ж")
    movies = Movie.objects.order_by("-year")
    assert movies[0].title == "Новый"


# --- 6. Тесты на дополнительные требования ПР9 ---
@pytest.mark.django_db
def test_exclude_inactive_actors():
    Actor.objects.create(
        full_name="Активный", age=30, role_type="Роль", is_active=True
    )
    Actor.objects.create(
        full_name="Неактивный", age=30, role_type="Роль", is_active=False
    )
    # Проверяем exclude
    results = Actor.objects.exclude(is_active=False)
    assert results.count() == 1
    assert results.first().full_name == "Активный"


@pytest.mark.django_db
def test_aggregate_average_age():
    Actor.objects.create(full_name="А1", age=20, role_type="Роль")
    Actor.objects.create(full_name="А2", age=40, role_type="Роль")
    # Проверяем aggregate
    result = Actor.objects.aggregate(avg_age=Avg("age"))
    assert result["avg_age"] == 30.0


@pytest.mark.django_db
def test_values_query():
    Actor.objects.create(full_name="А1", age=20, role_type="Роль")
    # Проверяем values (возвращает словарь)
    result = Actor.objects.values("full_name").first()
    assert result["full_name"] == "А1"

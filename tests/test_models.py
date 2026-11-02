import pytest
from models.actors import Actor, Movie

def test_actor_creation():
    actor = Actor(10, "Тестовый Актер", 30, "Главная роль", True)
    assert actor.id == 10
    assert actor.full_name == "Тестовый Актер"
    assert actor.age == 30
    assert actor.role_type == "Главная роль"
    assert actor.is_active is True

def test_actor_creation_inactive():
    actor = Actor(11, "Занятый Актер", 45, "Эпизод", False)
    assert actor.is_active is False

def test_actor_types():
    actor = Actor(1, "Джон Доу", 25, "Эпизод", False)
    assert isinstance(actor.id, int)
    assert isinstance(actor.full_name, str)
    assert isinstance(actor.age, int)
    assert isinstance(actor.is_active, bool)

def test_movie_creation():
    movie = Movie(5, "Тестовый Фильм", 2024, "Комедия")
    assert movie.id == 5
    assert movie.title == "Тестовый Фильм"
    assert movie.year == 2024
    assert movie.genre == "Комедия"

def test_movie_types():
    movie = Movie(1, "Фильм", 2020, "Боевик")
    assert isinstance(movie.id, int)
    assert isinstance(movie.title, str)
    assert isinstance(movie.year, int)

def test_actor_modification():
    actor = Actor(1, "Имя", 20, "Роль", True)
    actor.full_name = "Новое Имя"
    assert actor.full_name == "Новое Имя"

def test_actor_str():
    """Проверяем магический метод __str__."""
    actor = Actor(1, "Джон Доу", 25, "Эпизод", False)
    assert str(actor) == "Актер: Джон Доу, 25 лет, Амплуа: Эпизод (Занят)"

def test_actor_from_data():
    """Проверяем декоратор @classmethod для создания из словаря."""
    data = {"id": 2, "full_name": "Джейн Доу", "age": 30, "role_type": "Главная роль", "is_active": True}
    actor = Actor.from_data(data)
    assert actor.id == 2
    assert actor.full_name == "Джейн Доу"
    assert actor.is_active is True

def test_movie_actor_interaction():
    """Проверяем связь объектов: добавление актера в фильм."""
    movie = Movie(1, "Тестовый фильм", 2024, "Боевик")
    actor = Actor(3, "Тестовый Актер", 40, "Главная роль", True)
    
    # Взаимодействие объектов
    movie.add_actor(actor)
    
    assert len(movie.actors) == 1
    assert movie.actors[0].full_name == "Тестовый Актер"
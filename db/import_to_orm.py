import os
import sys
import json
import django
from pathlib import Path

# 1. Определяем корневую папку проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Добавляем её в пути поиска Python, чтобы он нашел папку actors_booking
sys.path.insert(0, str(BASE_DIR))

# 3. Указываем настройки Django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", 
    "actors_booking.settings"
)

# 4. Инициализируем Django
django.setup()

# 5. Импортируем модели (только после django.setup())
from actors.models import Actor, Movie  # noqa: E402


def load_json(filepath):
    full_path = BASE_DIR / filepath
    with open(full_path, encoding="utf-8") as f:
        return json.load(f)


def main():
    print("Начинаем перенос данных...")
    
    # 1. Загружаем актеров
    actors_data = load_json("data/actors.json")
    for data in actors_data:
        Actor.objects.update_or_create(
            id=data["id"],
            defaults={
                "full_name": data["full_name"],
                "age": data["age"],
                "role_type": data["role_type"],
                "is_active": data["is_active"]
            }
        )
    print(f"Загружено актеров: {len(actors_data)}")

    # 2. Загружаем фильмы
    movies_data = load_json("data/movies.json")
    for data in movies_data:
        Movie.objects.update_or_create(
            id=data["id"],
            defaults={
                "title": data["title"],
                "year": data["year"],
                "genre": data["genre"]
            }
        )
    print(f"Загружено фильмов: {len(movies_data)}")

    # 3. Загружаем связи (кастинг)
    cast_data = load_json("data/cast.json")
    for data in cast_data:
        movie = Movie.objects.get(id=data["movie_id"])
        actor = Actor.objects.get(id=data["actor_id"])
        movie.actors.add(actor)
    print(f"Загружено связей: {len(cast_data)}")

    print("-------------------------")
    print("Данные успешно перенесены в Django ORM!")
    print(f"Всего актеров в БД: {Actor.objects.count()}")
    print(f"Всего фильмов в БД: {Movie.objects.count()}")


if __name__ == "__main__":
    main()
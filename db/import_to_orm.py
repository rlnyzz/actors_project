import os
import json
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "actors_booking.settings")
django.setup()

from actors.models import Actor, Movie  # noqa: E402


def load_json(filepath):
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def main():
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

    # 3. Загружаем связи (кастинг)
    cast_data = load_json("data/cast.json")
    for data in cast_data:
        movie = Movie.objects.get(id=data["movie_id"])
        actor = Actor.objects.get(id=data["actor_id"])
        movie.actors.add(actor)

    print("Данные успешно перенесены в Django ORM!")
    print(f"Актеров: {Actor.objects.count()}")
    print(f"Фильмов: {Movie.objects.count()}")


if __name__ == "__main__":
    main()
from typing import List, Optional


class Actor:
    """Класс, описывающий актера."""

    def __init__(self, actor_id: int, full_name: str, age: int, role_type: str, is_active: bool) -> None:
        self.id = actor_id
        self.full_name = full_name
        self.age = age
        self.role_type = role_type
        self.is_active = is_active

    def __str__(self) -> str:
        """Строковое представление актера для вывода в консоль."""
        status = "Свободен" if self.is_active else "Занят"
        return f"Актер: {self.full_name}, {self.age} лет, Амплуа: {self.role_type} ({status})"

    @classmethod
    def from_data(cls, data: dict) -> "Actor":
        """Создание объекта Actor из словаря (например, загруженного из JSON)."""
        return cls(
            actor_id=data["id"],
            full_name=data["full_name"],
            age=data["age"],
            role_type=data["role_type"],
            is_active=bool(data["is_active"])
        )


class Movie:
    """Класс, описывающий фильм."""

    def __init__(self, movie_id: int, title: str, year: int, genre: str) -> None:
        self.id = movie_id
        self.title = title
        self.year = year
        self.genre = genre
        # Взаимодействие объектов: фильм хранит список связанных актеров
        self.actors: List[Actor] = []

    def __str__(self) -> str:
        """Строковое представление фильма."""
        return f"Фильм: {self.title} ({self.year}), Жанр: {self.genre}"

    @classmethod
    def from_data(cls, data: dict) -> "Movie":
        """Создание объекта Movie из словаря."""
        return cls(
            movie_id=data["id"],
            title=data["title"],
            year=data["year"],
            genre=data["genre"]
        )

    def add_actor(self, actor: Actor) -> None:
        """Метод для добавления актера в фильм (демонстрация связи объектов)."""
        self.actors.append(actor)
from django.db import models


class Actor(models.Model):
    full_name = models.CharField(
        max_length=200,
        verbose_name="ФИО"
    )
    age = models.PositiveIntegerField(
        verbose_name="Возраст"
    )
    role_type = models.CharField(
        max_length=100,
        verbose_name="Амплуа"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Свободен"
    )

    def __str__(self):
        return f"{self.full_name} ({self.role_type})"

    class Meta:
        verbose_name = "Актер"
        verbose_name_plural = "Актеры"
        ordering = ["full_name"]


class Movie(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Название фильма"
    )
    year = models.PositiveIntegerField(
        verbose_name="Год выпуска"
    )
    genre = models.CharField(
        max_length=100,
        verbose_name="Жанр"
    )
    actors = models.ManyToManyField(
        Actor,
        related_name="movies",
        verbose_name="Актеры"
    )

    def __str__(self):
        return f"{self.title} ({self.year})"

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
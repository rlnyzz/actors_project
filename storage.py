import json
from models.actors import Actor

import json
from typing import List
from models.actors import Actor

def load_actors(filepath="data/actors.json") -> List[Actor]:
    """Загружает актеров из JSON и создает объекты через from_data."""
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)
    # Используем classmethod для создания объектов из словарей
    return [Actor.from_data(item) for item in data]

def find_actor_by_id(actors: List[Actor], actor_id: int) -> Actor | None:
    """Поиск актера по ID."""
    for actor in actors:
        if actor.id == actor_id:
            return actor
    return None

def find_actor_by_id(actors, actor_id):
    for actor in actors:
        if actor.id == actor_id:
            return actor
    return None
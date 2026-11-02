import json
from models.actors import Actor

def load_actors(filepath="data/actors.json"):
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)
    return [Actor(**item) for item in data]

def find_actor_by_id(actors, actor_id):
    for actor in actors:
        if actor.id == actor_id:
            return actor
    return None
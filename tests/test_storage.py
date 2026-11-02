import pytest
from storage import load_actors, find_actor_by_id

def test_load_actors_returns_list():
    actors = load_actors("data/actors.json")
    assert isinstance(actors, list)

def test_load_actors_not_empty():
    actors = load_actors("data/actors.json")
    assert len(actors) > 0

def test_actors_are_objects():
    actors = load_actors("data/actors.json")
    assert hasattr(actors[0], 'full_name')
    assert hasattr(actors[0], 'age')

def test_find_actor_by_valid_id():
    actors = load_actors("data/actors.json")
    first_id = actors[0].id
    found = find_actor_by_id(actors, first_id)
    assert found is not None
    assert found.id == first_id

def test_find_actor_by_invalid_id():
    actors = load_actors("data/actors.json")
    assert find_actor_by_id(actors, 99999) is None

def test_find_actor_by_zero_id():
    actors = load_actors("data/actors.json")
    assert find_actor_by_id(actors, 0) is None

def test_find_actor_by_negative_id():
    actors = load_actors("data/actors.json")
    assert find_actor_by_id(actors, -5) is None
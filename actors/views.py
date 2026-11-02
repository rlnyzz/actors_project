from django.shortcuts import render
from storage import load_actors, find_actor_by_id

def actor_list(request):
    actors = load_actors("data/actors.json")
    return render(request, "actors/actor_list.html", {"actors": actors})

def actor_detail(request, actor_id):
    actors = load_actors("data/actors.json")
    actor = find_actor_by_id(actors, actor_id)
    return render(request, "actors/actor_detail.html", {"actor": actor}, status=404 if actor is None else 200)
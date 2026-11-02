from django.shortcuts import render
from db.database import get_connection

def actor_list(request):
    conn = get_connection()
    # Запрос 1: получаем всех актеров
    actors = conn.execute("SELECT * FROM actors ORDER BY full_name").fetchall()
    conn.close()
    return render(request, "actors/actor_list.html", {"actors": actors})

def actor_detail(request, actor_id):
    conn = get_connection()
    # Параметризованный запрос (защита от SQL-инъекций)
    actor = conn.execute("SELECT * FROM actors WHERE id = ?", (actor_id,)).fetchone()
    conn.close()
    # Если актер не найден, возвращаем 404
    return render(request, "actors/actor_detail.html", {"actor": actor}, status=404 if actor is None else 200)

def statistics(request):
    conn = get_connection()
    
    # Получаем статистику по амплуа (Запрос с GROUP BY)
    stats = conn.execute("SELECT role_type, COUNT(*) as count FROM actors GROUP BY role_type").fetchall()
    # Получаем общее количество
    total = conn.execute("SELECT COUNT(*) as total FROM actors").fetchone()
    
    # Если пользователь кликнул на амплуа (есть параметр role в URL)
    selected_role = request.GET.get("role")
    role_actors = []
    
    if selected_role:
        # Делаем параметризованный запрос, чтобы получить актеров этого амплуа
        role_actors = conn.execute("SELECT * FROM actors WHERE role_type = ?", (selected_role,)).fetchall()
        
    conn.close()
    
    context = {
        "stats": stats, 
        "total": total["total"],
        "selected_role": selected_role,
        "role_actors": role_actors
    }
    return render(request, "actors/statistics.html", context)

def movie_list(request):
    conn = get_connection()
    # Получаем фильмы
    movies = conn.execute("SELECT * FROM movies ORDER BY year DESC").fetchall()
    
    # Для каждого фильма получаем список актеров (можно сделать одним запросом, но для наглядности так)
    movies_with_actors = []
    for movie in movies:
        actors = conn.execute("""
            SELECT actors.full_name 
            FROM actors 
            JOIN movie_actors ON actors.id = movie_actors.actor_id 
            WHERE movie_actors.movie_id = ?
        """, (movie["id"],)).fetchall()
        
        # Превращаем в словарь, добавляя актеров
        movie_dict = dict(movie)
        movie_dict["actors"] = [a["full_name"] for a in actors]
        movies_with_actors.append(movie_dict)
        
    conn.close()
    return render(request, "actors/movie_list.html", {"movies": movies_with_actors})
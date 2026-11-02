import json
from db.database import get_connection

def load_json(filename):
    with open(filename, encoding="utf-8") as file:
        return json.load(file)

def main():
    conn = get_connection()
    
    # 1. Импорт актеров
    actors = load_json("data/actors.json")
    conn.execute("DELETE FROM actors")
    conn.executemany(
        "INSERT INTO actors (id, full_name, age, role_type, is_active) VALUES (?, ?, ?, ?, ?)",
        [(a["id"], a["full_name"], a["age"], a["role_type"], int(a["is_active"])) for a in actors]
    )
    
    # 2. Импорт фильмов
    movies = load_json("data/movies.json")
    conn.execute("DELETE FROM movies")
    conn.executemany(
        "INSERT INTO movies (id, title, year, genre) VALUES (?, ?, ?, ?)",
        [(m["id"], m["title"], m["year"], m["genre"]) for m in movies]
    )
    
    # 3. Импорт связей (кастинг)
    cast = load_json("data/cast.json")
    conn.execute("DELETE FROM movie_actors")
    conn.executemany(
        "INSERT INTO movie_actors (movie_id, actor_id) VALUES (?, ?)",
        [(c["movie_id"], c["actor_id"]) for c in cast]
    )
    
    conn.commit()
    conn.close()
    print("Импорт всех данных успешно завершен!")

if __name__ == "__main__":
    main()
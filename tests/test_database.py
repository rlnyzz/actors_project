import sqlite3

DB_PATH = "data/actors.sqlite"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def test_database_tables_exist():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    assert "actors" in tables
    assert "movies" in tables
    assert "movie_actors" in tables

def test_actors_table_count():
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) as c FROM actors").fetchone()["c"]
    conn.close()
    # В нашем JSON ровно 6 актеров
    assert count == 6

def test_movies_table_count():
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) as c FROM movies").fetchone()["c"]
    conn.close()
    # В нашем JSON 3 фильма
    assert count == 3

def test_parameterized_query():
    conn = get_db()
    actor = conn.execute("SELECT * FROM actors WHERE id = ?", (2,)).fetchone()
    conn.close()
    assert actor is not None
    assert "Скарлетт" in actor["full_name"]

def test_join_query():
    conn = get_db()
    query = """
        SELECT movies.title, actors.full_name
        FROM movie_actors
        JOIN movies ON movie_actors.movie_id = movies.id
        JOIN actors ON movie_actors.actor_id = actors.id
    """
    results = conn.execute(query).fetchall()
    conn.close()
    assert len(results) > 0

def test_group_by_query():
    conn = get_db()
    stats = conn.execute("SELECT role_type, COUNT(*) as c FROM actors GROUP BY role_type").fetchall()
    conn.close()
    assert len(stats) > 0

def test_active_actors_where():
    conn = get_db()
    active_actors = conn.execute("SELECT * FROM actors WHERE is_active = 1").fetchall()
    conn.close()
    assert len(active_actors) > 0
    for actor in active_actors:
        assert actor["is_active"] == 1
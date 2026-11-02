import sqlite3

DB_PATH = "data/actors.sqlite"

def get_connection():
    # Подключаемся к базе
    conn = sqlite3.connect(DB_PATH)
    # Позволяет обращаться к полям по именам (как к словарю)
    conn.row_factory = sqlite3.Row
    # Включаем проверку внешних ключей (требование методички)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
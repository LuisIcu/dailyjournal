import sqlite3

from .constants import PATH, Path

def get_connection()->sqlite3.Connection:
    Path(f'{PATH}/journalfiles').mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(f'{PATH}/journalfiles/journal_entries.db')

    # Projects table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            keyword TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'en proceso'
                CHECK (status IN ('en proceso', 'finalizado')),
            limit DATE)'''
    )

    # Activities table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            activity TEXT NOT NULL,
            project TEXT NOT NULL DEFAULT 'misc')'''
    )

    # Tasks table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            keyword TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'en proceso'
                CHECK (status IN ('en proceso', 'finalizado')),
            updated_at DATE NOT NULL)'''
    )
    return conn
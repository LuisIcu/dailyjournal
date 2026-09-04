import sqlite3

from .constants import PATH, Path

def get_connection()->sqlite3.Connection:
    Path(f'{PATH}/journalfiles').mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(f'{PATH}/journalfiles/journal_entries.db')

    conn.execute('PRAGMA foreign_keys = ON')

    # Projects table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            keyword TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'en proceso'
                CHECK (status IN (
                    'en proceso',
                    'finalizado',
                    'pausado',
                    'archivado',
                    'cancelado',
                    'permanente',
                    'por iniciar'
                )),
            deadline DATE
        )'''
    )
    conn.execute('''
        INSERT OR IGNORE INTO projects (keyword, name, description, status, deadline)
        VALUES (
            'misc',
            'Misceláneos',
            'Actividades que no pertenecen a un proyecto específico',
            'permanente',
            NULL)
    ''')

    # Activities table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY,
            date DATE NOT NULL,
            activity TEXT NOT NULL,
            project TEXT NOT NULL DEFAULT 'misc',
            FOREIGN KEY (project) REFERENCES projects(keyword)
        )'''
    )

    # Tasks table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            keyword TEXT PRIMARY KEY,
            project TEXT NOT NULL DEFAULT 'misc',
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'por iniciar'
                CHECK (status IN (
                    'en proceso',
                    'finalizado',
                    'pausado',
                    'archivado',
                    'cancelado',
                    'permanente',
                    'por iniciar'
                )),
            updated_at DATE NOT NULL,
            FOREIGN KEY (project) REFERENCES projects(keyword)
        )'''
    )
    return conn
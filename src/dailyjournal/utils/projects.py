from datetime import datetime
from pprint import pprint

from .connection import get_connection

def init_project(
        keyword:str,
        name:str,
        description:str,
        limit:datetime|None
    )->None:
    with get_connection() as conn:
        conn.execute(
            '''
            INSERT INTO projects
            (keyword, name, description, status, limit)
            VALUES(?, ?, ?, "en proceso", ?)
            ''',
            (keyword, name, description, limit)
        )
    return

def show_projects(status:str|None=None)->None:
    query = 'SELECT keyword, name, status FROM projects'
    if status is not None:
        query += f' WHERE status = "{status}"'
    with get_connection() as conn:
        projects = conn.execute(query)
        pprint(projects)
    return

def show_project_details(keyword:str)->None:
    with get_connection() as conn:
        project = conn.execute(f'SELECT * FROM project WHERE keyword = "{keyword}"')
    pprint(project)
    return

def end_project(keyword:str)->None:
    with get_connection() as conn:
        conn.execute(
            '''UPDATE projects
            SET status = "finalizado", deadline = NULL 
            WHERE keyword = ?''',
            (keyword)
        )
    return
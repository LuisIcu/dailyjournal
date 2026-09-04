from datetime import datetime
from pprint import pprint

from .connection import get_connection

def new_project(
        keyword:str,
        name:str,
        description:str,
        deadline:datetime|None=None,
    )->None:
    with get_connection() as conn:
        conn.execute(
            '''
            INSERT INTO projects
            (keyword, name, description, status, deadline)
            VALUES(?, ?, ?, "en proceso", ?)
            ''',
            (keyword, name, description, deadline)
        )
    return

def show_projects(status:str|None=None)->None:
    query = 'SELECT keyword, name, status FROM projects'
    if status is not None:
        query += f' WHERE status = "{status}"'
    with get_connection() as conn:
        projects = conn.execute(query).fetchall()
        pprint(projects)
    return

def show_project_details(keyword:str)->None:
    with get_connection() as conn:
        project = conn.execute(f'SELECT * FROM projects WHERE keyword = "{keyword}"').fetchone()
    pprint(project)
    return

def update_project(keyword:str, new_status:str)->None:
    with get_connection() as conn:
        conn.execute(
            '''UPDATE projects
            SET status = ?
            WHERE keyword = ?''',
            (new_status, keyword)
        )
    return
from datetime import datetime

from .connection import get_connection

def add_new_task(
        description:str,
        keyword:str,
        status:str = 'a iniciar',
        created_at:datetime = None
    ) -> None:
    if status not in ['a iniciar', 'en progreso', 'completada']:
        raise ValueError('Estado de tarea inválido. Debe ser "a iniciar", "en progreso" o "completada".')
    if created_at is None:
        created_at = datetime.now()
    with get_connection() as conn:
        conn.execute(
            'INSERT INTO tasks (created_at, description, keyword, status) VALUES (?, ?, ?, ?)',
            (created_at, description, keyword, status)
        )
        conn.commit()
    return
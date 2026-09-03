from .connection import get_connection
from datetime import datetime
from pprint import pprint

def add_journal_entry(activity:str, date:datetime=None)->None:
    if date is None:
        date = datetime.now()
    with get_connection() as conn:
        conn.execute(
            'INSERT INTO activities (date, activity) VALUES (?, ?)',
            (date, activity)
        )
        conn.commit()
    return

def list_activities(date_from:str = None, date_to:str = None):
    query = 'SELECT date, activity FROM activities'
    params = []
    if date_from and date_to:
        query += ' WHERE date BETWEEN ? AND ?'
        params = [date_from, date_to]
    query += ' ORDER BY date'
    with get_connection() as conn:
        pprint(conn.execute(query, params).fetchall())
    return
from pathlib import Path
from datetime import datetime
import sqlite3
import argparse
from pprint import pprint

PATH = Path(__file__).parent

def get_connection()->sqlite3.Connection:
    Path(f'{PATH}/journalfiles').mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(f'{PATH}/journalfiles/journal_entries.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            activity TEXT NOT NULL
        )
    ''')
    conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at DATE NOT NULL,
                description TEXT NOT NULL,
                keyword TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'a iniciar',
                updated_at DATE
            )
        ''')
    return conn

def parse_datetime(value: str) -> datetime:
    formatos = [
        '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d', '%Y%m%d', '%Y%m%d%H%M']
    for fmt in formatos:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise argparse.ArgumentTypeError(
        f'Formato de fecha inválido: "{value}". Usa "YYYY-MM-DD [HH:MM[:SS]]" o "YYYYMMDD[HHMM]"'
    )

def build_parser()->argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='dailyjournal',
        description='Daily Journal CLI'
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Subparser for adding journal entries
    add_parser = subparsers.add_parser('add', help='Registra una nueva actividad en el diario')
    add_parser.add_argument('-a', '--activity', required=True, dest='activity', help='Descripción de la actividad realizada')
    add_parser.add_argument('-d', '--date', dest='date', type=parse_datetime, default=datetime.now(), help='Fecha de la actividad (por defecto: fecha actual)')

    # Subparser for listing activities
    list_parser = subparsers.add_parser('print', help='Imprime el diario de actividades')
    list_parser.add_argument('-f', '--from', dest='date_from', type=parse_datetime, default=None, help='Fecha de inicio del rango')
    list_parser.add_argument('-t', '--to', dest='date_to', type=parse_datetime, default=None, help='Fecha de finalización del rango')

    # Subparser for adding tasks
    task_parser = subparsers.add_parser('task', help='Agrega una nueva tarea')
    task_parser.add_argument('-d', '--description', dest='description', help='Descripción de la tarea')
    task_parser.add_argument('-k', '--keyword', dest='keyword', help='Palabra clave para la tarea')
    task_parser.add_argument('-s', '--status', dest='status', default='a iniciar', help='Estado de la tarea (por defecto: "a iniciar") [opciones: "a iniciar", "en progreso", "completada"]')
    task_parser.add_argument('-c', '--created_at', dest='created_at', type=parse_datetime, default=datetime.now(), help='Fecha de creación de la tarea (por defecto: fecha actual)')
    
    return parser

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

def add_new_task(description:str, keyword:str, status:str = 'a iniciar', created_at:datetime = None) -> None:
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

def cli()->None:
    parser = build_parser()
    args = parser.parse_args()

    match args.command:
        case 'add':
            add_journal_entry(args.activity, args.date)
        case 'print':
            list_activities(args.date_from, args.date_to)
        case 'task':
            add_new_task(args.description, args.keyword, args.status, args.created_at)
        case _:
            print('Ingresar un comando válido')
    return
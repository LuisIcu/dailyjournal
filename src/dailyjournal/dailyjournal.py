from datetime import datetime
import argparse

from .utils.activities import add_journal_entry, list_activities
from .utils.tasks import add_new_task

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
        prog='myjournal',
        description='Daily Journal CLI'
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # SUBPARSERS FOR 'PROJECTS' COMMAND
    proj_parser = subparsers.add_parser('projects', help='Gestión de proyectos')
    proj_subparser = proj_parser.add_subparsers(dest='proj_commands', required=True)

    proj_add = proj_subparser.add_parser('add', help='Crear un nuevo proyecto')
    proj_add.add_argument('-k', '--keyword', dest='keyword', help='Clave del proyecto', required=True)
    proj_add.add_argument('-n', '--name', dest='name', help='Nombre del proyecto', required=True)
    proj_add.add_argument('-d', '--description', dest='description', help='Descripción del proyecto', required=True)
    proj_add.add_argument('-l', '--limit', dest='limit', help='Fecha límite del proyecto', default=None)

    proj_show = proj_subparser.add_parser('show', help='Mostrar los proyectos creados')
    proj_show.add_argument('-s', '--status', dest='status', help='Filtar los proyectos por el estado ["en proceso", "finalizado"]', default=None)

    proj_det = proj_subparser.add_parser('details', help='Mostrar los detalles de un proyecto')
    proj_det.add_argument('-k', '--keyword', dest='keyword', help='Clave del proyecto', default=None)

    proj_end = proj_subparser.add_parser('end', help='Marcar un proyecto como finalizado')
    proj_end.add_argument('-k', '--keyword', dest='keyword', help='Nombre del proyecto a marcar como finalizado', required=True)

    # SUBPARSERS FOR 'ACTIVITIES' COMMAND
    act_parser = subparsers.add_parser('activities', help='Gestión de actividadas realizadas')
    act_subparser = act_parser.add_subparsers(dest='act_commands', required=True)

    act_add = act_subparser.add_parser('add', help='Ingresar una entrada en el diario')
    act_add.add_argument('-a', '--activity',required=True, dest='activity',help='Descripción de la actividad realizada')
    act_add.add_argument('-d', '--date', dest='date', type=parse_datetime, default=None, help='Fecha de la actividad (por defecto: fecha actual)')
    act_add.add_argument('-p', '--project', dest='project', default='misc', help='Proyecto al cual pertenece la actividad')

    act_list = act_subparser.add_parser('list', help='Imprime el diario de actividades')
    act_list.add_argument('-f', '--from', dest='date_from', type=parse_datetime, default=None, help='Fecha de inicio del rango')
    act_list.add_argument('-t', '--to', dest='date_to', type=parse_datetime, default=None, help='Fecha de finalización del rango')

    # Subparser for adding tasks
    task_parser = subparsers.add_parser('task', help='Agrega una nueva tarea')
    task_subparser = task_parser.add_subparsers(dest='task_commands', required=True)

    task_add = task_subparser.add_parser('add', help='Crear una nueva tarea')
    task_add.add_argument('-k', '--keyword', dest='keyword', help='Palabra clave para la tarea')
    task_add.add_argument('-n', '--name', dest='name', help='Nombre para la tarea')
    task_add.add_argument('-d', '--description', dest='description', help='Descripción de la tarea')
    task_add.add_argument('-s', '--status', dest='status', default='en progreso', help='Estado de la tarea (por defecto: "a iniciar") ["en progreso", "completada"]')
    task_add.add_argument('-u', '--updated_at', dest='updated_at', type=parse_datetime, default=None, help='Última actualización de la tarea')
    
    return parser

def cli()->None:
    parser = build_parser()
    args = parser.parse_args()
    print(args)

    match args.command:
        case 'add':
            print(args.command)
            # add_journal_entry(args.activity, args.date)
        case 'print':
            print(args.command)
            # list_activities(args.date_from, args.date_to)
        case 'task':
            print(args.command)
            # add_new_task(args.description, args.keyword, args.status, args.created_at)
        case _:
            print('Ingresar un comando válido')
    return
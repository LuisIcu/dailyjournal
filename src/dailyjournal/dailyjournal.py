from datetime import datetime
import argparse

from .utils.projects import (
    new_project, 
    show_projects, 
    show_project_details, 
    update_project,
    update_project)
from .utils.activities import (
    add_journal_entry,
    list_activities)
from .utils.tasks import (
    add_new_task)

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

# PROJECTS FUNCTIONS
def new_project_func(args:argparse.Namespace)->None:
    new_project(args.keyword, args.name, args.description, args.deadline)

def show_projects_func(args:argparse.Namespace)->None:
    show_projects(args.status)

def show_project_details_func(args:argparse.Namespace)->None:
    show_project_details(args.keyword)

def update_project_func(args:argparse.Namespace)->None:
    update_project(args.keyword, args.new_status)

# ACTIVITIES FUNCTIONS
def add_journal_entry_func(args:argparse.Namespace)->None:
    add_journal_entry(args.activity, args.project, args.date)

def list_activities_func(args:argparse.Namespace)->None:
    list_activities(args.date_from, args.date_to)

# BUILD PARSER
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
    proj_add.add_argument('-dl', '--deadline', dest='deadline', type=parse_datetime, help='Fecha límite del proyecto', default=None)
    proj_add.set_defaults(func=new_project_func)

    proj_show = proj_subparser.add_parser('show', help='Mostrar los proyectos creados')
    proj_show.add_argument('-s', '--status', dest='status', help='Filtar los proyectos por el estado ["en proceso", "finalizado"]', default=None)
    proj_show.set_defaults(func=show_projects_func)

    proj_det = proj_subparser.add_parser('details', help='Mostrar los detalles de un proyecto')
    proj_det.add_argument('-k', '--keyword', dest='keyword', help='Clave del proyecto')
    proj_det.set_defaults(func=show_project_details_func)

    proj_end = proj_subparser.add_parser('end', help='Marcar un proyecto como finalizado')
    proj_end.add_argument('-k', '--keyword', dest='keyword', help='Nombre del proyecto a marcar como finalizado', required=True)
    proj_end.add_argument('-ns', '--new-status', dest='new_status', help='Nuevo estado para el proyecto', required=True)
    proj_end.set_defaults(func=update_project_func)

    # SUBPARSERS FOR 'ACTIVITIES' COMMAND
    act_parser = subparsers.add_parser('activities', help='Gestión de actividadas realizadas')
    act_subparser = act_parser.add_subparsers(dest='act_commands', required=True)

    act_add = act_subparser.add_parser('add', help='Ingresar una entrada en el diario')
    act_add.add_argument('-a', '--activity', required=True, dest='activity',help='Descripción de la actividad realizada')
    act_add.add_argument('-d', '--date', dest='date', type=parse_datetime, default=None, help='Fecha de la actividad (por defecto: fecha actual)')
    act_add.add_argument('-p', '--project', dest='project', default='misc', help='Proyecto al cual pertenece la actividad')
    act_add.set_defaults(func=add_journal_entry_func)

    act_list = act_subparser.add_parser('list', help='Imprime el diario de actividades')
    act_list.add_argument('-f', '--from', dest='date_from', type=parse_datetime, default=None, help='Fecha de inicio del rango')
    act_list.add_argument('-t', '--to', dest='date_to', type=parse_datetime, default=None, help='Fecha de finalización del rango')
    act_list.set_defaults(func=list_activities_func)

    # Subparser for adding tasks
    task_parser = subparsers.add_parser('task', help='Gestión de tareas')
    task_subparser = task_parser.add_subparsers(dest='task_commands', required=True)

    task_add = task_subparser.add_parser('add', help='Crear una nueva tarea')
    task_add.add_argument('-k', '--keyword', dest='keyword', help='Palabra clave para la tarea')
    task_add.add_argument('-n', '--name', dest='name', help='Nombre para la tarea')
    task_add.add_argument('-d', '--description', dest='description', help='Descripción de la tarea')
    task_add.add_argument('-s', '--status', dest='status', default='en progreso', help='Estado de la tarea (por defecto: "a iniciar") ["en progreso", "completada"]')
    task_add.add_argument('-u', '--updated_at', dest='updated_at', type=parse_datetime, default=None, help='Última actualización de la tarea')
    
    return parser

# CLI FUNCTION
def cli()->None:
    parser = build_parser()
    args = parser.parse_args()

    args.func(args)
    return
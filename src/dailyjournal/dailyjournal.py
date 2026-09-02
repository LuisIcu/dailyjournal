from pathlib import Path
from datetime import datetime

PATH = Path(__file__).parent

def add_journal_entry(activitie:str)->None:
    if not Path(f'{PATH}/journalfiles/journal_entries.csv').exists():
        with open(f'{PATH}/journalfiles/journal_entries.csv', 'w') as j:
            j.write('Fecha,Actividad\n')

    with open(f'{PATH}/journalfiles/journal_entries.csv', 'a') as j:
        j.write(f'{datetime.now():%Y-%m-%d %H:%M},{activitie}\n')
    return

def print_journal()->None:
    from pandas import read_csv
    if not Path(f'{PATH}/journalfiles/journal_entries.csv').exists():
        print('No se ha creado ningún journal')
        return
    journal = read_csv(f'{PATH}/journalfiles/journal_entries.csv', parse_dates=['Fecha'])
    print(journal)
    return

def cli()->None:
    from sys import argv
    match argv[1]:
        case '-n':
            activity = argv[2]
            if ',' in activity:
                print('No poner comas en la actividad')
            add_journal_entry(repr(argv[2].replace(',', '.')))
        case '-p':
            print_journal()
        case _:
            print('Ingresar un comando válido')
    return
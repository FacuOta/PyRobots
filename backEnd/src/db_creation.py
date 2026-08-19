from pony.orm import *

from settings import ruta

def create_db(is_Test: bool):
    if (not is_Test):
        db = Database()
        db.bind(provider='sqlite', filename=ruta('database.db'), create_db=True)
    else:
        db = Database()
        db.bind(provider='sqlite', filename = ':sharedmemory:')
    return db
from pony.orm import *

def create_db(is_Test: bool):
    if (not is_Test):
        db = Database()
        db.bind(provider='sqlite', filename = '../database.db', create_db = True)
    else:
        db = Database()
        db.bind(provider='sqlite', filename = ':sharedmemory:')
    return db
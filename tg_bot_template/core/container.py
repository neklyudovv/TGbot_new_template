from ..config.settings import settings
from ..infrastructure.db.connection import setup_db
from peewee_async import Manager

class Container:
    def __init__(self):
        self.settings = settings
        self.db_manager: Manager = setup_db(self.settings)

    def get_db_manager(self) -> Manager:
        return self.db_manager

container = Container()

def get_db_manager() -> Manager:
    return container.get_db_manager()

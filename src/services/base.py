from src.utils.dbmanager import DBManager

class BaseService :
    def __init__(self, db: DBManager | None = None) -> None : 
        self.db = db


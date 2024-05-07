from config import settings
from sqlalchemy import MetaData, create_engine


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


try:

    class DatabaseManager(metaclass=SingletonMeta):
        def __init__(self):
            self.engine = create_engine(settings.BASE_CONNECTION_MARKET_SERVER, pool_pre_ping=True)
            self.metadata = MetaData()
            self.metadata.reflect(bind=self.engine)

            # Add table name, if you require to connect to DB
            # self.stress_test_events = self.metadata.tables["table_name"]

except Exception as e:
    print(f"An error occurred during DatabaseManager instantiation: {e}")

# Uncomment below if database connection is necessary
# db_manager = DatabaseManager()
# object_name = db_manager.table_name

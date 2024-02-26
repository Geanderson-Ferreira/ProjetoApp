import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


#ENGINE = create_engine(DATABASE, pool_pre_ping=True, connect_args={'check_same_thread': False}, echo=True)


load_dotenv()

DATABASE = os.getenv('DATABASE')
DB_NAME = os.getenv('DB_NAME')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

API_PREFIX = '/api'
ENGINE = create_engine(DATABASE, connect_args={'check_same_thread': False}, echo=False)

# Função para ativar chaves estrangeiras no SQLite
@event.listens_for(ENGINE, 'connect')
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SESSION = sessionmaker(bind=ENGINE)
BASE = declarative_base()

#variavel para uso apenas em desenvolvimento
DEV_ENV_RUNNER_CONFIG = {
    'gean-macbookpro': 'uvicorn api:app --host 10.0.0.102 --port 8000 --reload',
    'DESKTOP-Q6PV6P4': 'uvicorn api:app --host 192.168.100.105 --port 8000 --reload'
}
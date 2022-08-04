from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from Hermione.conf import get_int_key, get_str_key
from Hermione import LOGGER

DB_URI = get_str_key("DATABASE_URL")
DB_URI_HEROKU = get_str_key("SQLALCHEMY_DATABASE_URI") 

if DB_URI == None:
    DB_URI = DB_URI_HEROKU
    
def start() -> scoped_session:
    engine = create_engine(DB_URI, client_encoding="utf8")
    LOGGER.info("[PostgreSQL] Connecting to database......")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
try:
    SESSION = start()
except Exception as e:
    LOGGER.exception(f'[PostgreSQL] Failed to connect due to {e}')
    exit()
   
LOGGER.info("[PostgreSQL] Connection successful, session started.")

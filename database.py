import os
import dotenv

from sqlalchemy import engine
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import Session, sessionmaker

from models import SQLBase

dotenv.load_dotenv()

conn_string = os.environ['DB_CONN_STRING']
opts = {}
if conn_string[:6] == "sqlite":
        opts["check_same_thread"] = False
engine = create_engine(f"{conn_string}", connect_args=opts)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def run_migrations(sql_engine: engine) -> None:
    SQLBase.metadata.create_all(sql_engine)

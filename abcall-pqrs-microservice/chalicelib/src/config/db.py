import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

db_session = None
engine = None

def init_db():
    global db_session
    global engine

    database_url = os.getenv('DATABASE_URL')
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db_session = scoped_session(SessionLocal)
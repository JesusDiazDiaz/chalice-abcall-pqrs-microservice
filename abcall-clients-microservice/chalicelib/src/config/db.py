from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

db_session = None
engine = None

def init_db():
    global db_session
    global engine

    engine = create_engine("postgresql://username:password@hostname:port/dbname")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db_session = scoped_session(SessionLocal)
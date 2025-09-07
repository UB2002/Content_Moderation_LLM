from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import time 


load_dotenv()


DB_URL = os.getenv("DATABASE_URL")

def call ():
    time.sleep(5)
    engine = create_engine(DB_URL, echo=True)
    return engine

engine = call()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db 
    finally :
        db.close()
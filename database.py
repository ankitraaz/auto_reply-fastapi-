# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://raaz:password@localhost/fastapidb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

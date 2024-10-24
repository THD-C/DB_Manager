import os
from sqlalchemy.orm import sessionmaker
from src.DB.engine import engine
from src.DB.startup import create_tables

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

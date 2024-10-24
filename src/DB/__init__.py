import os
from sqlalchemy.orm import sessionmaker
from src.DB.Tables.Order import Order
from src.DB.Tables.Transaction import Transaction
from src.DB.Tables.User import User
from src.DB.Tables.UserDetail import UserDetail
from src.DB.Tables.Wallet import Wallet
from src.DB.engine import engine
from src.DB.startup import create_tables

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

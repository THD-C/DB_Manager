import os
from sqlalchemy.orm import sessionmaker
from sqlmodel import or_
from src.DB.Tables.Order import Order
from src.DB.Tables.Transaction import Transaction
from src.DB.Tables.User import User
from src.DB.Tables.UserDetail import UserDetail
from src.DB.Tables.Wallet import Wallet
from src.DB.Tables.Payment import Payment
from src.DB.engine import engine

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from sqlmodel import SQLModel, Field
from src.DB.BaseDBOpsModel import BaseDBOpsModel
from datetime import datetime


class Transaction(SQLModel, BaseDBOpsModel, table=True):
    __tablename__: str = "transaction"

    id: int = Field(primary_key=True, default=None)
    date: datetime = Field()
    operation_type: str = Field()
    wallet_id: int = Field(foreign_key="wallet.id", nullable=False)
    nominal_value: float = Field()

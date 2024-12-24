from sqlmodel import SQLModel, Field
from src.DB.BaseDBOpsModel import BaseDBOpsModel
from datetime import datetime
from src.DB.Tables import TABLE_NAME_TRANSACTION, TABLE_NAME_WALLET, PK_WALLET


class Transaction(SQLModel, BaseDBOpsModel, table=True):
    __tablename__: str = TABLE_NAME_TRANSACTION

    id: int = Field(primary_key=True, default=None)
    date: datetime = Field()
    operation_type: str = Field()
    wallet_id: int = Field(
        foreign_key=f"{TABLE_NAME_WALLET}.{PK_WALLET}", nullable=False
    )
    nominal_value: float = Field()

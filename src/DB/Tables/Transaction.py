from sqlmodel import SQLModel, Field
from datetime import datetime


class Transaction(SQLModel, table=True):
    __tablename__: str = "transaction"

    ID: int = Field(primary_key=True, default=None)
    date: datetime = Field()
    operation_type: str = Field()
    wallet_ID: int = Field(foreign_key="wallet.ID", nullable=False)
    nominal_value: float = Field()

from sqlmodel import SQLModel, Field
from datetime import datetime
from src.DB.BaseDBOpsModel import BaseDBOpsModel
from src.DB.Tables import TABLE_NAME_PAYMENT, TABLE_NAME_USER, PK_USER

DEFAULT_DATE_EXECUTED = datetime(1970, 1, 1, 0, 0, 0, 0)


class Payment(SQLModel, BaseDBOpsModel, table=True):
    __tablename__: str = TABLE_NAME_PAYMENT

    id: str = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key=f"{TABLE_NAME_USER}.{PK_USER}", nullable=False)
    currency: str = Field(nullable=False)
    nominal: float = Field(nullable=False)
    state: int = Field()  # enum

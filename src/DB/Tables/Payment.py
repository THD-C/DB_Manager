from sqlmodel import SQLModel, Field
from datetime import datetime
from src.DB.BaseDBOpsModel import BaseDBOpsModel

DEFAULT_DATE_EXECUTED = datetime(1970, 1, 1, 0, 0, 0, 0)


class Payment(SQLModel, BaseDBOpsModel, table=True):
    __tablename__: str = "payment"

    id: int = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key="user.ID", nullable=False)
    currency: str = Field(nullable=False)
    nominal: float = Field(nullable=False)
    state: str = Field()  # enum

from sqlmodel import SQLModel, Field
from src.DB.BaseDBOpsModel import BaseDBOpsModel


class Wallet(SQLModel, BaseDBOpsModel, table=True):
    __tablename__: str = "wallet"

    id: int = Field(primary_key=True, default=None)
    user_id: int = Field(
        foreign_key="user.ID",
        nullable=False,
    )
    currency: str = Field()
    value: float = Field()

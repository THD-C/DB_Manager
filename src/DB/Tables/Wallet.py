from sqlmodel import SQLModel, Field
from src.DB.BaseDBOpsModel import BaseDBOpsModel
from src.DB.Tables import TABLE_NAME_WALLET, TABLE_NAME_USER, PK_USER


class Wallet(SQLModel, BaseDBOpsModel, table=True):
    __tablename__: str = TABLE_NAME_WALLET

    id: int = Field(primary_key=True, default=None)
    user_id: int = Field(
        foreign_key=f"{TABLE_NAME_USER}.{PK_USER}",
        nullable=False,
    )
    currency: str = Field()
    value: float = Field()
    is_crypto: bool = Field(default=False)

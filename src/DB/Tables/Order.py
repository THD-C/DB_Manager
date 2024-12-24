from sqlmodel import SQLModel, Field
from datetime import datetime
from src.DB.BaseDBOpsModel import BaseDBOpsModel
from src.DB.Tables import (
    TABLE_NAME_ORDER,
    TABLE_NAME_USER,
    TABLE_NAME_WALLET,
    PK_USER,
    PK_WALLET,
)

DEFAULT_DATE_EXECUTED = datetime(1970, 1, 1, 0, 0, 0, 0)


class Order(SQLModel, BaseDBOpsModel, table=True):
    __tablename__: str = TABLE_NAME_ORDER

    id: int = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key=f"{TABLE_NAME_USER}.{PK_USER}", nullable=False)
    fiat_wallet_id: int = Field(
        foreign_key=f"{TABLE_NAME_WALLET}.{PK_WALLET}", nullable=False
    )
    crypto_wallet_id: int = Field(
        foreign_key=f"{TABLE_NAME_WALLET}.{PK_WALLET}", nullable=False
    )
    date_created: datetime = Field(default_factory=datetime.now)
    date_executed: datetime = Field(default=DEFAULT_DATE_EXECUTED)
    status: str = Field()  # enum
    nominal: float = Field()
    cash_quantity: float = Field(nullable=True)
    price: float = Field()
    type: str = Field()  # enum [stop_loss, take_profit, instant]
    side: str = Field()  # enum [buy, sell]

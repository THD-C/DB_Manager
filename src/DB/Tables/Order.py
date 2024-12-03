from sqlmodel import SQLModel, Field
from datetime import datetime
from src.DB.BaseDBOpsModel import BaseDBOpsModel

DEFAULT_DATE_EXECUTED = datetime(1970, 1, 1, 0, 0, 0, 0)


class Order(SQLModel, BaseDBOpsModel, table=True):
    __tablename__: str = "order"

    id: int = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key="user.ID", nullable=False)
    fiat_wallet_id: int = Field(foreign_key="wallet.id", nullable=False)
    crypto_wallet_id: int = Field(foreign_key="wallet.id", nullable=False)
    date_created: datetime = Field(default_factory=datetime.now)
    date_executed: datetime = Field(default=DEFAULT_DATE_EXECUTED)
    status: str = Field()  # enum
    nominal: float = Field()
    cash_quantity: float = Field(nullable=True)
    price: float = Field()
    type: str = Field()  # enum [stop_loss, take_profit, instant]
    side: str = Field()  # enum [buy, sell]

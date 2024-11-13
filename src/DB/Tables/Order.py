from sqlmodel import SQLModel, Field
from datetime import datetime


class Order(SQLModel, table=True):
    __tablename__: str = "order"

    ID: int = Field(primary_key=True, default=None)
    user_ID: int = Field(foreign_key="user.ID", nullable=False)
    date_created: datetime = Field()
    date_executed: datetime = Field()
    status: str = Field()  # enum
    currency: str = Field()
    nominal: float = Field()
    cash_quantity: float = Field()
    price: float = Field()
    type: str = Field()  # enum [stop_loss, take_profit, instant]
    side: str = Field()  # enum [buy, sell]

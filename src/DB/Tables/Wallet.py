from sqlmodel import SQLModel, Field


class Wallet(SQLModel, table=True):
    __tablename__: str = "wallet"

    ID: int = Field(primary_key=True, default=None)
    user_ID: int = Field(foreign_key="user.ID", nullable=False)
    currency: str = Field()
    value: float = Field()

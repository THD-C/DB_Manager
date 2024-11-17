from sqlmodel import SQLModel, Field
from pydantic import field_validator
from src.DB.BaseDBOpsModel import BaseDBOpsModel


class Wallet(SQLModel, BaseDBOpsModel, table=True):
    __tablename__: str = "wallet"

    id: int = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key="user.ID", nullable=False,)
    currency: str = Field()
    value: float = Field()

    def __model_post_init__(self):
        self.id = int(self.id)
        self.user_id = int(self.user_id)
    
    # @field_validator("id", "user_id", mode="before")
    @field_validator("user_id", mode="plain")
    def parse_int(cls, value, field):
        print("user_id")
        return int(value)
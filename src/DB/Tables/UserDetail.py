from sqlmodel import SQLModel, Field
from src.DB.BaseDBOpsModel import BaseDBOpsModel


class UserDetail(SQLModel, BaseDBOpsModel, table=True):
    __tablename__: str = "user_detail"

    ID: int = Field(primary_key=True, default=None)
    name: str = Field()
    surname: str = Field()
    street: str = Field()
    building: str = Field()
    city: str = Field()
    postal_code: str = Field()
    country: str = Field()

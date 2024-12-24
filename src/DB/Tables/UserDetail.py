from sqlmodel import SQLModel, Field
from src.DB.BaseDBOpsModel import BaseDBOpsModel
from src.DB.Tables import TABLE_NAME_USER_DETAIL


class UserDetail(SQLModel, BaseDBOpsModel, table=True):
    __tablename__: str = TABLE_NAME_USER_DETAIL

    ID: int = Field(primary_key=True, default=None)
    name: str = Field()
    surname: str = Field()
    street: str = Field()
    building: str = Field()
    city: str = Field()
    postal_code: str = Field()
    country: str = Field()

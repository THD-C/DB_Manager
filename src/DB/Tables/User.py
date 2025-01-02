from sqlmodel import SQLModel, Field
from user.user_pb2 import AuthUser
from src.DB.BaseDBOpsModel import BaseDBOpsModel
from src.DB.Tables import TABLE_NAME_USER, TABLE_NAME_USER_DETAIL, PK_USER_DETAIL


class User(SQLModel, BaseDBOpsModel, table=True):
    __tablename__: str = TABLE_NAME_USER

    ID: int = Field(primary_key=True, default=None)
    username: str = Field(unique=True)
    email: str = Field(unique=True, nullable=False)
    password: str = Field(nullable=False)
    user_type: int = Field(nullable=False, default=1)

    user_detail_ID: int = Field(
        foreign_key=f"{TABLE_NAME_USER_DETAIL}.{PK_USER_DETAIL}",
        nullable=True,
        default=None,
        unique=True,
    )

    def __eq__(self, other):
        if isinstance(other, AuthUser):
            return (
                self.email == getattr(other, "login")
                or self.username == getattr(other, "login")
            ) and self.password == getattr(other, "password")

        if isinstance(other, User):
            return self.email == other.email and self.password == other.password

        return False

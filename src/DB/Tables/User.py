from sqlmodel import SQLModel, Field
from user.user_pb2 import AuthUser
from src.DB.BaseDBOpsModel import BaseDBOpsModel
import src.Utils as Utils


class User(SQLModel, BaseDBOpsModel, table=True):
    __tablename__: str = "user"

    ID: int = Field(primary_key=True, default=None)
    username: str = Field(unique=True)
    email: str = Field(unique=True, nullable=False)
    password: str = Field(nullable=False)

    user_detail_ID: int = Field(
        foreign_key="user_detail.ID", nullable=True, default=None
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

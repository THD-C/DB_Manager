from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__: str = "user"

    ID: int = Field(primary_key=True, default=None)
    username: str = Field()
    password: str = Field()

    user_detail_ID: int = Field(
        foreign_key="user_detail.ID", nullable=True, default=None
    )

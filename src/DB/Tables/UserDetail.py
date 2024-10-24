from sqlmodel import SQLModel, Field


class UserDetail(SQLModel, table=True):
    __tablename__: str = "user_detail"

    ID: int = Field(primary_key=True, default=None)
    name: str = Field()
    surname: str = Field()
    city: str = Field()
    postal_code: str = Field()
    street: str = Field()
    building: str = Field()

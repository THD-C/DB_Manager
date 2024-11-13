from sqlmodel import SQLModel, create_engine
from src.DB.engine import connection_string


def create_tables(drop_existing: bool = False):
    engine = create_engine(
        connection_string,
        # echo=True
    )
    if drop_existing:
        SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

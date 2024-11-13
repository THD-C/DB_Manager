import os
from sqlmodel import create_engine
from sqlalchemy import create_engine

# from src.Utils.OpenTelemetry.OpenTelemetry import instrument_sqlalchemy

LOCALHOST_PG = "postgresql://default:PL_tech_hand_elk@localhost:5432/thdc"

connection_string = os.getenv("POSTGRES_URL", LOCALHOST_PG)

engine = create_engine(connection_string)
# instrument_sqlalchemy(engine)

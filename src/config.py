import os
from dotenv import load_dotenv


load_dotenv()

SERVICE_NAME = "DB_Manager"

TEMPO_HOSTNAME = os.getenv("TEMPO_HOSTNAME", "Tempo")
TEMPO_PORT = os.getenv("TEMPO_PORT", "4317")

MONGO_MANAGER = os.getenv("MONGO_MANAGER", "Mongo_Manager")
MONGO_MANAGER_PORT = os.getenv("MONGO_MANAGER_PORT", 50051)

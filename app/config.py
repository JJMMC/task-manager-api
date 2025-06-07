import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del archivo .env

SECRET_KEY = os.getenv("SECRET_KEY", "superclave")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
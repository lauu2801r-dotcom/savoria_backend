from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Savoria API"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")

settings = Settings()
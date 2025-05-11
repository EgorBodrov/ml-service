from pathlib import Path
import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
load_dotenv(ROOT_DIR / ".env")


class Settings(BaseSettings):
    db_user: str = os.environ["POSTGRES_USER"]
    db_password: str = os.environ["POSTGRES_PASSWORD"]
    db_name: str = os.environ["POSTGRES_DATABASE"]
    db_host: str = os.environ["POSTGRES_HOST"]
    db_port: str = "5432"

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

settings = Settings()

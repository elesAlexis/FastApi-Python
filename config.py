from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    server: str
    database: str
    username: str
    password: str
    driver: str = '{ODBC Driver 17 for SQL Server}'
    db_auth_mode: Literal["sql", "windows"] = "sql"
    secret_key: str
    algorithm: str
    expiration_minutes: int

    class Config:
        env_file = ".env"  

settings = Settings()

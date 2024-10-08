from pydantic_settings import BaseSettings
from pathlib import Path

path = Path.cwd()
env_path = path / ".env"


# Add your details here 👇 if you choose to run without docker
# for testing(pytest) you must have your details here or create a .env in the root directory
class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    TEST_SQLALCHEMY_DATABASE_URL: str
    JWT_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRY_TIME: int = 20

    class Config:
        env_path = env_path
        env_file_encoding = "utf-8"


settings = Settings()

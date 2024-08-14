from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class AuthSettings(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str


class DatabaseSettings(BaseSettings):
    DB_PORT: str
    DB_HOST: str
    DB_NAME: str
    DB_PASSWORD: str
    DB_USER: str

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class Settings(AuthSettings, DatabaseSettings):
    ...


settings = Settings()

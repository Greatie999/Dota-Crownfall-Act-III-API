from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8000
    DB_URL: str
    JWT_SECRET_KEY: str = "09d25e094faa69563b93f7099f6f0fca2556c818166b7a4caa6cf63b88e8d3e7"
    API_SECRET_KEY: str = "X-PORSCHE911-X"
    ALGORITHM: str = "HS256"


settings = Settings(
    _env_file=".env",
    _env_file_encoding="utf-8",
)

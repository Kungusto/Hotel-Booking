from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings) :
    MODE : Literal["TEST", "DEV", "LOCAL", "PROD"]

    DB_NAME : str
    DB_USER : str
    DB_HOST : str
    DB_PORT : int
    DB_PASS : str

    @property
    def REDIS_URL(self) : 
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def DB_URL(self) :
        return  f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    JWT_SECRET_KEY : str
    JWT_ALGORITHM : str
    
    REDIS_HOST : str
    REDIS_PORT : int

    model_config = SettingsConfigDict(env_file='.env')
    
settings = Settings()


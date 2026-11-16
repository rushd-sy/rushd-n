from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


    TEST_DATABASE_URL: str
    DATABASE_URL: str
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings() # type: ignore

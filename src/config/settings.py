from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    fred_api_key: str
    twelve_data_api_key: str
    exchangerate_access_key: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    
    model_config = SettingsConfigDict(env_file=".env")
    
settings = Settings()
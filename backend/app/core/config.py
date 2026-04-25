import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str
    APP_ENV: str
    APP_HOST: str
    APP_PORT: int

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    REDIS_HOST: str
    REDIS_PORT: int

    WEAVIATE_URL: str
    WEAVIATE_GRPC_HOST: str
    WEAVIATE_GRPC_PORT: int

    DATABASE_URL: str
    REDIS_URL: str

    OPENAI_API_KEY: str = ""
    LLAMA_CLOUD_API_KEY: str = ""

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_EMBED_MODEL: str = os.getenv("GEMINI_EMBED_MODEL", "gemini-embedding-2")
    GEMINI_CHAT_MODEL: str = os.getenv("GEMINI_CHAT_MODEL", "gemini-3-flash-preview")




    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore" 
    )
    
settings = Settings()
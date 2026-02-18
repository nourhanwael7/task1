"""Application configuration."""

from functools import lru_cache
import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Runtime settings loaded from environment variables."""

    mongo_uri: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    database_name: str = os.getenv("MONGO_DB_NAME", "school")
    collection_name: str = os.getenv("MONGO_COLLECTION_NAME", "students")


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""

    return Settings()

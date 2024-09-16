from typing import Any, Dict, List, Optional, Union
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "Social Media"
    PROJECT_VERSION: str = "1.0.0"
    SECRET_KEY: str = "72b6dc51f41263d45c111670951419ef171a16abaccb201189144ea9d5ea13a6"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATA_BASE: str = "mysql+pymysql://root:Surya%400067@localhost:3306/socialmedia"

    # Define the base directory and image directory
    BASE_DIR: Path = Path(__file__).resolve().parent.parent  # Points to the 'Backend' folder
    PROFILE_IMAGE_DIR: Path = BASE_DIR / "image" / "profile"
    POST_IMAGE_DIR : Path = BASE_DIR / "image" / "post"

    class Config:
        case_sensitive = True

settings = Settings()

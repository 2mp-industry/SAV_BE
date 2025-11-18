# core/config.py
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator, ConfigDict
from dotenv import load_dotenv
import urllib.parse
import os

load_dotenv()

class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore" 
    )
    
    # SQL Server Configuration
    SQL_SERVER_SERVER: str = Field(default="DESKTOP-E225SOT")
    SQL_SERVER_DATABASE: str = Field(default="SAV")
    SQL_SERVER_USERNAME: str = Field(default="sa")
    SQL_SERVER_PASSWORD: str = Field(default="2MPINDUSTRY@2025")
    SQL_SERVER_DRIVER: str = Field(default="ODBC Driver 17 for SQL Server")
    
    # Application Settings
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    DATABASE_URL: Optional[str] = Field(default=None)
    ALLOWED_ORIGINS: str = ""
    OPENAI_API_KEY: Optional[str] = Field(default="dummy_key_for_local_dev")
    
    # Logging Configuration
    LOG_LEVEL: str = Field(default="INFO")
    JSON_LOGS: bool = Field(default=False)
    LOG_SQL_QUERIES: bool = Field(default=False)
    
    @field_validator("ALLOWED_ORIGINS")
    @classmethod
    def parse_allowed_origins(cls, v: str) -> List[str]:
        return v.split(",") if v else []
    
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def validate_database_url(cls, v, info):
        if v is None:
            # Get values from the current context instead of creating new instance
            values = info.data
            return cls._generate_sql_server_url(values)
        return v
    
    @classmethod
    def _generate_sql_server_url(cls, values: dict) -> str:
        """Generate SQL Server connection URL from values"""
        server = values.get("SQL_SERVER_SERVER", "DESKTOP-E225SOT")
        database = values.get("SQL_SERVER_DATABASE", "SAV")
        username = values.get("SQL_SERVER_USERNAME", "sa")
        password = values.get("SQL_SERVER_PASSWORD", "2MPINDUSTRY@2025")
        driver = values.get("SQL_SERVER_DRIVER", "ODBC Driver 17 for SQL Server")
        
        encoded_password = urllib.parse.quote_plus(password)
        return (
            f"mssql+pyodbc://{username}:{encoded_password}@"
            f"{server}/{database}?"
            f"driver={urllib.parse.quote_plus(driver)}"
        )

# Create settings instance
try:
    settings = Settings()
    print("Settings loaded successfully")
except Exception as e:
    print(f"Error loading settings: {e}")
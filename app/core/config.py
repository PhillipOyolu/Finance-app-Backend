from pydantic_settings import BaseSettings, SettingsConfigDict

class ConfigurationError(Exception):
    """Raised when critical configuration fails validation."""
    pass

class Settings(BaseSettings):
    PROJECT_NAME: str = "Finance_API"
    DATABASE_URL: str = "sqlite:///./finance.db"
    SECRET_KEY: str 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def validate_security(self):
        if self.SECRET_KEY == "your-secret-key" or len(self.SECRET_KEY) < 16:
            raise ConfigurationError(
                "SECRET_KEY must be set in .env with a secure key (at least 16 characters)."
            )

settings = Settings()
#Run validation on startup
settings.validate_security()
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Finance_API"
    DATABASE_URL: str = "sqlite:///./finance.db"
    SECRET_KEY: str = Field(..., description="Cryptographic signing key for JWT tokens")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        # Enforce minimum 32 characters (256-bit entropy) for production HMAC security
        if v == "your-secret-key" or len(v.strip()) < 32:
            raise ValueError(
                "SECRET_KEY must be configured in .env and contain at least 32 characters for secure token signing."
            )
        return v.strip()


settings = Settings()
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "MonetLink Enterprise"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    DATABASE_URL: str
    REDIS_URL: str
    ALLOWED_DOMAINS: Union[str, List[str]]

    @field_validator("ALLOWED_DOMAINS", mode="before")
    def assemble_domain_array(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [domain.strip() for domain in v.split(",")]
        return v

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()

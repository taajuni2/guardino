from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    ENV: str = Field(default="dev", description="Environment name like dev/prod")

    # Database
    DB_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/guardino",
        description="Async SQLAlchemy/asyncpg URL"
    )

    # Kafka
    KAFKA_BOOTSTRAP: str = "localhost:9092"
    KAFKA_GROUP_ID: str = "agent-consumer"
    KAFKA_TOPIC_AGENT_EVENTS: str = "agent-events"
    KAFKA_TOPIC_AGENT_LIFECYCLE: str = "agent-lifecycle"
    KAFKA_SSL: bool = False  # kannst du später erweitern (SASL, TLS, etc.)


    ACCESS_TOKEN_EXPIRE_MINUTES: int =Field(default=60, description="Access token expiration minutes")
    JWT_SECRET: str = Field(default="CHANGE_ME_SUPER_SECRET")

    class Config:
        env_file = ".env"  # .env wird nur als fallback genutzt

settings = Settings()

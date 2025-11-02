from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    ENV: str = Field(default="dev", description="Environment name like dev/prod")

    # Database
    DB_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/appdb",
        description="Async SQLAlchemy/asyncpg URL"
    )

    # Kafka
    KAFKA_BOOTSTRAP: str = "localhost:9092"
    KAFKA_GROUP_ID: str = "agent-consumer"
    KAFKA_TOPIC_FILE_EVENTS: str = "file_events"
    KAFKA_SSL: bool = False  # kannst du später erweitern (SASL, TLS, etc.)

    class Config:
        env_file = ".env"  # .env wird nur als fallback genutzt

settings = Settings()

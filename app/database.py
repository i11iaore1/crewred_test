from typing import Annotated

from fastapi import Depends
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session, sessionmaker


class PostgresConfig(BaseSettings):
    db_name: str = Field(validation_alias="PSQL_DB")
    user: str = Field(validation_alias="PSQL_USER")
    password: SecretStr = Field(validation_alias="PSQL_PASSWORD")
    host: str = Field(validation_alias="PSQL_HOST")
    port: int = Field(validation_alias="PSQL_PORT")

    model_config = SettingsConfigDict(extra="ignore")

    def _get_DSN(self, driver: str) -> str:
        return URL.create(
            drivername=f"postgresql+{driver}",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.db_name,
        ).render_as_string(hide_password=False)

    @property
    def dsn(self):
        return self._get_DSN(driver="psycopg")


pg_config = PostgresConfig()

engine = create_engine(pg_config.dsn)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]

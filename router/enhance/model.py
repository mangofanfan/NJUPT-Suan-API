from typing import Optional

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel, create_engine

sqlite_file_name = "data/njupt_api.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})


class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    teacher: Optional[str] = Field(default=None, nullable=True)
    classroom: Optional[str] = Field(default=None, nullable=True)
    weeks: list[int] = Field(default=[], sa_column=Column(JSON))
    day: int
    classes: list[int] = Field(default=[], sa_column=Column(JSON))


class Alias(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    originalName: Optional[str] = Field(default=None, nullable=True)  # noqa: N815
    aliasName: Optional[str] = Field(default=None, nullable=True)  # noqa: N815


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

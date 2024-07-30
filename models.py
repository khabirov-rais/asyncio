import atexit
import datetime
import os
from sqlalchemy import String, DateTime, func, JSON
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Qwerty123")
POSTGRES_USER = os.getenv("POSTGRES_USER", "pg_user")
POSTGRES_DB = os.getenv("POSTGRES_DB", "pg_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5454")

PG_DSN = (f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:'
          f'{POSTGRES_PORT}/{POSTGRES_DB}')

engine = create_async_engine(PG_DSN)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)



class Base(DeclarativeBase, AsyncAttrs):
    pass


class SwapiPeople(Base):
    __tablename__ = "swapi_people"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_person: Mapped[int] = mapped_column(nullable=True)
    birth_year: Mapped[str] = mapped_column(String(10))
    eye_color: Mapped[str] = mapped_column(String(20))
    films: Mapped[str] = mapped_column(String)
    gender: Mapped[str] = mapped_column(String(20))
    hair_color: Mapped[str] = mapped_column(String(20))
    height: Mapped[str] = mapped_column(String(20))
    homeworld: Mapped[str] = mapped_column(String(250))
    mass: Mapped[str] = mapped_column(String(20))
    name: Mapped[str] = mapped_column(String(100))
    skin_color: Mapped[str] = mapped_column(String(20))
    species:Mapped[str] = mapped_column(String(250))
    starships:Mapped[str] = mapped_column(String(250))
    vehicles:Mapped[str]=mapped_column(String(250))
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

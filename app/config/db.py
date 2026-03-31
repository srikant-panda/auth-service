from curses import echo
from sqlalchemy import MetaData, false, future, true
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
from os import getenv

load_dotenv()

DATABASE_URL = str(getenv("DATABASE_URL"))
DEFAULT_SCHEMA_NAME = "DRIVE_S"
metadata = MetaData(schema=DEFAULT_SCHEMA_NAME)

class Base(DeclarativeBase):
    metadata = metadata

engine = create_async_engine(DATABASE_URL,echo=True,future = True)

AsyncSessionLocal = async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)

async def getDb():
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except Exception as e:
        print(str(e))
        raise
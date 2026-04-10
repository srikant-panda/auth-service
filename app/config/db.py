from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
from os import getenv

load_dotenv()
BASE_URL = str(getenv("BASE_URL"))
DATABASE_URL = str(getenv("DATABASE_URL"))
DEFAULT_SCHEMA_NAME = "auth"
metadata = MetaData(schema=DEFAULT_SCHEMA_NAME)

class Base(DeclarativeBase):
    metadata = metadata

engine = create_async_engine(DATABASE_URL,echo=False,future = True,connect_args = {"statement_cache_size":0})

AsyncSessionLocal = async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)

async def getDb():
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except Exception as e:
        print(str(e))
        raise

from contextlib import asynccontextmanager
from dotenv.main import logger
from fastapi import FastAPI,HTTPException
from app.config import Base, engine,DEFAULT_SCHEMA_NAME
from app.models import UserModel
from sqlalchemy import text
from app.USER import UserRouter

@asynccontextmanager
async def lifespan(app : FastAPI):
    print("Applocation started.")
    try:
        async with engine.begin() as conn:
            await conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{DEFAULT_SCHEMA_NAME}"')) 
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        logger.exception("Database Connection failed.")
        raise RuntimeError("Database Connection failed.") from e
    yield
    
    await engine.dispose()
    print("Application stopped.")
    
app = FastAPI(lifespan=lifespan)

routers = [UserRouter]
for i in routers:
    app.include_router(router=i,prefix='/api')
    

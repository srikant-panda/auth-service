from contextlib import asynccontextmanager
from dotenv.main import logger
from fastapi import FastAPI,HTTPException
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_200_OK
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
        # print("Database Connection failed",str(e))
    yield
    
    await engine.dispose()
    print("Application stopped.")
    
app = FastAPI(lifespan=lifespan)

routers = [UserRouter]
for i in routers:
    app.include_router(router=i,prefix='/api')
    
@app.get('/health',tags=['Health'],status_code=HTTP_200_OK)
async def health():
    return {
        'msg' : 'ok',
        "status" : "running"
    }
@app.get('/')
async def home():
    return RedirectResponse(url='/health')
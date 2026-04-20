from contextlib import asynccontextmanager
from os import getenv
from dotenv.main import logger
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
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
    yield
    
    await engine.dispose()
    print("Application stopped.")
    
app = FastAPI(lifespan=lifespan)

frontend_origins_env = getenv("FRONTEND_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
frontend_origins = [origin.strip() for origin in frontend_origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
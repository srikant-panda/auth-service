from unittest import result
from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED, HTTP_202_ACCEPTED
from .UserPydanticModel import *
from .UserService import *
from app.config import getDb,AsyncSession

UserRouter = APIRouter(prefix='/user',tags=['USER'])

@UserRouter.post('/signup',status_code=HTTP_201_CREATED)
async def signup(payload : UserSignUPINfo,db : AsyncSession = Depends(getDb)):
    return await addUser(payload,db=db)
@UserRouter.post('/signin',status_code=HTTP_202_ACCEPTED)
async def signin(payload : UserSignININfo,db:AsyncSession=Depends(getDb)):
    return await verifyUser(payload=payload,db=db)
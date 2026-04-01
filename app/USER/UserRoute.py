from fastapi import APIRouter, Request
from starlette.status import HTTP_201_CREATED, HTTP_202_ACCEPTED
from .UserPydanticModel import *
from fastapi.security import OAuth2PasswordBearer
from .UserService import *
from app.config import getDb,AsyncSession

UserRouter = APIRouter(prefix='/user',tags=['USER'])

@UserRouter.post('/signup',status_code=HTTP_201_CREATED)
async def signup(payload : UserSignUPINfo,db : AsyncSession = Depends(getDb)):
    return await addUser(payload,db=db)
@UserRouter.post('/signin',status_code=HTTP_202_ACCEPTED)
async def signin(payload : UserSignININfo,response : Response ,db:AsyncSession=Depends(getDb)):
    return await verifyUser(payload=payload,db=db,response=response)

@UserRouter.post('/refresh',status_code=HTTP_202_ACCEPTED)
async def refersh_tokens(request : Request , response : Response , db : AsyncSession = Depends(getDb)):
    refresh_token=request.cookies.get('refresh_token')
    # print(request.cookies)
    return await validateRefershToken(refresh_token=refresh_token,response=response,db = db)


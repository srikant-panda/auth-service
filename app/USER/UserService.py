from app.services import HashService, pwd_context,JwtService
from sqlalchemy import select
# from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR
from starlette.status import *
from app.models import UserModel
from app.config import getDb,AsyncSession
from .UserPydanticModel import *
from fastapi import Depends, HTTPException

async def addUser(payload:UserSignUPINfo , db: AsyncSession) -> UserOutInfo:

    is_exist = await db.execute(select(UserModel).where(UserModel.email == payload.email))
    if is_exist.scalar_one_or_none():
        raise HTTPException(detail="User with this email already exist. Please try another email.",status_code=HTTP_409_CONFLICT)
    hashed_password = HashService(pwd_context=pwd_context).hashPassword(payload.password)
    # user_model = User(name=payload.name,email=payload.email,password=payload.password)
    # f_data = UserModel(**User(name=payload.name,email=payload.email,password=payload.password).model_dump())
    f_data = UserModel(name=payload.name,email=payload.email,password=hashed_password)
    db.add(f_data)
    await db.commit()
    await db.refresh(f_data)
    return UserOutInfo (user=User.model_validate(f_data))
    
async def verifyUser(payload : UserSignININfo,db : AsyncSession) -> JwtOut:
    user_db_result = await db.execute(select(UserModel).where(UserModel.email == payload.email))
    user_model = user_db_result.scalar_one_or_none()
    if not user_model:
        raise HTTPException(detail='User not found. Check the email.',status_code=HTTP_404_NOT_FOUND)
    is_valid = HashService(pwd_context=pwd_context).verifyPassword(password=payload.password , hash_password=user_model.password)
    
    if not is_valid:
        raise HTTPException(
    detail="Invalid credentials",
    status_code=HTTP_401_UNAUTHORIZED
)
    AccessToken = JwtService().createAccessToken(id=str(user_model.id))
    # RefreshToken = JwtService().createRefereshToken(id=str(user_model.id))
    
    return JwtOut(token=AccessToken,msg='User signed in.')
from datetime import datetime,timezone
from app.services import HashService,JwtService
from sqlalchemy import select
from starlette.status import *
from app.models import RefreshTokenModel, UserModel
from app.config import getDb,AsyncSession
from .UserPydanticModel import *
from fastapi import Depends, HTTPException,Response
from app.dependency import Dependency

async def addUser(payload:UserSignUPINfo , db: AsyncSession) -> UserOutInfo:

    is_exist = await db.execute(select(UserModel).where(UserModel.email == payload.email))
    if is_exist.scalar_one_or_none():
        raise HTTPException(detail="User with this email already exist. Please try another email.",status_code=HTTP_409_CONFLICT)
    hashed_password = HashService().hash_data(payload.password)
    f_data = UserModel(name=payload.name,email=payload.email,password=hashed_password)
    db.add(f_data)
    await db.commit()
    await db.refresh(f_data)
    return UserOutInfo (user=User.model_validate(f_data))
    
async def verifyUser(payload : UserSignININfo,db : AsyncSession , response : Response) -> JwtOut:
    user_db_result = await db.execute(select(UserModel).where(UserModel.email == payload.email))
    user_model = user_db_result.scalar_one_or_none()
    if not user_model:
        raise HTTPException(detail='User not found. Check the email.',status_code=HTTP_404_NOT_FOUND)
    is_valid = HashService().verify_data(data=payload.password , hash_data=user_model.password)
    
    if not is_valid:
        raise HTTPException(
    detail="Invalid credentials",
    status_code=HTTP_401_UNAUTHORIZED
)
    AccessToken = JwtService().createAccessToken(id=str(user_model.id))
    RefreshToken = JwtService().createRefreshToken(id=str(user_model.id))
    refresh_token_data = Dependency(db=db)
    result = refresh_token_data.jwt_decode(RefreshToken)
    new_row = RefreshTokenModel(userId = user_model.id,refresh_token=RefreshToken,expire_at = datetime.now(timezone.utc)+timedelta(days=7),jti = result['jti'])
    db.add(new_row)
    await db.commit()
    await db.refresh(new_row)
    response.set_cookie(
        key='refresh_token',
        value=RefreshToken,
        httponly=True,
        samesite='lax',
        max_age=7
    )
    return JwtOut(access_token=AccessToken,msg='User signed in.')


async def validateRefershToken(refersh_token : str, response : Response, db : AsyncSession) -> JwtOut:
    hashed_token = HashService().hash_data(refersh_token)
        
    db_result = await db.execute(select(RefreshTokenModel).where(RefreshTokenModel.refresh_token == hashed_token))
    token_row = db_result.scalar_one_or_none()
    
    if not token_row:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if token_row.revoked:
        raise HTTPException(detail='Invalid Token.',status_code=401)
    
    if token_row.expire_at < datetime.now(timezone.utc):
        raise HTTPException(detail='Token Expired.',status_code=401)
    
    token_row.revoked = True
    
    new_access_token= JwtService().createAccessToken(token_row.userId)
    new_refresh_token = JwtService().createRefreshToken(token_row.userId)
    old_token_payload = Dependency(db=db).jwt_decode(refersh_token)
    hashed_new_token = HashService().hash_data(new_refresh_token)
    new_row = RefreshTokenModel(userId = token_row.userId,refresh_token=hashed_new_token,expire_at = datetime.now(timezone.utc)+timedelta(days=7),jti=old_token_payload['jti'])
    db.add(new_row)
    await db.commit()
    await db.refresh(new_row)
    response.set_cookie(
        key='refresh_token',
        value=new_refresh_token,
        httponly=True,
        samesite='lax',
        max_age=7
    )
    return JwtOut(
        access_token= new_access_token,
        msg='Token refreshed.'
    )
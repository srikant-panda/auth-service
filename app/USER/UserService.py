from datetime import datetime,timezone,timedelta
from app.services import HashService,JwtService
from sqlalchemy import select
from starlette.status import *
from app.models import RefreshTokenModel, UserModel
from app.config import AsyncSession
from .UserPydanticModel import *
from fastapi import Depends, HTTPException, Request,Response
from app.dependency import Dependency



async def addUser(payload:UserSignUPINfo , db: AsyncSession) -> UserOutInfo:

    is_exist = await db.execute(select(UserModel).where(UserModel.email == payload.email))
    if is_exist.scalar_one_or_none():
        raise HTTPException(detail="User with this email already exist. Please try another email.",status_code=HTTP_409_CONFLICT)
    hashed_password = HashService().hash_password(password=payload.password)
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
    is_valid = HashService().verify_password(password=payload.password , hash_password=user_model.password)
    
    if not is_valid:
        raise HTTPException(
    detail="Invalid credentials",
    status_code=HTTP_401_UNAUTHORIZED
)
    is_token_exist = await db.execute(select(RefreshTokenModel).where(RefreshTokenModel.user_id==user_model.id,RefreshTokenModel.revoked == True))
    all_revoked_token = is_token_exist.scalars().all()
    if all_revoked_token:
        for i in all_revoked_token:
            await db.delete(i)
    await db.commit()
        # await db.refresh(is_token_exist)
    AccessToken = JwtService().createAccessToken(id=str(user_model.id))
    RefreshToken = JwtService().createRefreshToken(**RefreshTokenCreateInfo(user_id=str(user_model.id)).model_dump())
    hashed_token = HashService().hash_token(token=RefreshToken)
    print(hashed_token)
    refresh_token_data = Dependency(db=db)
    token_op = await refresh_token_data.jwt_decode(RefreshToken)
    new_row = RefreshTokenModel(**RefreshTokenDbInfo(refresh_token=hashed_token,user_id=token_op['sub'],jti=token_op['jti'],expire_at=datetime.now(timezone.utc)+timedelta(days=7)).model_dump())
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
    print(RefreshToken)
    return JwtOut(access_token=AccessToken,msg='User signed in.')


async def validateRefershToken(refresh_token : str, response : Response, db : AsyncSession) -> JwtOut:
    # refresh_token :str = request.cookies.get('refresh_token')
    # print(refresh_token,"hellodfkjdbff")
    if not refresh_token:
        raise HTTPException(detail='No refresh token given',status_code=401)
    hashed_token = HashService().hash_token(refresh_token)
    print(hashed_token)
        
    db_result = await db.execute(select(RefreshTokenModel).where(RefreshTokenModel.refresh_token == hashed_token))
    token_row = db_result.scalar_one_or_none()
    
    if not token_row:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if token_row.revoked:
        raise HTTPException(detail='Invalid Token.',status_code=401)
    
    if token_row.expire_at < datetime.now(timezone.utc):
        raise HTTPException(detail='Token Expired.',status_code=401)
    
    token_row.revoked = True
    
    new_access_token= JwtService().createAccessToken(str(token_row.user_id))
    new_refresh_token = JwtService().createRefreshToken(**RefreshTokenCreateInfo(user_id=str(token_row.user_id)).model_dump())
    new_token_payload = await Dependency(db=db).jwt_decode(new_refresh_token)
    hashed_new_token = HashService().hash_token(new_refresh_token)
    new_row = RefreshTokenModel(**RefreshTokenDbInfo(user_id = new_token_payload['sub'],refresh_token=hashed_new_token,expire_at = datetime.now(timezone.utc)+timedelta(days=7),jti=new_token_payload['jti']).model_dump())
    db.add(new_row)
    await db.commit()
    await db.refresh(new_row)
    response.set_cookie(
        key='refresh_token',
        value=new_refresh_token,
        httponly=True,
        samesite='lax',
        max_age=7 * 24 * 60 * 60
    )
    return JwtOut(
        access_token= new_access_token,
        msg='Token refreshed.'
    )
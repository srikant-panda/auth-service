from datetime import datetime,timezone,timedelta
from app.services import HashService,JwtService,EmailService
from sqlalchemy import select, update
from starlette.status import *
from app.models import RefreshTokenModel, UserModel
from app.config import AsyncSession
from .UserPydanticModel import *
from fastapi import HTTPException, Request,Response
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
    email_sent = True
    try:
        await send_verification_email(
        user_email=f_data.email,
        user_id=str(f_data.id)
        )
    except Exception:
        email_sent = False
    return UserOutInfo (user=User.model_validate(f_data),email_sent=email_sent)
    
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
    if not user_model.is_varified:
        email_sent = True
        try:
            await send_verification_email(
            user_email=user_model.email,
            user_id=str(user_model.id)
            )
        except Exception as e:
            email_sent = False
            print(str(e))
        if email_sent:
            raise HTTPException(403, "Email not verified. Check your email.")
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
    # print(hashed_token)
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
        max_age=7 * 24 * 60 * 60
    )
    print(RefreshToken)
    return JwtOut(access_token=AccessToken,msg='User signed in.')


async def validateRefershToken(refresh_token : str, response : Response, db : AsyncSession) -> JwtOut:
    if not refresh_token:
        raise HTTPException(detail='No refresh token given',status_code=401)
    hashed_token = HashService().hash_token(refresh_token)
        
    db_result = await db.execute(select(RefreshTokenModel).where(RefreshTokenModel.refresh_token == hashed_token))
    token_row = db_result.scalar_one_or_none()
    
    if not token_row:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if token_row.revoked:
        raise HTTPException(detail='Invalid Token.',status_code=401)
    
    if token_row.expire_at < datetime.now(timezone.utc):
        raise HTTPException(detail='Token Expired.',status_code=401)
    

    await db.execute(update(RefreshTokenModel).where(RefreshTokenModel.refresh_token==hashed_token).values(revoked=True))
    await db.commit()
    
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
    
async def signout(refresh_token : str , db:AsyncSession,response : Response) -> Base:
    if not refresh_token:
        raise HTTPException(detail='No refresh token given',status_code=401)
    refersh_token_data = JwtService().decode(refresh_token)
    current_user = refersh_token_data.get('sub')
    hashed_token = HashService().hash_token(refresh_token)
    db_result= await db.execute(select(RefreshTokenModel).where(RefreshTokenModel.refresh_token == hashed_token,RefreshTokenModel.user_id==current_user))
    token_row = db_result.scalar_one_or_none()
    if token_row:
        await db.delete(token_row)
        await db.commit()
        response.delete_cookie(
            key="refresh_token",
            httponly=True,
            samesite="lax"
    )
        return Base(
            msg="User Loged Out"
        )
async def verifyEmail(token :str, db:AsyncSession) -> Base:
    # if token is None:
    #     raise HTTPException(detail="Token Not Recived.",status_code=HTTP_400_BAD_REQUEST)
    try:
        result=JwtService().decode(token)
    except Exception as e:
        print(str(e))
        raise HTTPException(400, "Invalid token or expired")
    # if result.get('exp') < datetime.now(timezone.utc).timestamp():
    #     raise HTTPException(400, "Token expired")
    user_id = result.get("sub")
    if not user_id:
        raise HTTPException(400, "Invalid token")
    
    user = await db.get(UserModel,user_id)
    if not user:
        raise HTTPException(404, "User not found")

    if user.is_varified:
        return Base(msg="Already varified.")

    user.is_varified = True
    await db.commit()
    if user.is_varified:
        return Base(msg='Email verify successfully.')
    

async def send_verification_email(user_email: str, user_id: str):

    if not user_email:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="No user email given"
        )

    token = JwtService().createVerificationToken(user_id)

    BASE_URL = "http://localhost:8000"
    link = f"{BASE_URL}/api/user/verify-email?token={token}"

    try:
        await EmailService().send_email(
            to_email=user_email,
            subject="Verify your email address",
            body=f"""Welcome!

Please verify your email by clicking the link below:

{link}

If you did not sign up, ignore this email.
"""
        )
    except Exception as e:
        print(str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to send verification email"
        )

    return {"msg": "Verification email sent"}
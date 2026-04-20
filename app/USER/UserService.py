from datetime import datetime,timezone,timedelta
from app.services import HashService,JwtService,EmailService,OTPService
from sqlalchemy import select, update
from starlette.status import *
from app.models import RefreshTokenModel, UserModel,OtpModel
from app.config import AsyncSession,BASE_URL
from .UserPydanticModel import *
from fastapi import HTTPException,Response
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
        email_sent = False
        try:
            await send_verification_email(
            user_email=user_model.email,
            user_id=str(user_model.id)
            )
            email_sent = True
        except Exception as e:
            print(str(e))
    if not user_model.is_varified:
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
    
async def signout(refresh_token : str , db:AsyncSession,response : Response) -> Base|None:
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
async def verifyEmail(token :str, db:AsyncSession) -> Base|None:
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


async def resetPassword(data : ResetPasswordInfo, db: AsyncSession) -> Base|None:
    otp_result= await db.execute(select(OtpModel).where(OtpModel.email==data.email,OtpModel.is_varified==True))
    otp_varification_return = otp_result.scalar_one_or_none()
    print(otp_varification_return)

    if otp_varification_return:
        # if not otp_varification_return.is_varified:
        #     raise HTTPException(detail='USER not verified for passeord reset.',status_code=HTTP_400_BAD_REQUEST)
        db_result= await db.execute(select(UserModel).where(UserModel.email==data.email))
        db_data=db_result.scalar_one_or_none()
        if not db_data:
            raise HTTPException(detail='User not found. Check the email.',status_code=HTTP_404_NOT_FOUND)
        is_valid = HashService().verify_password(password=data.old_password , hash_password=db_data.password)

        if not is_valid:
            raise HTTPException(
        detail="Invalid credentials",
        status_code=HTTP_401_UNAUTHORIZED
        )
        hashed_password = HashService().hash_password(password=data.password)
        db_data.password = hashed_password
        await db.commit()
        return Base(msg='Password reset successfully.')
    raise HTTPException(detail='USER not verified for passeord reset.',status_code=HTTP_400_BAD_REQUEST)


async def forget_password(email:EmailStr,db:AsyncSession) :
    db_result = await db.execute(select(UserModel).where(UserModel.email ==email))
    result = db_result.scalar_one_or_none()
    if not result:
        raise HTTPException(detail='User with this Email Does Not exist.',status_code=HTTP_404_NOT_FOUND)
    otp = OTPService().generate_otp()
    hash_otp = HashService().hash_password(str(otp))
    while True:
        is_sent = await send_otp_email(user_email=email,otp=otp)
        if is_sent:
            expire_at = datetime.now()+timedelta(seconds=30)
            otp_row = OtpModel(expire_at=expire_at,**OtpInfoModel(email=email,otp=hash_otp).model_dump())
            db.add(otp_row)
            await db.commit()
            return Base(msg='Otp sent')
async def verify_otp(data:OtpInfoModel,db:AsyncSession)->Base|None:
    db_result= await db.execute(select(OtpModel).where(OtpModel.email==data.email))
    Scaler_result = db_result.scalars().all()
    if not Scaler_result:
        raise HTTPException(detail='Email Not Found.',status_code=HTTP_404_NOT_FOUND)
    
    result = None
    for i in Scaler_result:
        verify_result = HashService().verify_password(data.otp,i.otp)
        if verify_result:
            if i.expire_at < datetime.now(timezone.utc):
                raise HTTPException(detail='OTP EXPIRED.',status_code=HTTP_404_NOT_FOUND)
            result = i
            break
    if result is None:
        raise HTTPException(detail='Otp not matched.',status_code=HTTP_400_BAD_REQUEST)
    if result.is_varified:
        raise HTTPException(detail='OTP already verified..',status_code=HTTP_404_NOT_FOUND)
    result.is_varified=True
    db.add(result)
    await db.commit()
    return Base(msg="OTP verified.")


async def send_otp_email(user_email:str,otp:int):
    if not user_email:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="No user email given"
        )

    try:
        await EmailService().send_email(
            to_email=user_email,
            subject="password reset request verification otp",
            body=f"""Welcome!

Your verification otp is bellow given:

{otp}

If you did not sign up, ignore this email.
"""
        )
    except Exception as e:
        print(str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to send otp."
        )

    return {"msg": "OTP sent"}
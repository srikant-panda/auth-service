from app.models.user_model import AuthToken
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
    hashed_password = HashService().hash_data(payload.password)
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
    is_valid = HashService().verify_data(password=payload.password , hash_password=user_model.password)
    
    if not is_valid:
        raise HTTPException(
    detail="Invalid credentials",
    status_code=HTTP_401_UNAUTHORIZED
)
    AccessToken = JwtService().createAccessToken(id=str(user_model.id))
    RefreshToken = JwtService().createRefereshToken(id=str(user_model.id))
    hashed_refresh_token = HashService().hash_data(RefreshToken)
    
    return JwtOut(token=AccessToken,refresh_token=hashed_refresh_token,msg='User signed in.')


class AuthService:

    def __init__(self, db: AsyncSession, jwt_service: JwtService):
        self.db = db
        self.jwt_service = jwt_service

    async def refresh(self, refresh_token: str):
        hashed = HashService().hashPassword(refresh_token)

        result = await self.db.execute(
            select(AuthToken).where(
                AuthToken.token == hashed
            )
        )
        token_row = result.scalar_one_or_none()

        # ❌ invalid token
        if not token_row:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # ❌ revoked
        if token_row.revoked:
            raise HTTPException(status_code=401, detail="Token revoked")

        # ❌ expired
        if token_row.expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Token expired")

        # 🔥 ROTATION (important)
        token_row.revoked = True

        # create new tokens
        new_access = self.jwt_service.create_access_token(str(token_row.user_id))
        new_refresh = generate_refresh_token()

        new_row = RefreshTokenModel(
            user_id=token_row.user_id,
            token_hash=hash_token(new_refresh),
            expires_at=datetime.now(timezone.utc) + timedelta(days=7)
        )

        self.db.add(new_row)
        await self.db.commit()

        return {
            "access_token": new_access,
            "refresh_token": new_refresh
        }
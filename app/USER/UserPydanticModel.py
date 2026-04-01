from datetime import datetime, timedelta, timezone
from pydantic import BaseModel,ConfigDict,Field
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr
from uuid import UUID,uuid4

OauthSchema = OAuth2PasswordBearer(tokenUrl='/api/user/')


class Base(BaseModel):
    msg : str
    error : str|None = None

class User(BaseModel):
    id : UUID = Field(default_factory=uuid4)
    name : str
    email : EmailStr
    password : str
    role : str = "user"
    model_config = ConfigDict(extra='forbid',from_attributes=True)


class UserSignUPINfo(BaseModel):
    name : str
    email : EmailStr
    password : str

class UserOutInfo(BaseModel):
    user : User

class UserSignININfo(BaseModel):
    email : EmailStr
    password : str
    model_config = ConfigDict(extra="forbid")
    
class JwtOut(Base):
    access_token : str

class RefreshTokenCreateInfo(BaseModel):
    user_id : str
    jti : UUID = Field(default_factory=uuid4)

class RefreshTokenDbInfo(BaseModel):
    refresh_token : str
    user_id : UUID
    jti : UUID
    expire_at : datetime
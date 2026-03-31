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
    # username:str
    email : EmailStr
    password : str
    refressToken : str = None
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
    
class JwtOut(Base):
    access_token : str
# class CreateRefreshToken(BaseModel):
#     user_id : UUID
#     refresh_token : str
#     expire_at : datetime = Field(default_factory=datetime(timezone.utc)+timedelta(days=7))
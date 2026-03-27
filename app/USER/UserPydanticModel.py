from pydantic import BaseModel,ConfigDict,Field
from pydantic import EmailStr
from uuid import UUID,uuid4

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
    refresh_token :str
from uuid import UUID
from jose import JWTError,jwt
from datetime import datetime,timedelta,timezone
from typing import Any,Dict
from os import getenv


class JwtService:
    SECRET = getenv("SECRET")
    ALGORITHM = getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    REFRESH_TOKEN_EXPIRE_DAYS = int(getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
    VERIFICATION_TOKEN_EXPIRE_MINUTES= 5
    if not SECRET:
        raise RuntimeError("SECRET environment variable is required")
    
    def createAccessToken(self,id :str) -> str:
        data : dict = {"sub" : id,"type":"access"}
        
        expire = datetime.now(timezone.utc)+timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES) 
        
        data.update({"exp":expire.timestamp()})
        
        return jwt.encode(data,self.SECRET,self.ALGORITHM)
    def createRefreshToken(self,user_id :str,jti:UUID) -> str:
        data : dict = {"sub" : user_id,"type":"refresh","jti" : str(jti)}
        
        expire = datetime.now(timezone.utc)+timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS) 
        
        data.update({"exp":expire.timestamp()})
        
        return jwt.encode(data,self.SECRET,self.ALGORITHM)
    def createVerificationToken(self , id:str)->str:
        data:dict = {"sub":id,"type":'verification'}
        expire = datetime.now(timezone.utc)+timedelta(minutes=self.VERIFICATION_TOKEN_EXPIRE_MINUTES)
        data.update({"exp":expire})
        return jwt.encode(data,self.SECRET,self.ALGORITHM)
    
    def decode(self,token : str) -> Dict[str,Any] :
        try:
            return jwt.decode(token,self.SECRET,algorithms=[self.ALGORITHM])
        except JWTError as e:
            raise ValueError(f"Invalid JWT: {str(e)}")
from jose import JWTError,jwt
from datetime import datetime,timedelta,timezone
from typing import Any,Dict
from os import getenv


class JwtService:
    SECRET = getenv("SECRET","090878yhad788ayd8ds69yagdyudt7687s")
    ALGORITHM = getenv("ALGORITHM","HS256")
    EXPIRY_TIME_IN_MINUTES = int(getenv("EXPIRY_TIME","15"))
    EXPIRY_TIME_IN_DAYS = int(getenv("EXPIRY_TIME","7"))
    if not SECRET:
        raise RuntimeError("SECRET environment variable is required")
    
    def createAccessToken(self,id :str) -> str:
        data : dict = {"sub" : id}
        
        expire = datetime.now(timezone.utc)+timedelta(minutes=JwtService.EXPIRY_TIME_IN_MINUTES) 
        
        data.update({"exp":expire.timestamp()})
        
        return jwt.encode(data,JwtService.SECRET,JwtService.ALGORITHM)
    
    def createRefereshToken(self,id :str) -> str:
        data : dict = {"sub" : id}
        
        expire = datetime.now(timezone.utc)+timedelta(minutes=JwtService.EXPIRY_TIME_IN_DAYS) 
        
        data.update({"exp":expire.timestamp()})
        
        return jwt.encode(data,JwtService.SECRET,JwtService.ALGORITHM)
    
    def decode(self,token : str) -> Dict[str,Any] :
        try:
            return jwt.decode(token,JwtService.SECRET,algorithms=[JwtService.ALGORITHM])
        except JWTError as e:
            raise ValueError(f"Invalid JWT: {str(e)}")
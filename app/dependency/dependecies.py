from typing import Any,Dict
from sqlalchemy import select
from fastapi import HTTPException
from app.config import AsyncSession
from app.models import UserModel
from app.services import JwtService,HashService


class Dependency:
    
    def __init__(self,db:AsyncSession = None) -> None:
        self.db = db
    async def jwt_decode(self,token : str) -> Dict[str,Any]|str:
        data = JwtService().decode(token)
        
        if data is None:
            raise HTTPException(detail='Invalid Token.',status_code=401)
        if data['type'] == 'refresh':
            return data
        
        result = data.get('sub')
        
        if result is None:
            raise HTTPException(detail='Invalid Token data.',status_code=401)
        
        db_result = await self.db.execute(select(UserModel).where(UserModel.id == result.get('sub')))
        
        if db_result.scalar_one_or_none() is None:
            raise HTTPException('user not found',status_code=401)
        return data.get('id') 

    async def otp_verify(self,otp:str,db_otp:str) -> bool:
        result = HashService().verify_password(otp,db_otp)
        return result

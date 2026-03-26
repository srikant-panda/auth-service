from enum import auto
from warnings import deprecated
from passlib.context import CryptContext
from dotenv import load_dotenv
from os import getenv
load_dotenv()
class HashService:
    SECRET_KEY = str(getenv("SECRET_KEY"))
    
    def __init__(self, pwd_context : CryptContext) -> str:
        self.pwd_cotext = pwd_context
        
    def hashPassword(self,password : str) -> str:
        password_concat = password + self.SECRET_KEY
        
        return self.pwd_cotext.hash(password_concat)
    
    def verifyPassword(self, password : str , hash_password : str) -> bool:
        password_concat = password + self.SECRET_KEY
        return self.pwd_cotext.verify(password_concat,hash_password)
  
pwd_context = CryptContext(schemes=['argon2'],deprecated='auto')
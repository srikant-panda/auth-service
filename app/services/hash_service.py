from passlib.context import CryptContext
from dotenv import load_dotenv
from os import getenv
import hashlib
load_dotenv()
class HashService:
    SECRET_KEY = str(getenv("SECRET_KEY"))
    pwd_context = CryptContext(schemes=['argon2'],deprecated='auto')
    @classmethod   
    def hash_password(cls,password) -> str:
        return cls.pwd_context.hash(password)
    @classmethod
    def verify_password(cls,password: str,hash_password:str) -> bool:
        return cls.pwd_context.verify(password,hash_password)
    
    @staticmethod
    def hash_token(token : str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()
if __name__ == '__main__':
    # print(HashService().verifyPassword("Hello",'$argon2id$v=19$m=65536,t=3,p=4$NQbAmFOqtXbOeW8NgRBCCA$4aNs682SenJ0F2mbKeOIfic+Fzm13mgqrpdfxDhwzD8'))
    print(HashService().hash_token(''))
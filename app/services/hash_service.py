from passlib.context import CryptContext
from dotenv import load_dotenv
from os import getenv
load_dotenv()
class HashService:
    SECRET_KEY = str(getenv("SECRET_KEY"))
    pwd_context = CryptContext(schemes=['argon2'],deprecated='auto')
    @classmethod   
    def hash_data(cls,data) -> str:
        return cls.pwd_context.hash(data)
    @classmethod
    def verify_data(cls,data: str,hash_data:str) -> bool:
        return cls.pwd_context.verify(data,hash_data)
  
if __name__ == '__main__':
    print(HashService().verifyPassword("Hello",'$argon2id$v=19$m=65536,t=3,p=4$NQbAmFOqtXbOeW8NgRBCCA$4aNs682SenJ0F2mbKeOIfic+Fzm13mgqrpdfxDhwzD8'))
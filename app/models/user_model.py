from datetime import datetime,timezone
from email.policy import default
from uuid import uuid4
from sqlalchemy import Column,String,Uuid,func,DateTime
from sqlalchemy.orm import Mapped,mapped_column
from app.config import Base,DEFAULT_SCHEMA_NAME

class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = {"schema":DEFAULT_SCHEMA_NAME}
    id : Mapped[Uuid]= mapped_column(Uuid,default=uuid4,primary_key=True,index=True)
    name : Mapped[str] = mapped_column(String(200),nullable=False)
    email : Mapped[str] = mapped_column(String(200),nullable=False,index=True,unique=True)
    # username : Mapped[str] = mapped_column(String(200),nullable=False,unique=True,index=True)
    password : Mapped[str] = mapped_column(String(200),nullable=False)
    refreshToken : Mapped[str] = mapped_column(String(200),nullable=True)
    role: Mapped[str] = mapped_column(String(20),default="user",nullable=False,index=True)
    createdAt : Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    updatedAt : Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
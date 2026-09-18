import os
from datetime import datetime,timedelta,timezone
from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from jose import jwt,JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .database import get_db
from .models import User

SECRET=os.getenv("JWT_SECRET","change-this-secret")
pwd=CryptContext(schemes=["bcrypt"],deprecated="auto")
bearer=HTTPBearer(auto_error=False)

def hash_password(v): return pwd.hash(v)
def verify_password(v,h): return pwd.verify(v,h)
def create_token(uid):
    return jwt.encode({"sub":str(uid),"exp":datetime.now(timezone.utc)+timedelta(hours=24)},SECRET,algorithm="HS256")
def current_user(credentials:HTTPAuthorizationCredentials=Depends(bearer),db:Session=Depends(get_db)):
    if not credentials: raise HTTPException(status_code=401,detail="Authentication required")
    try: uid=int(jwt.decode(credentials.credentials,SECRET,algorithms=["HS256"])["sub"])
    except (JWTError,KeyError,ValueError): raise HTTPException(status_code=401,detail="Invalid token")
    user=db.get(User,uid)
    if not user: raise HTTPException(status_code=401,detail="User not found")
    return user

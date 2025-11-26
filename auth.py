from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
import os

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Simple local users
fake_users = {"userName": "admin",
              "password":"12345678"
              }

def create_access_token(user,pas):
        token_data = {"sub": user}
        token= jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        return token
    

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")
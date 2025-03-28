from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.config import Settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.models import User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password): 
    return pwd_context.hash(password)
# Эта функция хеширует пароль с использованием алгоритма bcrypt.
# pwd_context.hash(password) возвращает хешированный пароль, который можно хранить в базе данных.

def create_access_token(data: dict): 
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail='Could not validate',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try: 
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        email: str = payload.get('sub')
        if email is None: 
            raise credentials_exception
        user = await User.filter(email=email).first()
        if user is None: 
            raise credentials_exception
    except jwt.JWTError: 
        raise credentials_exception
    return user
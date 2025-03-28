from fastapi import APIRouter, Depends, HTTPException, status
from app.models import User
from app.schemas.user import Token, UserCreate, UserOut
from app.services import verify_password, get_password_hash, create_access_token
from app.config import Settings
from tortoise.exceptions import DoesNotExist
from fastapi.security import OAuth2PasswordBearer

from app.services.auth import get_current_user


router = APIRouter()

@router.post('/register')
async def register(user: UserCreate):
    existing_user = await User.filter(email=user.email).first()
    if existing_user: 
        raise HTTPException(status_code=400, detail='Email is already registered!')
    
    hashed_password = get_password_hash(user.password)

    new_user = await User.create(
        email = user.email,
        hashed_password = hashed_password
    )
    return new_user

@router.post('/login', response_model=Token)
async def login(user: UserCreate):
    db_user = await User.filter(email = user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail='Invalid cred')
    access_token = create_access_token(data={'sub': db_user.email})

    return { 'access_token': access_token, 'token_type': 'bearer'}

@router.get('/users/me', response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
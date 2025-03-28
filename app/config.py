import os
from dotenv import load_dotenv

load_dotenv()

class Settings: 
    PROJECT_NAME: str = os.getenv('PROJECT_NAME')
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'mysecretkey')
    ALGORITHM: str = os.getenv('ALGORITHM') 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30))
    DATABASE_URL: str = os.getenv("DATABASE_URL")
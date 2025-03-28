from tortoise.models import Model
from tortoise import fields
from passlib.hash import bcrypt

class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    hashed_password = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

def verify_password(self, password: str):
    return bcrypt.verify(password, self.hashed_password)

def set_password(self, password: str): 
    self.hashed_password = bcrypt.hash(password)
from fastapi import HTTPException,  status 
from datetime import datetime, timedelta
import jwt
from app.common.const import JWT_SECRET, JWT_ALGORITHM
from app.errors.exceptions import token_decode_ex,token_expired_ex

def create_token(data: dict = None, expires_delta: int = None):
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": datetime.utcnow() + timedelta(hours=expires_delta)})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def decode_token(token):
    try:
        token =token.replace('Bearer ','')
        payload = jwt.decode(token,key=JWT_SECRET,algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise token_expired_ex()
    except jwt.DecodeError:
        raise token_decode_ex()
    return payload
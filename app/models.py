from enum import Enum
from pydantic import BaseModel
from typing import List

# Enum----------------------------------------------------------------

class CupsSataeType(str,Enum):
    available : str = 'available'
    using :str = 'using'
    returned : str ='returned'
    cleanse : str = 'cleanse'
    loss : str ='loss'


class UsersSataeType(str,Enum):
    active : str = 'active'
    deleted :str = 'deleted'
    blocked : str ='blocked'
   

# Model----------------------------------------------------------------

class SignUpModel(BaseModel):
    username :str
    email : str
    password : str

class SignInModel(BaseModel):
    email : str
    password : str

class DisplayUserModel(BaseModel):
    username :str
    email : str 
    class Config():
        orm_mode = True


class AccessToken(BaseModel):
    accessToken: str 
    class Config():
        orm_mode = True

class RefreshToken(BaseModel):
    refreshToken: str 
    class Config():
        orm_mode = True

class Tokens(BaseModel):
    accessToken: str 
    refreshToken: str 

class UserToken(BaseModel):
    id: int
    username :str
    email : str 
    class Config():
        orm_mode = True


class CupsInfo(BaseModel):
    id : int
    status : CupsSataeType
    usedCount :int
    user : DisplayUserModel
    class Config():
        orm_mode = True

class CupId(BaseModel):
    goodAttitudeCup_Uid : int

class CupIdAndUserId(BaseModel):
    goodAttitudeCup_Uid : int
    userUid : int

class Cup(BaseModel):
    id : int
    status : CupsSataeType
    usedCount :int
    class Config():
        orm_mode = True


class UserMeModel(BaseModel):
    username :str
    email : str 
    status : UsersSataeType
    items : List[Cup] = []
    class Config():
        orm_mode = True
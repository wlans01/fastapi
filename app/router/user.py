from typing import List
from fastapi import APIRouter, Depends
from app.models import  DisplayUserModel, UserMeModel, UserToken
from starlette.requests import Request
from app.db.schema import Users 
from app.db.conn import db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/api/user',
    tags=['user']
)


# 모든 유저정보 가져오기
@router.get('/all',response_model=List[UserToken])
async def get_all_user(session:Session = Depends(db.session)):
    ''''''
    users = session.query(Users).all()
    return users
    


# 내정보
@router.get('/me',response_model=UserMeModel)
async def get_me_user(request:Request,session: Session = Depends(db.session)):
    ''''''
    user = request.state.user
    user_me = session.query(Users).filter(Users.id == user.id).first()
    return user_me

from app.errors.exceptions import already_exists ,token_expired_ex ,iogin_fail
from app.models import SignInModel, SignUpModel, UserMeModel,UserToken,AccessToken,RefreshToken
from sqlalchemy.orm import Session
from fastapi import APIRouter , Depends
from app.db.schema import Users
from app.db.conn import db
from app.db.hash import Hash
from app.auth import token as Token
from app.utils.time_format import TimeFormat
router = APIRouter(
    prefix='/api/auth',
    tags=['auth']
)

# Create User
@router.post('/signup',response_model=UserMeModel)
async def signup(request : SignUpModel, session: Session = Depends(db.session)):
    user = session.query(Users).filter(Users.email == request.email).first()
    if user:
        raise already_exists()
    new_user = Users(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password)
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.post('/signin',response_model=RefreshToken)
async def signin(request : SignInModel,session: Session = Depends(db.session)):
    ''''''
    user = session.query(Users).filter(Users.email == request.email)
    if not user.first():
        raise iogin_fail()
    if not Hash.verify(user.first().password,request.password):
        raise iogin_fail()
    token = dict(refreshToken= Token.create_token(data={"hellow":"world"}, expires_delta=10))
    user.update({
        Users.refreshToken :token['refreshToken']
    })
    session.commit()
    return token

@router.post('/refresh', response_model=AccessToken)
async def refresh_access_token(request : RefreshToken,session: Session = Depends(db.session)):
    ''''''
    Token.decode_token(request.refreshToken)
    refreshToken=request.refreshToken.replace('Bearer ','')
    print(refreshToken)
    user = session.query(Users).filter(Users.refreshToken == refreshToken).first()
    if not user:
        raise token_expired_ex()
    accesstoken = dict(
            accessToken=Token.create_token(data=UserToken.from_orm(user).dict()),expires_delta=5)   
    return accesstoken





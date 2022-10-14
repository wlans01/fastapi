from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.conn import db
from app.db.schema import Cups, Users
from app.errors.exceptions import blocked_user, cup_fail, not_found_user_ex, rent_fail
from app.models import CupId, CupIdAndUserId, CupsInfo, CupsSataeType, UsersSataeType
from app.utils.time_format import TimeFormat
router = APIRouter(
    prefix='/api/cup',
    tags=['cup']
)

@router.post('/',response_model=CupsInfo)
async def create_cup(session: Session = Depends(db.session)):
    ''''''
    new_cup = Cups( user_id = 1)
    session.add(new_cup)
    session.commit()
    session.refresh(new_cup)
    return new_cup


# 컵 상태 체크 대여상태면 반납
@router.patch('/state',response_model=CupsInfo)
async def cup_state_cheack(request: CupId,session: Session = Depends(db.session)):
    ''''''
    cup = session.query(Cups).filter(Cups.id == request.goodAttitudeCup_Uid)
    if not cup.first():
        raise cup_fail()
    cup_state =cup.first().status

    # 대여가능이면 available 반환 
    if cup_state == CupsSataeType.available:
        return cup.first()

    # 로스컵이라면 변환후 returned반환
    if cup_state == CupsSataeType.loss:
        cup.update({
            Cups.user_id : 1,
            Cups.updated_at : TimeFormat.ktc_datetime(),
            Cups.status : CupsSataeType.returned
        })   
        session.commit()
        return cup.first()

    # 대여중 컵이라면 변환후 returned 반환
    if cup_state == CupsSataeType.using:
        cup.update({
            Cups.user_id : 1,
            Cups.updated_at : TimeFormat.ktc_datetime(),
            Cups.status : CupsSataeType.returned
        }) 
        session.commit()
        return cup.first()
        
    # 컵 인식 실패
    raise cup_fail()

#컵 대여
@router.post('/rent')
async def cup_rent(request:CupIdAndUserId,session: Session = Depends(db.session)):
    ''''''
    cup = session.query(Cups).filter(Cups.id == request.goodAttitudeCup_Uid)
    user = session.query(Users).filter(Users.id == request.userUid)

    #  db 일치하지 않는 컵이면 대여불가
    if not cup.first():
        raise cup_fail()

    # 컵의 상태가 available이 아니면 대여불가
    if cup.first().status != CupsSataeType.available:
        raise rent_fail()

    #  db 일치하지 않는 유저면 대여불가
    if not user.first():
        raise not_found_user_ex(user_id=request.userUid)

    # 블락계정이면 대여불가
    if user.first().status == UsersSataeType.blocked:
        raise blocked_user()

    # 컵상태 업데이트
    update_cup = cup.update({
        Cups.usedCount :cup.first().usedCount +1,
        Cups.user_id : request.userUid,
        Cups.updated_at : TimeFormat.ktc_datetime(),
        Cups.status : CupsSataeType.using
    })
    # 유저 상태 업데이트
    if len(user.first().items) >=2:
        user.update({Users.status : UsersSataeType.blocked})
    
    session.commit()
    return cup.first()

# 로스처리
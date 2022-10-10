from fastapi import HTTPException, status

def api_exception(ex: Exception = None):
    return HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail={
        "msg":f"서버에 문제가 생겼습니다.",
        "detail":"server error",
        "code":f"{status.HTTP_500_INTERNAL_SERVER_ERROR}{'1'.zfill(4)}",
        'ex':str(ex),
    })

def token_expired_ex(ex: Exception = None): 
   return HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "msg":f"세션이 만료되어 로그아웃 되었습니다.",
        "detail":"Token Expired",
        "code":f"{status.HTTP_400_BAD_REQUEST}{'1'.zfill(4)}",
        'ex':str(ex),
    })
    
def token_decode_ex(ex: Exception = None): 
   return HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "msg":f"비정상적인 접근입니다.",
        "detail":"Token has been compromised.",
        "code":f"{status.HTTP_400_BAD_REQUEST}{'2'.zfill(4)}",
        'ex':str(ex),
    })

def not_authorized(ex: Exception = None): 
   return HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail={
        "msg":f"로그인이 필요한 서비스 입니다.",
        "detail":"Authorization Required.",
        "code":f"{status.HTTP_401_UNAUTHORIZED}{'1'.zfill(4)}",
        'ex':str(ex),
    })

def not_found_user_ex(user_id:int,ex: Exception = None): 
   return HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail={
        "msg":f"해당 유저를 찾을 수 없습니다.",
        "detail":"Not Found User ID : {user_id}",
        "code":f"{status.HTTP_404_NOT_FOUND}{'1'.zfill(4)}",
        'ex':str(ex),
    })

def already_exists(ex: Exception = None): 
   return HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail={
        "msg":f"이미 존재하는 유저입니다.",
        "detail":"Already Exists User.",
        "code":f"{status.HTTP_404_NOT_FOUND}{'2'.zfill(4)}",
        'ex':str(ex),
    })

def iogin_fail(ex: Exception = None):
    return HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail={
        "msg":f"로그인 정보가 일지하지 않습니다.",
        "detail":"Invalid Info.",
        "code":f"{status.HTTP_404_NOT_FOUND}{'2'.zfill(4)}",
        'ex':str(ex),
    })

def cup_fail(ex: Exception = None):
    return HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail={
        "msg":f"해당 컵을 찾을 수 없습니다",
        "detail":"Cup Invalid Info.",
        "code":f"{status.HTTP_404_NOT_FOUND}{'3'.zfill(4)}",
        'ex':str(ex),
    })

def rent_fail(ex: Exception = None):
    return HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail={
        "msg":f"대여가 불가능한 컵입니다.",
        "detail":"Can not rent",
        "code":f"{status.HTTP_404_NOT_FOUND}{'4'.zfill(4)}",
        'ex':str(ex),
    })

def blocked_user(ex: Exception = None):
    return HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail={
        "msg":f"대여가 불가능한 유저입니다입니다.",
        "detail":"Blocked User",
        "code":f"{status.HTTP_404_NOT_FOUND}{'5'.zfill(4)}",
        'ex':str(ex),
    })
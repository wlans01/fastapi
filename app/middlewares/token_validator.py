from starlette.requests import Request
from app.common.const import EXCEPT_PATH_LIST,EXCEPT_PATH_REGEX
import re
from app.auth import token as Token
from app.errors.exceptions import not_authorized , api_exception
from app.models import UserToken
from starlette.responses import JSONResponse
import sqlalchemy.exc

async def access_control(request: Request,call_next):
    ''''''
    request.state.inspect = None
    request.state.user = None
    request.state.is_admin_access = None

    ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
    headers = request.headers
    cookies = request.cookies
    url = request.url.path
    try:
        if await url_pattern_check(url, EXCEPT_PATH_REGEX) or url in EXCEPT_PATH_LIST:
            response = await call_next(request)
            # if url != "/":
            #     await api_logger(request=request, response=response)
            return response

    
        if 'authorization' in headers.keys():
            token =headers.get("authorization")
            try:
                token_info = Token.decode_token(token)
                request.state.user = UserToken(**token_info)
            except Exception as e:
                error = not_authorized()
                response = JSONResponse(status_code= error.status_code,content=error.detail)
            finally:
                response = await call_next(request)
        else:
            error = not_authorized()
            response = JSONResponse(status_code= error.status_code,content=error.detail)
        
        
    except Exception as e:
        print(e)
        error = api_exception(ex=e)
        response = JSONResponse(status_code= error.status_code,content=error.detail)
   

    return response

async def url_pattern_check(path, pattern):
    result = re.match(pattern, path)
    if result:
        return True
    return False



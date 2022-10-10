from dataclasses import asdict
from fastapi import Depends, FastAPI
from fastapi.security import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn
from app.common.config import conf
from app.db.conn import db,Base
from app.middlewares.token_validator import access_control
from app.router import auth, index,user,cup

API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)

def create_app():
    ''''''

    
    c= conf()
    app = FastAPI()
    conf_dict = asdict(c)
    db.init_app(app,**conf_dict)

    #미들웨어 정의
    app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)
    

    #라우터 정의
    app.include_router(index.router)
    app.include_router(auth.router)
    app.include_router(cup.router,dependencies=[Depends(API_KEY_HEADER)])
    app.include_router(user.router,dependencies=[Depends(API_KEY_HEADER)])
    
    return app


app = create_app()

if __name__ == '__main__':
    uvicorn.run('main:app' ,host='127.0.0.1',port=8080,reload=True)
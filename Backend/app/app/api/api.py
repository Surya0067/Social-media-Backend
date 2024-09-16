from fastapi import APIRouter, Depends
from api.endpoints import login, authentication, user, post, chat


api_router = APIRouter()
api_router.include_router(login.router, prefix="/login",tags=["login"])
api_router.include_router(authentication.router,prefix="/auth",tags=["Authentication"])
api_router.include_router(user.router, prefix="/users", tags = ["User"])
api_router.include_router(post.router, prefix="/post", tags = ["Post"])
api_router.include_router(chat.router, prefix="/chat", tags = ["Chat"])
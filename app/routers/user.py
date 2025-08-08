from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependency import get_current_user, get_db
from app.schemas.request.user import UserRegister
from app.schemas.response.user import GetUserMe, PostUserRegister
from app.services.user import create_user

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register", response_model=PostUserRegister, summary="✅ 회원가입")
async def register(user: UserRegister, db: AsyncSession = Depends(get_db)):
    user = await create_user(db, user)
    if not user:
        return {"success": False, "message": None}
    return {"success": True, "message": None}


@router.get("/me", response_model=GetUserMe, summary="✅ 내정보")
async def read_user_me(user=Depends(get_current_user)):
    return {"success": True, "message": None, "data": user}

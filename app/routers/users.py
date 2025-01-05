from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependency import get_current_user, get_db
from app.schemas.request.users import UserRegister
from app.schemas.response.users import GetUserMe, PostUserRegister
from app.services.users import create_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=PostUserRegister, summary="✅ 회원가입")
def register(user: UserRegister, db: Session = Depends(get_db)):
    user = create_user(db, user)
    if not user:
        return {"success": False, "message": None}
    return {"success": True, "message": None}


@router.get("/me", response_model=GetUserMe, summary="✅ 내정보")
def read_user_me(user=Depends(get_current_user)):
    """
    Get current user.
    """
    return {"success": True, "message": None, "data": user}

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependency import get_db
from app.schemas.request.user import UserRegister
from app.schemas.response.user import PostUserRegister
from app.services.user import create_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=PostUserRegister)
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    user = create_user(db, user)
    if not user:
        return {"success": False, "message": None}
    return {"success": True, "message": None}

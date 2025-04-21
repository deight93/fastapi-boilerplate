from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.dependency import get_db
from app.schemas.response.auth import PostAuthLogin, PostAuthRefresh
from app.services.auth import login_user, refresh_tokens

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=PostAuthLogin,
    summary="✅ 로그인",
)
def post_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    tokens = login_user(db, form_data)
    tokens.update({"success": True, "message": None})
    return tokens


@router.post(
    "/refresh-token",
    response_model=PostAuthRefresh,
    summary="✅ 리프레시 토큰",
)
def post_refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    tokens = refresh_tokens(refresh_token, db)
    response = {"success": True, "message": None}
    response.update(data=tokens)
    return response

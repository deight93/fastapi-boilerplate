from fastapi import APIRouter, Depends, Path, Security
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependency import get_current_user, get_db
from app.schemas.request.item import (
    ItemInsertRequest,
    ItemListRequest,
    ItemUpdateRequest,
)
from app.schemas.response.base import BaseResponse
from app.schemas.response.item import (
    ItemDetailResponse,
    ItemListResponse,
)
from app.services.item import (
    create_item,
    delete_item,
    get_item,
    get_items,
    hard_delete_item,
    update_item,
)

router = APIRouter(prefix="/item", tags=["item"])


@router.post(
    "",
    response_model=BaseResponse,
    summary="✅ 아이템 등록 (최고 관리자)",
)
async def create_item_endpoint(
    item: ItemInsertRequest,
    db: AsyncSession = Depends(get_db),
    admin=Security(get_current_user, scopes=["admin"]),
):
    await create_item(item, db, admin)
    return BaseResponse.success_response(None)


@router.get(
    "",
    response_model=ItemListResponse,
    summary="✅ 아이템 목록 (관리자)",
)
async def get_items_endpoint(
    query_params: ItemListRequest = Depends(),
    db: AsyncSession = Depends(get_db),
):
    items = await get_items(query_params, db)
    return BaseResponse.success_response(None, data=items)


@router.get(
    "/{item_id}",
    response_model=ItemDetailResponse,
    summary="✅ 아이템 상세 (관리자)",
)
async def get_item_endpoint(
    item_id: int = Path(title="아이템 DB ID", description="아이템 DB ID"),
    db: AsyncSession = Depends(get_db),
):
    item = await get_item(item_id, db)
    return BaseResponse.success_response(None, data=item)


@router.put(
    "/{item_id}",
    response_model=BaseResponse,
    summary="✅ 아이템 수정 (최고관리자)",
)
async def update_item_endpoint(
    item_update: ItemUpdateRequest,
    item_id: int = Path(title="아이템 DB ID", description="아이템 DB ID"),
    db: AsyncSession = Depends(get_db),
    admin=Security(get_current_user, scopes=["admin"]),
):
    await update_item(item_id, item_update, db, admin)
    return BaseResponse.success_response(None)


@router.delete(
    "/{item_id}",
    response_model=BaseResponse,
    summary="✅ 아이템 삭제(소프트) (최고관리자)",
)
async def delete_item_endpoint(
    item_id: int = Path(title="아이템 DB ID", description="아이템 DB ID"),
    db: AsyncSession = Depends(get_db),
    admin=Security(get_current_user, scopes=["admin"]),
):
    await delete_item(item_id, db, admin)
    return BaseResponse.success_response(None)


@router.delete(
    "/{item_id}/hard-delete",
    response_model=BaseResponse,
    summary="✅ 아이템 삭제(하드) (최고관리자)",
)
async def hard_delete_item_endpoint(
    item_id: int = Path(title="아이템 DB ID", description="아이템 DB ID"),
    db: AsyncSession = Depends(get_db),
    admin=Security(get_current_user, scopes=["admin"]),
):
    await hard_delete_item(item_id, db, admin)
    return BaseResponse.success_response(None)

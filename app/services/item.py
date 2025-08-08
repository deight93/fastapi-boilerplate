from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppError, ErrorCode
from app.models.item import Item
from app.models.user import User
from app.schemas.request.item import (
    ItemInsertRequest,
    ItemListRequest,
    ItemUpdateRequest,
)
from app.schemas.response.item import ItemRead


# 아이템 생성
async def create_item(
    item: ItemInsertRequest,
    db: AsyncSession,
    user: User,
):
    new_item = Item(
        title=item.title,
        content=item.content,
        user_id=user.id,
    )
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item


# 아이템 목록 조회
async def get_items(
    query: ItemListRequest,
    db: AsyncSession,
):
    stmt = select(Item).where(Item.deleted_at.is_(None))

    if query.title:
        stmt = stmt.where(Item.title.ilike(f"%{query.title}%"))
    if query.content:
        stmt = stmt.where(Item.content.ilike(f"%{query.content}%"))

    count_stmt = select(func.count()).select_from(
        stmt.with_only_columns(Item.id).subquery()
    )
    total_count = (await db.execute(count_stmt)).scalar_one()

    stmt = stmt.order_by(Item.created_at.desc()).offset(query.offset)
    if query.limit:
        stmt = stmt.limit(query.limit)

    result = await db.execute(stmt)
    items = result.scalars().all()

    return {"results": items, "total_count": total_count}


# 아이템 단건 조회
async def get_item(
    item_id: int,
    db: AsyncSession,
):
    item = await db.get(Item, item_id)
    if not item or item.deleted_at:
        raise AppError(ErrorCode.NOT_FOUND_404, 404)
    return ItemRead.model_validate(item)


# 아이템 수정
async def update_item(
    item_id: int,
    item_update: ItemUpdateRequest,
    db: AsyncSession,
    user: User,
):
    item = await db.get(Item, item_id)
    if not item or item.deleted_at:
        raise AppError(ErrorCode.NOT_FOUND_404, 404)
    if item_update.title is not None:
        item.title = item_update.title
    if item_update.content is not None:
        item.content = item_update.content
    item.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(item)
    return item


# 아이템 소프트 삭제
async def delete_item(
    item_id: int,
    db: AsyncSession,
    user: User,
):
    item = await db.get(Item, item_id)
    if not item or item.deleted_at:
        raise AppError(ErrorCode.NOT_FOUND_404, 404)
    item.deleted_at = datetime.utcnow()
    await db.commit()


# 아이템 하드 삭제
async def hard_delete_item(
    item_id: int,
    db: AsyncSession,
    user: User,
):
    item = await db.get(Item, item_id)
    if not item:
        raise AppError(ErrorCode.NOT_FOUND_404, 404)
    await db.delete(item)
    await db.commit()

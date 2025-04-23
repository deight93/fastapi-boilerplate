import logging
from typing import Any

from asyncpg import UniqueViolationError
from fastapi import HTTPException, status
from sqlalchemy import Column, DateTime, func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, declarative_mixin, declared_attr


@declarative_mixin
class Timestamp:
    created_at = Column(
        DateTime, nullable=False, server_default=func.now(), comment="생성일시"
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="수정일시",
    )
    deleted_at = Column(DateTime, nullable=True, comment="삭제일시")


class Base(DeclarativeBase):
    id: Any
    __name__: str
    # Generate __tablename__ automatically

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

    async def save(self, db_session: AsyncSession):
        """

        :param db_session:
        :return:
        """
        try:
            db_session.add(self)
            return await db_session.commit()
        except SQLAlchemyError as ex:
            logging.error(f"Error inserting instance of {self}: {repr(ex)}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex)
            ) from ex

    async def delete(self, db_session: AsyncSession):
        """

        :param db_session:
        :return:
        """
        try:
            await db_session.delete(self)
            await db_session.commit()
            return True
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex)
            ) from ex

    async def update(self, db: AsyncSession, **kwargs):
        """

        :param db:
        :param kwargs
        :return:
        """
        try:
            for k, v in kwargs.items():
                setattr(self, k, v)
            return await db.commit()
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex)
            ) from ex

    async def save_or_update(self, db: AsyncSession):
        try:
            db.add(self)
            return await db.commit()
        except IntegrityError as exception:
            if isinstance(exception.orig, UniqueViolationError):
                return await db.merge(self)
            else:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=repr(exception),
                ) from exception
        finally:
            await db.close()

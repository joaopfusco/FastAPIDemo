from typing import Type
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.entity import Entity

class BaseService:
    def __init__(self, model: Type[Entity]):
        self.model = model

    def query(self):
        return select(self.model)
    
    async def execute_query(self, session: AsyncSession, query):
        result = await session.execute(query)
        return result.scalars()

    async def get_all(self, session: AsyncSession):
        stmt = self.query()
        result = await self.execute_query(session, stmt)
        return result.all()

    async def get_one(self, item_id: int, session: AsyncSession):
        stmt = self.query().where(self.model.id == item_id)
        result = await self.execute_query(session, stmt)
        item = result.first()
        if not item:
            raise Exception("Not found")
        return item

    async def create(self, data: BaseModel, session: AsyncSession):
        try:
            obj = self.model(**data.model_dump())
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj
        except Exception as e:
            await session.rollback()
            raise e

    async def update(self, item_id: int, data: BaseModel, session: AsyncSession):
        try:
            db_item = await self.get_one(item_id, session)
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(db_item, key, value)
            await session.commit()
            await session.refresh(db_item)
            return db_item
        except Exception as e:
            await session.rollback()
            raise e

    async def remove(self, item_id: int, session: AsyncSession):
        try:
            db_item = await self.get_one(item_id, session)
            await session.delete(db_item)
            await session.commit()
            return {"detail": "Deleted"}
        except Exception as e:
            await session.rollback()
            raise e

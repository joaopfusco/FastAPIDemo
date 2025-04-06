from fastapi import APIRouter, Depends, HTTPException
from typing import Type, List, Callable, Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from odata_query.sqlalchemy import apply_odata_query
from app.db.database import get_db
from app.models.entity import Entity
from app.services.base_service import BaseService
from sqlalchemy.future import select

class BaseRouter(APIRouter):
    def __init__(
        self,
        service: Type[BaseService],
        schema: Type[BaseModel],
        create_schema: Optional[Type[BaseModel]],
        update_schema: Optional[Type[BaseModel]],
        model: Type[Entity],
        db: Callable = Depends(get_db),
        prefix: str = "",
        tags: Optional[List[str]] = None,
    ):
        super().__init__(prefix=prefix, tags=tags or [model.__name__])

        self.service = service(model)
        self.schema = schema
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.db = db

        self.add_routes()

    async def try_execute(self, func: Callable, *args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def add_routes(self):
        @self.get("/", response_model=List[self.schema])
        async def get_all(session: AsyncSession = Depends(self.db)):
            return await self.try_execute(lambda: self.service.get_all(session))

        @self.get("/{item_id}", response_model=self.schema)
        async def get_one(item_id: int, session: AsyncSession = Depends(self.db)):
            return await self.try_execute(lambda: self.service.get_one(item_id, session))

        @self.get("/odata/", response_model=List[self.schema])
        async def odata(query: Optional[str] = None, session: AsyncSession = Depends(self.db)):
            async def func():
                if query:
                    stmt = apply_odata_query(select(self.model), query)
                    result = await session.execute(stmt)
                    return result.scalars().all()
                return await self.service.get_all(session)

            return await self.try_execute(lambda: func())

        @self.post("/", response_model=self.schema)
        async def create(item: self.create_schema, session: AsyncSession = Depends(self.db)):  # type: ignore
            return await self.try_execute(lambda: self.service.create(item, session))

        @self.put("/{item_id}", response_model=self.schema)
        async def update(item_id: int, item: self.update_schema, session: AsyncSession = Depends(self.db)):  # type: ignore
            return await self.try_execute(lambda: self.service.update(item_id, item, session))

        @self.delete("/{item_id}", response_model=dict)
        async def remove(item_id: int, session: AsyncSession = Depends(self.db)):
            return await self.try_execute(lambda: self.service.remove(item_id, session))

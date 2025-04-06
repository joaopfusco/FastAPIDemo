from fastapi import APIRouter, Depends, HTTPException
from typing import Type, List, Callable, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.entity import Entity
from app.services.base_service import BaseService

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
        tags: List[str] = None,
    ):
        super().__init__(prefix=prefix, tags=tags or [model.__name__])

        self.service = service
        self.schema = schema
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.db = db

        self.add_routes()

    def try_execute(self, func: Callable, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def add_routes(self):
        @self.get("/", response_model=List[self.schema])
        def get_all(session: Session = Depends(self.db)):
            return self.try_execute(lambda: self.service.get(session))

        @self.get("/{item_id}", response_model=self.schema)
        def get_one(item_id: int, session: Session = Depends(self.db)):
            return self.try_execute(lambda: self.service.get_one(item_id, session))

        @self.post("/", response_model=self.schema)
        def create(item: self.create_schema, session: Session = Depends(self.db)): # type: ignore
            return self.try_execute(lambda: self.service.create(item, session))

        @self.put("/{item_id}", response_model=self.schema)
        def update(item_id: int, item: self.update_schema, session: Session = Depends(self.db)): # type: ignore
            return self.try_execute(lambda: self.service.update(item_id, item, session))

        @self.delete("/{item_id}", response_model=dict)
        def remove(item_id: int, session: Session = Depends(self.db)):
            return self.try_execute(lambda: self.service.remove(item_id, session))

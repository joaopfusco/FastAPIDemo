from fastapi import APIRouter, Depends, HTTPException
from typing import Type, List, Callable, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import get_db
from app.models.entity import Entity

class BaseRouter(APIRouter):
    def __init__(
        self,
        schema: Type[BaseModel],
        create_schema: Optional[Type[BaseModel]],
        update_schema: Optional[Type[BaseModel]],
        db_model: Type[Entity],
        db: Callable = Depends(get_db),
        prefix: str = "",
        tags: List[str] = None,
    ):
        super().__init__(prefix=prefix, tags=tags or [db_model.__name__])

        self.schema = schema
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.db_model = db_model
        self.db = db

        self.add_routes()

    def get_all(self, session: Session):
        return session.query(self.db_model).all()

    def get_one(self, item_id: int, session: Session):
        item = session.query(self.db_model).get(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Not found")
        return item

    def create(self, item: Type[BaseModel], session: Session):
        try:
            item = self.create_schema(**item.model_dump())
            obj = self.db_model(**item.model_dump())
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def update(self, item_id: int, item: Type[BaseModel], session: Session):
        try:
            db_item = session.query(self.db_model).get(item_id)
            if not db_item:
                raise HTTPException(status_code=404, detail="Not found")
            for key, value in item.model_dump().items():
                setattr(db_item, key, value)
            session.commit()
            return db_item
        except SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    def remove(self, item_id: int, session: Session):
        try:
            db_item = session.query(self.db_model).get(item_id)
            if not db_item:
                raise HTTPException(status_code=404, detail="Not found")
            session.delete(db_item)
            session.commit()
            return {"detail": "Deleted"}
        except SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def add_routes(self):
        @self.get("/", response_model=List[self.schema])
        def get_all(session: Session = Depends(self.db)):
            return self.get_all(session)

        @self.get("/{item_id}", response_model=self.schema)
        def get_one(item_id: int, session: Session = Depends(self.db)):
            return self.get_one(item_id, session)

        @self.post("/", response_model=self.schema)
        def create(item: self.create_schema, session: Session = Depends(self.db)): # type: ignore
            return self.create(item, session)

        @self.put("/{item_id}", response_model=self.schema)
        def update(item_id: int, item: self.update_schema, session: Session = Depends(self.db)): # type: ignore
            return self.update(item_id, item, session)

        @self.delete("/{item_id}", response_model=dict)
        def remove(item_id: int, session: Session = Depends(self.db)):
            return self.remove(item_id, session)

from fastapi import Depends
from typing import Type, Callable, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.entity import Entity

class BaseService:
    def __init__(self, model: Type[Entity]):
        self.model = model

    def get(self, session: Session):
        return session.query(self.model)

    def get_one(self, item_id: int, session: Session):
        item = self.get(session).filter(self.model.id == item_id).first()
        if not item:
            raise Exception("Not found")
        return item

    def create(self, data: BaseModel, session: Session):
        try:
            obj = self.model(**data.model_dump())
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj
        except Exception as e:
            session.rollback()
            raise e

    def update(self, item_id: int, data: BaseModel, session: Session):
        try:
            db_item = self.get_one(item_id, session)
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(db_item, key, value)
            session.commit()
            session.refresh(db_item)
            return db_item
        except Exception as e:
            session.rollback()
            raise e
    
    def remove(self, item_id: int, session: Session):
        try:
            db_item = self.get_one(item_id, session)
            session.delete(db_item)
            session.commit()
            return {"detail": "Deleted"}
        except Exception as e:
            session.rollback()
            raise e

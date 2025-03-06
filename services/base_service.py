from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Type, Generic, TypeVar, List

ModelType = TypeVar("ModelType")
SchemaType = TypeVar("SchemaType")

class BaseService(Generic[ModelType, SchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_all(self, db: Session) -> List[SchemaType]:
        return db.query(self.model).all()

    def get_one(self, db: Session, id: int) -> SchemaType:
        obj = db.query(self.model).filter(self.model.id == id).first()
        if not obj:
            raise HTTPException(status_code=404, detail="Item not found")
        return obj

    def create(self, db: Session, item: SchemaType) -> SchemaType:
        new_item = self.model(**item.dict())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

    def update(self, db: Session, id: int, item: SchemaType) -> SchemaType:
        obj = db.query(self.model).filter(self.model.id == id).first()
        if not obj:
            raise HTTPException(status_code=404, detail="Item not found")
        for key, value in item.dict().items():
            setattr(obj, key, value)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, id: int) -> dict:
        obj = db.query(self.model).filter(self.model.id == id).first()
        if not obj:
            raise HTTPException(status_code=404, detail="Item not found")
        db.delete(obj)
        db.commit()
        return {"message": "Item deleted successfully"}
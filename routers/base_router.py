from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Type, Generic, TypeVar, List

from db.database import get_db

ModelType = TypeVar("ModelType")
ServiceType = TypeVar("ServiceType")
SchemaType = TypeVar("SchemaType")

class BaseRouter(Generic[ModelType, ServiceType, SchemaType]):
    def __init__(self, model: Type[ModelType], service: Type[ServiceType], prefix: str, tag: str):
        self.model = model
        self.service = service
        self.prefix = prefix
        self.tag = tag

    def get_router(self) -> APIRouter:
        router = APIRouter(prefix=self.prefix, tags=[self.tag])

        router.add_api_route("/", self.get_all, methods=["GET"])
        router.add_api_route("/{id}", self.get_one, methods=["GET"])
        router.add_api_route("/", self.create, methods=["POST"])
        router.add_api_route("/{id}", self.update, methods=["PUT"])
        router.add_api_route("/{id}", self.delete, methods=["DELETE"])

        return router

    def get_all(self, db: Session = Depends(get_db)) -> List[SchemaType]:
        service_instance = self.service()
        return service_instance.get_all(db)

    def get_one(self, id: int, db: Session = Depends(get_db)) -> SchemaType:
        service_instance = self.service()
        return service_instance.get_one(db, id)

    def create(self, item: SchemaType, db: Session = Depends(get_db)) -> SchemaType:
        service_instance = self.service()
        return service_instance.create(db, item)

    def update(self, id: int, item: SchemaType, db: Session = Depends(get_db)) -> SchemaType:
        service_instance = self.service()
        return service_instance.update(db, id, item)

    def delete(self, id: int, db: Session = Depends(get_db)) -> dict:
        service_instance = self.service()
        return service_instance.delete(db, id)

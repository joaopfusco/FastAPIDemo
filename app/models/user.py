from sqlalchemy import Column, String
from app.models.entity import Entity

class User(Entity):
    username = Column(String, unique=True, index=True)
    password = Column(String)
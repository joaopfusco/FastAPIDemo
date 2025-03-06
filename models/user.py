from sqlalchemy import Column, String
from models.entity import Entity

class User(Entity):
    username = Column(String, unique=True, index=True)
    password = Column(String)

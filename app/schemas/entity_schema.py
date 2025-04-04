from pydantic import BaseModel
from datetime import datetime

class EntitySchema(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

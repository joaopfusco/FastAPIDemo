from pydantic import BaseModel, Field
from datetime import datetime

class EntitySchema(BaseModel):
    id: int = Field(..., frozen=True)
    created_at: datetime = Field(..., frozen=True)
    updated_at: datetime = Field(..., frozen=True)

    class Config:
        from_attributes = True

from pydantic import BaseModel
from datetime import datetime

class EntitySchema(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True,
    }

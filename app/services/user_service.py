from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.services.base_service import BaseService

class UserService(BaseService):
    def __init__(self):
        super().__init__(User)
        
    async def get_all(self, session: AsyncSession):
        print("Override no get_all")
        return await super().get_all(session)
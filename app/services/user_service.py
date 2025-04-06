from sqlalchemy.ext.asyncio import AsyncSession
from app.services.base_service import BaseService

class UserService(BaseService):
    async def get_all(self, session: AsyncSession):
        print("Override no get_all")
        return await super().get_all(session)

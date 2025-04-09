from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilitiesService(BaseService):
    async def get_all_uslugi(self):
        return await self.db.uslugi.get_all()

    async def add_uslugi(self, data):
        result = await self.db.uslugi.add(data=data)
        await self.db.commit()
        test_task.delay()
        return result

from datetime import datetime
from src.services.base import BaseService 
from src.exceptions.exceptions import DepartureBeforeArrivalException

class RoomsService(BaseService) :
    async def get_room_by_date_and_hotel(
        self, 
        date_from: datetime,
        date_to: datetime,
        hotel_id
    ) :
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
    
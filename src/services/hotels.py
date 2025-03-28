from src.services.base import BaseService
from src.exceptions.exceptions import check_date_to_after_date_from
from src.schemas.hotels import HotelPATCH

class HotelSevice(BaseService) : 
    async def get_hotels_filtered_by_time(
        self,
        pagination,
        title,
        location,
        date_from,
        date_to,
    ) :
        check_date_to_after_date_from(date_from=date_from, date_to=date_to)
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )
    
    async def hotel_by_id(self, hotel_id: int) :
        return await self.db.hotels.get_one(id=hotel_id)
    
    async def add_hotel(self, data) : 
        hotel = await self.db.hotels.add(data=data)
        await self.db.commit()
        return hotel
    
    async def delete_hotel(self, hotel_id) :
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
        
    async def patch_and_put_hotel(self, hotel_id, data: HotelPATCH, is_patch: bool = False) : 
        await self.db.hotels.edit(data=data, is_patch=is_patch, id=hotel_id)
        await self.db.commit()
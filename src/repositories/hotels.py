from sqlalchemy import select, insert, func

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm

class HotelsRepository(BaseRepository) :
    model = HotelsOrm 
    
    async def get_all(self, location, title, limit, offset) :
        query = select(HotelsOrm)
        
        if title :
            query = query.filter(HotelsOrm.title.like(f'%{title}%')) 
        if location :
            query = query.filter(HotelsOrm.location.like(f'%{location}%'))
            
        query = (
                query
                .limit(limit)
                .offset(offset)
        )

        
        result = await self.session.execute(query)
        
        return result.scalars().all()
    
    async def add(self, hotel_data) : 
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await self.session.execute(add_hotel_stmt)
        
        query = select(func.max(HotelsOrm.id))
        
        result = await self.session.execute(query)
        
        id = result.scalars().all()[0]
                
        query = select(HotelsOrm).filter_by(id=id)
        
        result = await self.session.execute(query)
        
        return result.scalars().all()
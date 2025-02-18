from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm

class BookingsRepository(BaseRepository) : 
    model = BookingsOrm
    mapper = BookingDataMapper
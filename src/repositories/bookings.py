from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.schemas.bookings import AddBookings

class BookingsRepository(BaseRepository) : 
    model = BookingsOrm
    schema = AddBookings
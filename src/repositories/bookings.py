from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm

class BookingsRepository(BaseRepository) : 
    model = BookingsOrm
    # доделать схему
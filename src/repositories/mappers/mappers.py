from src.models.facilities import RoomsFacilitiesOrm, UslugiOrm
from src.schemas.facilities import RoomsFacilities, Uslugi
from src.schemas.rooms import Room, RoomWithRels
from src.schemas.users import User
from src.schemas.bookings import AddBookings
from src.models.bookings import BookingsOrm
from src.models.users import UsersOrm
from src.models.hotels import HotelsOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.hotels import Hotel
from src.models.rooms import RoomsOrm

class HotelDataMapper(DataMapper) : 
    db_model = HotelsOrm
    schema = Hotel

class RoomDataMapper(DataMapper) : 
    db_model = RoomsOrm
    schema = Room

class RoomDataMapperWithRels(DataMapper) :
    db_model = RoomsOrm
    schema = RoomWithRels

class UserDataMapper(DataMapper) : 
    db_model = UsersOrm
    schema = User

class BookingDataMapper(DataMapper) : 
    db_model = BookingsOrm
    schema = AddBookings
    
class FacilitiesDataMapper(DataMapper) :
    db_model = RoomsFacilitiesOrm
    schema = RoomsFacilities
    
class UslugiDataMapper(DataMapper) :
    db_model = UslugiOrm
    schema = Uslugi
    

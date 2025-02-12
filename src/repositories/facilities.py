from src.repositories.base import BaseRepository
from src.models.facilities import UslugiOrm, RoomsFacilitiesOrm

# pydantic
from src.schemas.facilities import Uslugi, RoomsFacilities

class FacilitiesRepository(BaseRepository) : 
    model = RoomsFacilitiesOrm
    schema = RoomsFacilities
    
class UslugiRepository(BaseRepository) :
    model = UslugiOrm
    schema = Uslugi

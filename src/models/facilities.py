from sqlalchemy import String
from src.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey

class UslugiOrm(Base) : 
    __tablename__ = 'facilites'
    
    id : Mapped[int] = mapped_column(primary_key=True)
    title : Mapped[str] = mapped_column(String(100))
    
    rooms: Mapped[list["RoomsOrm"]] = relationship(
        back_populates="facilities",
        secondary="rooms_facilities"
    )

class RoomsFacilitiesOrm(Base) : 
    __tablename__ = 'rooms_facilities'

    id : Mapped[int] = mapped_column(primary_key=True)
    room_id : Mapped[int] = mapped_column(ForeignKey('rooms.id'))    
    facility_id : Mapped[int] = mapped_column(ForeignKey('facilites.id'))    
    
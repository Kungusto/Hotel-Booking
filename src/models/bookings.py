from src.database import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey, Date

from datetime import date

class BookingsOrm(Base) : 
    __tablename__ = 'bookings'
    
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    room_id : Mapped[int] = mapped_column(Integer, ForeignKey('rooms.id'))
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    date_from : Mapped[date] = mapped_column(Date(), default=date.today())
    date_to : Mapped[date] = mapped_column(Date())
    price : Mapped[int]
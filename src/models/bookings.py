from src.database import Base

<<<<<<< HEAD
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, Integer, Date

from datetime import date, timedelta


=======
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey, Date

from datetime import date
>>>>>>> 5e8bfa6c51a63e06bdd375c044a7326f03e5a06b

class BookingsOrm(Base) : 
    __tablename__ = 'bookings'
    
<<<<<<< HEAD
    id : Mapped[int] = mapped_column(primary_key=True)
    room_id : Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    user_id : Mapped[int] = mapped_column(ForeignKey('users.id'))
    date_from : Mapped[date] = mapped_column(Date, default=lambda: date.today())
    date_to : Mapped[date] = mapped_column(Date, default=lambda: date.today() + timedelta(days=1))
    price : Mapped[int] = mapped_column(Integer)
    
=======
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    room_id : Mapped[int] = mapped_column(Integer, ForeignKey('rooms.id'))
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    date_from : Mapped[date] = mapped_column(Date(), default=date.today())
    date_to : Mapped[date] = mapped_column(Date())
    price : Mapped[int]
>>>>>>> 5e8bfa6c51a63e06bdd375c044a7326f03e5a06b

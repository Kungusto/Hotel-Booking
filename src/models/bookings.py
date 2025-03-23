from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, Integer, Date
from datetime import date, timedelta
from sqlalchemy.ext.hybrid import hybrid_property
from src.database import Base

class BookingsOrm(Base) : 
    __tablename__ = 'bookings'
    
    id : Mapped[int] = mapped_column(primary_key=True)
    room_id : Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    user_id : Mapped[int] = mapped_column(ForeignKey('users.id'))
    date_from : Mapped[date] = mapped_column(Date, default=lambda: date.today())
    date_to : Mapped[date] = mapped_column(Date, default=lambda: date.today() + timedelta(days=1))
    price : Mapped[int] = mapped_column(Integer)
    
    @hybrid_property
    def total_cost(self) :
        return self.price * (self.date_to - self.date_from).days
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from src.database import Base


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    name: Mapped[str] = mapped_column(String(20))
    nickname: Mapped[str] = mapped_column(String(35))
    hashedpassword: Mapped[str]

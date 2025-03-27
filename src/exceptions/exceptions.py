from datetime import date
from fastapi import HTTPException


class NabronirovalException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(NabronirovalException):
    detail = "Не осталось свободных номеров"


class UserAlreadyExistsException(NabronirovalException):
    detail = "Пользователь уже существует"


class DepartureBeforeArrivalException(NabronirovalException):
    detail = "Дата выезда раньше даты заезда"

def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
     if date_to <= date_from:
        raise DepartureBeforeArrivalException


class NoChangesException(NabronirovalException):
    detail = "Изменений не замечено"

class OutOfRangeException(NabronirovalException) :
    detail = "Длина ввода превышает допустимое значение"


class NabronirovalHTTPException(HTTPException) :
    detail = None 
    status_code = 400
    
    def __init__(self)  :
        super().__init__(status_code=self.status_code, detail=self.detail)

class RoomNotFoundHTTPException(NabronirovalHTTPException) :
    detail = "Номер не найден"
    status_code = 404

class HotelNotFoundHTTPException(NabronirovalHTTPException) :
    detail = "Отель не найден"
    status_code = 404

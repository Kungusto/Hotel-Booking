from datetime import date
from fastapi import HTTPException


class NabronirovalException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


# --- Not Found Exceptions
class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class UslugiNotFoundException(ObjectNotFoundException):
    detail = "Удобство не найдено"


class UserNotFoundException(ObjectNotFoundException):
    detail = "Пользователь не найден"


# --------------


class WrongPasswordException(NabronirovalException):
    detail = "Неверный пароль"


class AllRoomsAreBookedException(NabronirovalException):
    detail = "Не осталось свободных номеров"


class UserAlreadyExistsException(NabronirovalException):
    detail = "Пользователь уже существует"


class DepartureBeforeArrivalException(NabronirovalException):
    detail = "Дата выезда раньше даты заезда"


class RoomHasBookingsError(NabronirovalException):
    detail = "На номер уже есть бронирования"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise DepartureBeforeArrivalException


class NoChangesException(NabronirovalException):
    detail = "Изменений не замечено"


class OutOfRangeException(NabronirovalException):
    detail = "Длина ввода превышает допустимое значение"


class NabronirovalHTTPException(HTTPException):
    detail = None
    status_code = 400

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class DepartureBeforeArrivalHTTPException(NabronirovalHTTPException):
    detail = "Выезд не может быть раньше заезда и наоборот"


# --- Not Found Excpetions
class ObjectNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404


class RoomNotFoundHTTPException(ObjectNotFoundHTTPException):
    detail = "Номер не найден"


class HotelNotFoundHTTPException(ObjectNotFoundHTTPException):
    detail = "Отель не найден"


class UslugiNotFoundHTTPException(ObjectNotFoundHTTPException):
    detail = "Услуга не найдена"


class UserNotFoundHTTPException(ObjectNotFoundHTTPException):
    detail = "Пользователь не найден"


# -------------------------

class EmailNotRegistratedHTTPException(NabronirovalHTTPException) : 
    detail = "Этот E-mail не зарегестрирован"

class OutOfRangeHTTPException(NabronirovalHTTPException):
    detail = "Длина ввода превышает допустимое значение"


class RoomHasBookingsHTTPException(NabronirovalHTTPException):
    detail = "На номер уже существуют бронирования!"


class InternalServerErrorHTTPException(NabronirovalHTTPException):
    status_code = 500
    detail = "На стороне сервера произошла непредвиденная ошибка"


class UserAlreadyExistsHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Пользователь с этим email уже существует"


class WrongPasswordHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Неверный пароль"


class AllRoomsAreBookedHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "На данный момент нет свободных номеров"

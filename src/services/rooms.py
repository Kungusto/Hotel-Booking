from datetime import datetime
import logging
from sqlalchemy.exc import IntegrityError, DataError, DBAPIError
from asyncpg.exceptions import ForeignKeyViolationError
from src.services.base import BaseService
from src.exceptions.exceptions import (
    UslugiNotFoundException,
    ObjectNotFoundException,
    RoomNotFoundException,
    HotelNotFoundException,
    RoomHasBookingsError,
    OutOfRangeException,
)
from src.schemas.rooms import (
    RoomAddRequest,
    RoomAdd,
    PATCHRoom,
    PATCHRoomAdd,
    PUTRoomAdd,
)
from src.schemas.facilities import RoomsFacilitiesAdd


class RoomsService(BaseService):
    async def get_room_by_date_and_hotel(
        self, date_from: datetime, date_to: datetime, hotel_id: int
    ):
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_room_by_id(self, hotel_id: int, room_id: int):
        return await self.db.rooms.get_one_or_none_with_rels(
            id=room_id, hotel_id=hotel_id
        )

    async def add_room_with_rels(self, hotel_id: int, data: RoomAddRequest):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as ex :
            raise HotelNotFoundException from ex
        try:
            data_to_add = RoomAdd(hotel_id=hotel_id, **data.model_dump())
            room_data = await self.db.rooms.add(data_to_add)
            dates_for_facilities = [
                RoomsFacilitiesAdd(room_id=room_data.id, facility_id=id_fclty)
                for id_fclty in data.facilities_ids
            ]
            if dates_for_facilities:
                await self.db.facilities.add_bulk(dates_for_facilities)
        except IntegrityError as ex:
            logging.error(ex)
            if isinstance(ex.orig.__cause__, ForeignKeyViolationError):
                logging.info(f"Ошибка {type(ex).__name__} обработана")
                raise UslugiNotFoundException from ex

    async def patch_room_with_rels(
        self, hotel_id: int, room_id: int, request: PATCHRoom
    ) -> None:
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex
        try:
            await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex
        _room_data_dict = request.model_dump(exclude_unset=True)
        data = PATCHRoomAdd(**_room_data_dict)
        await self.db.rooms.edit(data, is_patch=True, id=room_id)
        if "facilities_ids" in _room_data_dict:
            try:
                await self.db.facilities.set_room_facilities(
                    room_id=room_id, facilities_ids=request.facilities_ids
                )
            except IntegrityError as ex:
                logging.error(ex)
                if isinstance(ex.orig.__cause__, ForeignKeyViolationError):
                    logging.info(f"Ошибка {type(ex).__name__} обработана")
                    raise UslugiNotFoundException from ex

    async def put_room_with_rels(self, hotel_id: int, room_id: int, request: PATCHRoom):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex
        try:
            await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex
        _room_data_dict = request.model_dump()
        data = PUTRoomAdd(**_room_data_dict)
        await self.db.rooms.edit(data, is_patch=True, id=room_id)
        if "facilities_ids" in _room_data_dict:
            try:
                await self.db.facilities.set_room_facilities(
                    room_id=room_id, facilities_ids=request.facilities_ids
                )
            except IntegrityError as ex:
                logging.error(ex)
                if isinstance(ex.orig.__cause__, ForeignKeyViolationError):
                    logging.info(f"Ошибка {type(ex).__name__} обработана")
                    raise UslugiNotFoundException from ex

    async def delete_room(self, hotel_id: int, room_id: int):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex
        try:
            await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex
        try:
            await self.db.rooms.delete(id=room_id)
        except IntegrityError as ex:
            if isinstance(ex.orig.__cause__, ForeignKeyViolationError):
                logging.info(f"Ошибка {type(ex).__name__} обработана")
                raise RoomHasBookingsError from ex
            else:
                logging.exception(ex)
        except DBAPIError as ex:
            if isinstance(ex.orig.__cause__, DataError):
                raise OutOfRangeException
            else:
                logging.error("Ошибка не была обработана!")
                raise ex

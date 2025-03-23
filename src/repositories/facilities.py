from sqlalchemy import delete, insert, select
from src.repositories.base import BaseRepository
from src.models.facilities import UslugiOrm, RoomsFacilitiesOrm
from src.repositories.mappers.mappers import FacilitiesDataMapper, UslugiDataMapper
from src.schemas.facilities import RoomsFacilitiesAdd


class FacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    mapper = FacilitiesDataMapper

    async def set_room_facilities(self, room_id: int, facilities_ids: list[int]):
        """Добавляет недостающие удобства и удаляет лишние"""
        get_rooms_stmt = select(RoomsFacilitiesOrm.facility_id).filter_by(
            room_id=room_id
        )
        not_sorted_result = await self.session.execute(
            get_rooms_stmt
        )  # вытаскиваем все строчки по номеру комнаты

        all_fclts_ids = {
            model.facility_id for model in not_sorted_result
        }  # вытаскиваем все айдишники
        ids_to_delete = all_fclts_ids - set(
            facilities_ids
        )  # вычисляем айдишники на удаление
        ids_to_add = (
            set(facilities_ids) - all_fclts_ids
        )  # вычисляем айдишники на добавление

        if ids_to_delete:
            delete_stmt = (
                delete(self.model)
                .filter(self.model.facility_id.in_(ids_to_delete))
                .filter_by(room_id=room_id)
            )
            await self.session.execute(delete_stmt)

        if ids_to_add:
            data_to_add = [
                RoomsFacilitiesAdd(room_id=room_id, facility_id=fclt_id)
                for fclt_id in ids_to_add
            ]
            add_bulk_stmt = insert(self.model).values(
                [item.model_dump() for item in data_to_add]
            )
            await self.session.execute(add_bulk_stmt)


class UslugiRepository(BaseRepository):
    model = UslugiOrm
    mapper = UslugiDataMapper

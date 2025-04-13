from fastapi import APIRouter, UploadFile
from src.services.images import ImageService
from src.exceptions.exceptions import WrongFormatFileException, WrongFormatFileHTTPException

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post(
        path="",
        summary="Загрузка изображений для отелей",
        description="Поддерживаемые форматы: .jpg .jpeg .png .webp"
)
def upload_image(file: UploadFile):
    try : 
        ImageService(None).upload_message(file)
    except WrongFormatFileException as ex :
        raise WrongFormatFileHTTPException from ex 
    return {"status": "OK"}

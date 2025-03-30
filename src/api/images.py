import shutil
from src.tasks.tasks import resize_image
from fastapi import APIRouter, UploadFile
from src.services.images import ImageService
router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("")
def upload_image(file: UploadFile):
    ImageService(None).upload_message(file)
    return {"status": "OK"}
import shutil
from src.tasks.tasks import resize_image
from fastapi import APIRouter, UploadFile

router = APIRouter(prefix='/images', tags=['Изображения отелей'])

@router.post("")
def upload_image(file: UploadFile) : 
    image_path = f'src/static/images/{file.filename}'
    with open(image_path, 'wb+') as new_file : 
        shutil.copyfileobj(file.file, new_file)

    resize_image.delay(image_path)
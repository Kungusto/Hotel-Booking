import logging
from src.services.base import BaseService
import shutil
from src.tasks.tasks import resize_image
from fastapi import UploadFile


class ImageService(BaseService):
    def upload_message(self, file: UploadFile):
        image_path = f"src/static/images/{file.filename}"
        with open(image_path, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)
            logging.info(f"Записан новый файл по адресу: {image_path}")
        resize_image.delay(image_path)

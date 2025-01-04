from fastapi import FastAPI, Query, Body

# добавление src в поле видимости
import sys
from pathlib import Path 

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as router_hotels
import uvicorn

from src.config import settings


from src.database import *
 

app = FastAPI()

app.include_router(router_hotels)

if __name__ == '__main__' :
    uvicorn.run(app)
    
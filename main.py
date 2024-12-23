from fastapi import FastAPI, Query, Body
from hotels import router as router_hotels
import uvicorn

app = FastAPI()

app.include_router(router_hotels)

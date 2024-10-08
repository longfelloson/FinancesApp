from fastapi import (
    FastAPI,
    Request,
)
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

import database
from auth.router import router as auth_roter
from operations.router import router as operations_roter
from users.router import router as users_roter

templates = Jinja2Templates(directory="../templates")
app = FastAPI()
app.include_router(auth_roter)
app.include_router(operations_roter)
app.include_router(users_roter)

app.mount("/static", StaticFiles(directory="../static"), name="static")


@app.on_event("startup")
async def startup():
    """Set all necessary utils"""
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    await database.create_tables()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

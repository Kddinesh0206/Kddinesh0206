from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi.staticfiles import (
    StaticFiles
)

from app.config import (
    get_settings
)

from app.routes import (
    router
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    settings = get_settings()

    settings.panels_path.mkdir(
        parents=True,
        exist_ok=True
    )

    settings.exports_path.mkdir(
        parents=True,
        exist_ok=True
    )

    yield


settings = get_settings()


app = FastAPI(

    title="ComicCraft",

    description=(
        "AI Comic Story Creator "
        "using Gemini and image generation."
    ),

    version="1.0.0",

    lifespan=lifespan
)


app.mount(

    "/static",

    StaticFiles(
        directory="static"
    ),

    name="static"
)


app.include_router(
    router
)
from fastapi import FastAPI
from tortoise import Tortoise
from app.config import Settings
from app.routers.routes import router


app = FastAPI(title=Settings.PROJECT_NAME)

async def lifespan(app: FastAPI):
    await Tortoise.init(
        db_url=Settings.DATABASE_URL,
        modules={'models': ["app.models"]}
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


app.include_router(router, prefix='/auth', tags=['auth'])


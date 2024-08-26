import uvicorn

from src.settings import settings

uvicorn.run(
    "src.app:app",
    host=settings.SERVER_HOST,
    port=settings.SERVER_PORT,
    reload=True,
    workers=4
)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import routers

app = FastAPI(
    title="Dota Crownfall API",
    root_path="/api"
)

for router in routers:
    app.include_router(router)


@app.get(
    "/",
    include_in_schema=False
)
async def root():
    return {"message": "Dota Crownfall API"}


app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

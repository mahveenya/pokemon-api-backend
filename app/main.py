from fastapi import FastAPI

from app.routers.ability_router import router as ability_router
from app.routers.pokemon_router import router as pokemon_router

app = FastAPI()
app.include_router(pokemon_router)
app.include_router(ability_router)


@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok"}

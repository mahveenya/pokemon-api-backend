from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import AppError
from app.routers.ability_router import router as ability_router
from app.routers.pokemon_router import router as pokemon_router

app = FastAPI()
app.include_router(pokemon_router)
app.include_router(ability_router)


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok"}

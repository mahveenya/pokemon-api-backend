from fastapi import APIRouter, Depends, Request, status

from app.constants import Endpoints
from app.db.session import get_session
from app.schemas.pokemon_schema import (
    PokemonCreateSchema,
    PokemonListSchema,
    PokemonSchema,
)
from app.services.pokemon_service import (
    create_pokemon,
    delete_pokemon,
    get_pokemon_list,
)
from app.services.pokemon_service import (
    get_pokemon as get_pokemon_service,
)

router = APIRouter(prefix=f"{Endpoints.POKEMON_BASE}", tags=["pokemon"])


@router.post(
    "",
    response_model=PokemonSchema,
    status_code=status.HTTP_201_CREATED,
    responses={409: {"description": "Pokemon or ability name already exists"}},
)
async def create_pokemon_endpoint(
    request: Request,
    payload: PokemonCreateSchema,
    session=Depends(get_session),
) -> PokemonSchema:
    return await create_pokemon(session, payload, request)


@router.get("", response_model=PokemonListSchema)
async def list_pokemons(
    request: Request,
    offset: int = 0,
    limit: int = 20,
    session=Depends(get_session),
) -> PokemonListSchema:
    return await get_pokemon_list(session, offset, limit, request)


@router.get(
    "/{id_or_name}",
    response_model=PokemonSchema,
    responses={
        404: {"description": "Pokemon not found"},
        501: {"description": "Search by name is not implemented yet"},
    },
)
async def get_pokemon(
    request: Request, id_or_name: str, session=Depends(get_session)
) -> PokemonSchema:
    return await get_pokemon_service(session, id_or_name, request)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"description": "Pokemon not found"},
    },
)
async def delete_pokemon_endpoint(id: int, session=Depends(get_session)) -> None:
    await delete_pokemon(session, id)

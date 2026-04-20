from fastapi import APIRouter, Depends, HTTPException, Request

from app.constants import Endpoints
from app.db.session import get_session
from app.schemas.pokemon_schema import PokemonListSchema, PokemonSchema
from app.services.pokemon_service import get_pokemon_by_id, get_pokemon_list
from app.utils.helpers import build_base_url

router = APIRouter(prefix=f"{Endpoints.POKEMON_BASE}", tags=["pokemon"])


@router.get("", response_model=PokemonListSchema)
async def list_pokemons(
    request: Request,
    offset: int = 0,
    limit: int = 20,
    session=Depends(get_session),
) -> PokemonListSchema:
    base_url = f"{build_base_url(request)}{Endpoints.POKEMON_BASE}"
    return await get_pokemon_list(session, offset, limit, base_url)


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
    if id_or_name.isdigit():
        base_url = f"{build_base_url(request)}{Endpoints.POKEMON_BASE}"
        pokemon = await get_pokemon_by_id(session, int(id_or_name), base_url)
        if pokemon is None:
            raise HTTPException(status_code=404, detail="Pokemon not found")
        return pokemon
    else:
        raise HTTPException(
            status_code=501, detail="Search by name is not implemented yet"
        )

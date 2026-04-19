from fastapi import FastAPI, HTTPException
from fastapi.params import Depends

from app.constants import Endpoints
from app.db.session import get_session
from app.schemas.ability_schema import AbilitySchema
from app.schemas.pokemon_schema import PokemonListSchema, PokemonSchema
from app.services.ability_service import get_ability_by_id
from app.services.pokemon_service import get_pokemon_by_id, get_pokemon_list

app = FastAPI()


@app.get(Endpoints.HEALTH_CHECK)
async def health_check():
    return {"status": "ok"}


@app.get(Endpoints.POKEMON_LIST, response_model=PokemonListSchema)
async def list_pokemons(
    offset: int = 0,
    limit: int = 20,
    session=Depends(get_session),
) -> PokemonListSchema:
    return await get_pokemon_list(session, offset, limit)


@app.get(
    Endpoints.POKEMON_DETAIL,
    response_model=PokemonSchema,
    responses={
        404: {"description": "Pokemon not found"},
        501: {"description": "Search by name is not implemented yet"},
    },
)
async def get_pokemon(id_or_name: str, session=Depends(get_session)) -> PokemonSchema:
    if id_or_name.isdigit():
        pokemon = await get_pokemon_by_id(session, int(id_or_name))
        if pokemon is None:
            raise HTTPException(status_code=404, detail="Pokemon not found")
        return pokemon
    else:
        raise HTTPException(
            status_code=501, detail="Search by name is not implemented yet"
        )


@app.get(
    Endpoints.ABILITY_DETAIL,
    response_model=AbilitySchema,
    responses={
        404: {"description": "Ability not found"},
        501: {"description": "Search by name is not implemented yet"},
    },
)
async def get_ability(id_or_name: str, session=Depends(get_session)) -> AbilitySchema:
    if id_or_name.isdigit():
        ability = await get_ability_by_id(session, int(id_or_name))
        if ability is None:
            raise HTTPException(status_code=404, detail="Ability not found")
        return ability
    else:
        raise HTTPException(
            status_code=501, detail="Search by name is not implemented yet"
        )

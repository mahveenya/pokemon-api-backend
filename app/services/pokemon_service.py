from app.constants import Endpoints
from app.repositories.ability_repository import get_ability_db_models_by_pokemon_id
from app.repositories.pokemon_repository import (
    count_pokemon_db_models,
    get_pokemon_db_model_by_id,
    get_pokemon_db_models,
)
from app.schemas.ability_schema import AbilityInfoSchema, AbilityNamedAPIResourceSchema
from app.schemas.pokemon_schema import (
    PokemonListSchema,
    PokemonNamedAPIResourceSchema,
    PokemonSchema,
)
from app.utils.pagination import build_pagination


async def get_pokemon_list(session, offset, limit) -> PokemonListSchema:
    pokemons = await get_pokemon_db_models(session, offset, limit)
    if not pokemons:
        return PokemonListSchema(count=0, next=None, previous=None, results=[])

    total = await count_pokemon_db_models(session)

    results = [PokemonNamedAPIResourceSchema.from_model(p) for p in pokemons]

    next_url, previous_url = build_pagination(
        Endpoints.POKEMON_BASE, total, offset, limit
    )

    return PokemonListSchema(
        count=total,
        next=next_url,
        previous=previous_url,
        results=results,
    )


async def get_pokemon_by_id(session, pokemon_id) -> PokemonSchema | None:
    pokemon = await get_pokemon_db_model_by_id(session, pokemon_id)
    if not pokemon:
        return None

    abilities = await get_ability_db_models_by_pokemon_id(session, pokemon_id)
    abilities_resources = [
        AbilityNamedAPIResourceSchema.from_model(a) for a in abilities
    ]
    abilities_info = AbilityInfoSchema.from_resources(abilities_resources)
    return PokemonSchema(
        id=pokemon_id,
        name=pokemon.name,
        abilities=abilities_info,
    )

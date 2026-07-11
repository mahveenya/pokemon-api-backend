from app.exceptions import (
    FeatureNotImplementedError,
    ResourceConflictError,
    ResourceNotFoundError,
)
from app.repositories.ability_repository import (
    get_ability_db_model_by_name,
    get_ability_db_models_by_pokemon_id,
)
from app.repositories.pokemon_repository import (
    count_pokemon_db_models,
    create_pokemon_db_model,
    delete_pokemon_db_model,
    get_pokemon_db_model_by_id,
    get_pokemon_db_model_by_name,
    get_pokemon_db_models,
)
from app.schemas.ability_schema import AbilityInfoSchema
from app.schemas.common import NamedAPIResourceSchema
from app.schemas.pokemon_schema import (
    PokemonListSchema,
    PokemonSchema,
)
from app.utils.helpers import build_pagination


async def get_pokemon_list(session, offset, limit, request) -> PokemonListSchema:
    pokemons = await get_pokemon_db_models(session, offset, limit)
    if not pokemons:
        return PokemonListSchema(count=0, next=None, previous=None, results=[])

    total = await count_pokemon_db_models(session)
    results = [
        NamedAPIResourceSchema.from_model(
            p, request.app.url_path_for("get_pokemon", id_or_name=p.id)
        )
        for p in pokemons
    ]
    list_path = request.app.url_path_for("list_pokemons")
    next_url, previous_url = build_pagination(list_path, total, offset, limit)

    return PokemonListSchema(
        count=total,
        next=next_url,
        previous=previous_url,
        results=results,
    )


async def get_pokemon(session, id_or_name, request) -> PokemonSchema:
    if not id_or_name.isdigit():
        raise FeatureNotImplementedError("Search by name is not implemented yet")

    pokemon = await get_pokemon_by_id(session, int(id_or_name), request)
    if pokemon is None:
        raise ResourceNotFoundError("Pokemon not found")
    return pokemon


async def get_pokemon_by_id(session, pokemon_id, request) -> PokemonSchema | None:
    pokemon = await get_pokemon_db_model_by_id(session, pokemon_id)
    if not pokemon:
        return None

    abilities = await get_ability_db_models_by_pokemon_id(session, pokemon_id)
    abilities_resources = [
        NamedAPIResourceSchema.from_model(
            a, request.app.url_path_for("get_ability", id_or_name=a.id)
        )
        for a in abilities
    ]
    abilities_info = AbilityInfoSchema.from_resources(abilities_resources)

    return PokemonSchema(
        id=pokemon_id,
        name=pokemon.name,
        abilities=abilities_info,
    )


async def create_pokemon(session, data, request) -> PokemonSchema:
    if await get_pokemon_db_model_by_name(session, data.name):
        raise ResourceConflictError(f"Pokemon '{data.name}' already exists")

    for ability in data.abilities:
        if await get_ability_db_model_by_name(session, ability.name):
            raise ResourceConflictError(f"Ability '{ability.name}' already exists")

    abilities = [a.model_dump() for a in data.abilities]
    pokemon = await create_pokemon_db_model(session, data.name, abilities)
    pokemon_schema = await get_pokemon_by_id(session, pokemon.id, request)
    if pokemon_schema is None:
        raise RuntimeError("Failed to retrieve created Pokemon")
    return pokemon_schema


async def delete_pokemon(session, pokemon_id: int) -> None:
    if await get_pokemon_db_model_by_id(session, pokemon_id) is None:
        raise ResourceNotFoundError("Pokemon not found")

    await delete_pokemon_db_model(session, pokemon_id)

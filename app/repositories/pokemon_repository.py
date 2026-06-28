from sqlalchemy import func, select

from app.db.models import AbilityModel, PokemonModel
from app.repositories.ability_repository import get_ability_db_model_by_name


async def get_pokemon_db_models(session, offset, limit):
    stmt = select(PokemonModel).order_by(PokemonModel.id).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


async def count_pokemon_db_models(session):
    stmt = select(func.count()).select_from(PokemonModel)
    return await session.scalar(stmt)


async def get_pokemon_db_model_by_id(session, pokemon_id):
    stmt = select(PokemonModel).where(PokemonModel.id == pokemon_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_pokemon_db_model(session, name, abilities) -> PokemonModel:
    pokemon = PokemonModel(name=name)

    for ability in abilities:
        existing = await get_ability_db_model_by_name(session, ability["name"])
        if existing:
            pokemon.abilities.append(existing)
        else:
            pokemon.abilities.append(
                AbilityModel(
                    name=ability["name"],
                    effect_entries=ability["effect_entries"],
                )
            )

    session.add(pokemon)
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    await session.refresh(pokemon)
    return pokemon

from sqlalchemy import delete, func, select

from app.db.models import AbilityModel, PokemonModel


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


async def get_pokemon_db_model_by_name(session, name):
    stmt = select(PokemonModel).where(PokemonModel.name == name)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_pokemon_db_model(session, name, abilities) -> PokemonModel:
    pokemon = PokemonModel(name=name)

    for ability in abilities:
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


async def delete_pokemon_db_model(session, pokemon_id) -> None:
    stmt = delete(PokemonModel).where(PokemonModel.id == pokemon_id)
    await session.execute(stmt)
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise

from sqlalchemy import delete, func, select, update
from sqlalchemy.orm import selectinload

from app.db.models import PokemonModel


async def get_pokemon_db_models(session, offset, limit, search=None):
    stmt = select(PokemonModel).order_by(PokemonModel.id)
    if search:
        stmt = stmt.where(PokemonModel.name.ilike(f"%{search}%"))
    stmt = stmt.offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


async def count_pokemon_db_models(session, search=None):
    stmt = select(func.count()).select_from(PokemonModel)
    if search:
        stmt = stmt.where(PokemonModel.name.ilike(f"%{search}%"))
    return await session.scalar(stmt)


async def get_pokemon_db_model_by_id(session, pokemon_id):
    stmt = select(PokemonModel).where(PokemonModel.id == pokemon_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_pokemon_db_model_by_name(session, name):
    stmt = select(PokemonModel).where(PokemonModel.name == name)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_pokemon_db_model(session, name, ability_models) -> PokemonModel:
    pokemon = PokemonModel(name=name)
    pokemon.abilities.extend(ability_models)

    session.add(pokemon)
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    await session.refresh(pokemon)
    return pokemon


async def set_pokemon_abilities(session, pokemon_id, ability_models) -> None:
    stmt = (
        select(PokemonModel)
        .where(PokemonModel.id == pokemon_id)
        .options(selectinload(PokemonModel.abilities))
    )
    pokemon = (await session.execute(stmt)).scalar_one()
    pokemon.abilities = list(ability_models)
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise


async def update_pokemon_db_model(session, pokemon_id, values) -> None:
    stmt = update(PokemonModel).where(PokemonModel.id == pokemon_id).values(**values)
    await session.execute(stmt)
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise


async def delete_pokemon_db_model(session, pokemon_id) -> None:
    stmt = delete(PokemonModel).where(PokemonModel.id == pokemon_id)
    await session.execute(stmt)
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise

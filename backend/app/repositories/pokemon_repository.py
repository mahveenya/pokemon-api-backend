from sqlalchemy import select, func
from app.db.models import PokemonModel


async def get_pokemon_db_models(session, offset, limit):
    stmt = select(PokemonModel).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


async def count_pokemon_db_models(session):
    stmt = select(func.count()).select_from(PokemonModel)
    return await session.scalar(stmt)


async def get_pokemon_db_model_by_id(session, pokemon_id):
    stmt = select(PokemonModel).where(PokemonModel.id == pokemon_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

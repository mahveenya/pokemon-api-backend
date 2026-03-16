from sqlalchemy import select
from app.db.models.ability_model import AbilityModel
from app.db.models.pokemon_ability_model import PokemonAbilityModel


async def get_ability_db_model_by_id(session, ability_id) -> AbilityModel | None:
    stmt = select(AbilityModel).where(AbilityModel.id == ability_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_ability_db_models_by_pokemon_id(
    session, pokemon_id
) -> list[AbilityModel]:
    stmt = (
        select(AbilityModel)
        .join(PokemonAbilityModel)
        .where(PokemonAbilityModel.pokemon_id == pokemon_id)
    )
    result = await session.execute(stmt)
    return result.scalars().all()

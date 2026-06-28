from app.exceptions import FeatureNotImplementedError, ResourceNotFoundError
from app.repositories.ability_repository import get_ability_db_model_by_id
from app.schemas.ability_schema import AbilitySchema


async def get_ability(session, id_or_name) -> AbilitySchema:
    if not id_or_name.isdigit():
        raise FeatureNotImplementedError("Search by name is not implemented yet")

    ability = await get_ability_by_id(session, int(id_or_name))
    if ability is None:
        raise ResourceNotFoundError("Ability not found")
    return ability


async def get_ability_by_id(session, ability_id) -> AbilitySchema | None:
    ability_db_model = await get_ability_db_model_by_id(session, ability_id)
    if not ability_db_model:
        return None

    return AbilitySchema.from_orm_obj(ability_db_model)

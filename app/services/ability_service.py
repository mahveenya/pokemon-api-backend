from app.exceptions import (
    FeatureNotImplementedError,
    ResourceConflictError,
    ResourceNotFoundError,
)
from app.repositories.ability_repository import (
    get_ability_db_model_by_id,
    get_ability_db_model_by_name,
    update_ability_db_model,
)
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


async def update_ability(session, ability_id: int, data) -> AbilitySchema:
    if await get_ability_db_model_by_id(session, ability_id) is None:
        raise ResourceNotFoundError("Ability not found")

    values = data.model_dump(exclude_unset=True)

    if "name" in values:
        existing = await get_ability_db_model_by_name(session, values["name"])
        if existing and existing.id != ability_id:
            raise ResourceConflictError(f"Ability '{values['name']}' already exists")

    if values:
        await update_ability_db_model(session, ability_id, values)

    ability = await get_ability_by_id(session, ability_id)
    if ability is None:
        raise RuntimeError("Failed to retrieve updated Ability")
    return ability

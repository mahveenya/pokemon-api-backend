from app.exceptions import (
    FeatureNotImplementedError,
    ResourceConflictError,
    ResourceNotFoundError,
)
from app.repositories.ability_repository import (
    count_ability_db_models,
    get_ability_db_model_by_id,
    get_ability_db_model_by_name,
    get_ability_db_models,
    update_ability_db_model,
)
from app.schemas.ability_schema import AbilityListSchema, AbilitySchema
from app.schemas.common import NamedAPIResourceSchema
from app.utils.helpers import build_pagination


async def get_ability_list(
    session, offset, limit, request, search=None
) -> AbilityListSchema:
    abilities = await get_ability_db_models(session, offset, limit, search)
    if not abilities:
        return AbilityListSchema(count=0, next=None, previous=None, results=[])

    total = await count_ability_db_models(session, search)
    results = [
        NamedAPIResourceSchema.from_model(
            a, request.app.url_path_for("get_ability", id_or_name=a.id)
        )
        for a in abilities
    ]
    list_path = request.app.url_path_for("list_abilities")
    next_url, previous_url = build_pagination(list_path, total, offset, limit, search)

    return AbilityListSchema(
        count=total,
        next=next_url,
        previous=previous_url,
        results=results,
    )


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

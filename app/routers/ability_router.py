from fastapi import APIRouter, Depends, Request

from app.constants import Endpoints
from app.db.session import get_session
from app.schemas.ability_schema import (
    AbilityListSchema,
    AbilitySchema,
    AbilityUpdateSchema,
)
from app.services.ability_service import get_ability as get_ability_service
from app.services.ability_service import get_ability_list, update_ability

router = APIRouter(prefix=Endpoints.ABILITY_BASE, tags=["ability"])


@router.get("", response_model=AbilityListSchema)
async def list_abilities(
    request: Request,
    offset: int = 0,
    limit: int = 20,
    search: str | None = None,
    session=Depends(get_session),
) -> AbilityListSchema:
    return await get_ability_list(session, offset, limit, request, search)


@router.get(
    "/{id_or_name}",
    response_model=AbilitySchema,
    responses={
        404: {"description": "Ability not found"},
        501: {"description": "Search by name is not implemented yet"},
    },
)
async def get_ability(id_or_name: str, session=Depends(get_session)) -> AbilitySchema:
    return await get_ability_service(session, id_or_name)


@router.patch(
    "/{id}",
    response_model=AbilitySchema,
    responses={
        404: {"description": "Ability not found"},
        409: {"description": "Ability name already exists"},
    },
)
async def update_ability_endpoint(
    id: int,
    payload: AbilityUpdateSchema,
    session=Depends(get_session),
) -> AbilitySchema:
    return await update_ability(session, id, payload)

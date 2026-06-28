from fastapi import APIRouter, Depends

from app.constants import Endpoints
from app.db.session import get_session
from app.schemas.ability_schema import AbilitySchema
from app.services.ability_service import get_ability as get_ability_service

router = APIRouter(prefix=Endpoints.ABILITY_BASE, tags=["ability"])


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

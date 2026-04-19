from fastapi import APIRouter, Depends, HTTPException

from app.constants import Endpoints
from app.db.session import get_session
from app.schemas.ability_schema import AbilitySchema
from app.services.ability_service import get_ability_by_id

router = APIRouter(prefix=Endpoints.ABILITY_BASE, tags=["ability"])


@router.get(
    Endpoints.ABILITY_DETAIL,
    response_model=AbilitySchema,
    responses={
        404: {"description": "Ability not found"},
        501: {"description": "Search by name is not implemented yet"},
    },
)
async def get_ability(id_or_name: str, session=Depends(get_session)) -> AbilitySchema:
    if id_or_name.isdigit():
        ability = await get_ability_by_id(session, int(id_or_name))
        if ability is None:
            raise HTTPException(status_code=404, detail="Ability not found")
        return ability
    else:
        raise HTTPException(
            status_code=501, detail="Search by name is not implemented yet"
        )

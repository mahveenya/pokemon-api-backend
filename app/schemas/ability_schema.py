from typing import Annotated

from pydantic import Field

from app.schemas.base_schema import BaseSchema
from app.schemas.common import NamedAPIResourceSchema
from app.schemas.effect_schema import EffectCreateSchema, EffectSchema


class AbilitySchema(BaseSchema):
    id: int
    name: str
    effect_entries: list[EffectSchema]


class AbilityInfoSchema(BaseSchema):
    ability: NamedAPIResourceSchema

    @classmethod
    def from_resources(cls, resources: list[NamedAPIResourceSchema]):
        return [cls(ability=r) for r in resources]


class AbilityCreateSchema(BaseSchema):
    name: str
    effect_entries: Annotated[list[EffectCreateSchema], Field(min_length=1)]

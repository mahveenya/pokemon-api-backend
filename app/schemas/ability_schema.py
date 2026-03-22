from app.schemas.base_schema import BaseSchema
from app.schemas.common import NamedAPIResourceSchema
from app.schemas.effect_schema import EffectSchema


class AbilitySchema(BaseSchema):
    id: int
    name: str
    effect_entries: list[EffectSchema]


class AbilityInfoSchema(BaseSchema):
    ability: NamedAPIResourceSchema

    @classmethod
    def from_resources(cls, resources: list[NamedAPIResourceSchema]):
        return [cls(ability=r) for r in resources]

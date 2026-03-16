from app.schemas.base_schema import BaseSchema
from app.schemas.common import NamedAPIResourceSchema


class LanguageSchema(BaseSchema):
    name: str


class EffectSchema(BaseSchema):
    effect: str
    short_effect: str
    language: LanguageSchema


class AbilitySchema(BaseSchema):
    id: int
    name: str
    effect_entries: list[EffectSchema]


class AbilityInfoSchema(BaseSchema):
    ability: NamedAPIResourceSchema

    @classmethod
    def from_resources(cls, resources: list[NamedAPIResourceSchema]):
        return [cls(ability=r) for r in resources]

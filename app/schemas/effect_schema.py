from app.schemas.base_schema import BaseSchema
from app.schemas.common import LanguageSchema


class EffectSchema(BaseSchema):
    effect: str | None
    short_effect: str
    language: LanguageSchema


class EffectCreateSchema(BaseSchema):
    effect: str | None
    short_effect: str
    language: LanguageSchema

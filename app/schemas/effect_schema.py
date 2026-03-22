from app.schemas.common import LanguageSchema
from app.schemas.base_schema import BaseSchema


class EffectSchema(BaseSchema):
    effect: str
    short_effect: str
    language: LanguageSchema

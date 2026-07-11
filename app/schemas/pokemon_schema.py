from typing import Annotated

from pydantic import Field

from app.schemas.ability_schema import AbilityInfoSchema
from app.schemas.base_schema import BaseSchema
from app.schemas.common import NamedAPIResourceSchema


class PokemonSchema(BaseSchema):
    id: int
    name: str
    abilities: list[AbilityInfoSchema]


class PokemonListSchema(BaseSchema):
    count: int
    next: str | None
    previous: str | None
    results: list[NamedAPIResourceSchema] = []  # noqa: RUF012


class PokemonCreateSchema(BaseSchema):
    name: str
    ability_ids: Annotated[list[int], Field(min_length=1)]


class PokemonUpdateSchema(BaseSchema):
    name: str | None = None
    ability_ids: list[int] | None = None

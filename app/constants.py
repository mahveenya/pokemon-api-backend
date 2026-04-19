import os

DATABASE_URL = os.environ["DATABASE_URL"]


class Endpoints:
    POKEMON_BASE = "/api/v1/pokemon"
    ABILITY_BASE = "/api/v1/ability"
    POKEMON_DETAIL = "/{id_or_name}"
    ABILITY_DETAIL = "/{id_or_name}"
    HEALTH_CHECK = "/api/v1/health"


class ResourceTypes:
    POKEMON = "pokemon"
    ABILITY = "ability"

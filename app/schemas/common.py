from app.schemas.base_schema import BaseSchema


class LanguageSchema(BaseSchema):
    name: str


class NamedAPIResourceSchema(BaseSchema):
    name: str
    url: str

    @classmethod
    def from_model(cls, model, url):
        return cls(
            name=model.name,
            url=url,
        )

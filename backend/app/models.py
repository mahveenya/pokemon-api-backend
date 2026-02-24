from sqlalchemy import Integer, String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base


class Pokemon(Base):
    __tablename__ = "pokemon"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    weight: Mapped[int] = mapped_column(Integer, nullable=False)

    abilities = relationship(
        "Ability",
        secondary="pokemon_ability",
        back_populates="pokemons",
    )


class Ability(Base):
    __tablename__ = "ability"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    effect: Mapped[str] = mapped_column(Text, nullable=False)

    pokemons = relationship(
        "Pokemon",
        secondary="pokemon_ability",
        back_populates="abilities",
    )


class PokemonAbility(Base):
    __tablename__ = "pokemon_ability"

    pokemon_id: Mapped[int] = mapped_column(
        ForeignKey("pokemon.id", ondelete="CASCADE"),
        primary_key=True,
    )

    ability_id: Mapped[int] = mapped_column(
        ForeignKey("ability.id", ondelete="CASCADE"),
        primary_key=True,
    )

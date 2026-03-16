import asyncio
from app.db.models import AbilityModel, PokemonModel, PokemonAbilityModel
from app.db.session import AsyncSessionLocal


async def prepopulate_database():
    """Prepopulate the database with initial Pokemon and Ability data."""
    async with AsyncSessionLocal() as session:
        abilities_data = [
            {
                "name": "overgrow",
                "effect_entries": [
                    {
                        "effect": "Powers up Grass-type moves when the Pokémon's HP is low.",
                        "language": {"name": "en"},
                    }
                ],
            },
            {
                "name": "blaze",
                "effect_entries": [
                    {
                        "effect": "Powers up Fire-type moves when the Pokémon's HP is low.",
                        "language": {"name": "en"},
                    }
                ],
            },
            {
                "name": "torrent",
                "effect_entries": [
                    {
                        "effect": "Powers up Water-type moves when the Pokémon's HP is low.",
                        "language": {"name": "en"},
                    }
                ],
            },
            {
                "name": "chlorophyll",
                "effect_entries": [
                    {
                        "effect": "Doubles Speed during strong sunlight.",
                        "language": {"name": "en"},
                    }
                ],
            },
        ]

        abilities = []
        for ability_data in abilities_data:
            ability = AbilityModel(**ability_data)
            session.add(ability)
            abilities.append(ability)

        await session.flush()  # Get IDs for abilities

        pokemons_data = [
            {"name": "bulbasaur"},
            {"name": "charmander"},
            {"name": "squirtle"},
            {"name": "venusaur"},
        ]

        pokemons = []
        for pokemon_data in pokemons_data:
            pokemon = PokemonModel(**pokemon_data)
            session.add(pokemon)
            pokemons.append(pokemon)

        await session.flush()  # Get IDs for pokemons

        # Associate abilities with Pokemon
        associations = [
            (pokemons[0], abilities[0]),  # bulbasaur - overgrow
            (pokemons[0], abilities[3]),  # bulbasaur - chlorophyll
            (pokemons[1], abilities[1]),  # charmander - blaze
            (pokemons[2], abilities[2]),  # squirtle - torrent
            (pokemons[3], abilities[0]),  # venusaur - overgrow
            (pokemons[3], abilities[3]),  # venusaur - chlorophyll
        ]

        for pokemon, ability in associations:
            pokemon_ability = PokemonAbilityModel(
                pokemon_id=pokemon.id, ability_id=ability.id
            )
            session.add(pokemon_ability)

        await session.commit()
        print("Database prepopulated successfully!")


if __name__ == "__main__":
    asyncio.run(prepopulate_database())

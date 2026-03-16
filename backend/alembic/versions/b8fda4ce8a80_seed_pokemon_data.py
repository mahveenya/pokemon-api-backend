"""seed pokemon data

Revision ID: b8fda4ce8a80
Revises: a7fda4ce8a79
Create Date: 2026-03-16 00:00:00.000000

"""

import json
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "b8fda4ce8a80"
down_revision: Union[str, Sequence[str], None] = "a7fda4ce8a79"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade: insert seed data."""
    # Insert abilities
    abilities = [
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

    for ability in abilities:
        op.execute(
            sa.text(
                "INSERT INTO ability (name, effect_entries) VALUES (:name, CAST(:effect_entries AS JSON)) ON CONFLICT (name) DO NOTHING"
            ).bindparams(
                name=ability["name"],
                effect_entries=json.dumps(ability["effect_entries"]),
            )
        )

    # Insert pokemon
    op.execute(
        sa.text(
            """
            INSERT INTO pokemon (name) VALUES
            ('bulbasaur'),
            ('charmander'),
            ('squirtle'),
            ('venusaur')
            ON CONFLICT (name) DO NOTHING;
        """
        )
    )

    # Insert pokemon_ability associations

    op.execute(
        sa.text(
            """
            INSERT INTO pokemon_ability (pokemon_id, ability_id)
            SELECT p.id, a.id FROM pokemon p, ability a
            WHERE (p.name, a.name) IN (
                ('bulbasaur', 'overgrow'),
                ('bulbasaur', 'chlorophyll'),
                ('charmander', 'blaze'),
                ('squirtle', 'torrent'),
                ('venusaur', 'overgrow'),
                ('venusaur', 'chlorophyll')
            )
            ON CONFLICT DO NOTHING;
        """
        )
    )


def downgrade() -> None:
    """Downgrade: remove seed data."""
    op.execute(
        sa.text(
            """
            DELETE FROM pokemon_ability WHERE pokemon_id IN (1, 2, 3, 4);
            DELETE FROM pokemon WHERE name IN ('bulbasaur', 'charmander', 'squirtle', 'venusaur');
            DELETE FROM ability WHERE name IN ('overgrow', 'blaze', 'torrent', 'chlorophyll');
        """
        )
    )

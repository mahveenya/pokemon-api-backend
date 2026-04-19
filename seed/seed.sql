BEGIN;

-- Seed abilities
INSERT INTO ability (name, effect_entries) VALUES
('overgrow', $$[{"effect":"When this Pokémon has 1/3 or less of its HP remaining, its grass-type moves inflict 1.5× as much regular damage.","short_effect":"Strengthens grass moves to inflict 1.5× damage at 1/3 max HP or less.","language":{"name":"en"}}]$$::json),
('blaze', $$[{"effect":"When this Pokémon has 1/3 or less of its HP remaining, its fire-type moves inflict 1.5× as much regular damage.","short_effect":"Strengthens fire moves to inflict 1.5× damage at 1/3 max HP or less.","language":{"name":"en"}}]$$::json),
('torrent', $$[{"effect":"When this Pokémon has 1/3 or less of its HP remaining, its water-type moves inflict 1.5× as much regular damage.","short_effect":"Strengthens water moves to inflict 1.5× damage at 1/3 max HP or less.","language":{"name":"en"}}]$$::json),
('chlorophyll', $$[{"effect":"This Pokémon's Speed is doubled during strong sunlight.","short_effect":"Doubles Speed during strong sunlight.","language":{"name":"en"}}]$$::json)
ON CONFLICT (name) DO NOTHING;

-- Seed pokemon
INSERT INTO pokemon (name) VALUES
('bulbasaur'),
('charmander'),
('squirtle'),
('venusaur')
ON CONFLICT (name) DO NOTHING;

-- Seed pokemon_ability associations
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
ON CONFLICT (pokemon_id, ability_id) DO NOTHING;

COMMIT;

---
name: DND.SRD.Skill
description: Look up rules, spells, monsters, classes, races, equipment, and treasure from the D&D 5th Edition System Reference Document (Creative Commons BY 4.0).
user-invocable: true
---

# D&D 5th Edition System Reference Document (SRD v5.1)

This repository contains the complete D&D 5th Edition Systems Reference Document, converted to Markdown. It is the official open reference for D&D 5e core rules, published by Wizards of the Coast under the Creative Commons Attribution 4.0 International Licence (CC-BY-4.0).

The SRD does not contain all D&D 5e content — it covers one subclass per class, a subset of spells, monsters, and magic items, and the core rules framework.

## Content Structure

### Core Rules

| Directory | What It Contains |
|---|---|
| `Gameplay/Abilities.md` | Ability scores, modifiers, ability checks, saving throws, advantage/disadvantage |
| `Gameplay/Combat.md` | Initiative, attack rolls, damage, movement, actions, conditions in combat |
| `Gameplay/Adventuring.md` | Time, movement, resting, travel, environment, social interaction |

### Character Building

| Directory | What It Contains |
|---|---|
| `Races/` | Racial traits and subraces — one file per race: `Dragonborn.md`, `Dwarf.md`, `Elf.md`, `Gnome.md`, `Half-Elf.md`, `Halfling.md`, `Half-Orc.md`, `Human.md`, `Tiefling.md`. General racial traits in `# Racial Traits.md` |
| `Classes/` | Class features, subclasses, and spell lists — one file per class: `Barbarian.md`, `Bard.md`, `Cleric.md`, `Druid.md`, `Fighter.md`, `Monk.md`, `Paladin.md`, `Ranger.md`, `Rogue.md`, `Sorcerer.md`, `Warlock.md`, `Wizard.md` |
| `Characterizations/` | `Alignment.md`, `Backgrounds.md`, `Beyond 1st Level.md`, `Feats.md`, `Inspiration.md`, `Languages.md`, `Multiclassing.md` |

### Spells

| Directory | What It Contains |
|---|---|
| `Spells/` | One file per spell, named exactly (e.g. `Fireball.md`, `Acid Arrow.md`, `Cure Wounds.md`). Each includes: level, school, casting time, range, components, duration, description, and higher-level scaling |
| `Spells (Alt)/` | The same spells grouped into larger files by letter or category |

### Monsters & Creatures

| Directory | What It Contains |
|---|---|
| `Monsters/` | One file per monster. Each stat block includes: size/type/alignment, AC, HP, speed, ability scores, saves, skills, senses, languages, challenge rating, traits, and actions |
| `Monsters (Alt)/` | The same monsters grouped into larger files alphabetically (`Monsters A.md` ... `Monsters Z.md`) and by creature type (`Creatures A-C.md` etc.). Also includes `NPCs.md` and `# Monster Statistics.md` |

**Monster file naming conventions:**
- Standard: `{Name}.md` (e.g. `Aboleth.md`)
- Dragons: `{Age} {Colour} Dragon ({Type}).md` (e.g. `Adult Red Dragon (Chromatic).md`, `Ancient Gold Dragon (Metallic).md`)
- NPCs: `{Name} (NPC).md` (e.g. `Archmage (NPC).md`, `Acolyte (NPC).md`)
- Creatures/beasts: `{Name} (Creature).md` (e.g. `Baboon (Creature).md`, `Axe Beak (Creature).md`)

### Equipment

| Directory | What It Contains |
|---|---|
| `Equipment/Armor.md` | Armour types, AC, properties |
| `Equipment/Weapons.md` | Weapon types, damage, properties, martial/simple |
| `Equipment/Gear.md` | Adventuring gear, packs, equipment lists |
| `Equipment/Tools.md` | Artisan's tools, gaming sets, musical instruments |
| `Equipment/Coinage.md` | Currency and exchange rates |
| `Equipment/Expenses.md` | Lifestyle expenses, services, food/lodging |
| `Equipment/Trade Goods.md` | Trade goods and values |
| `Equipment/Transportation.md` | Mounts, vehicles, travel |
| `Equipment/Selling Treasure.md` | Rules for selling loot |

### Treasure & Magic Items

| Directory | What It Contains |
|---|---|
| `Treasure/` | One file per magic item (e.g. `Bag of Holding.md`, `Vorpal Sword.md`, `Deck of Many Things.md`). Includes rarity, attunement, and description. Also `# Magic Items.md` (overview), `## Artifacts.md`, and `## Sentient Magic.md` |
| `Treasure (Alt)/` | The same items grouped into larger files |

### Gamemastering

| Directory | What It Contains |
|---|---|
| `Gamemastering/Conditions.md` | All conditions (Blinded, Charmed, Frightened, etc.) |
| `Gamemastering/Diseases.md` | Disease mechanics and examples |
| `Gamemastering/Madness.md` | Madness effects and tables |
| `Gamemastering/Objects.md` | Object AC, HP, and interactions |
| `Gamemastering/Pantheons.md` | Deity lists and domains |
| `Gamemastering/Planes.md` | Planar descriptions |
| `Gamemastering/Poisons.md` | Poison types and effects |
| `Gamemastering/Traps.md` | Trap mechanics and examples |

## Finding Content

- **By exact name**: Read the file directly — `Spells/Fireball.md`, `Monsters/Aboleth.md`, `Treasure/Bag of Holding.md`
- **By partial name**: Glob with a wildcard — `Spells/*Fire*.md`, `Monsters/*Dragon*.md`
- **By keyword in content**: Grep across the relevant directory — e.g. searching for "sneak attack" in `Classes/`, or "resistance" in `Gamemastering/Conditions.md`
- **Prefer the individual file directories** (`Spells/`, `Monsters/`, `Treasure/`) for targeted lookups. Use the `(Alt)` directories when browsing or when you need multiple entries at once.

## Licence

This work includes material taken from the System Reference Document 5.1 ("SRD 5.1") by Wizards of the Coast LLC. The SRD 5.1 is licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/legalcode).

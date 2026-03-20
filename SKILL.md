---
name: dnd-srd
description: Reference the D&D 5e SRD for text-based games, TTRPGs, D&D sessions, and rules lookups. Covers rules, spells, monsters, classes, species, equipment, and treasure (Creative Commons BY 4.0).
user-invocable: true
metadata:
  version: 5.2.1
---

# D&D 5th Edition System Reference Document (SRD v5.2.1)

This repository contains the complete D&D 5th Edition Systems Reference Document (v5.2.1), converted to Markdown. It is the official open reference for D&D 5e core rules, published by Wizards of the Coast under the Creative Commons Attribution 4.0 International Licence (CC-BY-4.0).

Use this skill when the user wants to play a text-based game, run a TTRPG session, play D&D, look up rules, or reference any D&D 5e content. Read the relevant files to provide accurate, source-backed answers and game content.

The SRD does not contain all D&D 5e content — it covers one subclass per class, a subset of spells, monsters, and magic items, and the core rules framework.

## Content Structure

### Core Rules

| Directory | What It Contains |
|---|---|
| `Gameplay/Abilities.md` | Ability scores, modifiers, D20 Tests, saving throws, Heroic Inspiration, proficiency |
| `Gameplay/Combat.md` | Actions (Attack, Dash, Dodge, Help, Hide, Influence, Magic, Ready, Search, Study, Utilize), combat, damage/healing |
| `Gameplay/Adventuring.md` | Exploration, vision/light, hiding, hazards, travel, social interaction |
| `Rules Glossary/Rules Glossary.md` | Alphabetical definitions of all game terms, conditions, and actions |

### Character Building

| Directory | What It Contains |
|---|---|
| `Species/` | Species traits — one file per species: `Dragonborn.md`, `Dwarf.md`, `Elf.md`, `Gnome.md`, `Goliath.md`, `Halfling.md`, `Human.md`, `Orc.md`, `Tiefling.md` |
| `Classes/` | Class features, subclasses, and embedded spell lists — one file per class: `Barbarian.md`, `Bard.md`, `Cleric.md`, `Druid.md`, `Fighter.md`, `Monk.md`, `Paladin.md`, `Ranger.md`, `Rogue.md`, `Sorcerer.md`, `Warlock.md`, `Wizard.md` |
| `Characterizations/` | `Backgrounds.md` (Acolyte, Criminal, Sage, Soldier), `Feats.md` (Origin, General, Fighting Style, Epic Boon), `Languages.md`, `Multiclassing.md`, `Trinkets.md` |

### Spells

| Directory | What It Contains |
|---|---|
| `Spells/Spellcasting.md` | General spellcasting rules (preparation, casting, components, slots) |
| `Spells/` | One file per spell (e.g. `Fireball.md`, `Acid Arrow.md`). Each includes: level, school, class list, casting time, range, components, duration, description |
| `Spells (Alt)/` | The same spells grouped by first letter (`Spells A.md` ... `Spells Z.md`) |

### Monsters & Animals

| Directory | What It Contains |
|---|---|
| `Monsters/` | One file per monster/NPC. Stat blocks include: size/type/alignment, AC, Initiative, HP, speed, ability scores with saves, CR, traits, actions, bonus actions, reactions, legendary actions |
| `Monsters (Alt)/` | The same monsters grouped alphabetically (`Monsters A.md` ... `Monsters Z.md`) |
| `Animals/` | One file per beast/animal. Same stat block format as monsters |
| `Animals (Alt)/` | Animals grouped alphabetically |

**Monster file naming conventions:**
- Standard: `{Name}.md` (e.g. `Aboleth.md`, `Goblin Warrior.md`)
- Dragons: `{Age} {Colour} Dragon.md` (e.g. `Adult Red Dragon.md`, `Ancient Gold Dragon.md`)
- Wyrmlings: `{Colour} Dragon Wyrmling.md` (e.g. `Red Dragon Wyrmling.md`)
- NPCs are mixed in alphabetically (no `(NPC)` suffix): `Archmage.md`, `Priest Acolyte.md`, `Spy.md`

**Omitted monsters** (use listed replacements): Duergar (use Spy), Elf/Drow (use Priest Acolyte), Deep Gnome (use Scout), Lizardfolk (use Scout), Orc (use Tough).

### Equipment

| Directory | What It Contains |
|---|---|
| `Equipment/Weapons.md` | Weapon tables, properties, and Mastery Properties (new in 5.2.1) |
| `Equipment/Armor.md` | Armour types, Armour Training, armour table |
| `Equipment/Tools.md` | Artisan's Tools and Other Tools with structured rules |
| `Equipment/Gear.md` | Adventuring gear descriptions and table |
| `Equipment/Coinage.md` | Currency and coin values |
| `Equipment/Expenses.md` | Lifestyle expenses, food/lodging, hirelings, spellcasting services |
| `Equipment/Transportation.md` | Mounts, vehicles, Large Vehicles |
| `Equipment/Crafting.md` | Crafting nonmagical items, brewing potions, scribing spell scrolls |
| `Equipment/Selling Treasure.md` | Rules for selling equipment |

### Treasure & Magic Items

| Directory | What It Contains |
|---|---|
| `Treasure/` | One file per magic item (e.g. `Bag of Holding.md`, `Vorpal Sword.md`, `Mysterious Deck.md`). Includes rarity, attunement, and description |
| `Treasure (Alt)/` | The same items grouped by first letter |

### Gameplay Toolbox (Gamemastering)

| Directory | What It Contains |
|---|---|
| `Gamemastering/Travel.md` | Travel pace, terrain, extended travel, vehicles |
| `Gamemastering/Curses.md` | Curse types and examples |
| `Gamemastering/Magical Contagions.md` | Contagion mechanics (formerly Diseases) |
| `Gamemastering/Environmental Effects.md` | Extreme weather, hazardous terrain |
| `Gamemastering/Fear and Mental Stress.md` | Fear effects and mental stress (formerly Madness) |
| `Gamemastering/Poisons.md` | Poison types, purchasing, harvesting |
| `Gamemastering/Traps.md` | Trap mechanics (nuisance/deadly) |
| `Gamemastering/Combat Encounters.md` | Encounter building and XP budgets |
| `Gamemastering/Creating a Background.md` | Custom background creation rules |

## Finding Content

- **By exact name**: Read the file directly — `Spells/Fireball.md`, `Monsters/Aboleth.md`, `Treasure/Bag of Holding.md`
- **By partial name**: Glob with a wildcard — `Spells/*Fire*.md`, `Monsters/*Dragon*.md`
- **By keyword in content**: Grep across the relevant directory — e.g. searching for "sneak attack" in `Classes/`, or "Exhaustion" in `Rules Glossary/`
- **For conditions and game terms**: Check `Rules Glossary/Rules Glossary.md` first
- **For spell lists**: Check the class file directly (spell lists are embedded in each class)
- **Prefer the individual file directories** (`Spells/`, `Monsters/`, `Treasure/`) for targeted lookups. Use the `(Alt)` directories when browsing or when you need multiple entries at once.

## Licence

This work includes material from the System Reference Document 5.2.1 ("SRD 5.2.1") by Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd. The SRD 5.2.1 is licensed under the Creative Commons Attribution 4.0 International License, available at https://creativecommons.org/licenses/by/4.0/legalcode.

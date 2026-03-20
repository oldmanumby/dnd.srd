#!/usr/bin/env python3
"""
Extract and format SRD 5.2.1 content from raw PDF-to-text into individual Markdown files.

Usage:
    python scripts/extract.py spells
    python scripts/extract.py monsters
    python scripts/extract.py animals
    python scripts/extract.py magic-items
    python scripts/extract.py all
"""

import re
import sys
from pathlib import Path

# Project root
ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "5.2.1.md"

# Page artifact pattern: lines like "107 System Reference Document 5.2.1"
PAGE_ARTIFACT = re.compile(r"^\d+ System Reference Document 5\.2\.1$")

# --- Section line ranges (approximate, from analysis) ---
SECTIONS = {
    "spells": (9183, 15924),
    "monsters": (23367, 31077),
    "animals": (31078, 32912),
    "magic_items": (18760, 23022),
}

# --- Creature sizes for monster/animal boundary detection ---
SIZES = {"Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan"}

# --- Spell level/school pattern ---
# Matches "Level 2 Evocation (Wizard)" or "Evocation Cantrip (Sorcerer, Wizard)"
# Matches complete or partial level lines (class list may wrap to next line)
SPELL_LEVEL_RE = re.compile(
    r"^(?:Level (\d+) (\w+)|(\w+) Cantrip) \((.+?)(?:\))?$"
)

# --- Monster/Animal stat line patterns ---
CREATURE_TYPE_RE = re.compile(
    r"^(Tiny|Small|Medium|Large|Huge|Gargantuan) "
    r"(\w[\w ]*?)(?:\s*\([\w\s,]+\))?,\s*(.+)$"
)
AC_INIT_RE = re.compile(r"^AC \d+")

# --- Magic item category/rarity pattern ---
ITEM_CATEGORIES = {
    "Armor", "Weapon", "Potion", "Ring", "Rod", "Staff", "Wand",
    "Wondrous Item", "Scroll",
}
ITEM_RARITY_RE = re.compile(
    r"^(Armor|Weapon|Potion|Ring|Rod|Staff|Wand|Wondrous Item|Scroll)"
    r"(?:\s*\([^)]+\))?,\s*"
    r"(Common|Uncommon|Rare|Very Rare|Legendary|Artifact)"
)
# Category line without rarity (rarity on next line)
ITEM_CATEGORY_RE = re.compile(
    r"^(Armor|Weapon|Potion|Ring|Rod|Staff|Wand|Wondrous Item|Scroll)"
    r"\s*\([^)]+\),?\s*$"
)


def read_source():
    """Read the full source file and return as list of lines."""
    with open(SOURCE, "r", encoding="utf-8") as f:
        return f.readlines()


def read_section(lines, start, end):
    """Extract a section by line numbers (1-indexed) and strip page artifacts."""
    section = []
    for line in lines[start - 1 : end]:
        stripped = line.rstrip("\n")
        if PAGE_ARTIFACT.match(stripped):
            continue
        section.append(stripped)
    return section


def write_file(directory, filename, content):
    """Write content to a file, creating directories as needed."""
    directory.mkdir(parents=True, exist_ok=True)
    filepath = directory / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


def sanitise_filename(name):
    """Convert a name to a safe filename."""
    # Replace characters that are problematic in filenames
    name = name.replace("/", "-").replace("\\", "-")
    name = name.replace(":", " -").replace("*", "")
    name = name.replace("?", "").replace('"', "").replace("<", "").replace(">", "")
    name = name.replace("|", "-")
    return name.strip()


# =============================================================================
# SPELL EXTRACTION
# =============================================================================

def find_spell_boundaries(section_lines):
    """Find spell name + level line pairs to identify spell boundaries."""
    boundaries = []
    i = 0
    while i < len(section_lines) - 1:
        line = section_lines[i].strip()
        next_line = section_lines[i + 1].strip() if i + 1 < len(section_lines) else ""

        if SPELL_LEVEL_RE.match(next_line) and line and not line.startswith("Casting Time"):
            # This line is a spell name, next line is the level/school
            boundaries.append(i)
        i += 1
    return boundaries


def extract_spells(lines):
    """Extract individual spells from the source."""
    start, end = SECTIONS["spells"]
    section = read_section(lines, start, end)

    # Skip the "Spell Descriptions" header line
    # Find where actual spell content starts
    spell_start = 0
    for i, line in enumerate(section):
        if line.strip() == "Spell Descriptions":
            spell_start = i + 1
            break

    section = section[spell_start:]
    boundaries = find_spell_boundaries(section)

    spells = {}
    for idx, boundary in enumerate(boundaries):
        # Determine end of this spell
        if idx + 1 < len(boundaries):
            spell_end = boundaries[idx + 1]
        else:
            spell_end = len(section)

        spell_lines = section[boundary:spell_end]
        name = spell_lines[0].strip()
        body_lines = spell_lines[1:]

        # Format to markdown
        md = format_spell_md(name, body_lines)
        spells[name] = md

    return spells


def format_spell_md(name, body_lines):
    """Format raw spell lines into proper Markdown."""
    md_lines = [f"### {name}", ""]

    # First line should be level/school (class list may wrap)
    if body_lines:
        level_line = body_lines[0].strip()
        consumed = 1
        # Join wrapped class list lines
        while not level_line.endswith(")") and consumed < len(body_lines):
            level_line += " " + body_lines[consumed].strip()
            consumed += 1
        match = re.match(r"^(?:Level (\d+) (\w+)|(\w+) Cantrip) \((.+)\)$", level_line)
        if match:
            level_num, school1, school2, classes = match.groups()
            if level_num:
                md_lines.append(f"*Level {level_num} {school1}* ({classes})")
            else:
                md_lines.append(f"*{school2} Cantrip* ({classes})")
            md_lines.append("")
            body_lines = body_lines[consumed:]

    # Process remaining lines
    i = 0
    in_description = False
    while i < len(body_lines):
        line = body_lines[i].strip()

        # Skip empty lines at the start
        if not line and not in_description:
            i += 1
            continue

        # Bold labels for spell properties
        if line.startswith("Casting Time:"):
            md_lines.append(f"**Casting Time:** {line[len('Casting Time:'):].strip()}")
            md_lines.append("")
        elif line.startswith("Range:"):
            md_lines.append(f"**Range:** {line[len('Range:'):].strip()}")
            md_lines.append("")
        elif line.startswith("Components:"):
            # Components may span multiple lines
            comp_text = line[len("Components:"):].strip()
            # Check if next lines are continuation (no colon label)
            while (i + 1 < len(body_lines) and
                   body_lines[i + 1].strip() and
                   not body_lines[i + 1].strip().startswith("Duration:")):
                i += 1
                comp_text += " " + body_lines[i].strip()
            md_lines.append(f"**Components:** {comp_text}")
            md_lines.append("")
        elif line.startswith("Duration:"):
            md_lines.append(f"**Duration:** {line[len('Duration:'):].strip()}")
            md_lines.append("")
            in_description = True
        elif line.startswith("Using a Higher-Level Spell Slot."):
            text = line[len("Using a Higher-Level Spell Slot."):].strip()
            # Join continuation only if text doesn't end with a complete sentence
            while (text and not text.endswith(".") and not text.endswith(")") and
                   i + 1 < len(body_lines) and body_lines[i + 1].strip()):
                i += 1
                text += " " + body_lines[i].strip()
            md_lines.append(f"***Using a Higher-Level Spell Slot.*** {text}")
            break  # Nothing meaningful after this in a spell
        elif line.startswith("Cantrip Upgrade."):
            md_lines.append(f"***Cantrip Upgrade.*** {line[len('Cantrip Upgrade.'):].strip()}")
            while (i + 1 < len(body_lines) and body_lines[i + 1].strip()):
                i += 1
                md_lines[-1] += " " + body_lines[i].strip()
            break  # Nothing meaningful after this in a spell
        elif in_description:
            if not line:
                md_lines.append("")
            else:
                # Regular description paragraph
                para = line
                while (i + 1 < len(body_lines) and
                       body_lines[i + 1].strip() and
                       not body_lines[i + 1].strip().startswith("Using a Higher-Level") and
                       not body_lines[i + 1].strip().startswith("Cantrip Upgrade.")):
                    next_stripped = body_lines[i + 1].strip()
                    # Check if next line is a sub-heading (e.g. "Audible Alarm.")
                    # These are lines that end with a period and are followed by description
                    # Actually, let's just join continuation lines
                    i += 1
                    para += " " + next_stripped
                md_lines.append(para)
                md_lines.append("")

        i += 1

    # Clean up trailing empty lines
    while md_lines and md_lines[-1] == "":
        md_lines.pop()
    md_lines.append("")

    return "\n".join(md_lines)


# =============================================================================
# MONSTER / ANIMAL EXTRACTION
# =============================================================================

def find_creature_boundaries(section_lines):
    """Find creature stat block boundaries."""
    boundaries = []
    i = 0
    while i < len(section_lines) - 2:
        line = section_lines[i].strip()
        next_line = section_lines[i + 1].strip() if i + 1 < len(section_lines) else ""

        # A creature boundary is: Name line, then Size/Type/Alignment line,
        # then AC line. Also filter out lines that are clearly not names.
        line_after = section_lines[i + 2].strip() if i + 2 < len(section_lines) else ""
        if (line and
            CREATURE_TYPE_RE.match(next_line) and
            line_after.startswith("AC ") and
            not line.startswith("AC ") and
            not line.startswith("MOD ") and
            not line.startswith("Str ") and
            not line.startswith("HP ") and
            not line[0].isdigit()):
            boundaries.append(i)

        i += 1

    return boundaries


def extract_creatures(lines, section_key):
    """Extract individual creature stat blocks (monsters or animals)."""
    start, end = SECTIONS[section_key]
    section = read_section(lines, start, end)

    # Skip header lines (e.g. "Monsters A–Z" or "Animals")
    content_start = 0
    for i, line in enumerate(section):
        stripped = line.strip()
        if stripped in ("Monsters A–Z", "Animals"):
            content_start = i + 1
            break

    section = section[content_start:]

    # Handle the case where monster name is repeated on two consecutive lines
    # (e.g. "Aboleth\nAboleth\nLarge Aberration...")
    boundaries = find_creature_boundaries(section)

    creatures = {}
    for idx, boundary in enumerate(boundaries):
        if idx + 1 < len(boundaries):
            creature_end = boundaries[idx + 1]
        else:
            creature_end = len(section)

        creature_lines = section[boundary:creature_end]

        # Get name - check if name is repeated
        name = creature_lines[0].strip()
        body_start = 1
        if body_start < len(creature_lines) and creature_lines[body_start].strip() == name:
            body_start = 1  # Keep the repeated name — it's the stat block header

        body_lines = creature_lines[body_start:]
        md = format_creature_md(name, body_lines)
        creatures[name] = md

    return creatures


def format_creature_md(name, body_lines):
    """Format raw creature stat block lines into proper Markdown."""
    md_lines = [f"## {name}", ""]

    i = 0
    while i < len(body_lines):
        line = body_lines[i].strip()

        if not line:
            i += 1
            continue

        # Size/Type/Alignment line
        if CREATURE_TYPE_RE.match(line):
            md_lines.append(f"*{line}*")
            md_lines.append("")
        # AC and Initiative
        elif line.startswith("AC "):
            md_lines.append(f"**{line}**")
            md_lines.append("")
        # HP
        elif line.startswith("HP "):
            md_lines.append(f"**{line}**")
            md_lines.append("")
        # Speed
        elif line.startswith("Speed "):
            md_lines.append(f"**{line}**")
            md_lines.append("")
        # Ability score header
        elif line == "MOD SAVE MOD SAVE MOD SAVE":
            # Next two lines are the ability scores
            scores = []
            for j in range(1, 3):
                if i + j < len(body_lines):
                    scores.append(body_lines[i + j].strip())
            md_lines.append("")
            md_lines.append("| | MOD | SAVE | | MOD | SAVE |")
            md_lines.append("|---|:---:|:---:|---|:---:|:---:|")
            # Parse the ability score lines
            for score_line in scores:
                parts = score_line.split()
                if len(parts) >= 9:
                    # e.g. "Str 21 +5 +5 Dex 9 −1 +3 Con 15 +2 +6"
                    md_lines.append(
                        f"| **{parts[0]}** {parts[1]} | {parts[2]} | {parts[3]} "
                        f"| **{parts[4]}** {parts[5]} | {parts[6]} | {parts[7]} "
                        f"| **{parts[8]}** {parts[9] if len(parts) > 9 else ''} "
                        f"| {parts[10] if len(parts) > 10 else ''} | {parts[11] if len(parts) > 11 else ''} |"
                    )
            md_lines.append("")
            i += 2  # Skip the score lines we already processed
        # CR line
        elif line.startswith("CR "):
            md_lines.append(f"**{line}**")
            md_lines.append("")
        # Section headings within stat block
        elif line in ("Traits", "Actions", "Bonus Actions", "Reactions", "Legendary Actions"):
            md_lines.append(f"### {line}")
            md_lines.append("")
        # Property lines (Skills, Senses, Languages, Resistances, Immunities, Gear, etc.)
        elif any(line.startswith(prop) for prop in (
            "Skills ", "Senses ", "Languages ", "Resistances ", "Immunities ",
            "Gear ", "Damage Resistances ", "Damage Immunities ",
            "Condition Immunities ",
        )):
            md_lines.append(f"**{line}**")
            md_lines.append("")
        else:
            # Regular text (trait/action descriptions)
            # Join continuation lines
            para = line
            while (i + 1 < len(body_lines) and
                   body_lines[i + 1].strip() and
                   not body_lines[i + 1].strip().startswith("AC ") and
                   not body_lines[i + 1].strip().startswith("HP ") and
                   not body_lines[i + 1].strip().startswith("Speed ") and
                   not body_lines[i + 1].strip().startswith("CR ") and
                   not body_lines[i + 1].strip().startswith("MOD SAVE") and
                   not body_lines[i + 1].strip() in ("Traits", "Actions", "Bonus Actions", "Reactions", "Legendary Actions") and
                   not CREATURE_TYPE_RE.match(body_lines[i + 1].strip())):
                next_line = body_lines[i + 1].strip()
                if not next_line:
                    break
                # Check if next line starts a new action/trait (name followed by period)
                # e.g. "Multiattack. The aboleth..."
                # Only break if it looks like a new entry heading
                if (re.match(r"^[A-Z][\w\s()/]+\.", next_line) and
                    not para.endswith(",") and
                    not para.endswith("and") and
                    not para.endswith("or")):
                    break
                i += 1
                para += " " + next_line
            md_lines.append(para)
            md_lines.append("")

        i += 1

    # Clean up trailing empty lines
    while md_lines and md_lines[-1] == "":
        md_lines.pop()
    md_lines.append("")

    return "\n".join(md_lines)


# =============================================================================
# MAGIC ITEM EXTRACTION
# =============================================================================

def find_magic_item_boundaries(section_lines):
    """Find magic item boundaries."""
    boundaries = []
    i = 0
    while i < len(section_lines) - 1:
        line = section_lines[i].strip()
        next_line = section_lines[i + 1].strip() if i + 1 < len(section_lines) else ""

        # An item boundary is: Name line, then Category/Rarity line
        # Rarity may be on same line as category, or on the next line
        is_cat = ITEM_RARITY_RE.match(next_line) or ITEM_CATEGORY_RE.match(next_line)
        # Also check i+2 for multi-line names (name continuation on i+1)
        line_after = section_lines[i + 2].strip() if i + 2 < len(section_lines) else ""
        is_cat_2 = (not is_cat and next_line and next_line[0].islower() and
                    (ITEM_RARITY_RE.match(line_after) or ITEM_CATEGORY_RE.match(line_after)))
        cat_kws = ("Armor", "Weapon", "Potion", "Wondrous", "Ring", "Rod", "Staff", "Wand", "Scroll", "or ")
        is_name = line and not any(line.startswith(k) for k in cat_kws) and not line[0].islower()
        if (is_cat or is_cat_2) and is_name:
            boundaries.append(i)

        i += 1

    return boundaries


def extract_magic_items(lines):
    """Extract individual magic items from the source."""
    start, end = SECTIONS["magic_items"]
    section = read_section(lines, start, end)

    # Skip header
    content_start = 0
    for i, line in enumerate(section):
        if line.strip() == "Magic Items A–Z":
            content_start = i + 1
            break

    # Skip introductory paragraph until we hit the first item
    while content_start < len(section):
        line = section[content_start].strip()
        if line and content_start + 1 < len(section):
            next_l = section[content_start + 1].strip()
            if ITEM_RARITY_RE.match(next_l) or ITEM_CATEGORY_RE.match(next_l):
                break
        content_start += 1

    section = section[content_start:]
    boundaries = find_magic_item_boundaries(section)

    items = {}
    for idx, boundary in enumerate(boundaries):
        if idx + 1 < len(boundaries):
            item_end = boundaries[idx + 1]
        else:
            item_end = len(section)

        item_lines = section[boundary:item_end]
        name = item_lines[0].strip()

        # Handle multi-line names (e.g. "Amulet of Proof against Detection\nand Location")
        body_start = 1
        if (body_start < len(item_lines) and
            not ITEM_RARITY_RE.match(item_lines[body_start].strip()) and
            item_lines[body_start].strip()):
            # This might be continuation of the name
            potential_continuation = item_lines[body_start].strip()
            if (body_start + 1 < len(item_lines) and
                ITEM_RARITY_RE.match(item_lines[body_start + 1].strip())):
                name = name + " " + potential_continuation
                body_start = 2

        body_lines = item_lines[body_start:]
        md = format_magic_item_md(name, body_lines)
        items[name] = md

    return items


def format_magic_item_md(name, body_lines):
    """Format raw magic item lines into proper Markdown."""
    md_lines = [f"### {name}", ""]

    i = 0
    if body_lines:
        # First line is category/rarity
        rarity_line = body_lines[0].strip()
        # May span multiple lines if long
        while (i + 1 < len(body_lines) and
               not body_lines[i + 1].strip() == "" and
               not any(c.islower() for c in body_lines[i + 1].strip()[:5]) is False):
            # Check if next line continues the rarity description
            next_stripped = body_lines[i + 1].strip()
            if next_stripped.startswith("or ") or next_stripped.startswith("("):
                rarity_line += " " + next_stripped
                i += 1
            else:
                break
        md_lines.append(f"*{rarity_line}*")
        md_lines.append("")
        i += 1

    # Process remaining lines as description
    while i < len(body_lines):
        line = body_lines[i].strip()

        if not line:
            md_lines.append("")
            i += 1
            continue

        # Table lines (e.g. "1d100 Creature Type...")
        if re.match(r"^\d+[d–]\d+", line) or line.startswith("1d"):
            md_lines.append(line)
        else:
            # Regular paragraph - join continuation lines
            para = line
            while (i + 1 < len(body_lines) and
                   body_lines[i + 1].strip() and
                   not re.match(r"^\d+[d–]\d+", body_lines[i + 1].strip()) and
                   not body_lines[i + 1].strip().startswith("1d")):
                next_stripped = body_lines[i + 1].strip()
                i += 1
                para += " " + next_stripped
            md_lines.append(para)

        md_lines.append("")
        i += 1

    # Clean up trailing empty lines
    while md_lines and md_lines[-1] == "":
        md_lines.pop()
    md_lines.append("")

    return "\n".join(md_lines)


# =============================================================================
# GROUPED (ALT) FILE GENERATION
# =============================================================================

def generate_alt_files(items, output_dir, prefix):
    """Generate grouped files by first letter (for Alt directories)."""
    output_dir.mkdir(parents=True, exist_ok=True)
    grouped = {}
    for name, content in sorted(items.items()):
        letter = name[0].upper()
        if letter not in grouped:
            grouped[letter] = []
        grouped[letter].append(content)

    for letter, contents in sorted(grouped.items()):
        filename = f"{prefix} {letter}.md"
        combined = "\n".join(contents)
        write_file(output_dir, filename, combined)

    print(f"  Generated {len(grouped)} grouped files in {output_dir}")


# =============================================================================
# MAIN EXTRACTION COMMANDS
# =============================================================================

def cmd_spells():
    """Extract all spells."""
    print("Extracting spells...")
    lines = read_source()
    spells = extract_spells(lines)

    output_dir = ROOT / "Spells"
    # Clear existing spell files
    if output_dir.exists():
        for f in output_dir.glob("*.md"):
            f.unlink()

    for name, content in spells.items():
        filename = f"{sanitise_filename(name)}.md"
        write_file(output_dir, filename, content)

    print(f"  Extracted {len(spells)} spells to {output_dir}")

    # Generate Alt files
    alt_dir = ROOT / "Spells (Alt)"
    if alt_dir.exists():
        for f in alt_dir.glob("*.md"):
            f.unlink()
    generate_alt_files(spells, alt_dir, "Spells")

    return spells


def cmd_monsters():
    """Extract all monsters."""
    print("Extracting monsters...")
    lines = read_source()
    monsters = extract_creatures(lines, "monsters")

    output_dir = ROOT / "Monsters"
    # Clear existing monster files
    if output_dir.exists():
        for f in output_dir.glob("*.md"):
            f.unlink()

    for name, content in monsters.items():
        filename = f"{sanitise_filename(name)}.md"
        write_file(output_dir, filename, content)

    print(f"  Extracted {len(monsters)} monsters to {output_dir}")

    # Generate Alt files
    alt_dir = ROOT / "Monsters (Alt)"
    if alt_dir.exists():
        for f in alt_dir.glob("*.md"):
            f.unlink()
    generate_alt_files(monsters, alt_dir, "Monsters")

    return monsters


def cmd_animals():
    """Extract all animals."""
    print("Extracting animals...")
    lines = read_source()
    animals = extract_creatures(lines, "animals")

    output_dir = ROOT / "Animals"
    output_dir.mkdir(parents=True, exist_ok=True)

    for name, content in animals.items():
        filename = f"{sanitise_filename(name)}.md"
        write_file(output_dir, filename, content)

    print(f"  Extracted {len(animals)} animals to {output_dir}")

    # Generate Alt files
    alt_dir = ROOT / "Animals (Alt)"
    alt_dir.mkdir(parents=True, exist_ok=True)
    generate_alt_files(animals, alt_dir, "Animals")

    return animals


def cmd_magic_items():
    """Extract all magic items."""
    print("Extracting magic items...")
    lines = read_source()
    items = extract_magic_items(lines)

    output_dir = ROOT / "Treasure"
    # Clear existing item files (but keep overview files)
    if output_dir.exists():
        for f in output_dir.glob("*.md"):
            if not f.name.startswith("#") and not f.name.startswith("##"):
                f.unlink()

    for name, content in items.items():
        filename = f"{sanitise_filename(name)}.md"
        write_file(output_dir, filename, content)

    print(f"  Extracted {len(items)} magic items to {output_dir}")

    # Generate Alt files
    alt_dir = ROOT / "Treasure (Alt)"
    if alt_dir.exists():
        for f in alt_dir.glob("*.md"):
            f.unlink()
    generate_alt_files(items, alt_dir, "Magic Items")

    return items


def cmd_all():
    """Extract everything."""
    cmd_spells()
    cmd_monsters()
    cmd_animals()
    cmd_magic_items()


# =============================================================================
# DIAGNOSTIC: List extracted names without writing files
# =============================================================================

def cmd_list(section):
    """List extracted names for a section (dry run)."""
    lines = read_source()
    if section == "spells":
        items = extract_spells(lines)
    elif section == "monsters":
        items = extract_creatures(lines, "monsters")
    elif section == "animals":
        items = extract_creatures(lines, "animals")
    elif section == "magic-items":
        items = extract_magic_items(lines)
    else:
        print(f"Unknown section: {section}")
        return

    print(f"\n{section.upper()} ({len(items)} entries):")
    for name in sorted(items.keys()):
        print(f"  {name}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    if command == "spells":
        cmd_spells()
    elif command == "monsters":
        cmd_monsters()
    elif command == "animals":
        cmd_animals()
    elif command == "magic-items":
        cmd_magic_items()
    elif command == "all":
        cmd_all()
    elif command == "list":
        if len(sys.argv) < 3:
            print("Usage: extract.py list <spells|monsters|animals|magic-items>")
            sys.exit(1)
        cmd_list(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)

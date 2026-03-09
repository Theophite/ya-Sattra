# CLAUDE.md — Ya-Sattra (Post-Interdict Empire)

## Project Overview

This is a worldbuilding and creative writing framework for a far-future science fiction setting called the **Post-Interdict Empire**. It consists of ~156 Markdown documents organized by domain, ~14 Python tools for procedural generation and validation, and 2 large YAML data files. There is no traditional build system, test suite, or CI/CD pipeline — this is a documentation and tools project.

The setting describes an empire that maintains systems designed for interstellar civilization on a single trapped world (the former California coast). Stories emerge from characters navigating the gap between institutional fiction and lived reality.

**Creator/Maintainer:** Andreas Schou

---

## Repository Structure

### Document Organization

Files use category prefixes for navigation. The naming convention is `Category_-_Subject.md`:

| Prefix | Content |
|--------|---------|
| `00_Index_-_*` | Master index and RAG navigation guide |
| `Guide_-_*` | Writing standards, style guidance |
| `System_-_*` | Economic, educational, patent systems |
| `Government_-_*` | Satara council, institutional structure |
| `Bureau_-_*` | The six Bureaux (Lens, Sword, etc.) |
| `Religion_-_*` | Oracle Cult, Penitent Church |
| `Caste_-_*` | Biological castes and type specimens |
| `Species_-_*` | Non-human species (Many, Ta-Kefyeh) |
| `City_-_*` / `Region_-_*` | Geographic locations |
| `Ya-Sattra_District_-_*` | District-level detail (~24 files) |
| `Culture_-_*` | Food, media, entertainment |
| `Name_Generator_-_*` | Naming conventions by culture |
| `Language_-_*` | Grammar, registers, linguistic constraints |
| `Person_-_*` | Character dossiers |
| `Organization_-_*` / `Guild_-_*` | Institutions and groups |
| `Scenario_-_*` | Story scenario frameworks |
| `Templates_-_*` | In-universe document examples |
| `Mysteries_-_*` | The Emperor, First Whorl, vel-kerith |
| `Examples_-_*` | Story vignettes and tone models |

### The Eight Domains

1. **Cosmology & Ancient History** — Oracles, Testaments, the Interdict, temporal mechanics
2. **Imperial Structure** — Six Bureaux, Satara council, Whorls, the Emperor
3. **Geography** — Ya-Sattra, ya-Don, ya-Tsatsa, Republic of Ganat, Thousand Kingdoms
4. **Biological Engineering / Castes** — Highborn, labor castes, Warborn, Technical Castes
5. **Social Organizations** — Oracle Cult, Penitent Church, guilds, criminal organizations
6. **Economics & Technology** — Aureate patents, lectors, Many (banking organism), currency
7. **Reference Materials** — Naming conventions, aesthetics, glossary
8. **Character & Household Dossiers** — Families, crisis documentation, detailed characters

### Key Reference Files

- `00_Index_-_Project_Navigation.md` — Start here. Master index with RAG lookup guidance.
- `Guide_-_Writing_Stories.md` — Core writing principles and narrative style
- `Guide_-_Writing_Inner_City.md` — Tone for arcology and First Whorl scenes
- `Guide_-_Visual_Design_and_Architecture.md` — Materials, colors, sensory vocabulary
- `Language_-_Imperial_Grammar_and_Registers.md` — Grammar, registers, authentication constraints
- `Caste_-_Type_Specimens_Catalog.md` — ~30 castes through individual examples
- `Templates_-_In-Universe_Documents.md` — Examples of circumlocution and formal documents

---

## Python Tools

All tools are Python 3.6+ scripts in the repository root. No virtual environment or package manager is used.

### Dependencies

- **PyYAML** — Required for glossary and imperial_roots data loading
- **ftfy** — Optional, for mojibake (UTF-8 corruption) repair
- Standard library only for everything else

### Core Tools

| Script | Purpose | Key Commands |
|--------|---------|-------------|
| `glossary.py` | Term lookup and validation | `lookup`, `search`, `category`, `scan`, `scene-setup` |
| `name_generator.py` | Culture-specific name generation | `--culture imperial`, `--batch 5`, `--stub-fill` |
| `imperial_roots.py` | Morphological root lookup | `lookup`, `search`, `batch`, `find`, `generate` |
| `scenario_initiator.py` | Tarot-driven scenario creation | `--draw`, `--create`, `--card`, `--word` |
| `input_check.py` | Session state tracking | Scene location, character notes, plot events, questions |

### Generators

| Script | Purpose |
|--------|---------|
| `white_sheet_generator.py` | Story seeds for the "White Sheet" newspaper |
| `market_encounters.py` | Fourth Whorl market scene encounters |
| `lift_encounters.py` | Daily lift commute encounters |
| `morning_generator.py` | Atmospheric opening elements |
| `soldier_kit_generator.py` | Equipment loadouts by soldier function |

### Maintenance

| Script | Purpose |
|--------|---------|
| `copy_project.py` | File copying with mojibake correction |
| `fix_mojibake.py` | UTF-8 corruption repair |

### Data Files

- `glossary_data.yaml` (~1.3MB) — Structured glossary with ~300+ entries. Edit using entry markers: `# --- Entry Name ---` through `# --- end Entry Name ---`
- `imperial_roots_data.yaml` (~49KB) — Morphological roots, particles, suffixes

### Running Tools

```bash
python3 glossary.py lookup "Aureate"
python3 glossary.py scan some_document.md
python3 name_generator.py --culture imperial --batch 5
python3 imperial_roots.py lookup vel
python3 scenario_initiator.py --draw
```

Note: Some scripts have hardcoded paths (`/home/claude/`, `/mnt/project/`) from their original deployment context. These may need adjustment.

---

## Markdown Conventions

### Frontmatter

All content documents use YAML frontmatter:

```yaml
---
title: Document Title
type: guide | system | location | caste | scenario | ...
parent: null | Parent Document Name
glossary_terms:
  - Term1
  - Term2
guidance:
  - "Key principle for writing in this context"
  - "Another principle"
see_also:
  - Related Document.md
---
```

The `guidance:` array contains load-bearing creative principles. Always read these before working with a document.

### Heading Hierarchy

- `#` — Document title (one per file)
- `##` — Major sections
- `###` — Subsections
- `####` — Sub-subsections (rare)

---

## Writing Conventions

These principles govern all creative content in the project:

1. **Material circumstances first** — Every character needs concrete economic and institutional pressures before abstract motivations. What is their job? What are they paid? What do they owe?

2. **Documentary fragment** — Present stories as fragments of larger realities (ledgers, diaries, confessions, assessments). Maintains uncertainty, reflects how people actually experience institutions.

3. **Institutional fiction vs. lived reality** — The gap between what systems claim and what they actually do is where stories live. Characters participate in maintaining fictions even knowing they don't work.

4. **Moral complexity without melodrama** — Characters whose compromises seem reasonable from inside their circumstances. No clear redemption arcs, no pure heroes or villains.

5. **Sensory detail does work** — Colors, materials, tastes encode character, economics, history, and culture. Specific beats vague, sensory beats abstract.

6. **Cross-context encounters** — When contexts collide, neither side should be simply wrong.

7. **Emotional register by depth** — Fourth Whorl: commercial chaos. First Whorl: exhausted, profound sadness. Temporal mechanics are routine, not mystical.

---

## Consistency Rules

- **Check the glossary** before introducing or naming anything. Run `glossary.py scan` on new documents for canonicity.
- **Check the name generator** for the character's culture before assigning names. Imperial, Ganati, and Akama names follow distinct phonological rules.
- **Check Language - Imperial Grammar and Registers** before writing dialogue. There are grammatical registers, authentication constraints, and things that cannot be said in formal speech.
- **Consult the relevant Bureau document** before creating institutions — understand jurisdictional boundaries.
- **Consult Guide - Visual Design and Architecture** before describing places — materials and colors carry meaning.

---

## Known Issues

- **Mojibake**: UTF-8 corruption can occur during file transit. Use `fix_mojibake.py` or the ftfy library to repair.
- **Duplicate filenames**: Some files exist with both spaces and underscores in names (e.g., `Caste - Sewer-Fishers - Clan Benru.md` and `Caste_-_Sewer-Fishers_-_Clan_Benru.md`). The underscore variants are canonical.
- **Hardcoded paths**: Some Python scripts reference `/home/claude/` or `/mnt/project/` — adjust as needed for your environment.
- **No test suite**: Validation is manual. Use `glossary.py scan` for term consistency checks and `input_check.py --show` for session state review.

---

## Workflow for AI Assistants

1. **Start with the Index**: Read `00_Index_-_Project_Navigation.md` for orientation.
2. **Use the glossary**: Run `glossary.py lookup` or `glossary.py search` before RAG searches for quick definitions.
3. **Follow the guides**: The `Guide_-_*` files contain the creative standards. Read the relevant guide before producing content.
4. **Read frontmatter guidance**: The `guidance:` arrays in YAML frontmatter contain principles specific to that document.
5. **Validate output**: Run `glossary.py scan` on any new or modified documents.
6. **Respect naming**: Use the appropriate name generator for character names.
7. **Log conflicts**: If you discover contradictions between documents, note them in `RESTRUCTURING_LOG.md`.

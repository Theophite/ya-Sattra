# Glossary Usage Skill

The ya-Sattra project uses `glossary.py` as the canonical source of truth for all setting terminology. **Always verify terms against the glossary before using them in documents or code.**

## Core Principle

The glossary is the **semantic hub** for this RAG-structured TTRPG documentation. Every front matter `glossary_terms` field should contain ONLY terms that exist in the glossary with their **canonical spelling**.

## Available Commands

### Basic Lookups
```bash
python3 glossary.py lookup <term>           # Exact match (use FIRST before assuming a term exists)
python3 glossary.py search <query>          # Search across all fields (finds term in any entry)
python3 glossary.py check <term>            # Verify existence + suggest similar terms
python3 glossary.py category <category>     # List all: caste, location, organization, concept, person
python3 glossary.py related <term>          # Get term + all its related entries
```

### Hierarchy Commands
```bash
python3 glossary.py tree <name> [depth]     # Unified hierarchy (locations OR organizations)
python3 glossary.py location-tree <name>    # Show location hierarchy (legacy, use tree instead)
python3 glossary.py scene-setup <location>  # Full context for scene writing
python3 glossary.py path <start> <end> -v   # Find path between locations
```

### Caste Queries
```bash
python3 glossary.py caste-feature <feat> <value>  # Find by: morphology, scale, compulsion, lifespan, cognition, population
python3 glossary.py caste-trait <trait>           # Search physical_traits and special fields
python3 glossary.py caste-compare <c1> <c2>       # Side-by-side comparison
```

### Document Analysis
```bash
python3 glossary.py scan <filepath> [-v]    # Find all glossary terms in a document
python3 glossary.py validate-refs <file>    # Check that glossary_terms in front matter exist
python3 glossary.py who-references <term>   # Find all entries that reference a term
```

### Context Building
```bash
python3 glossary.py context-bundle <terms>  # Get definitions for comma-separated list
python3 glossary.py expand <term> [depth]   # Recursively expand related terms
```

## Command Behavior Notes

### `tree` Command
- Shows hierarchy based on `parent` field (locations use location_features.parent, orgs use top-level parent)
- **Empty tree is valid**: Bureau of the Scale intentionally has NO Institutes
- Depth parameter limits recursion (default: 3)

### `expand` Command
- Shows `↩ Term (see above)` for already-visited terms to avoid infinite loops
- Depth parameter limits how far to follow related terms

### `search` vs `lookup`
- `lookup` finds exact entry names only
- `search` finds terms mentioned anywhere in entries (use to check if concept exists but isn't an entry)

Example: "Autofactory" has no entry but `search` shows it's mentioned in 12 entries

### `validate-refs` Command
- Returns canonical names for valid terms (may differ from what's in file)
- Suggests similar terms for invalid entries

## Workflow: Verifying Terminology

**ALWAYS** use this workflow before adding terms to front matter:

```bash
# 1. Scan the document to find what terms are present
python3 glossary.py scan path/to/document.md

# 2. For each potential term, verify it exists
python3 glossary.py lookup "Eighth Testament"

# 3. If term doesn't exist, check for canonical form
python3 glossary.py check "Eighth Oracle"
# Output: "Did you mean: Eighth Testament, Oracles, ..."

# 4. Only add terms that return valid lookups
```

## Common Mistakes (Lessons Learned)

### 1. Using Non-Canonical Terms
**WRONG:** Adding "Eighth Oracle" to glossary_terms
**RIGHT:** Use `glossary.py lookup` first - the canonical term is "Eighth Testament"

Common corrections needed:
- "Ironback" → "Ironbone"
- "Companion Guild" → "Companions Guild"
- "Testament" (singular) → "Testaments"
- "Medials" → "Medial Castes"
- "Republic of Ganat" → "Ganat"
- "Occultant" → "Occultants" (plural)
- "Charter" → "City-of-Glass Charter" (full name)

### 2. Sub-Concepts Without Entries
Some concepts are mentioned in other entries but don't have their own:
- "Dominion" is one of the Seven Virtues (use `lookup "Seven Virtues"` to see it)
- "Autofactory" is mentioned in 12 entries but has no dedicated entry

Use `search` to find where a concept is documented before assuming it needs its own entry.

### 3. Creating Duplicate Entries
When adding new entries to glossary_data.yaml, **always search first**:
```bash
python3 glossary.py search "Institute of Flow"
```
Creating a duplicate entry will silently overwrite the original due to YAML key semantics.

### 4. Not Using the Glossary At All
The glossary exists to be used! Before making assumptions about setting terminology:
```bash
python3 glossary.py lookup <whatever you're about to write>
```

### 5. Missing Parent Fields for Organizations
When adding Institute entries, include `parent` field to enable hierarchy queries:
```yaml
Institute of Somatic Grace:
  category: organization
  parent: Bureau of the Creche    # This enables tree queries
  short: "..."
```

## Alias Support

The glossary supports aliases for common variations:
- `Occultant` → `Occultants`
- `Charter` / `the Charter` → `City-of-Glass Charter`
- `Colonel-Hereditary` → `Colonels-Hereditary`
- `Autofactories` → `Autofactory`
- `Plasma Lances` → `Plasma Lance`
- Individual Virtues have Testament aliases: `First Virtue` → `Initiation`, etc.

**Note**: Use `search` to find entries by alias since `lookup` requires exact names.

## Remaining Gaps

Terms that may still need entries:
- **Standing Orders** - immutable constitution from First Whorl
- **Sevenfold Silence** - Oracle Cult practice

## Structural Notes

### Bureaus and Institutes
- **Bureau of the Creche**: 7 Institutes
- **Bureau of the Coin**: 2 Institutes
- **Bureau of the Scale**: NO Institutes (intentionally - "vast contradictory accumulation of courts")
- **Bureau of the Lens**: 7 Institutes
- **Bureau of the Sword**: 7 Institutes
- **Bureau of the Rod**: 6 Institutes

### Location Hierarchy
```
ya-Sattra (city)
  └── District (Medina Quarter, Iron Yards, etc.)
      └── Neighborhood (Great Bazaar, Forge Terrace, etc.)
          └── Site (specific buildings, monuments)
```

## Adding New Entries

### Template for Organizations
```yaml
# ═══ Entry Name ═══
Entry Name:
  category: organization
  parent: Parent Organization      # For hierarchies
  short: "One-line description."
  details: |
    Longer description if needed.
  rag_pointer: "Source Document Title"
  related: [Term1, Term2, Term3]
# ─── end Entry Name ───
```

### Validation After Adding
```bash
python3 -c "import yaml; yaml.safe_load(open('glossary_data.yaml')); print('Valid!')"
```

## Example Outputs

### tree command
```
python3 glossary.py tree "Bureau of the Lens"

Bureau of the Lens [organization]
  └── Institute for the Suppression of Knowledge [organization]
  └── Institute of Domestic Intelligence [organization]
  └── Institute of Imperial Record [organization]
  └── Institute of Informational Orthodoxy [organization]
  └── Institute of the Echo [organization]
  └── Institute of the Eye [organization]
  └── Institute of the Lattice [organization]
```

### who-references command
```
python3 glossary.py who-references "Bureau of the Lens"

  Has 'Bureau of the Lens' as PARENT (7):
    • Institute of the Lattice [organization]
    • Institute for the Suppression of Knowledge [organization]
    ...

  In RELATED field (23):
    • Quarantine Shed [location]
    • Satara [organization]
    ...
```

### validate-refs command
```
python3 glossary.py validate-refs Government_-_Satara_and_Bureaus.md

  ✓ VALID (14 terms):
    • Satara
    • Bureau of the Creche
    ...

  ✗ INVALID (4 terms):
    • Standing Orders → try: Sifting Grounds, Ganati Border, Undying Empire
    • Dominion → try: Compulsion, Companions Guild, Semi-Sentient
    ...
```

## Quick Reference: Feature Values

### Caste Features
- morphology: baseline, modified, divergent, merged, parasitic, variable
- scale: tiny, small, baseline, tall, giant, variable
- compulsion: triggers, susceptible, immune, unknown
- lifespan: reduced, baseline, extended, variable
- cognition: baseline, enhanced, specialized, reduced, semi
- population: extinct, remnant, rare, common, majority

### Location Features
- level: territory, city, district, neighborhood, site
- location_type: polity, settlement, administrative, industrial, commercial, residential, religious, military, arcology, infrastructure, geographic, grouping, educational, underground, monument

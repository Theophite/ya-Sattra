# Enrich Location Aesthetic

Enrich a glossary location entry with culturally-specific aesthetic details.

## Arguments

$ARGUMENTS - Location term to enrich (e.g., "Third Whorl", "Virgin River Junction")

## Workflow

### Step 1: Look Up the Location

Run the glossary lookup to get the current entry:

```bash
python3 glossary.py lookup "$ARGUMENTS" -v
```

Extract from the entry:
- Current `short` and `details` text (the seed)
- `parent` location (determines culture chain)
- `location_type` and `level`
- Any existing `aesthetic_features`
- `real_world_anchor` if present

### Step 2: Determine Cultural Context

Trace the parent chain to identify the governing culture(s):

| Parent Chain Contains | Primary Culture | Material Culture Doc |
|----------------------|-----------------|---------------------|
| ya-Sattra, Inner City, Medina Quarter | Imperial | Aesthetics_-_Imperial_Material_Culture.md |
| ya-Sattra, Antediluvian Quarter | Antediluvian | Aesthetics_-_Antediluvian_Material_Culture.md |
| ya-Sattra, Iron Yards, Middens, Ridge | Imperial (working class) | Aesthetics_-_Imperial_Material_Culture.md |
| Ganat, Taho | Ganati | Aesthetics_-_Ganati_Material_Culture.md |
| Thousand Kingdoms, Ogon | Akama | Aesthetics_-_Akama_Material_Culture.md |
| ya-Tsatsa | Ya-Tsatsa | Aesthetics_-_Ya-Tsatsa_Material_Culture.md |
| ya-Don | Ya-Don | Aesthetics_-_Ya-Don_Material_Culture.md |
| Asovoë | Avouvar | Aesthetics_-_Avouvar_Material_Culture.md |

If the location sits at a cultural boundary (e.g., Amber Quarter in ya-Don has Ganati influence), load multiple docs.

### Step 3: Load Reference Documents

Read the relevant material culture document(s) identified above.

Then read the first 200 lines of `Guide_-_Visual_Design_and_Architecture.md` to get the Six Axes framework:
1. Time Horizon (short/medium/long/very long)
2. Energy Economy (abundant free/abundant conditional/scarce/variable)
3. Competition Axis (personal equipment/collective infrastructure/credentials/trade goods)
4. Inheritance Ratio (inherited/subtractive/additive/inherited anchor with expansion)
5. Constraint Type (weight/material/ideology/comprehension/biology/authentication)
6. Activity Density (waiting/moving/maintaining/competing/deliberating/trading/observing)

### Step 4: Analyze the Location

Using the existing entry text as seed, determine:

**From the Six Axes:**
- What is this location's time horizon? (How long have people been looking at this?)
- What energy economy applies? (What's cheap/expensive/conditional here?)
- What do people compete over here?
- How much is inherited vs. built?
- What are the primary constraints?
- What activities fill the time here?

**From the Material Culture:**
- What objects, materials, colors characterize this culture?
- How do repairs and wear patterns manifest?
- What does display mean here?

### Step 5: Generate Enriched Description

Write a new `details` field that:

1. **Keeps the factual content** from the existing entry (population, function, key locations)
2. **Adds sensory specifics** derived from the Six Axes analysis:
   - Visual: materials, colors, wear patterns, light quality
   - Auditory: characteristic sounds
   - Olfactory: smells if relevant
   - Tactile: textures, temperatures
3. **Uses culturally-specific vocabulary** from the material culture doc
4. **Avoids inventing non-canonical terms** - use glossary.py to verify any term you're uncertain about

The description should be 100-250 words, using concrete details rather than abstract characterizations.

### Step 6: Add Visual Features

If the entry lacks a `visual` list under `location_features`, add one with 4-6 bullet points capturing:
- Dominant materials and construction
- Light quality and color palette
- Characteristic sounds or activity patterns
- Key visual landmarks or features

### Step 7: Update the Glossary

Edit the glossary_data.yaml file to update the entry with:
- Enriched `short` (one sentence, captures visual essence)
- Enriched `details` (100-250 words with sensory specifics)
- Added `visual` list if missing

Use the standard entry markers to locate the entry:
```
# ═══ Entry Name ═══
...
# ─── end Entry Name ───
```

### Step 8: Validate

Run the scan tool to check for undefined terms:
```bash
python3 glossary.py scan glossary_data.yaml -v | grep -A5 "$ARGUMENTS"
```

If any invented terms appear, revise to use canonical vocabulary.

## Example Output

For "Third Whorl", the enrichment might produce:

**short:** "The industrial and utility core of the Inner City—the Engine Room."

**details:**
```
Cavernous halls house colossal water recycling plants, geothermal heat exchangers,
and power distribution substations. The architecture is functional grandeur—bronze
walls with bas-reliefs that serve as integrated data conduits and diagnostic panels.

The air is clean but carries ozone and the scent of chilled metal from coolant pumps.
Sounds: deep machinery hum felt more than heard, rhythmic clang of presses, water
flowing through bronze pipes. Vast cloistered office complexes house thousands of
scribes, styluses scratching on tablets, quiet conversations replacing the Fourth
Whorl's market cacophony.

Key locations: Bureau of the Rod Central Control (tiered amphitheater of consoles),
the Lineal Vaults (cryogenic genetic archive), the Mint (fortress of deafening
archaeotech presses), Terminal Manifold (logistics operations), residential enclaves
for senior bureaucrats avoiding Whorl-Lag.
```

**visual:**
```yaml
visual:
  - cavernous halls with massive machinery
  - functional bronze architecture (bas-reliefs as data conduits)
  - deep machinery hum, rhythmic clanging, water flowing
  - ozone and chilled metal scent
  - vast cloistered offices
```

## Notes

- Synthesize, don't copy. Use the aesthetic documents to inform details, not to transplant text.
- Reduce unique terms where possible. Prefer existing glossary vocabulary.
- The existing entry text is the seed—preserve its factual content while adding sensory richness.
- When in doubt about a term's canonicity, run `python3 glossary.py lookup "term"` to verify.

# Audit Location Aesthetics

Find glossary location entries that need aesthetic enrichment.

## Arguments

$ARGUMENTS - Optional: minimum character threshold (default: 200), or "all" to list all locations sorted by description length

## Workflow

### Step 1: Analyze Location Entries

Run this Python script to find sparse location entries:

```python
import yaml

with open('glossary_data.yaml', 'r') as f:
    data = yaml.safe_load(f)

entries = data.get('entries', {})
threshold = 200  # or parse from $ARGUMENTS

locations = []
for term, entry in entries.items():
    if entry.get('category') == 'location':
        desc = entry.get('short', '') + ' ' + entry.get('details', '')
        desc_len = len(desc.strip())

        # Check for aesthetic_features
        has_aesthetics = 'aesthetic_features' in entry
        has_visual = 'visual' in entry.get('location_features', {})

        locations.append({
            'term': term,
            'desc_len': desc_len,
            'has_aesthetics': has_aesthetics,
            'has_visual': has_visual,
            'parent': entry.get('location_features', {}).get('parent', 'unknown')
        })

# Sort by description length
locations.sort(key=lambda x: x['desc_len'])

print(f"LOCATIONS NEEDING ENRICHMENT (description < {threshold} chars):")
print("=" * 70)
for loc in locations:
    if loc['desc_len'] < threshold:
        flags = []
        if not loc['has_aesthetics']: flags.append('no aesthetic_features')
        if not loc['has_visual']: flags.append('no visual list')
        flag_str = f" [{', '.join(flags)}]" if flags else ""
        print(f"{loc['desc_len']:4d} chars | {loc['term']}{flag_str}")
        print(f"           parent: {loc['parent']}")
```

### Step 2: Group by Culture

Organize the sparse entries by their cultural context:

| Culture | Parent Chain | Count |
|---------|-------------|-------|
| Imperial Core | ya-Sattra, Inner City, Medina Quarter | ? |
| Imperial Working | Iron Yards, Middens, Ridge | ? |
| Ganati | Ganat, Taho | ? |
| Akama | Thousand Kingdoms, Ogon | ? |
| Ya-Tsatsa | ya-Tsatsa | ? |
| Ya-Don | ya-Don | ? |
| Avouvar | Asovoë | ? |
| Other | various | ? |

### Step 3: Prioritize

Recommend which entries to enrich first based on:
1. Shortest descriptions (most need)
2. Entries with no `aesthetic_features` or `visual` list
3. Entries in well-documented cultures (where source material exists)

### Step 4: Report

Output a list of recommended entries to enrich, grouped by culture, with commands to run:

```
RECOMMENDED ENRICHMENT ORDER:

## Imperial Core (5 entries)
/enrich-location Third Whorl
/enrich-location Fourth Whorl
...

## Ganati (3 entries)
/enrich-location Virgin River Junction
...
```

## Example Output

```
LOCATIONS NEEDING ENRICHMENT (description < 200 chars):
======================================================================
  72 chars | Virgin River Junction [no aesthetic_features, no visual list]
           parent: Ganat
  96 chars | Third Whorl [no visual list]
           parent: Inner City
 125 chars | Akama District [no aesthetic_features, no visual list]
           parent: Upper City
...

GROUPED BY CULTURE:

Imperial Core (2 entries):
  - Third Whorl (96 chars)
  - Second Whorl (156 chars)

Ganati (1 entry):
  - Virgin River Junction (72 chars)

Ya-Tsatsa (2 entries):
  - Akama District (125 chars)
  - Lower City (127 chars)

RECOMMENDED: Start with Ya-Tsatsa entries (good source docs available)
```

## Notes

- This command only audits; use `/enrich-location` to actually enrich entries
- Entries with `aesthetic_features` may still benefit from enrichment if the `details` field is sparse
- Consider batch processing entries from the same culture together for efficiency

# Glossary Usage Skill

The ya-Sattra project uses `glossary.py` as the canonical source of truth for all setting terminology. **Always verify terms against the glossary before using them in documents or code.**

## Core Principle

The glossary is the **semantic hub** for this RAG-structured TTRPG documentation. Every front matter `glossary_terms` field should contain ONLY terms that exist in the glossary with their **canonical spelling**.

## Available Commands

### Basic Lookups
```bash
python3 glossary.py lookup <term>           # Exact match (use FIRST before assuming a term exists)
python3 glossary.py search <query>          # Search across all fields
python3 glossary.py check <term>            # Verify existence + suggest similar terms
python3 glossary.py category <category>     # List all: caste, location, organization, concept, person
python3 glossary.py related <term>          # Get term + all its related entries
```

### Location Queries
```bash
python3 glossary.py location-tree <name>    # Show hierarchy (parent/children)
python3 glossary.py scene-setup <location>  # Full context for scene writing
python3 glossary.py tree <name>             # Unified hierarchy tree (locations OR organizations)
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

Other common mistakes:
- "Ironback" → should be "Ironbone"
- "Companion Guild" → should be "Companions Guild"
- "Testament" (singular) → should be "Testaments"
- "Medials" → should be "Medial Castes"
- "Republic of Ganat" → should be "Ganat"

### 2. Creating Duplicate Entries
When adding new entries to glossary_data.yaml, **always search first**:
```bash
python3 glossary.py search "Institute of Flow"
```
Creating a duplicate entry will silently overwrite the original due to YAML key semantics.

### 3. Not Using the Glossary At All
The glossary exists to be used! Before making assumptions about setting terminology:
```bash
python3 glossary.py lookup <whatever you're about to write>
```

### 4. Missing Parent Fields for Organizations
When adding Institute entries, include `parent` field to enable hierarchy queries:
```yaml
Institute of Somatic Grace:
  category: organization
  parent: Bureau of the Creche    # This enables org-tree queries
  short: "..."
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

## Hierarchical Queries

### Organization Hierarchy
For organizations like Bureaus and Institutes:
```bash
python3 glossary.py tree "Bureau of the Lens"
# Shows: Bureau → all child Institutes
```

### Location Hierarchy
```bash
python3 glossary.py tree "ya-Sattra"
# Shows: City → Districts → Neighborhoods → Sites
```

## Scanning Documents for Context

Before writing narrative content in a location:
```bash
# Get full scene setup
python3 glossary.py scene-setup "Lampblack Yards"

# Or expand from a starting term
python3 glossary.py expand "Lampblack Yards" 2
```

This ensures you have correct terminology, nearby locations, relevant castes, and aesthetic vocabulary.

## Front Matter Best Practices

```yaml
---
title: "Document Title"
type: setting_doc
glossary_terms:
  - Term One        # Each must be verifiable via: glossary.py lookup "Term One"
  - Term Two
  - Parent Location # Include hierarchy context
guidance: |
  Brief description of document purpose and RAG retrieval hints.
see_also:
  - Related_Document.md
---
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

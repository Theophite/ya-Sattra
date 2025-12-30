# RAG Restructuring Log

## Purpose
Track conflicts discovered during glossary-grounded document restructuring, how they were resolved, and questions that remain open.

---

## Resolved Conflicts

### 1. Sewer-Fisher Clan Count
- **Source**: Sewer-Fishers entry said "five clans: Venn, Hasket, Cho, Sarn, Benru"
- **Conflict**: Loak entry said "one of six sewer-fisher clans"
- **Resolution**: Changed to "six clans: Loak, Venn, Hasket, Cho, Sarn, Benru" in both Sewer-Fishers and Technical Castes entries
- **Commit**: ce22f38

### 2. Cho Clan - Lockworks Control vs Maintenance
- **Source doc**: "Clan Cho: Keepers of the Lockworks" - implies control
- **Glossary**: Said Cho controls "electrical monopoly and Ridge gondola" - no mention of Lockworks
- **Middens doc resolution**:
  - Hanged Men CONTROL Lockworks (political power, access, punishment)
  - Cho clan MAINTAINS Lockworks under contract (technical expertise, 60-person crew)
  - Cho ALSO controls Lantern-Heaps electrical monopoly + gondola to Ridge
  - Riva Fen-Cho operates from Lockworks command center in Gallows 12th floor
- **Resolution**: Updated both glossary Cho entry and Clan Cho file to reflect this dual role
- **Commit**: ce22f38

### 3. Missing Clan Glossary Entries
- **Issue**: Hasket, Sarn, Venn clans only mentioned in Sewer-Fishers special notes, not as separate entries
- **Resolution**: Added full glossary entries for all three clans
- **Commit**: ce22f38

### 4. Benru Clan Location - Two Locations (Not a Conflict)
- **Glossary**: "documentation services in the Gallows"
- **My file**: "three-story structure near Vetch-Rise, in the Iron Yards"
- **Source doc**: "three-story structure just outside Vetch-Rise, in the Iron Yards"
- **Middens doc**: "Clan Benru occupies the fifth floor archive" + "Their archive in Hollow-Egress"
- **Resolution**: NOT a conflict - they have TWO locations:
  - Residence/brokerage in Iron Yards (near Salvage Guild for business)
  - Documentation desk/archive in Hollow-Egress (serving Middens workers)
- **Status**: RESOLVED

### 5. Hollow-Egress "Five-Clan Cooperative" - Correct (Not a Conflict)
- **Glossary**: "Five-clan cooperative tenement controlling Lift-3"
- **Apparent conflict**: There are SIX sewer-fisher clans total
- **Resolution**: This is CORRECT - five clans share Hollow-Egress:
  - Loak (Lift-3 operations, Merra's kitchen)
  - Benru (fifth floor archive)
  - Venn (rigging)
  - Hasket (security, aquaculture)
  - Sarn (deep access)
- **Cho is NOT in Hollow-Egress** - they're in Lantern-Heaps (electrical) and Gallows (Lockworks)
- **Status**: RESOLVED

---

## Open Questions

### 1. Sarn Clan - Deep Populations
- **Source implies**: Deep populations may not be human
- **Question**: Are deep populations confirmed non-human, or is this ambiguous by design?
- **Status**: Treated as deliberately ambiguous in restructured file - per Middens doc: "These uncertainties are features, not omissions—the Middens residents don't know either."

---

## Glossary Entries Added This Session

1. **Hasket** - stevedore fosterings, aquaculture, distillery, hidden armory
2. **Sarn** - deep populations, Jargon, no Oracle shrine
3. **Venn** - high-altitude rigging, toll-avoidance, luck carabiner

---

## Glossary Entries Modified This Session

1. **Sewer-Fishers** - clan count (5→6), clan role descriptions expanded
2. **Technical Castes** - clan count reference (5→6)
3. **Cho** - added Lockworks maintenance, Fen connection, expanded details

---

## Documents Created/Modified

### Created (Sewer-Fishers batch - first pass):
- Caste - Sewer-Fishers - Overview.md
- Caste - Sewer-Fishers - Clan Benru.md
- Caste - Sewer-Fishers - Clan Loak.md
- Caste - Sewer-Fishers - Clan Venn.md
- Caste - Sewer-Fishers - Clan Hasket.md
- Caste - Sewer-Fishers - Clan Cho.md (revised)
- Caste - Sewer-Fishers - Clan Sarn.md
- Vignettes - Merras Kitchen.md

### Created (Technical Castes batch - glossary-grounded):
- Caste - Technical Castes - Overview.md
- Caste - Technical Castes - Far Ib.md
- Caste - Technical Castes - Mathematics Primer.md

---

## Middens Document Analysis (COMPLETE)

**Source:** Ya-Sattra_District_-_Middens.md (887 lines)

**Glossary coverage verified:**
- All 7 tenements have glossary entries ✓
- Hanged Men, Chain-Men, Valve-Saint Parish have entries ✓
- Sewer-fisher clans already restructured ✓

### Created (Middens batch - glossary-grounded):
1. Ya-Sattra District - Middens - Overview.md ✓
2. Ya-Sattra District - Middens - The Gallows.md ✓
3. Ya-Sattra District - Middens - Bright-Spire.md ✓
4. Ya-Sattra District - Middens - Hollow-Egress.md ✓
5. Ya-Sattra District - Middens - Sump-Gate.md ✓
6. Ya-Sattra District - Middens - Lantern-Heaps.md ✓
7. Ya-Sattra District - Middens - Knife-Edge.md ✓
8. Ya-Sattra District - Middens - Vetch-Rise.md ✓
9. Organization - Hanged Men.md ✓
10. Organization - Valve-Saint Parish.md ✓

**Sewer-fisher clans:** Cross-referenced to existing clan files (no duplication)

**Guidance notes added per file:**
- Gallows: Water control structure, execution ritual, floor-by-floor power hierarchy
- Bright-Spire: Architecture as oppression, compression gradient, revolution mathematics
- Hollow-Egress: Five-clan (not six) cooperative, transition chambers, depth access
- Sump-Gate: The dome mystery, Mutterer modifications, tidal worship
- Lantern-Heaps: Cho electrical monopoly, chip bazaar jargon, gondola monopoly
- Knife-Edge: Fifteen-degree lean, tilted gait, adapted techniques
- Vetch-Rise: Access control, transient market mobility, Astal warrens

---

## Ridge Document Analysis (COMPLETE)

**Source:** Ya-Sattra_District_-_Ridge.md (~163 lines)

**Glossary coverage verified:**
- Ridge, Horizon Row, Penthouse Block, The Arcades have entries ✓
- Val Family, Marzen Family, Galen Family have entries ✓

### Created (Ridge batch - glossary-grounded):
1. Ya-Sattra District - Ridge - Overview.md ✓
2. Ya-Sattra District - Ridge - Horizon Row.md ✓
3. Ya-Sattra District - Ridge - Penthouse Block.md ✓
4. Ya-Sattra District - Ridge - The Arcades.md ✓
5. Organization - Val Family.md ✓
6. Organization - Marzen Family.md ✓
7. Organization - Galen Family.md ✓

**Key guidance notes:**
- Three families with complementary monopolies (water, electricity, intelligence)
- Interdependence prevents conflict (Vals need Marzen power, Marzens need Val water)
- Sideways arcology creates "tilted gait" marking Ridge residents
- Cho gondola is only direct Middens-Ridge connection

---

## Iron Yards Document Analysis (COMPLETE)

**Source:** Ya-Sattra_District_-_Iron_Yards.md (~354 lines)

**Glossary coverage verified:**
- Iron Yards, Torchline Row, Salvage Dome, Archive Gate, Forge Terrace have entries ✓
- Salvage Guild, Pipefitters Union, Yen Tam Beneficial Society have entries ✓
- Iron Yards Boys has entry ✓

### Created (Iron Yards batch - glossary-grounded):
1. Ya-Sattra District - Iron Yards - Overview.md ✓
2. Ya-Sattra District - Iron Yards - Salvage Dome.md ✓
3. Ya-Sattra District - Iron Yards - Torchline Row.md ✓
4. Organization - Salvage Guild.md ✓
5. Organization - Pipefitters Union.md ✓
6. Organization - Yen Tam Beneficial Society.md ✓

**Key guidance notes:**
- Three powers model: Guild (sales), Union (labor), Yen Tam (vice)
- Debt cycles trap workers (extraction economy theme)
- Lira Three-Stone legend (40-meter throw, declined leadership)
- Cross-caste solidarity in Union contradicts caste hierarchy

---

## Castes of Mankind Document Analysis (COMPLETE)

**Source:** Caste_-_Type_Specimens_Catalog.md (~500+ lines)

**Glossary coverage verified:**
- All major caste categories have entries ✓
- Individual caste variants (Ironbone, Springheel, etc.) have entries ✓

### Created (Castes batch - glossary-grounded):
1. Caste - Highborn.md ✓ (three phenotypes, Compulsion ethics)
2. Caste - Warborn.md ✓ (three variants, cancer timeline, Chain-Men)
3. Caste - Labor Castes.md ✓ (Ironbone, Redback, Springheel, Beamcrawler, Ductworker, Orevet, Ashrat, Karst)
4. Caste - Near-Baseline.md ✓ (Compulsion susceptibility, majority population)
5. Caste - Colonist Castes.md ✓ (Serrulata: Sarruk, Nasif, Uliq, Draëthen)

**Key guidance notes:**
- Each caste has specific failure mode (documented per file)
- Warborn: cancer by 40, the Blink, heat radiation
- Labor castes: Ironbone stiffens, Redback binary failure, Springheel tendon tears
- Highborn: fragile bones (elongated), uncanny valley (optimized), born incomplete (integrated)

---

## Medina Quarter Document Analysis (COMPLETE)

**Source:** Ya-Sattra_District_-_Medina_Quarter.md (~655 lines - largest source document)

**Glossary coverage verified:**
- Medina Quarter, Great Bazaar, Archive Gate, Fourth Whorl have entries ✓
- Guild-related terms (Booksellers' Row, etc.) have entries ✓
- Foreign commerce terms (Ganati, Avouvar, ta-Kefyeh) have entries ✓

### Created (Medina batch - glossary-grounded):
1. Ya-Sattra District - Medina - Overview.md ✓
2. Ya-Sattra District - Medina - Guild System.md ✓
3. Ya-Sattra District - Medina - Great Bazaar.md ✓
4. Ya-Sattra District - Medina - Bureau Presence.md ✓
5. Ya-Sattra District - Medina - Entertainment.md ✓
6. Ya-Sattra District - Medina - Notable Buildings.md ✓
7. Ya-Sattra District - Medina - Businesses.md ✓

**Key guidance notes:**
- Central concern: managed contradiction (bridging what Empire claims vs what it needs)
- Guild charters predate Bureau authority - permits impossible, guild membership cuts through
- Three market layers: white (guild), gray (paperwork pending), black margins (back rooms)
- Polyphonic singers are Highborn bastards in administrative gaps - no Bureau will categorize them
- Ancient buildings show 40,000+ years of occupation - wear patterns have no analogue

---

## Next in Traversal Graph

**Completed this session:**
- Ridge (from Middens `related:`)
- Iron Yards (from Middens `related:`)
- Warborn castes (from Hanged Men Chain-Men connection)
- Medina Quarter (from Archive Gate connection)

**Remaining from traversal:**
- Bureau documents (Lens, Sword, Satara overview) - already well-structured, need front matter
- Malpais War, City of Glass (from Hanged Men history)
- ya-Tsatsa (from Yen Tam origin)

---

## Documents With Front Matter Added (No Split Required)

These documents were already well-structured with internal navigation. Added YAML front matter for RAG compatibility.

### Guild_-_Companions__Physicians_.md ✓
- Added guidance rules for Mutterer management
- Key concepts: monastic order (not trade guild), cascades, chimes, Witness inheritance
- Already has internal RAG Navigation section

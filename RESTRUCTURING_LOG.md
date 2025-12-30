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

## Middens Document Analysis (In Progress)

**Source:** Ya-Sattra_District_-_Middens.md (887 lines)

**Current glossary coverage:**
- All 7 tenements have glossary entries ✓
- Hanged Men, Chain-Men, Valve-Saint Parish have entries ✓
- Sewer-fisher clans already restructured ✓

**Proposed split structure:**
1. Ya-Sattra District - Middens - Overview.md (geographic, connections, summary)
2. Ya-Sattra District - Middens - The Gallows.md
3. Ya-Sattra District - Middens - Bright-Spire.md
4. Ya-Sattra District - Middens - Hollow-Egress.md
5. Ya-Sattra District - Middens - Sump-Gate.md
6. Ya-Sattra District - Middens - Lantern-Heaps.md
7. Ya-Sattra District - Middens - Knife-Edge.md
8. Ya-Sattra District - Middens - Vetch-Rise.md
9. Organization - Hanged Men.md (extensive section with 7 Knot member profiles + history)
10. Organization - Valve-Saint Parish.md

**Sewer-fisher clans section:** Reference existing clan files, don't duplicate

**Next steps:**
- Create Overview file with front matter
- Create tenement files with building-specific guidance
- Extract Hanged Men to standalone org document

---

## Next in Traversal Graph

From Middens `related:` field → Ridge, Iron Yards, Hanged Men doc
- Hanged Men doc will reveal connections to Warborn castes, Malpais War
- Ridge will connect to Cho gondola, salvage reconditioning
- Iron Yards will connect to Salvage Guild, Pipefitters Union

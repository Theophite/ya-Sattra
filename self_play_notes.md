# Self-Play Scenario Validation Notes

This file tracks problems encountered during the self-play scenario creation and validation process.

## Session Info
- Date: 2025-12-30
- Task: Create scenario, self-play through it, validate with input_check.py

---

## Problems Encountered

### Problem 1: Seed Term Encoding Issue
- **Time**: Session start
- **Issue**: `scenario_initiator.py --draw` returned seed term "VÃ£Â¶LÃ£«Rath" with corrupted Unicode
- **Likely intended**: "Völrath" or similar
- **Resolution**: Will look up glossary for valid seed term to use instead

### Problem 2: input_check.py Hardcoded Paths
- **Time**: Beginning of self-play validation
- **Issue**: `input_check.py` has hardcoded paths (`/home/claude`, `/mnt/project`) that don't exist in this environment
- **Error**: `FileNotFoundError: [Errno 2] No such file or directory: '/mnt/project'`
- **Location**: Lines 42-43 and line 134 of input_check.py
- **Resolution**: Modified script to use `/home/user/ya-Sattra` - working now

### Problem 3: False Positives on Sentence-Initial Words
- **Time**: Multiple turns
- **Issue**: input_check.py flags normal words at sentence start as proper nouns
- **Examples**: "Finally", "Fourteen", "Voices", "Ahead", "Only", "Standing", "Their"
- **Reason**: Capitalized at start of sentence, detected as proper noun
- **Impact**: Minor - adds noise to RAG NEEDED list
- **Suggestion**: Could add heuristic to skip first word of sentences

---

## Validation Results Log

### Summary Statistics
- **Total turns validated**: 16 (8 player actions + 8 GM responses)
- **Successful validations**: 16/16
- **Known terms correctly identified**:
  - Castes: Highborn, Völërath, Szkovërin, Draëthen
  - Locations: Brennholm, Puget Sound
  - Concepts: Compulsion, Records
  - Persons: Grey-Patch (Draëthen naming convention)
- **Scenario-specific terms flagged for RAG** (correctly): Keth, Theven, Mava, Lenna, Brennek, val-Morren, val-Oss, val-Kess, Veth, Ironhand, Archive, Hall, Founding, Ledger
- **False positives** (sentence-initial words): Finally, Fourteen, Voices, Ahead, Only, Standing, Their, Another, Who, Wands

### Turn-by-Turn Log

| Turn | Player Action | GM Response |
|------|---------------|-------------|
| 1 | Highborn (caste), Keth/Theven (RAG) | — |
| 2 | (no new terms) | Compulsion (concept), Grey-Patch (person) |
| 3 | Archive/Hall/Founding/Ledger (RAG) | Lenna/val-Kess (RAG) |
| 4 | Brennholm (location), val-Morren (RAG) | Veth/val-Oss (RAG) |
| 5 | (no new terms) | Imperial (RAG) |
| 6 | Records (concept) | False positives only |
| 7 | (no new terms) | False positives only |
| 8 | (no new terms) | Wands (tarot suit, not in glossary) |

---

## Second Scenario: "The Unwritten Chord"

**Card**: 3 of Wands (foresight, expansion, waiting for returns)
**Seed**: Verethani (Highborn without Compulsion, sing in ya-Don Furnaces)
**Setting**: ya-Don, the Furnaces, Chamber 7-Keth-Ascending
**Turns**: 16

### Validation Results

| Turn | Key Terms Found |
|------|-----------------|
| 1 | Furnaces, Threshold (locations) |
| 4 | Ashrat (caste) |
| 5 | Near-Baseline (caste), Bureau of the Rod, Furnace Board, Lector (glossary) |
| 6 | Verethani (caste) |
| 10 | Archons, Technical Castes (castes), Interdict (concept) |

**Correctly identified**: 12 setting terms
**Scenario-specific RAG flags**: 14 invented terms
**No new problems encountered** in second scenario

---

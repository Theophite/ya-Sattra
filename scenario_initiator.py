#!/usr/bin/env python3
"""
Scenario Initiator for the Post-Interdict Empire.

Draws Tarot cards and random glossary terms to seed a new scenario.
Generates a .md file with scenario framework and initializes the cache.

Usage:
    scenario_initiator.py                 # Single draw: 1 card + 1 word, show prompt
    scenario_initiator.py --draw          # Multi-draw: 3 cards + 5 terms for selection
    scenario_initiator.py --draw-single   # Old behavior: 1 card + 1 word (no file)
    scenario_initiator.py --create <name> # Create scenario file after drawing
    scenario_initiator.py --word          # Just pull a random glossary word
    scenario_initiator.py --card          # Just draw a Tarot card
    scenario_initiator.py --list-cards    # Show all available cards

Multi-Draw Selection:
    The --draw command presents 3 tarot cards and 5 glossary terms weighted
    by category (locations preferred) and content richness. Select one card
    + one term combination based on narrative potential, then proceed with
    scenario generation using your selection.
"""

import sys
import os
import random
import json
from datetime import datetime
from pathlib import Path

# Glossary integration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKING_DIR = '/home/claude'
PROJECT_DIR = '/mnt/project'
GLOSSARY_AVAILABLE = False

for search_dir in [SCRIPT_DIR, WORKING_DIR, PROJECT_DIR]:
    if GLOSSARY_AVAILABLE:
        break
    if os.path.exists(search_dir) and os.path.exists(os.path.join(search_dir, 'glossary.py')):
        sys.path.insert(0, search_dir)
        try:
            import glossary as G
            GLOSSARY_AVAILABLE = True
        except ImportError:
            if search_dir in sys.path:
                sys.path.remove(search_dir)

# =============================================================================
# TAROT DECK
# =============================================================================

MAJOR_ARCANA = [
    ("The Fool", "Beginnings, innocence, spontaneity, a free spirit"),
    ("The Magician", "Manifestation, resourcefulness, power, inspired action"),
    ("The High Priestess", "Intuition, sacred knowledge, the subconscious mind"),
    ("The Empress", "Femininity, beauty, nature, nurturing, abundance"),
    ("The Emperor", "Authority, structure, control, fatherhood"),
    ("The Hierophant", "Spiritual wisdom, tradition, conformity, institutions"),
    ("The Lovers", "Love, harmony, relationships, choices, alignment"),
    ("The Chariot", "Control, willpower, success, determination"),
    ("Strength", "Inner strength, bravery, compassion, self-control"),
    ("The Hermit", "Soul-searching, introspection, inner guidance"),
    ("Wheel of Fortune", "Good luck, karma, cycles, destiny, turning point"),
    ("Justice", "Fairness, truth, law, cause and effect"),
    ("The Hanged Man", "Pause, surrender, letting go, new perspectives"),
    ("Death", "Endings, change, transformation, transition"),
    ("Temperance", "Balance, moderation, patience, purpose"),
    ("The Devil", "Shadow self, attachment, addiction, restriction"),
    ("The Tower", "Sudden change, upheaval, chaos, revelation"),
    ("The Star", "Hope, faith, purpose, renewal, spirituality"),
    ("The Moon", "Illusion, fear, anxiety, subconscious, intuition"),
    ("The Sun", "Positivity, fun, warmth, success, vitality"),
    ("Judgement", "Reflection, reckoning, awakening, rebirth"),
    ("The World", "Completion, integration, accomplishment, travel"),
]

SUITS = {
    "Wands": "creativity, energy, inspiration, ambition, growth",
    "Cups": "emotions, relationships, feelings, intuition, connection",  
    "Swords": "intellect, conflict, decisions, truth, mental clarity",
    "Pentacles": "material wealth, career, manifestation, practical matters",
}

COURT_CARDS = ["Page", "Knight", "Queen", "King"]
NUMBERED_CARDS = list(range(1, 11))  # Ace through Ten

def get_minor_arcana():
    """Generate all minor arcana cards."""
    cards = []
    for suit, meaning in SUITS.items():
        # Numbered cards
        for num in NUMBERED_CARDS:
            if num == 1:
                name = f"Ace of {suit}"
            else:
                name = f"{num} of {suit}"
            cards.append((name, f"{suit}: {meaning}"))
        # Court cards
        for court in COURT_CARDS:
            name = f"{court} of {suit}"
            cards.append((name, f"{suit}: {meaning}"))
    return cards

def get_full_deck():
    """Return the full 78-card Tarot deck."""
    return MAJOR_ARCANA + get_minor_arcana()

def draw_card(reversed_chance=0.3):
    """Draw a random Tarot card, possibly reversed."""
    deck = get_full_deck()
    card_name, meaning = random.choice(deck)
    is_reversed = random.random() < reversed_chance

    if is_reversed:
        return f"{card_name} (Reversed)", meaning, True
    return card_name, meaning, False


def draw_multiple_cards(n=3, reversed_chance=0.3):
    """Draw n random Tarot cards without replacement, possibly reversed."""
    deck = get_full_deck()
    selected = random.sample(deck, min(n, len(deck)))
    results = []
    for card_name, meaning in selected:
        is_reversed = random.random() < reversed_chance
        if is_reversed:
            results.append((f"{card_name} (Reversed)", meaning, True))
        else:
            results.append((card_name, meaning, False))
    return results


# =============================================================================
# RANDOM GLOSSARY TERM
# =============================================================================

def get_random_word(category=None, weighted=True):
    """
    Pull a random word from the glossary.
    
    Args:
        category: Optional filter (caste, location, organization, concept, etc.)
        weighted: If True, favor entries with richer content (longer details, more related terms)
    
    Returns:
        Tuple of (term, entry) or (term, None) if glossary unavailable
    """
    if not GLOSSARY_AVAILABLE:
        # Fallback: return a term from the hardcoded special terms
        from input_check import SPECIAL_TERMS
        term = random.choice(list(SPECIAL_TERMS))
        return (term.title(), None)

    # Get all entries - validate glossary structure first
    try:
        if not hasattr(G, 'ENTRIES') or G.ENTRIES is None:
            print("Warning: Glossary ENTRIES not available, using fallback", file=sys.stderr)
            from input_check import SPECIAL_TERMS
            term = random.choice(list(SPECIAL_TERMS))
            return (term.title(), None)
        entries = list(G.ENTRIES.values())
    except (AttributeError, TypeError) as e:
        print(f"Warning: Error accessing glossary entries: {e}", file=sys.stderr)
        from input_check import SPECIAL_TERMS
        term = random.choice(list(SPECIAL_TERMS))
        return (term.title(), None)
    
    # Filter by category if specified
    if category:
        entries = [e for e in entries if e.category.lower() == category.lower()]
    
    if not entries:
        return (None, None)
    
    if weighted:
        # Weight by richness: entries with more content are more interesting seeds
        weights = []
        for e in entries:
            weight = 1.0
            if e.details:
                weight += len(e.details) / 100  # Longer details = more weight
            if e.related:
                weight += len(e.related) * 0.5  # More connections = more weight
            if e.rag_pointer:
                weight += 1.0  # Has deeper documentation
            if e.caste_features or e.location_features:
                weight += 1.5  # Structured data = richer
            weights.append(weight)
        
        entry = random.choices(entries, weights=weights, k=1)[0]
    else:
        entry = random.choice(entries)
    
    return (entry.term, entry)


def format_word_result(term, entry):
    """Format a random word result for display."""
    lines = [f"WORD: {term}"]

    if entry:
        lines.append(f"  Category: {entry.category}")
        lines.append(f"  {entry.short}")
        if entry.details:
            # Truncate long details
            details = entry.details.strip()
            if len(details) > 200:
                details = details[:200] + "..."
            lines.append(f"  {details}")
        if entry.related:
            lines.append(f"  Related: {', '.join(entry.related[:5])}")
        if entry.rag_pointer:
            lines.append(f"  → RAG: {entry.rag_pointer}")
    
    return "\n".join(lines)


# =============================================================================
# SCENARIO GENERATION
# =============================================================================

def generate_scenario_prompt(card_name, card_meaning, is_reversed, term, entry):
    """Generate the creative prompt for scenario writing."""
    
    reversal_note = ""
    if is_reversed:
        reversal_note = """
The card is REVERSED. Consider how the card's themes might manifest as:
- Blocked or delayed expression of the upright meaning
- Internal rather than external manifestation  
- Excess or deficiency of the card's qualities
- The shadow side or challenge of the archetype
"""
    
    term_context = ""
    if entry:
        term_context = f"""
SEED TERM: {term}
Category: {entry.category}
Description: {entry.short}
"""
        if entry.details:
            term_context += f"Details: {entry.details.strip()[:300]}...\n"
        if entry.related:
            term_context += f"Related concepts: {', '.join(entry.related[:5])}\n"
        if entry.rag_pointer:
            term_context += f"Source document: {entry.rag_pointer}\n"
    else:
        term_context = f"""
SEED TERM: {term}
(No glossary entry - this may be a term to explore or define through play)
"""
    
    prompt = f"""
═══════════════════════════════════════════════════════════════════════════════
SCENARIO SEED
═══════════════════════════════════════════════════════════════════════════════

CARD: {card_name}
Traditional meaning: {card_meaning}
{reversal_note}
{term_context}

═══════════════════════════════════════════════════════════════════════════════
INSTRUCTIONS FOR SCENARIO CREATION (CANTILEVER METHOD)
═══════════════════════════════════════════════════════════════════════════════

PROCEED IMMEDIATELY. Do not ask for confirmation or present options. Look up the 
seed term and related concepts using the glossary and RAG, then begin writing the 
scenario. The user asked for a random scenario; generate it.

This template uses the CANTILEVER mechanism: each section you write constrains 
what can follow, until the resolution is forced by accumulated weight rather 
than invented fresh.

THE PROCESS:

1. SET YOUR SEEDS
   - Run the --card and --seed commands shown in the template
   - These provide thematic direction and concrete grounding

2. ARTICULATE THE QUESTION AND THE GUN
   - Central question: What does this card mean for someone in this situation?
   - The gun: The physical thing that will force resolution
   - These must be set before building the scenario

3. BUILD THE MATERIALS (before act break)
   - Write Overview, Protagonist, Characters, Locations, Introduction
   - After EACH section, log constraints using --constrain
   - A constraint is a fact you've established that narrows possible resolutions
   - Example: "Kira refuses to use Compulsion" constrains what she can do
   - Example: "The engineers died with expressions of confusion" constrains what the wing contains

4. HIT THE ACT BREAK
   - Run --act-break to see all your constraints
   - The synthesis question appears: "How does [CARD] resolve through [GUN]?"
   - If you've built correctly, only a narrow band of answers fit
   - The answer should feel discovered, not invented

5. COMPLETE SYNTHESIS
   - Run --synthesize with your answer
   - Then write The Mystery and Trajectories sections
   - These are constrained by everything above

THE KEY INSIGHT:
Don't start by knowing what's in the closed wing. Start by knowing the card's
theme, then build a protagonist whose situation embodies that theme, then
build characters who represent different answers to the question, then
describe the gun's location with care—and by then, what's in the wing
should be obvious. The mystery emerges from the constraints.

WHAT MAKES A GOOD CONSTRAINT:
- Specific facts, not vague feelings
- Things that rule out possibilities
- Character decisions that have consequences
- Physical details that must be explained
- Relationships that create obligations

BAD: "Kira has complicated feelings about her heritage"
GOOD: "Kira has spent 17 years suppressing her voice—refuses to use Compulsion"

BAD: "Something bad happened in the closed wing"
GOOD: "Three engineers died attempting to force entry—expressions showed confusion, not pain"

AFTER WRITING:
1. Run `glossary.py scan <scenario_file>` to check all terms
2. Run `--act-break` to verify constraints lead to synthesis
3. Audit invented details against established lore
4. Revise any conflicts before play begins

-------------------------------------------------------------------------------
CHARACTER NAMING: USE STUBS FIRST, FILL LATER
-------------------------------------------------------------------------------

Use NAME STUBS instead of inventing names. Stubs with the same identifier
produce the same name throughout the document.

FORMAT:
    [NAME:region:type:id]           - e.g., [NAME:imperial:professional:archivist]
    [NAME:region:type:gender:id]    - e.g., [NAME:imperial:bureau:f:junior]

The identifier (id) links references to the same character. All stubs with
matching region:type:id get the same generated name.

REGIONS AND TYPES:
    imperial    - personal, aureate, bureau, professional, management, lower, homiletic
    tsatsan     - personal, aureate, family, full
    ganati      - personal, unmarked, compound, scaled
    akama       - personal, malpais, ogon, kmadhol, astrological, epithet
    avouvar     - personal, full, precinct
    caste       - mutterer, astal, draethen, takefyeh, pierrot, choir
    clone       - personal, batch, abject

EXAMPLE USAGE:
    "The archivist [NAME:imperial:professional:arch] found the document."
    "Three days later, [NAME:imperial:professional:arch] still hadn't slept."
    -> Both become the same name, e.g., "Avar Kalir"

    "[NAME:caste:mutterer:1] and [NAME:caste:mutterer:2] worked in pairs."
    -> Two different Mutterer names

After scenario is complete:
    python3 name_generator.py fill /home/claude/Scenario_-_<Name>.md
"""
    return prompt


def create_scenario_file(name, card_name, card_meaning, is_reversed, term, entry):
    """Create a .md scenario file with the framework."""
    
    # Sanitize filename
    safe_name = "".join(c for c in name if c.isalnum() or c in " -_").strip()
    safe_name = safe_name.replace(" ", "_").lower()
    filename = f"/home/claude/scenario_{safe_name}.md"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    reversal = ""
    if is_reversed:
        reversal = " *(Reversed)*"
    
    term_section = f"**Term:** {term}"
    if entry:
        term_section += f" ({entry.category})"
        term_section += f"\n\n{entry.short}"
        if entry.rag_pointer:
            term_section += f"\n\n*Source: {entry.rag_pointer}*"
    
    content = f"""# {name}

*Generated: {timestamp}*

## Seeds

**Card:** {card_name}{reversal}
*{card_meaning}*

{term_section}

```bash
# Initialize cantilever
python3 input_check.py --card "{card_name.split(' (')[0]}" "{card_meaning}"
python3 input_check.py --seed "{term}" "{entry.category if entry else 'unknown'}"
```

---

## The Central Question

[What does this card mean for someone in this situation? Frame it as a question the scenario explores.]

*Example: "What does Judgement mean for someone selling their inheritance to foreigners?"*

```bash
python3 input_check.py --central-question "YOUR QUESTION HERE"
```

---

## The Gun

[The physical thing that will force resolution. Not a metaphor—an actual object, place, or mechanism that embodies the card's theme and will demand the protagonist make a choice.]

*The gun must be concrete. "The closed wing" not "her past." "The authentication key" not "her heritage."*

```bash
python3 input_check.py --gun "YOUR GUN HERE"
```

---

## Overview

[One paragraph describing the scenario's central situation. What is happening? What is at stake? What decisions will the protagonist face?]

## The Narrative Shape

[Two to three paragraphs describing the territory. What forces are in motion? What might happen? This is a sandbox—describe the landscape, not the path.]

---

## Context Notes

[Timeline, political context, key facts. What Records are relevant? What recent events matter?]

---

## The Protagonist

### [Name]

[Physical description: caste markers, age, dress, mannerisms. Ground them in specific sensory detail.]

[Background: Where did they come from? What shaped them? What do they carry?]

### What They Want

[The conscious desire that drives their daily choices.]

### What They Fear

[The thing they work to avoid—perhaps consciously, perhaps not.]

### What They Can Do

[Specific capabilities: skills, knowledge, access, resources.]

### What They Cannot Do

[Specific limitations: what's beyond them, what requires help or luck.]

### What They Know / Don't Know

[The scope and gaps in their understanding.]

### Their Emotional Architecture

[How they handle feeling. What they permit. What they wall off.]

### Playing This Character

[The experiential texture of being them. How do they make decisions? What do they notice first?]

```bash
# Log constraints from protagonist
python3 input_check.py --constrain "PROTAGONIST FACT THAT NARROWS RESOLUTION"
python3 input_check.py --constrain "ANOTHER CONSTRAINT"
```

---

## Key Characters

### [Name] — [Role]

[Physical description. Caste, age, how they carry themselves.]

[Their situation: what brought them here, what pressures they face.]

**What they want:**

**How they operate:**

**How they speak:**

**Their relationship to the protagonist:**

**How they embody or challenge the card's theme:**

**Introduction:** [Brief scene sketch of how they first appear.]

```bash
python3 input_check.py --constrain "CHARACTER FACT THAT NARROWS RESOLUTION"
```

---

### [Name] — [Role]

[Physical description.]

[Their situation.]

**What they want:**

**How they operate:**

**How they speak:**

**Their relationship to the protagonist:**

**How they embody or challenge the card's theme:**

**Introduction:**

```bash
python3 input_check.py --constrain "CHARACTER FACT THAT NARROWS RESOLUTION"
```

---

## Supporting Cast

| Character | Role | Key Detail |
|-----------|------|------------|
| [Name] | [Function] | [One memorable trait] |
| [Name] | [Function] | [One memorable trait] |

---

## Key Locations

### [The Gun Location]

*This is where the gun lives. Describe it with care—this space will host the resolution.*

[Physical description: architecture, materials, light, sound, smell.]

[What it means: why this place matters, what tensions run through it.]

[What's actually here that will matter:]

```bash
python3 input_check.py --constrain "LOCATION FACT THAT NARROWS RESOLUTION"
```

---

### [Secondary Location]

[Physical description.]

[Significance and function.]

---

### [Tertiary Location]

[Physical description.]

[Significance and function.]

---

## The Introduction

[A fully-written opening scene, 400-600 words. Establish the ordinary before disrupting it. End on a moment that demands response.]

[This is prose, not notes. The actual opening of play.]

---

# ═══════════════════════════════════════════════════════════════════
# ACT BREAK — STOP AND SYNTHESIZE
# ═══════════════════════════════════════════════════════════════════

Before writing the sections below, run:

```bash
python3 input_check.py --act-break
```

This will display:
- Your card and gun
- All accumulated constraints
- The synthesis question: "How does [CARD] resolve through [GUN]?"

**The answer must cohere with ALL constraints.** If you've built the scenario correctly, only a narrow band of answers fit. The mystery isn't invented fresh—it's discovered from what you've already established.

Once you have your answer:

```bash
python3 input_check.py --synthesize "YOUR SYNTHESIS ANSWER"
```

Only then proceed to the sections below.

---

## The Mystery

[What is actually going on? This is your synthesis answer expanded. The hidden truth that the gun will reveal.]

[This section answers: What does the protagonist find when they engage with the gun? What was always true but hidden? How does it force the reckoning the card demanded?]

[The answer should feel inevitable given the constraints—not a twist, but a recognition.]

---

## Trajectories

What happens if the protagonist...

### ...engages with the gun directly?

[What do they find? What choice does it force? What are the consequences?]

### ...avoids the gun and pursues their original goal?

[What do they gain? What do they lose? How does the card's theme manifest anyway?]

### ...gives the gun to someone else?

[What happens when another character gets what they wanted? How does that reshape the situation?]

### ...tries to destroy or neutralize the gun?

[Is this possible? What does the attempt cost? What does it reveal?]

---

## Cross-Reference Guide

| Topic | Document |
|-------|----------|
| [Subject] | [Document name] |
| [Subject] | [Document name] |

---

## Session Notes

[Space for tracking what actually happens in play.]
"""

    # Ensure directory exists
    file_dir = os.path.dirname(filename)
    if file_dir:
        try:
            os.makedirs(file_dir, exist_ok=True)
        except PermissionError:
            print(f"ERROR: Permission denied creating directory: {file_dir}", file=sys.stderr)
            return None
        except OSError as e:
            print(f"ERROR: Failed to create directory: {file_dir}", file=sys.stderr)
            print(f"  Details: {e}", file=sys.stderr)
            return None

    # Write scenario file
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except PermissionError:
        print(f"ERROR: Permission denied writing scenario file: {filename}", file=sys.stderr)
        return None
    except IOError as e:
        print(f"ERROR: Failed to write scenario file: {filename}", file=sys.stderr)
        print(f"  Details: {e}", file=sys.stderr)
        return None

    return filename


def initialize_scenario_cache(name, filename, card_name, card_meaning, term, entry):
    """Initialize the session cache for a new scenario with cantilever fields.

    Returns:
        dict: The initialized cache, or None if write failed.
    """
    cache_file = '/home/claude/session_cache.json'

    cache = {
        "scenario_name": name,
        "scenario_file": filename,
        # Cantilever mechanism
        "card": {
            "name": card_name.split(" (")[0],  # Remove (Reversed) if present
            "meaning": card_meaning
        },
        "seed": {
            "term": term,
            "category": entry.category if entry else "unknown"
        },
        "central_question": None,
        "gun": None,
        "constraints": [],
        "synthesis": None,
        # Scene tracking
        "scene": f"Scenario: {name} (building - before act break)",
        "events": [f"Scenario created from {card_name} + {term}"],
        "questions": [],
        # Knowledge cache
        "glossary": {},
        "characters": {},
        "notes": [],
        "rag_results": {}
    }

    # Ensure directory exists
    cache_dir = os.path.dirname(cache_file)
    if cache_dir:
        try:
            os.makedirs(cache_dir, exist_ok=True)
        except OSError as e:
            print(f"ERROR: Failed to create cache directory: {cache_dir}", file=sys.stderr)
            print(f"  Details: {e}", file=sys.stderr)
            return None

    # Write cache file
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2)
    except PermissionError:
        print(f"ERROR: Permission denied writing cache file: {cache_file}", file=sys.stderr)
        return None
    except TypeError as e:
        print(f"ERROR: Failed to serialize cache to JSON: {e}", file=sys.stderr)
        return None
    except IOError as e:
        print(f"ERROR: Failed to write cache file: {cache_file}", file=sys.stderr)
        print(f"  Details: {e}", file=sys.stderr)
        return None

    return cache


# =============================================================================
# MAIN
# =============================================================================

def main():
    args = sys.argv[1:]
    
    # Help
    if not args or '-h' in args or '--help' in args:
        print(__doc__)
        return
    
    # List all cards
    if '--list-cards' in args:
        print("\n=== MAJOR ARCANA ===\n")
        for name, meaning in MAJOR_ARCANA:
            print(f"  {name}")
            print(f"    {meaning}\n")
        print("\n=== MINOR ARCANA ===\n")
        for suit, meaning in SUITS.items():
            print(f"  {suit}: {meaning}")
            print(f"    Ace through 10, Page, Knight, Queen, King\n")
        return
    
    # Just draw a card
    if '--card' in args:
        card_name, meaning, is_reversed = draw_card()
        reversal = " [REVERSED]" if is_reversed else ""
        print(f"\nCARD: {card_name}{reversal}")
        print(f"  {meaning}")
        if is_reversed:
            print("  (Consider blocked, internal, excessive, or shadow manifestations)")
        return
    
    # Just get a random word
    if '--word' in args:
        # Check for category filter
        category = None
        if '--category' in args:
            idx = args.index('--category')
            if idx + 1 < len(args):
                category = args[idx + 1]
        
        term, entry = get_random_word(category=category)
        if term:
            print(f"\n{format_word_result(term, entry)}")
        else:
            print("No matching terms found.")
        return
    
    # Multi-draw for selection (new --draw behavior)
    if '--draw' in args and '--create' not in args:
        # Draw 3 cards and 5 terms for selection
        cards = draw_multiple_cards(n=3)
        terms = draw_weighted_terms(n=5, include_persons=True)

        print(f"\n{format_selection_prompt(cards, terms)}")
        return

    # Single draw (old --draw behavior, now --draw-single)
    if '--draw-single' in args:
        card_name, meaning, is_reversed = draw_card()
        term, entry = get_random_word()

        reversal = " [REVERSED]" if is_reversed else ""
        print(f"\n{'='*70}")
        print(f"CARD: {card_name}{reversal}")
        print(f"  {meaning}")
        if is_reversed:
            print("  (Blocked/internal/excessive/shadow)")
        print(f"\n{format_word_result(term, entry)}")
        print(f"{'='*70}")
        
        if '--create' in args:
            # Get scenario name
            idx = args.index('--create')
            if idx + 1 < len(args):
                name = " ".join(args[idx + 1:])
            else:
                # Generate name from card and term
                card_short = card_name.split()[0] if " " in card_name else card_name
                name = f"The {card_short} and the {term}"
            
            filename = create_scenario_file(name, card_name, meaning, is_reversed, term, entry)
            if filename is None:
                print("Failed to create scenario file. Aborting.", file=sys.stderr)
                return

            cache = initialize_scenario_cache(name, filename, card_name, meaning, term, entry)
            if cache is None:
                print("Warning: Scenario file created but cache initialization failed.", file=sys.stderr)

            print(f"\n✔ Created: {filename}")
            print(f"✔ Initialized session cache with cantilever")
            print(f"\nCANTILEVER WORKFLOW:")
            print(f"  1. Fill in Central Question and Gun sections first")
            print(f"  2. Build Protagonist, Characters, Locations")
            print(f"  3. After each section, run: input_check.py --constrain \"fact\"")
            print(f"  4. Write Introduction")
            print(f"  5. Run: input_check.py --act-break")
            print(f"  6. Answer the synthesis question")
            print(f"  7. Run: input_check.py --synthesize \"your answer\"")
            print(f"  8. Write Mystery and Trajectories")
            print(f"\nVERIFICATION:")
            print(f"  • glossary.py scan {filename}")
            print(f"  • Check invented terms against established lore")
            # Show the creative prompt
            print(generate_scenario_prompt(card_name, meaning, is_reversed, term, entry))
        else:
            # Generate name from card and term
            card_short = card_name.split()[0] if " " in card_name else card_name
            name = f"The {card_short} and the {term}"

        filename = create_scenario_file(name, card_name, meaning, is_reversed, term, entry)
        cache = initialize_scenario_cache(name, filename, card_name, meaning, term, entry)

        print(f"\n✓ Created: {filename}")
        print(f"✓ Initialized session cache with cantilever")
        print(f"\nCANTILEVER WORKFLOW:")
        print(f"  1. Fill in Central Question and Gun sections first")
        print(f"  2. Build Protagonist, Characters, Locations")
        print(f"  3. After each section, run: input_check.py --constrain \"fact\"")
        print(f"  4. Write Introduction")
        print(f"  5. Run: input_check.py --act-break")
        print(f"  6. Answer the synthesis question")
        print(f"  7. Run: input_check.py --synthesize \"your answer\"")
        print(f"  8. Write Mystery and Trajectories")
        print(f"\nVERIFICATION:")
        print(f"  • glossary.py scan {filename}")
        print(f"  • Check invented terms against established lore")
        # Show the creative prompt
        print(generate_scenario_prompt(card_name, meaning, is_reversed, term, entry))
        return
    
    # Default: draw and show prompt
    card_name, meaning, is_reversed = draw_card()
    term, entry = get_random_word()
    
    reversal = " [REVERSED]" if is_reversed else ""
    print(f"\n{'='*70}")
    print(f"CARD: {card_name}{reversal}")
    print(f"  {meaning}")
    print(f"\n{format_word_result(term, entry)}")
    print(f"{'='*70}")
    print(generate_scenario_prompt(card_name, meaning, is_reversed, term, entry))


if __name__ == "__main__":
    main()

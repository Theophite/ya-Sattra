#!/usr/bin/env python3
"""
Scenario Initiator for the Post-Interdict Empire.

Draws a Tarot card and a random glossary term to seed a new scenario.
Generates a .md file with scenario framework and initializes the cache.

Usage:
    scenario_initiator.py                 # Draw card + word, show prompt
    scenario_initiator.py --draw          # Just draw card + word (no file)
    scenario_initiator.py --create <name> # Create scenario file after drawing
    scenario_initiator.py --word          # Just pull a random glossary word
    scenario_initiator.py --card          # Just draw a Tarot card
    scenario_initiator.py --list-cards    # Show all available cards
"""

import sys
import os
import random
import json
from datetime import datetime
from pathlib import Path

# Glossary integration
WORKING_DIR = '/home/claude'
PROJECT_DIR = '/mnt/project'
GLOSSARY_AVAILABLE = False

for search_dir in [WORKING_DIR, PROJECT_DIR]:
    if GLOSSARY_AVAILABLE:
        break
    if os.path.exists(search_dir) and os.path.exists(os.path.join(search_dir, 'glossary.py')):
        sys.path.insert(0, search_dir)
        try:
            import glossary as G
            GLOSSARY_AVAILABLE = True
        except ImportError:
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
INSTRUCTIONS FOR SCENARIO CREATION
═══════════════════════════════════════════════════════════════════════════════

Create a sandbox scenario document that weaves these elements together.
The card provides THEMATIC direction. The term provides CONCRETE grounding.

This should be a reference document for running the scenario, not a script.
Characters have agendas; the narrative shape describes forces in motion;
what actually happens emerges from play.

KEY SECTIONS TO DEVELOP:

1. OVERVIEW AND NARRATIVE SHAPE
   - One paragraph on the central situation
   - 2-3 paragraphs on forces in motion and how this might unfold
   - Describe the territory, not the path through it

2. THE PROTAGONIST
   - Rich physical description grounded in caste and circumstance
   - Psychological depth: wants, fears, blind spots, emotional architecture
   - CAPABILITIES: What can they do? Be specific about skills, access, resources
   - LIMITATIONS: What is beyond them? What requires help or luck?
   - What they know and what they don't know
   - PLAYING GUIDANCE: The experiential texture of being this person—
     how their interiority filters perception, what choices feel natural,
     what they notice first, how they handle uncertainty and anger

3. KEY CHARACTERS (2-4)
   - Full physical descriptions
   - Their situations and pressures
   - What they want, how they operate, how they speak
   - INTRODUCTION SCENES: Write a brief scene sketch for each showing
     how they first appear—where, when, what draws them to attention

4. KEY LOCATIONS (2-4)
   - Physical description: materials, light, sound, smell, proportions
   - What the location means and reveals about the world
   - Who you find here, what activities belong to this space

5. THE INTRODUCTION
   - A fully-written opening scene (400-600 words)
   - Establish the ordinary before disrupting it
   - Ground in sensory detail and protagonist's perspective
   - End on a moment that demands response

6. SUPPORTING ELEMENTS
   - Supporting cast table (brief sketches)
   - Food and daily life (material culture)
   - Cross-reference guide to project documents

Remember:
- Ground the supernatural in the mundane
- Characters have comprehensible human motivations
- The strangeness is structural, not psychological
- Show the world through action, not exposition
- Write characters as people, not plot functions

AFTER WRITING:
1. Run `glossary.py scan <scenario_file>` to check all terms
2. Search RAG for any flagged terms to verify accuracy
3. Audit invented details against established lore:
   - Do caste capabilities match their documentation?
   - Does location geography fit the parent region?
   - Do institutions and economics behave consistently?
4. Revise any conflicts before play begins
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

---

## Overview

[One paragraph describing the scenario's central situation. What is happening? What is at stake? What decisions will the protagonist face?]

## The Narrative Shape

[Two to three paragraphs describing the general arc without prescribing specific events. What is the situation at the start? What forces are in motion? What kinds of developments might occur? This is a sandbox—the shape describes the territory, not the path through it.]

---

## Context Notes

[Timeline, political context, key facts needed to run this scenario. What Records are relevant? What recent events matter? What is the ambient political situation?]

---

## The Player Character

### [Name]

[Physical description: caste markers, age, dress, mannerisms. What does someone see when they look at this person? Ground them in specific sensory detail.]

[Background: Where did they come from? What shaped them? What do they carry from their past? Two to three paragraphs of history and psychology.]

### What They Want

[The conscious desire that drives their daily choices.]

### What They Fear

[The thing they work to avoid—perhaps consciously, perhaps not.]

### What They Can Do

[Their capabilities: skills, knowledge, physical abilities, social access. What problems can they solve? What resources can they draw on? Be specific—not "good with people" but "can read a merchant's mood from how they arrange their hands, knows the protocols for addressing a curate, has favors owed by three dock supervisors."]

### What They Cannot Do

[Their limitations: skills they lack, places they cannot access, people who won't speak to them, physical constraints. What problems are beyond them? What would require help, luck, or sacrifice?]

### What They Know

[The scope of their knowledge. What can they access? What are they expert in? What have they learned that others don't know?]

### What They Don't Know

[The gaps in their understanding. Things they assume wrongly. Things they haven't thought to question. Mysteries that will unfold through play.]

### Their Emotional Architecture

[How they handle feeling. What they permit themselves. What they wall off. The texture of their inner life.]

### Playing This Character

[Guidance for the player on inhabiting this person. What is the general tenor of being them? How does their interiority filter their perception of events? What kinds of choices feel natural to them, and what would feel like a departure? 

This should describe the experiential texture of playing them—not what they do, but what it feels like to be them making decisions. Are they cautious or impulsive? Do they read situations through loyalty, through profit, through principle? When they're uncertain, do they act or wait? What do they notice first when entering a room? What makes them angry, and what do they do with that anger?]

---

## Key Characters

### [Name] — [Role]

[Physical description: enough to see them. Caste, age, how they carry themselves, what makes them visually distinctive.]

[Their situation: what brought them here, what they're dealing with, what pressures they're under. Two paragraphs minimum.]

**What they want:** [The thing they're pursuing.]

**How they operate:** [Their methods, their style, their constraints.]

**How they speak:** [Register, verbal tics, what they avoid saying.]

**Their relationship to the protagonist:** [The history, the current dynamic, the tensions or alignments.]

**Introduction:** [How they first appear in the scenario. Where, when, what they're doing, what draws them into the protagonist's attention. Write this as a brief scene sketch—a paragraph or two that could be expanded into the actual moment of introduction.]

---

### [Name] — [Role]

[Physical description.]

[Their situation.]

**What they want:**

**How they operate:**

**How they speak:**

**Their relationship to the protagonist:**

**Introduction:**

---

### [Name] — [Role]

[Physical description.]

[Their situation.]

**What they want:**

**How they operate:**

**How they speak:**

**Their relationship to the protagonist:**

**Introduction:**

---

## Supporting Cast

Brief sketches of characters who appear but aren't central:

| Character | Role | Key Detail |
|-----------|------|------------|
| [Name] | [Function] | [One memorable trait, fact, or line of dialogue] |
| [Name] | [Function] | [One memorable trait, fact, or line of dialogue] |
| [Name] | [Function] | [One memorable trait, fact, or line of dialogue] |

---

## Key Locations

### [Primary Location Name]

[Physical description: architecture, materials, light, sound, smell. Ground the reader in the space. What does it feel like to stand here? What are the proportions, the textures, the ambient sounds?]

[What it means: why this place matters, what happens here, who controls it, what tensions run through it. What does this location reveal about the world?]

[What you find here: the kinds of people, activities, objects that belong to this space. The rhythm of its use.]

---

### [Secondary Location Name]

[Physical description.]

[Significance and function.]

---

### [Tertiary Location Name]

[Physical description.]

[Significance and function.]

---

## The Introduction

[A fully-written opening scene, 400-600 words, that establishes the protagonist in their situation and presents the inciting disruption. This is where play begins.]

[Show, don't tell. Ground the reader in sensory detail and the protagonist's perspective. Establish the ordinary before disrupting it. End on a moment that demands response—a question asked, a document received, a person arriving, something noticed that changes everything.]

[This section should be written as prose, not notes. It is the actual opening of play.]

---

## Food and Daily Life

[What do people eat here? What are the small rituals of ordinary existence? What makes this place feel lived-in? Ground the scenario in material culture.]

---

## Cross-Reference Guide

[What project documents should be consulted for deeper information on topics in this scenario?]

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


def initialize_scenario_cache(name, filename, card_name, term):
    """Initialize the session cache for a new scenario.

    Returns:
        dict: The initialized cache, or None if write failed.
    """
    cache_file = '/home/claude/session_cache.json'

    cache = {
        "scenario_name": name,
        "scenario_file": filename,
        "seed_card": card_name,
        "seed_term": term,
        "scene": f"Scenario: {name} (not yet started)",
        "events": [f"Scenario created from {card_name} + {term}"],
        "questions": [],
        "glossary": {},
        "characters": {},
        "notes": [],
        "rag_summaries": {},
        "rag_rerun": []
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
    
    # Draw both card and word
    if '--draw' in args or '--create' in args:
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

            cache = initialize_scenario_cache(name, filename, card_name, term)
            if cache is None:
                print("Warning: Scenario file created but cache initialization failed.", file=sys.stderr)

            print(f"\n✔ Created: {filename}")
            if cache is not None:
                print(f"✔ Initialized session cache")
            print(f"\nNext steps:")
            print(f"  1. Read the prompt below")
            print(f"  2. Search project knowledge for relevant documents")
            print(f"  3. Fill in the scenario file")
            print(f"  4. Run: glossary.py scan {filename}")
            print(f"     - Verify all proper nouns are canonical")
            print(f"     - Check for terms that need RAG lookup")
            print(f"  5. Audit for lore accuracy:")
            print(f"     - Cross-reference invented details against established documents")
            print(f"     - Verify caste capabilities match their documentation")
            print(f"     - Check location geography against parent documents")
            print(f"     - Ensure institutions and economics behave consistently")
            print(f"  6. Use --scene to set starting location when ready to play")
            
            # Show the creative prompt
            print(generate_scenario_prompt(card_name, meaning, is_reversed, term, entry))
        else:
            # Just show the prompt without creating file
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

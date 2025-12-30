#!/usr/bin/env python3
"""
Imperial Language Root Lookup

A fast lookup tool for Imperial morphological roots. Use this for understanding
word construction, generating plausible names, and parsing Imperial compounds.

Data is loaded from imperial_roots_data.yaml. Edit that file directly using str_replace
by matching entry markers: # ═══ Entry Name ═══ through # ─── end Entry Name ───

SETUP
=====
    cp /mnt/project/imperial_roots.py /home/claude/
    cp /mnt/project/imperial_roots_data.yaml /home/claude/

COMMANDS
========
    imperial_roots.py lookup <term>           Exact match lookup
    imperial_roots.py search <query>          Search across all fields
    imperial_roots.py category <cat>          List by category (particle/suffix/root/etc)
    imperial_roots.py batch <word> ...        Parse notated words (vel.eth, ya-Don)
    imperial_roots.py find <text>             Find roots in text
    imperial_roots.py related <root>          Show roots related to a concept
    imperial_roots.py craft                   List craftsmanship-related roots
    imperial_roots.py compound <word>         Look up known compound
    imperial_roots.py generate <pattern>      Generate word from root pattern
    imperial_roots.py all [--verbose|--raw]   Dump all morphemes

NOTATION
========
    Dots separate morphemes:       vel.eth (harmony-pattern)
    Hyphens mark incomplete forms: vel- (the root), -eth (the suffix)
    Brackets mark grammatical:     [past], [dative], [nominative]

WORD STRUCTURE
==============
    Imperial words = STEM + TERMINAL
    Stems can combine multiple roots: vel.ameth.kir- (harmony-cycle-rotation-)
    Terminals complete words: vel.ameth.kir.eth (the calendar)

ASPECTUAL TERMINALS (for verbal constructions):
    -eth  (pattern)   → continuous, habitual, ongoing
    -al   (capacity)  → ability, potential, continuous capability
    -ov   (act)       → discrete, punctual, completed instance

VALIDATION
==========
    python3 -c "import yaml; yaml.safe_load(open('imperial_roots_data.yaml')); print('Valid!')"
"""

import sys
import os
import re
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Tuple

# Try to import yaml, provide helpful error if missing
try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml --break-system-packages")
    sys.exit(1)


@dataclass
class Morpheme:
    """Represents a particle, suffix, root, or other morphological unit."""
    form: str
    description: str
    category: str
    notes: Optional[str] = None
    examples: Optional[List[str]] = None
    related: Optional[List[str]] = None
    components: Optional[List[str]] = None  # For compounds
    gloss: Optional[str] = None  # For compounds


# =============================================================================
# DATA LOADING
# =============================================================================

DATA_FILE = os.path.join(os.path.dirname(__file__), "imperial_roots_data.yaml")

_cache: Dict[str, Any] = {}


def load_data() -> Dict[str, Any]:
    """Load and cache YAML data.

    Returns:
        dict: Loaded data with 'morphemes', 'compounds', and 'raw' keys.

    Raises:
        SystemExit: If data file is missing or cannot be parsed.
    """
    if _cache:
        return _cache

    if not os.path.exists(DATA_FILE):
        print(f"ERROR: Data file not found: {DATA_FILE}", file=sys.stderr)
        print("Run: cp /mnt/project/imperial_roots_data.yaml /home/claude/", file=sys.stderr)
        sys.exit(1)

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"ERROR: Failed to parse YAML file: {DATA_FILE}", file=sys.stderr)
        print(f"  Details: {e}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"ERROR: Permission denied reading: {DATA_FILE}", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"ERROR: Encoding error reading YAML file: {DATA_FILE}", file=sys.stderr)
        print(f"  Details: {e}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"ERROR: Failed to read data file: {DATA_FILE}", file=sys.stderr)
        print(f"  Details: {e}", file=sys.stderr)
        sys.exit(1)

    if data is None:
        print(f"ERROR: YAML file is empty: {DATA_FILE}", file=sys.stderr)
        sys.exit(1)
    
    # Build unified morpheme index
    morphemes = {}

    for category in ['particles', 'suffixes', 'roots', 'class_vii', 'emperor_specific', 'jargon']:
        if category not in data:
            continue
        category_data = data[category]
        # Validate category data is a dict
        if not isinstance(category_data, dict):
            print(f"Warning: Category '{category}' is not a dict, skipping", file=sys.stderr)
            continue
        for key, entry in category_data.items():
            # Skip null entries
            if entry is None:
                print(f"Warning: Null entry for key '{key}' in category '{category}', skipping", file=sys.stderr)
                continue
            # Validate entry is a dict
            if not isinstance(entry, dict):
                print(f"Warning: Entry for '{key}' is not a dict, skipping", file=sys.stderr)
                continue
            # Normalize category names
            cat_norm = {
                'particles': 'particle',
                'suffixes': 'suffix',
                'roots': 'root',
            }.get(category, category)
            m = Morpheme(
                form=entry.get('form', key),
                description=entry.get('description', ''),
                category=cat_norm,
                notes=entry.get('notes'),
                examples=entry.get('examples'),
                related=entry.get('related'),
            )
            morphemes[key.lower()] = m
            # Also index by form without hyphens
            clean_form = entry.get('form', key).replace('-', '').lower()
            if clean_form != key.lower():
                morphemes[clean_form] = m

    # Build compounds index
    compounds = {}
    if 'compounds' in data:
        compounds_data = data['compounds']
        # Validate compounds data is a dict
        if not isinstance(compounds_data, dict):
            print(f"Warning: 'compounds' section is not a dict, skipping", file=sys.stderr)
        else:
            for key, entry in compounds_data.items():
                # Skip null entries
                if entry is None:
                    print(f"Warning: Null entry for compound '{key}', skipping", file=sys.stderr)
                    continue
                if not isinstance(entry, dict):
                    print(f"Warning: Compound entry '{key}' is not a dict, skipping", file=sys.stderr)
                    continue
                c = Morpheme(
                    form=key,
                    description=entry.get('gloss', ''),
                    category='compound',
                    components=entry.get('components'),
                    gloss=entry.get('gloss'),
                )
                compounds[key.lower()] = c
    
    _cache['morphemes'] = morphemes
    _cache['compounds'] = compounds
    _cache['raw'] = data
    
    return _cache


def get_morphemes() -> Dict[str, Morpheme]:
    """Get all morphemes indexed by key."""
    return load_data()['morphemes']


def get_compounds() -> Dict[str, Morpheme]:
    """Get all compounds indexed by key."""
    return load_data()['compounds']


def get_raw() -> Dict[str, Any]:
    """Get raw YAML data."""
    return load_data()['raw']


# =============================================================================
# LOOKUP FUNCTIONS
# =============================================================================

def lookup(term: str) -> Optional[Morpheme]:
    """Look up a morpheme by key or form."""
    morphemes = get_morphemes()
    key = term.lower().replace('-', '')
    return morphemes.get(key)


def lookup_compound(term: str) -> Optional[Morpheme]:
    """Look up a known compound."""
    compounds = get_compounds()
    return compounds.get(term.lower())


def search(query: str) -> List[Tuple[str, Morpheme]]:
    """Search across all fields."""
    morphemes = get_morphemes()
    compounds = get_compounds()
    query_lower = query.lower()
    results = []
    seen = set()
    
    for key, m in morphemes.items():
        if m.form in seen:
            continue
        if query_lower in key or query_lower in m.form.lower():
            results.append((key, m))
            seen.add(m.form)
            continue
        if query_lower in m.description.lower():
            results.append((key, m))
            seen.add(m.form)
            continue
        if m.notes and query_lower in m.notes.lower():
            results.append((key, m))
            seen.add(m.form)
            continue
        if m.examples:
            for ex in m.examples:
                if query_lower in ex.lower():
                    results.append((key, m))
                    seen.add(m.form)
                    break
    
    # Also search compounds
    for key, c in compounds.items():
        if query_lower in key or (c.gloss and query_lower in c.gloss.lower()):
            results.append((key, c))
    
    return results


def list_by_category(category: str) -> List[Tuple[str, Morpheme]]:
    """List all morphemes in a category."""
    morphemes = get_morphemes()
    # Normalize category name
    cat_map = {
        'particles': 'particle',
        'particle': 'particle',
        'suffixes': 'suffix',
        'suffix': 'suffix',
        'roots': 'root',
        'root': 'root',
        'class_vii': 'class_vii',
        'emperor_specific': 'emperor_specific',
        'emperor': 'emperor_specific',
        'jargon': 'jargon',
        'compound': 'compound',
        'compounds': 'compound',
    }
    cat = cat_map.get(category.lower(), category.lower())
    
    results = []
    seen = set()
    for key, m in morphemes.items():
        if m.category == cat and m.form not in seen:
            results.append((key, m))
            seen.add(m.form)
    
    if cat == 'compound':
        for key, c in get_compounds().items():
            results.append((key, c))
    
    return sorted(results, key=lambda x: x[1].form.lower().replace('-', ''))


def find_related(root_key: str) -> List[Tuple[str, Morpheme]]:
    """Find roots related to a given root."""
    morphemes = get_morphemes()
    target = lookup(root_key)
    if not target:
        return []
    
    results = []
    seen = set()
    
    # Direct related field
    if target.related:
        for rel in target.related:
            m = lookup(rel)
            if m and m.form not in seen:
                results.append((rel, m))
                seen.add(m.form)
    
    # Reverse lookup - find things that list this as related
    for key, m in morphemes.items():
        if m.form in seen:
            continue
        if m.related and root_key.lower() in [r.lower() for r in m.related]:
            results.append((key, m))
            seen.add(m.form)
    
    return results


def list_craft_roots() -> List[Tuple[str, Morpheme]]:
    """List craftsmanship-related roots."""
    craft_keys = [
        # Heat/fire working
        'thur', 'vosh',
        # Shaping/forming
        'mas', 'lam', 'kir', 'per', 'kov',
        # Cutting/removing
        'kor', 'shev', 'del',
        # Joining/connecting
        'gar', 'tesh', 'vor',
        # Finishing
        'pol', 'kash',
        # Measurement/precision
        'kedh',
        # Specialized
        'gash', 'veren', 'merev',
        # Tools/implements
        'ot',
        # Materials/value
        'kem', 'aur', 'pel',
        # Labor
        'dal', 'shar'
    ]
    results = []
    for key in craft_keys:
        m = lookup(key)
        if m:
            results.append((key, m))
    return results


# =============================================================================
# BATCH PARSING
# =============================================================================

def parse_word(word: str) -> Dict[str, Any]:
    """Parse a notated Imperial word into its components."""
    morphemes = get_morphemes()
    
    # Handle bracketed prefixes like [past]
    tense = None
    if word.startswith('['):
        match = re.match(r'\[([^\]]+)\]-?(.+)', word)
        if match:
            tense = match.group(1)
            word = match.group(2)
    
    # Handle particle prefixes
    particle = None
    for p in ['ya-', 'es-', 'ta-']:
        if word.lower().startswith(p):
            particle = p.rstrip('-')
            word = word[len(p):]
            break
    
    # Split on dots
    parts = word.replace('-', '').split('.')
    
    found = []
    notes = []
    
    for part in parts:
        m = lookup(part)
        if m:
            found.append({
                'form': part,
                'meaning': m.description.split('.')[0],
                'position': m.category
            })
        else:
            # Try partial matches
            found.append({
                'form': part,
                'meaning': '?',
                'position': 'unknown'
            })
            notes.append(f"'{part}' not found in morpheme database")
    
    # Build gloss
    gloss_parts = []
    if tense:
        gloss_parts.append(f"[{tense}]")
    if particle:
        m = lookup(particle)
        if m:
            gloss_parts.append(m.description.split('.')[0].lower())
    for f in found:
        if f['meaning'] != '?':
            gloss_parts.append(f['meaning'].lower())
        else:
            gloss_parts.append(f['form'])
    
    return {
        'original': word,
        'tense': tense,
        'particle': particle,
        'morphemes': found,
        'gloss': '-'.join(gloss_parts) if gloss_parts else word,
        'notes': notes
    }


def batch_parse(words: List[str]) -> Dict[str, Dict]:
    """Parse multiple words."""
    return {w: parse_word(w) for w in words}


# =============================================================================
# TEXT SCANNING
# =============================================================================

def find_roots_in_text(text: str) -> List[Tuple[str, List[str]]]:
    """Find Imperial roots in arbitrary text."""
    morphemes = get_morphemes()
    
    # Extract potential Imperial words (capitalized or with dots/hyphens)
    patterns = [
        r'\b[A-Z][a-z]+(?:-[A-Z][a-z]+)*\b',  # Capitalized, possibly hyphenated
        r'\b[a-z]+\.[a-z.]+\b',  # Dot-separated notation
        r'\bya-[A-Z][a-z]+\b',  # ya- prefix
        r'\bes-[A-Z][a-z]+\b',  # es- prefix
        r'\bta-?[A-Z][a-z]+\b',  # ta- prefix
    ]
    
    candidates = set()
    for pattern in patterns:
        candidates.update(re.findall(pattern, text))
    
    results = []
    for word in candidates:
        found_roots = []
        # Normalize
        clean = word.lower().replace('-', '.').replace('ya.', '').replace('es.', '').replace('ta.', '')
        parts = clean.split('.')
        
        for part in parts:
            # Try exact match
            if part in morphemes:
                found_roots.append(part)
                continue
            # Try prefix matching (for fossilized forms)
            for key in morphemes:
                if part.startswith(key) and len(key) >= 3:
                    found_roots.append(key)
                    break
        
        if found_roots:
            results.append((word, found_roots))
    
    return results


# =============================================================================
# FORMATTING
# =============================================================================

def format_morpheme(m: Morpheme, verbose: bool = True) -> str:
    """Format a morpheme for display."""
    lines = [
        f"\n{'='*60}",
        f"  {m.form.upper()}  [{m.category}]",
        f"{'='*60}",
        f"\n{m.description}"
    ]
    
    if m.notes:
        lines.append(f"\n[{m.notes}]")
    
    if m.examples and verbose:
        lines.append("\nExamples:")
        for ex in m.examples[:5]:
            lines.append(f"  • {ex}")
    
    if m.related:
        lines.append(f"\nRelated: {', '.join(m.related)}")
    
    if m.components:
        lines.append(f"\nComponents: {' + '.join(m.components)}")
        if m.gloss:
            lines.append(f"Gloss: {m.gloss}")
    
    return '\n'.join(lines)


def format_parse(word: str, analysis: Dict, verbose: bool = True) -> str:
    """Format a parsed word for display."""
    lines = [f"\n{'─'*50}", f"  {word}"]
    
    if analysis.get('tense'):
        lines.append(f"  Tense: [{analysis['tense']}]")
    if analysis.get('particle'):
        lines.append(f"  Particle: {analysis['particle']}-")
    
    lines.append("\n  Components:")
    for m in analysis['morphemes']:
        marker = {
            'particle': 'â—†',
            'suffix': 'â—‹',
            'root': '●',
            'class_vii': '★',
            'emperor_specific': '✕',
            'jargon': 'â—‡',
            'unknown': '?'
        }.get(m['position'], '?')
        lines.append(f"    {marker} {m['form']:12} → {m['meaning']}")
    
    lines.append(f"\n  Gloss: {analysis['gloss']}")
    
    if analysis['notes'] and verbose:
        lines.append("\n  Notes:")
        for note in analysis['notes']:
            lines.append(f"    • {note}")
    
    return '\n'.join(lines)


# =============================================================================
# CLI
# =============================================================================

def print_help():
    """Print usage help."""
    print(__doc__)


def main():
    if len(sys.argv) < 2:
        print_help()
        return
    
    cmd = sys.argv[1].lower()
    
    if cmd in ['help', '-h', '--help']:
        print_help()
        return
    
    if cmd == 'lookup':
        if len(sys.argv) < 3:
            print("Usage: imperial_roots.py lookup <term>")
            return
        term = sys.argv[2]
        m = lookup(term)
        if m:
            print(format_morpheme(m))
        else:
            # Try compound
            c = lookup_compound(term)
            if c:
                print(format_morpheme(c))
            else:
                results = search(term)
                if results:
                    print(f"No exact match for '{term}'. Similar:")
                    for key, m in results[:5]:
                        print(f"  • {m.form}: {m.description[:50]}...")
                else:
                    print(f"No match found for '{term}'")
    
    elif cmd == 'search':
        if len(sys.argv) < 3:
            print("Usage: imperial_roots.py search <query>")
            return
        query = ' '.join(sys.argv[2:])
        results = search(query)
        if results:
            print(f"\nFound {len(results)} matches for '{query}':\n")
            for key, m in results:
                print(f"  {m.form:15} [{m.category:8}] {m.description[:45]}...")
        else:
            print(f"No matches for '{query}'")
    
    elif cmd == 'category':
        if len(sys.argv) < 3:
            print("Usage: imperial_roots.py category <category>")
            print("Categories: particle, suffix, root, class_vii, emperor_specific, jargon, compound")
            return
        cat = sys.argv[2]
        results = list_by_category(cat)
        if results:
            print(f"\n{'='*60}")
            print(f"  {cat.upper()} ({len(results)} entries)")
            print(f"{'='*60}\n")
            for key, m in results:
                print(f"  {m.form:18} {m.description[:50]}...")
        else:
            print(f"No entries for category '{cat}'")
            print("Categories: particle, suffix, root, class_vii, emperor_specific, jargon, compound")
    
    elif cmd == 'batch':
        if len(sys.argv) < 3:
            print("Usage: imperial_roots.py batch <word> [word2] ...")
            print("\nExamples:")
            print("  imperial_roots.py batch vel.eth ya-Don SETAL.ser")
            return
        verbose = '-v' in sys.argv or '--verbose' in sys.argv
        words = [w for w in sys.argv[2:] if not w.startswith('-')]
        results = batch_parse(words)
        for word in words:
            print(format_parse(word, results[word], verbose=verbose))
        print()
    
    elif cmd == 'find':
        if len(sys.argv) < 3:
            print("Usage: imperial_roots.py find <text>")
            return
        text = ' '.join(sys.argv[2:])
        results = find_roots_in_text(text)
        if results:
            print(f"\nRoots found in text:\n")
            for word, roots in results:
                print(f"  {word}:")
                for root in roots:
                    m = lookup(root)
                    if m:
                        print(f"    → {m.form}: {m.description[:50]}...")
        else:
            print("No recognizable roots found.")
    
    elif cmd == 'related':
        if len(sys.argv) < 3:
            print("Usage: imperial_roots.py related <root>")
            return
        root = sys.argv[2]
        results = find_related(root)
        if results:
            print(f"\nRoots related to '{root}':\n")
            for key, m in results:
                print(f"  {m.form:15} {m.description[:50]}...")
        else:
            m = lookup(root)
            if m:
                print(f"No related roots found for '{root}'")
            else:
                print(f"Root '{root}' not found")
    
    elif cmd == 'craft':
        results = list_craft_roots()
        print(f"\n{'='*60}")
        print(f"  CRAFTSMANSHIP ROOTS ({len(results)} entries)")
        print(f"{'='*60}\n")
        for key, m in results:
            print(f"  {m.form:15} {m.description[:50]}...")
        print("\nUse 'imperial_roots.py lookup <root>' for details.")
    
    elif cmd == 'compound':
        if len(sys.argv) < 3:
            print("Usage: imperial_roots.py compound <word>")
            return
        term = sys.argv[2]
        c = lookup_compound(term)
        if c:
            print(format_morpheme(c))
        else:
            print(f"Compound '{term}' not found in database.")
            print("Use 'imperial_roots.py batch <word>' to parse unknown compounds.")
    
    elif cmd == 'all':
        verbose = '-v' in sys.argv or '--verbose' in sys.argv
        raw = '-r' in sys.argv or '--raw' in sys.argv
        
        morphemes = get_morphemes()
        compounds = get_compounds()
        
        if raw:
            seen = set()
            for m in morphemes.values():
                if m.form not in seen:
                    print(m.form)
                    seen.add(m.form)
            for c in compounds.values():
                print(c.form)
            return
        
        categories = ['particle', 'suffix', 'root', 'class_vii', 'emperor_specific', 'jargon']
        
        for cat in categories:
            results = list_by_category(cat)
            if not results:
                continue
            
            print(f"\n{'='*60}")
            print(f"  {cat.upper()} ({len(results)} entries)")
            print(f"{'='*60}\n")
            
            for key, m in results:
                if verbose:
                    print(f"{m.form}")
                    print(f"  {m.description}")
                    if m.notes:
                        print(f"  [{m.notes}]")
                    if m.examples:
                        for ex in m.examples[:2]:
                            print(f"    • {ex}")
                    print()
                else:
                    desc = m.description.split('.')[0]
                    if len(desc) > 50:
                        desc = desc[:47] + "..."
                    print(f"  {m.form:18} {desc}")
        
        # Compounds
        print(f"\n{'='*60}")
        print(f"  COMPOUNDS ({len(compounds)} entries)")
        print(f"{'='*60}\n")
        for key, c in sorted(compounds.items()):
            if c.components:
                comp_str = ' + '.join(c.components)
                print(f"  {c.form:18} ← {comp_str}")
    
    else:
        print(f"Unknown command: {cmd}")
        print_help()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Post-Interdict Empire Glossary

A fast lookup tool for setting terminology. Use this BEFORE RAG searches
when you need quick definitions or to verify term existence.

Data is loaded from glossary_data.yaml. Edit that file directly using str_replace
by matching entry markers: # ═══ Entry Name ═══ through # ─── end Entry Name ───

SETUP
=====
    cp /mnt/project/glossary.py /home/claude/
    cp /mnt/project/glossary_data.yaml /home/claude/

COMMANDS
========
    glossary.py lookup <term>           Exact match lookup
    glossary.py search <query>          Search across all fields
    glossary.py category <category>     List all entries (caste/location/organization/concept)
    glossary.py random [category]       Get a random entry (optionally from specific category)
    glossary.py caste-feature <f> <v>   Find castes by feature value
    glossary.py caste-compare <c1> <c2> Compare two castes
    glossary.py caste-trait <trait>     Find castes with specific trait
    glossary.py scene-setup <location>  Get location details for scene writing
    glossary.py location-tree <loc>     Show location hierarchy
    glossary.py scan <filepath> [-v]    Scan document for all glossary terms (canonicity check)
    glossary.py scan-text [-v]          Scan piped text (cat doc.txt | glossary.py scan-text)

VALIDATION
==========
    python3 -c "import yaml; yaml.safe_load(open('glossary_data.yaml')); print('Valid!')"

ADDING ENTRIES
==============
Entries are alphabetical within category sections. To insert, find the preceding
entry's end marker and use str_replace:

    old_str="  # ─── end Serrulata ───\\n\\n  # ═══ Springheel ═══"
    new_str=\"\"\"  # ─── end Serrulata ───

  # ═══ Sewer-Fishers ═══
  Sewer-Fishers:
    category: caste
    short: "Description."
    ...
  # ─── end Sewer-Fishers ───

  # ═══ Springheel ═══\"\"\"

ENTRY TEMPLATES
===============
Caste:
    # ═══ Name ═══
    Name:
      category: caste
      short: "One-line description."
      details: |
        Optional longer description.
      rag_pointer: "Source Document"
      related: [Term1, Term2]
      caste_features:
        morphology: baseline|modified|divergent|merged|parasitic|variable
        scale: tiny|small|baseline|tall|giant|variable
        compulsion: triggers|susceptible|immune|unknown
        lifespan: reduced|baseline|extended|variable
        cognition: baseline|enhanced|specialized|reduced|semi
        population: extinct|remnant|rare|common|majority
        physical_traits: ["trait one", "trait two"]
        original_function: "designed purpose"
        current_role: "current purpose"
        distribution: ["location one"]
        health_issues: ["issue one"]
        special: ["unique characteristic"]
    # ─── end Name ───

Location:
    # ═══ Name ═══
    Name:
      category: location
      short: "One-line description."
      rag_pointer: "Source Document"
      related: [Term1, Term2]
      location_features:
        level: site|neighborhood|district|city|territory
        location_type: settlement|infrastructure|commercial|religious|administrative|residential|industrial|underground|educational|polity
        parent: Parent Location
        children: [Child1, Child2]
        controlling_entity: "Who runs it"
        population: "~50,000"
        primary_function: "Main purpose"
    # ─── end Name ───

Organization/Concept:
    # ═══ Name ═══
    Name:
      category: organization  (or: concept)
      short: "One-line description."
      details: "Optional longer description."
      rag_pointer: "Source Document"
      related: [Term1, Term2]
    # ─── end Name ───

COMMON ERRORS
=============
    "Unknown Compulsion value: variable" -> Use: triggers|susceptible|immune|unknown
    "Unknown Lifespan value: unknown"    -> Use: reduced|baseline|extended|variable
    YAML parse error                     -> Check 2-space indent, quote strings with colons
    Entry not found after adding         -> Verify marker format: ═══ and ───

OUTPUT
======
    cp /home/claude/glossary_data.yaml /mnt/user-data/outputs/
"""

import sys
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Set
from difflib import get_close_matches
from enum import Enum


# =============================================================================
# CASTE FEATURE SCHEMA
# =============================================================================

class Morphology(Enum):
    """Body plan relative to unmodified humans."""
    BASELINE = "baseline"
    MODIFIED_HUMANOID = "modified"
    DIVERGENT = "divergent"
    MERGED = "merged"
    PARASITIC = "parasitic"
    VARIABLE = "variable"


class Scale(Enum):
    """Size relative to baseline humans (~1.7m)."""
    TINY = "tiny"
    SMALL = "small"
    BASELINE = "baseline"
    TALL = "tall"
    GIANT = "giant"
    VARIABLE = "variable"


class Compulsion(Enum):
    """Relationship to Compulsion mechanism."""
    TRIGGERS = "triggers"
    SUSCEPTIBLE = "susceptible"
    IMMUNE = "immune"
    UNKNOWN = "unknown"


class Lifespan(Enum):
    """Life expectancy category."""
    REDUCED = "reduced"
    BASELINE = "baseline"
    EXTENDED = "extended"
    VARIABLE = "variable"


class Cognition(Enum):
    """Cognitive modification status."""
    BASELINE = "baseline"
    ENHANCED = "enhanced"
    SPECIALIZED = "specialized"
    REDUCED = "reduced"
    SEMI_SENTIENT = "semi"


class Population(Enum):
    """Approximate population scale."""
    EXTINCT = "extinct"
    REMNANT = "remnant"
    RARE = "rare"
    COMMON = "common"
    MAJORITY = "majority"


@dataclass
class CasteFeatures:
    """Structured properties of an engineered caste."""
    morphology: Morphology
    scale: Scale
    compulsion: Compulsion
    lifespan: Lifespan
    cognition: Cognition
    population: Population
    
    physical_traits: List[str] = field(default_factory=list)
    original_function: str = ""
    current_role: str = ""
    distribution: List[str] = field(default_factory=list)
    interfertile_with: List[str] = field(default_factory=list)
    health_issues: List[str] = field(default_factory=list)
    lifespan_note: str = ""
    special: List[str] = field(default_factory=list)


# =============================================================================
# LOCATION FEATURE SCHEMA
# =============================================================================

class Level(Enum):
    """Hierarchical position in location tree."""
    TERRITORY = "territory"
    CITY = "city"
    DISTRICT = "district"
    NEIGHBORHOOD = "neighborhood"
    SITE = "site"


class LocationType(Enum):
    """Functional character of location."""
    POLITY = "polity"
    SETTLEMENT = "settlement"
    ADMINISTRATIVE = "administrative"
    INDUSTRIAL = "industrial"
    COMMERCIAL = "commercial"
    RESIDENTIAL = "residential"
    RELIGIOUS = "religious"
    MILITARY = "military"
    ARCOLOGY = "arcology"
    INFRASTRUCTURE = "infrastructure"
    GEOGRAPHIC = "geographic"
    GROUPING = "grouping"
    EDUCATIONAL = "educational"
    UNDERGROUND = "underground"
    MONUMENT = "monument"


@dataclass
class LocationFeatures:
    """Structured properties of a location."""
    level: Level
    location_type: LocationType
    
    parent: str = ""
    children: List[str] = field(default_factory=list)
    member_of: str = ""
    aliases: List[str] = field(default_factory=list)
    
    controlling_entity: str = ""
    population: str = ""
    primary_function: str = ""
    castes_present: List[str] = field(default_factory=list)
    
    temporal_effects: str = ""
    hazards: List[str] = field(default_factory=list)
    notable_features: List[str] = field(default_factory=list)
    
    borders: Dict[str, List[str]] = field(default_factory=dict)
    transit: List[Dict[str, str]] = field(default_factory=list)
    real_world_anchor: str = ""


@dataclass
class AestheticFeatures:
    """Visual and material culture details for a location or culture."""
    visual_vocabulary: List[str] = field(default_factory=list)
    materials: List[str] = field(default_factory=list)
    colors: List[str] = field(default_factory=list)
    sensory: List[str] = field(default_factory=list)
    intention: str = ""
    environment: str = ""
    key_elements: List[str] = field(default_factory=list)
    construction: str = ""


@dataclass
class GlossaryEntry:
    term: str
    category: str
    short: str
    details: str = ""
    rag_pointer: str = ""
    related: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)
    caste_features: Optional[CasteFeatures] = None
    location_features: Optional[LocationFeatures] = None
    aesthetic_features: Optional[AestheticFeatures] = None
    local_aesthetic: str = ""
    person_location: str = ""  # For category=person: where they're based


# =============================================================================
# YAML LOADING
# =============================================================================

def str_to_enum(enum_class, value):
    """Convert string to enum value."""
    if value is None:
        return None
    value = str(value).lower()
    for member in enum_class:
        if member.value == value:
            return member
    raise ValueError(f"Unknown {enum_class.__name__} value: {value}")


def load_caste_features(data: dict) -> CasteFeatures:
    """Load CasteFeatures from YAML dict."""
    return CasteFeatures(
        morphology=str_to_enum(Morphology, data.get('morphology')),
        scale=str_to_enum(Scale, data.get('scale')),
        compulsion=str_to_enum(Compulsion, data.get('compulsion')),
        lifespan=str_to_enum(Lifespan, data.get('lifespan')),
        cognition=str_to_enum(Cognition, data.get('cognition')),
        population=str_to_enum(Population, data.get('population')),
        physical_traits=data.get('physical_traits', []),
        original_function=data.get('original_function', ''),
        current_role=data.get('current_role', ''),
        distribution=data.get('distribution', []),
        interfertile_with=data.get('interfertile_with', []),
        health_issues=data.get('health_issues', []),
        lifespan_note=data.get('lifespan_note', ''),
        special=data.get('special', [])
    )


def load_location_features(data: dict) -> LocationFeatures:
    """Load LocationFeatures from YAML dict."""
    return LocationFeatures(
        level=str_to_enum(Level, data.get('level')),
        location_type=str_to_enum(LocationType, data.get('location_type')),
        parent=data.get('parent', ''),
        children=data.get('children', []),
        member_of=data.get('member_of', ''),
        aliases=data.get('aliases', []),
        controlling_entity=data.get('controlling_entity', ''),
        population=data.get('population', ''),
        primary_function=data.get('primary_function', ''),
        castes_present=data.get('castes_present', []),
        temporal_effects=data.get('temporal_effects', ''),
        hazards=data.get('hazards', []),
        notable_features=data.get('notable_features', []),
        borders=data.get('borders', {}),
        transit=data.get('transit', []),
        real_world_anchor=data.get('real_world_anchor', '')
    )


def load_aesthetic_features(data: dict) -> AestheticFeatures:
    """Load AestheticFeatures from YAML dict."""
    return AestheticFeatures(
        visual_vocabulary=data.get('visual_vocabulary', []),
        materials=data.get('materials', []),
        colors=data.get('colors', []),
        sensory=data.get('sensory', []),
        intention=data.get('intention', ''),
        environment=data.get('environment', ''),
        key_elements=data.get('key_elements', []),
        construction=data.get('construction', '')
    )


def load_entry(term: str, data: dict) -> GlossaryEntry:
    """Load a single GlossaryEntry from YAML dict."""
    caste_features = None
    location_features = None
    aesthetic_features = None
    
    if 'caste_features' in data:
        caste_features = load_caste_features(data['caste_features'])
    
    if 'location_features' in data:
        location_features = load_location_features(data['location_features'])
    
    if 'aesthetic_features' in data:
        aesthetic_features = load_aesthetic_features(data['aesthetic_features'])
    
    return GlossaryEntry(
        term=term,
        category=data.get('category', ''),
        short=data.get('short', ''),
        details=data.get('details', ''),
        rag_pointer=data.get('rag_pointer', ''),
        related=data.get('related', []),
        aliases=data.get('aliases', []),
        caste_features=caste_features,
        location_features=location_features,
        aesthetic_features=aesthetic_features,
        local_aesthetic=data.get('local_aesthetic', ''),
        person_location=data.get('person_location', '')
    )


def load_glossary(yaml_path: Path = None) -> Dict[str, GlossaryEntry]:
    """Load all glossary entries from YAML file."""
    if yaml_path is None:
        yaml_path = Path(__file__).parent / "glossary_data.yaml"
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    entries = {}
    for term, entry_data in data.get('entries', {}).items():
        entry = load_entry(term, entry_data)
        entries[term.lower()] = entry
    
    return entries


# =============================================================================
# GLOBAL ENTRIES - Loaded on import
# =============================================================================

ENTRIES: Dict[str, GlossaryEntry] = {}

def _init_entries():
    """Initialize entries from YAML file."""
    global ENTRIES
    try:
        ENTRIES = load_glossary()
    except Exception as e:
        print(f"Warning: Could not load glossary_data.yaml: {e}", file=sys.stderr)
        ENTRIES = {}

_init_entries()


# =============================================================================
# QUERY FUNCTIONS
# =============================================================================

def lookup(term: str) -> Optional[GlossaryEntry]:
    """Look up a term directly, including by alias."""
    # Direct lookup first
    entry = ENTRIES.get(term.lower())
    if entry:
        return entry
    
    # Check aliases (both top-level and location_features.aliases)
    term_lower = term.lower()
    for entry in ENTRIES.values():
        # Check top-level aliases
        if entry.aliases:
            for alias in entry.aliases:
                if alias.lower() == term_lower:
                    return entry
        # Check location_features.aliases
        if entry.location_features and entry.location_features.aliases:
            for alias in entry.location_features.aliases:
                if alias.lower() == term_lower:
                    return entry
    
    return None


def search(query: str) -> List[GlossaryEntry]:
    """Search terms, shorts, and details for query string."""
    query_lower = query.lower()
    results = []
    for entry in ENTRIES.values():
        if (query_lower in entry.term.lower() or
            query_lower in entry.short.lower() or
            query_lower in entry.details.lower()):
            results.append(entry)
    return results


def category(cat: str) -> List[GlossaryEntry]:
    """Get all entries in a category."""
    return [e for e in ENTRIES.values() if e.category.lower() == cat.lower()]


def related(term: str) -> List[GlossaryEntry]:
    """Get an entry and all its related entries."""
    entry = lookup(term)
    if not entry:
        return []
    results = [entry]
    for rel in entry.related:
        rel_entry = lookup(rel)
        if rel_entry:
            results.append(rel_entry)
    return results


def check(term: str) -> Dict[str, Any]:
    """Check if term exists, return entry and similar terms if not."""
    entry = lookup(term)
    if entry:
        return {"exists": True, "entry": entry, "similar": []}
    
    all_terms = [e.term for e in ENTRIES.values()]
    similar = get_close_matches(term, all_terms, n=5, cutoff=0.4)
    return {"exists": False, "entry": None, "similar": similar}


import random as _random

def random_entry(cat: str = None, weighted: bool = True) -> Optional[GlossaryEntry]:
    """
    Get a random glossary entry.
    
    Args:
        cat: Optional category filter (caste, location, organization, concept, etc.)
        weighted: If True, favor entries with richer content
    
    Returns:
        A random GlossaryEntry, or None if no entries match
    """
    entries = list(ENTRIES.values())
    
    if cat:
        entries = [e for e in entries if e.category.lower() == cat.lower()]
    
    if not entries:
        return None
    
    if weighted:
        # Weight by richness: entries with more content are more interesting
        weights = []
        for e in entries:
            weight = 1.0
            if e.details:
                weight += len(e.details) / 100
            if e.related:
                weight += len(e.related) * 0.5
            if e.rag_pointer:
                weight += 1.0
            if e.caste_features or e.location_features:
                weight += 1.5
            weights.append(weight)
        
        return _random.choices(entries, weights=weights, k=1)[0]
    else:
        return _random.choice(entries)


# =============================================================================
# CASTE-SPECIFIC QUERIES
# =============================================================================

def caste_by_feature(feature: str, value: str) -> List[GlossaryEntry]:
    """Find castes by a specific feature value."""
    results = []
    for entry in ENTRIES.values():
        if not entry.caste_features:
            continue
        cf = entry.caste_features
        feature_lower = feature.lower()
        
        if feature_lower == "morphology" and cf.morphology.value == value.lower():
            results.append(entry)
        elif feature_lower == "scale" and cf.scale.value == value.lower():
            results.append(entry)
        elif feature_lower == "compulsion" and cf.compulsion.value == value.lower():
            results.append(entry)
        elif feature_lower == "lifespan" and cf.lifespan.value == value.lower():
            results.append(entry)
        elif feature_lower == "cognition" and cf.cognition.value == value.lower():
            results.append(entry)
        elif feature_lower == "population" and cf.population.value == value.lower():
            results.append(entry)
    
    return results


def caste_by_trait(trait: str) -> List[GlossaryEntry]:
    """Find castes with a trait in physical_traits or special."""
    trait_lower = trait.lower()
    results = []
    for entry in ENTRIES.values():
        if not entry.caste_features:
            continue
        cf = entry.caste_features
        for t in cf.physical_traits + cf.special:
            if trait_lower in t.lower():
                results.append(entry)
                break
    return results


def caste_compare(caste1: str, caste2: str) -> Dict[str, Any]:
    """Compare two castes side by side."""
    e1 = lookup(caste1)
    e2 = lookup(caste2)
    
    if not e1 or not e1.caste_features:
        return {"error": f"'{caste1}' not found or not a caste"}
    if not e2 or not e2.caste_features:
        return {"error": f"'{caste2}' not found or not a caste"}
    
    cf1 = e1.caste_features
    cf2 = e2.caste_features
    
    return {
        "caste1": e1.term,
        "caste2": e2.term,
        "comparison": {
            "morphology": (cf1.morphology.value, cf2.morphology.value),
            "scale": (cf1.scale.value, cf2.scale.value),
            "compulsion": (cf1.compulsion.value, cf2.compulsion.value),
            "lifespan": (cf1.lifespan.value, cf2.lifespan.value),
            "cognition": (cf1.cognition.value, cf2.cognition.value),
            "population": (cf1.population.value, cf2.population.value),
        },
        "original_function": (cf1.original_function, cf2.original_function),
        "current_role": (cf1.current_role, cf2.current_role),
    }


# =============================================================================
# MULTI-WORD TERM EXTRACTION
# =============================================================================

def get_multi_word_terms() -> set:
    """
    Extract all multi-word terms from the glossary.
    
    Returns a set of lowercase term names that contain spaces or hyphens.
    This is used by input_check.py to find glossary terms in user text.
    """
    _init_entries()
    multi_word = set()
    for term in ENTRIES.keys():
        # Include terms with spaces or hyphens (multi-word terms)
        if ' ' in term or '-' in term:
            multi_word.add(term.lower())
    return multi_word


def get_all_terms() -> set:
    """
    Get all glossary term names (lowercase).
    
    Returns a set of all term names for quick membership testing.
    """
    _init_entries()
    return {term.lower() for term in ENTRIES.keys()}


# =============================================================================
# DOCUMENT SCANNING FOR CANONICITY CHECKS
# =============================================================================

import re

def _build_term_patterns() -> List[tuple]:
    """Build regex patterns for all glossary terms, sorted by length (longest first)."""
    patterns = []
    for term, entry in ENTRIES.items():
        # Escape special regex chars and build word-boundary pattern
        escaped = re.escape(term)
        # Allow for hyphen/space variation (e.g., "ya-Sattra" matches "ya Sattra")
        escaped = escaped.replace(r'\ ', r'[\s\-]').replace(r'\-', r'[\s\-]')
        pattern = re.compile(r'\b' + escaped + r'\b', re.IGNORECASE)
        patterns.append((term, pattern, entry))
    
    # Sort by term length descending so longer terms match first
    patterns.sort(key=lambda x: -len(x[0]))
    return patterns


def scan_document(text: str, include_counts: bool = True) -> Dict[str, Any]:
    """
    Scan document text for all glossary terms.
    
    Returns:
        {
            "found": {term: {"entry": GlossaryEntry, "count": int, "contexts": [str]}},
            "by_category": {category: [terms]},
            "stats": {"total_terms": int, "unique_terms": int, ...},
            "potential_issues": [str]  # Terms that look canonical but aren't in glossary
        }
    """
    patterns = _build_term_patterns()
    found = {}
    matched_spans = []  # Track matched positions to avoid double-counting
    
    for term, pattern, entry in patterns:
        matches = list(pattern.finditer(text))
        if not matches:
            continue
        
        # Filter out matches that overlap with already-matched longer terms
        valid_matches = []
        for m in matches:
            overlaps = False
            for start, end in matched_spans:
                if not (m.end() <= start or m.start() >= end):
                    overlaps = True
                    break
            if not overlaps:
                valid_matches.append(m)
                matched_spans.append((m.start(), m.end()))
        
        if valid_matches:
            # Extract context snippets (30 chars before/after)
            contexts = []
            for m in valid_matches[:3]:  # Limit to 3 examples
                start = max(0, m.start() - 30)
                end = min(len(text), m.end() + 30)
                snippet = text[start:end].replace('\n', ' ')
                if start > 0:
                    snippet = '...' + snippet
                if end < len(text):
                    snippet = snippet + '...'
                contexts.append(snippet)
            
            found[term] = {
                "entry": entry,
                "count": len(valid_matches),
                "contexts": contexts
            }
    
    # Organize by category
    by_category = {}
    for term, data in found.items():
        cat = data["entry"].category
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(term)
    
    # Sort each category alphabetically
    for cat in by_category:
        by_category[cat].sort()
    
    # Compute stats
    stats = {
        "total_terms": sum(d["count"] for d in found.values()),
        "unique_terms": len(found),
        "by_category": {cat: len(terms) for cat, terms in by_category.items()}
    }
    
    # Look for potential issues: capitalized multi-word phrases that look like proper nouns
    # but aren't in the glossary
    potential_issues = _find_potential_terms(text, found)
    
    return {
        "found": found,
        "by_category": by_category,
        "stats": stats,
        "potential_issues": potential_issues
    }


def _find_potential_terms(text: str, found: Dict) -> List[str]:
    """Find capitalized phrases that might be undefined terms."""
    # Pattern for capitalized phrases that look like proper nouns
    # e.g., "Bureau of Something", "The Something", "ya-Something"
    patterns = [
        r'\b(Bureau of (?:the )?[A-Z][a-z]+)\b',
        r'\b(Institute of (?:the )?[A-Z][a-z]+)\b', 
        r'\b(ya-[A-Z][a-z]+)\b',
        r'\b(es-[A-Z][a-z]+)\b',
        r'\b([A-Z][a-z]+ (?:Caste|Quarter|District|Parish|Guild|House|Household))\b',
        r'\b((?:First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth) [A-Z][a-z]+)\b',
    ]
    
    found_lower = {t.lower() for t in found.keys()}
    all_terms_lower = {t.lower() for t in ENTRIES.keys()}
    
    potential = set()
    for pattern in patterns:
        for m in re.finditer(pattern, text):
            term = m.group(1)
            if term.lower() not in all_terms_lower:
                potential.add(term)
    
    return sorted(potential)


def format_scan_report(result: Dict[str, Any], verbose: bool = False) -> str:
    """Format scan results as a readable report.
    
    Always shows full definitions for locations (to catch geographic errors).
    In verbose mode, shows definitions for all categories.
    """
    lines = []
    lines.append("=" * 70)
    lines.append("  GLOSSARY TERM SCAN REPORT")
    lines.append("=" * 70)
    
    # Stats summary
    stats = result["stats"]
    lines.append(f"\n  SUMMARY")
    lines.append(f"  {'─' * 40}")
    lines.append(f"  Total term occurrences: {stats['total_terms']}")
    lines.append(f"  Unique terms found: {stats['unique_terms']}")
    lines.append("")
    
    # By category
    lines.append(f"  BY CATEGORY")
    lines.append(f"  {'─' * 40}")
    for cat, count in sorted(stats["by_category"].items()):
        lines.append(f"  {cat:20} {count:4} terms")
    lines.append("")
    
    # LOCATIONS - always show full definitions (critical for geographic accuracy)
    if "location" in result["by_category"]:
        terms = result["by_category"]["location"]
        lines.append(f"\n  LOCATIONS ({len(terms)}) — full definitions for geographic accuracy")
        lines.append(f"  {'─' * 60}")
        for term in terms:
            data = result["found"][term]
            entry = data["entry"]
            count = data["count"]
            lines.append(f"\n  • {term} ({count}x)")
            lines.append(f"    {entry.short}")
            # Show real-world anchor if available
            if entry.location_features and entry.location_features.real_world_anchor:
                lines.append(f"    📍 Real world: {entry.location_features.real_world_anchor}")
            # Show borders if available (critical for travel/route planning)
            if entry.location_features and entry.location_features.borders:
                borders = entry.location_features.borders
                border_str = ", ".join(f"{d}: {', '.join(locs)}" for d, locs in borders.items())
                lines.append(f"    🧭 Borders: {border_str}")
    
    # Other categories - compact or verbose
    for cat in ["caste", "organization", "concept"]:
        if cat not in result["by_category"]:
            continue
        terms = result["by_category"][cat]
        
        if verbose:
            lines.append(f"\n  {cat.upper()} ({len(terms)})")
            lines.append(f"  {'─' * 40}")
            for term in terms:
                data = result["found"][term]
                entry = data["entry"]
                count = data["count"]
                lines.append(f"  • {term} ({count}x): {entry.short[:70]}...")
        else:
            # Compact listing for non-location categories
            lines.append(f"\n  {cat.upper()}: {', '.join(terms[:10])}")
            if len(terms) > 10:
                lines.append(f"      ... and {len(terms) - 10} more")
    
    # Potential issues
    if result["potential_issues"]:
        lines.append(f"\n  ⚠️  POTENTIAL UNDEFINED TERMS")
        lines.append(f"  {'─' * 40}")
        lines.append("  These look like setting terms but aren't in the glossary:")
        for term in result["potential_issues"][:15]:
            lines.append(f"  • {term}")
        if len(result["potential_issues"]) > 15:
            lines.append(f"  ... and {len(result['potential_issues']) - 15} more")
    
    lines.append("")
    lines.append("=" * 70)
    return "\n".join(lines)


def scan_file(filepath: str) -> Dict[str, Any]:
    """Scan a file for glossary terms."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return scan_document(text)


# =============================================================================
# LOCATION-SPECIFIC QUERIES
# =============================================================================

def location_lookup(name: str) -> Optional[GlossaryEntry]:
    """Look up location by name or alias."""
    entry = lookup(name)
    if entry and entry.category == "location":
        return entry
    
    name_lower = name.lower()
    for entry in ENTRIES.values():
        if entry.category != "location":
            continue
        if not entry.location_features:
            continue
        for alias in entry.location_features.aliases:
            if alias.lower() == name_lower:
                return entry
    return None


def locations_by_level(level: str) -> List[GlossaryEntry]:
    """Get all locations at a given hierarchical level."""
    try:
        level_enum = str_to_enum(Level, level)
    except ValueError:
        return []
    
    return [e for e in ENTRIES.values()
            if e.location_features and e.location_features.level == level_enum]


def locations_by_type(loc_type: str) -> List[GlossaryEntry]:
    """Get all locations of a given type."""
    try:
        type_enum = str_to_enum(LocationType, loc_type)
    except ValueError:
        return []
    
    return [e for e in ENTRIES.values()
            if e.location_features and e.location_features.location_type == type_enum]


def locations_with_caste(caste: str) -> List[GlossaryEntry]:
    """Find locations where a caste is present."""
    caste_lower = caste.lower()
    results = []
    for entry in ENTRIES.values():
        if not entry.location_features:
            continue
        for c in entry.location_features.castes_present:
            if caste_lower in c.lower():
                results.append(entry)
                break
    return results


def adjacent_to(location_name: str) -> List[GlossaryEntry]:
    """Find all locations adjacent to the given location."""
    entry = location_lookup(location_name)
    if not entry or not entry.location_features:
        return []
    
    adjacent = set()
    for direction, locs in entry.location_features.borders.items():
        for loc in locs:
            adjacent.add(loc)
    
    results = []
    for loc_name in adjacent:
        loc_entry = location_lookup(loc_name)
        if loc_entry:
            results.append(loc_entry)
    return results


def neighbors(location_name: str, direction: str = None) -> Dict[str, List[str]]:
    """Get neighbors in a specific direction or all directions."""
    entry = location_lookup(location_name)
    if not entry or not entry.location_features:
        return {"error": f"Location '{location_name}' not found"}
    
    borders = entry.location_features.borders
    if direction:
        return {direction: borders.get(direction, [])}
    return dict(borders)


def location_tree(name: str, depth: int = 2) -> Dict[str, Any]:
    """Get location hierarchy tree."""
    entry = location_lookup(name)
    if not entry:
        return {"error": f"Location '{name}' not found"}
    
    lf = entry.location_features
    result = {
        "name": entry.term,
        "level": lf.level.value if lf else None,
        "type": lf.location_type.value if lf else None,
        "population": lf.population if lf else None,
        "borders": dict(lf.borders) if lf else {},
        "children": []
    }
    
    if depth > 0 and lf and lf.children:
        for child_name in lf.children:
            child_entry = location_lookup(child_name)
            if child_entry:
                child_lf = child_entry.location_features
                result["children"].append({
                    "name": child_entry.term,
                    "level": child_lf.level.value if child_lf else None,
                    "type": child_lf.location_type.value if child_lf else None
                })
    
    return result


def persons_at_location(location_name: str) -> List[GlossaryEntry]:
    """Find all persons directly at a location (exact match)."""
    location_lower = location_name.lower()
    results = []
    for entry in ENTRIES.values():
        if entry.category == "person" and entry.person_location:
            if entry.person_location.lower() == location_lower:
                results.append(entry)
    return results


def _get_all_children(location_name: str, visited: set = None) -> List[str]:
    """Recursively get all children locations."""
    if visited is None:
        visited = set()
    
    if location_name.lower() in visited:
        return []
    visited.add(location_name.lower())
    
    entry = location_lookup(location_name)
    if not entry or not entry.location_features:
        return []
    
    children = []
    for child_name in entry.location_features.children:
        children.append(child_name)
        children.extend(_get_all_children(child_name, visited))
    
    return children


def persons_in_location_tree(location_name: str) -> Dict[str, List[GlossaryEntry]]:
    """Find all persons at a location and all its children.
    
    Returns dict mapping location names to lists of persons there.
    """
    results = {}
    
    # First, get persons at the main location
    direct = persons_at_location(location_name)
    if direct:
        results[location_name] = direct
    
    # Then get all children and their persons
    children = _get_all_children(location_name)
    for child_name in children:
        child_persons = persons_at_location(child_name)
        if child_persons:
            results[child_name] = child_persons
    
    return results


# =============================================================================
# LOCATION GRAPH PATH FINDING
# =============================================================================

def build_location_graph() -> Dict[str, Set[str]]:
    """Build adjacency graph from location relationships.
    
    Edges are created from:
    - Parent-child relationships (bidirectional)
    - Border relationships (extract all location names)
    
    Returns dict mapping location names to sets of connected locations.
    """
    graph: Dict[str, Set[str]] = {}
    glossary = load_glossary()
    
    # Get all locations
    locations = {name: entry for name, entry in glossary.items() 
                 if entry.category == 'location'}
    
    # Create case-insensitive lookup
    name_map = {name.lower(): name for name in locations.keys()}
    
    def resolve_name(ref: str) -> Optional[str]:
        """Resolve a reference to an actual location name (case-insensitive)."""
        if not ref:
            return None
        return name_map.get(ref.lower())
    
    # Initialize all nodes
    for name in locations:
        graph[name] = set()
    
    for name, entry in locations.items():
        lf = entry.location_features
        if not lf:
            continue
        
        # Parent-child edges (bidirectional)
        parent_key = resolve_name(lf.parent)
        if parent_key:
            graph[name].add(parent_key)
            graph[parent_key].add(name)
        
        for child in lf.children:
            child_key = resolve_name(child)
            if child_key:
                graph[name].add(child_key)
                graph[child_key].add(name)
        
        # Border edges (extract location names from all directions)
        for direction, border_locs in lf.borders.items():
            if isinstance(border_locs, list):
                for loc in border_locs:
                    loc_key = resolve_name(loc)
                    if loc_key:
                        graph[name].add(loc_key)
                        graph[loc_key].add(name)
            elif isinstance(border_locs, str):
                loc_key = resolve_name(border_locs)
                if loc_key:
                    graph[name].add(loc_key)
                    graph[loc_key].add(name)
    
    return graph


def find_path(start: str, end: str, graph: Dict[str, Set[str]] = None) -> Optional[List[str]]:
    """Find shortest path between two locations using BFS.
    
    Args:
        start: Starting location name
        end: Destination location name
        graph: Optional pre-built graph (builds one if not provided)
    
    Returns:
        List of location names forming the path, or None if no path exists.
    """
    if graph is None:
        graph = build_location_graph()
    
    # Normalize names (case-insensitive matching)
    name_map = {n.lower(): n for n in graph.keys()}
    start_key = name_map.get(start.lower())
    end_key = name_map.get(end.lower())
    
    if not start_key:
        return None  # Start not found
    if not end_key:
        return None  # End not found
    if start_key == end_key:
        return [start_key]
    
    # BFS
    from collections import deque
    queue = deque([(start_key, [start_key])])
    visited = {start_key}
    
    while queue:
        current, path = queue.popleft()
        
        for neighbor in graph.get(current, set()):
            if neighbor == end_key:
                return path + [neighbor]
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None  # No path found


def format_path(path: List[str], verbose: bool = False) -> str:
    """Format a path for display.
    
    Args:
        path: List of location names
        verbose: If True, show relationship type between nodes
    """
    if not path:
        return "No path found."
    
    if len(path) == 1:
        return f"Already at {path[0]}."
    
    lines = [f"\n{'─' * 50}"]
    lines.append(f"  PATH: {path[0]} → {path[-1]}")
    lines.append(f"  Steps: {len(path) - 1}")
    lines.append(f"{'─' * 50}\n")
    
    glossary = load_glossary() if verbose else {}
    
    for i, loc in enumerate(path):
        if i == 0:
            prefix = "START"
        elif i == len(path) - 1:
            prefix = "  END"
        else:
            prefix = f"   {i:2d}"
        
        lines.append(f"  {prefix} → {loc}")
        
        if verbose and i < len(path) - 1:
            # Determine relationship to next location
            next_loc = path[i + 1]
            entry = glossary.get(loc)
            
            rel = "connected"
            if entry and entry.location_features:
                lf = entry.location_features
                # Case-insensitive comparisons
                if lf.parent and lf.parent.lower() == next_loc.lower():
                    rel = "↑ parent"
                elif any(c.lower() == next_loc.lower() for c in lf.children):
                    rel = "↓ child"
                else:
                    # Check borders
                    for direction, locs in lf.borders.items():
                        if isinstance(locs, list):
                            if any(l.lower() == next_loc.lower() for l in locs):
                                rel = f"→ {direction}"
                                break
                        elif isinstance(locs, str) and locs.lower() == next_loc.lower():
                            rel = f"→ {direction}"
                            break
                            break
            
            lines.append(f"         ({rel})")
    
    lines.append(f"\n{'─' * 50}")
    return "\n".join(lines)


def graph_stats() -> Dict[str, any]:
    """Get statistics about the location graph."""
    graph = build_location_graph()
    
    # Count nodes and edges
    nodes = len(graph)
    edges = sum(len(neighbors) for neighbors in graph.values()) // 2
    
    # Find isolated nodes (no connections)
    isolated = [name for name, neighbors in graph.items() if len(neighbors) == 0]
    
    # Find most connected nodes
    by_connections = sorted(graph.items(), key=lambda x: len(x[1]), reverse=True)
    hubs = [(name, len(neighbors)) for name, neighbors in by_connections[:10]]
    
    # Find graph components using BFS
    visited = set()
    components = []
    
    for start in graph:
        if start in visited:
            continue
        
        # BFS to find component
        component = set()
        queue = [start]
        while queue:
            node = queue.pop()
            if node in visited:
                continue
            visited.add(node)
            component.add(node)
            queue.extend(graph[node] - visited)
        
        components.append(component)
    
    return {
        "nodes": nodes,
        "edges": edges,
        "isolated": isolated,
        "hubs": hubs,
        "components": len(components),
        "largest_component": max(len(c) for c in components) if components else 0,
    }


# =============================================================================
# UNIFIED TREE (LOCATIONS AND ORGANIZATIONS)
# =============================================================================

# Cache for raw YAML data (parent field access)
_RAW_DATA_CACHE: Dict[str, dict] = {}


def _get_raw_data() -> Dict[str, dict]:
    """Load and cache raw YAML data for parent field access."""
    global _RAW_DATA_CACHE
    if not _RAW_DATA_CACHE:
        yaml_path = Path(__file__).parent / "glossary_data.yaml"
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                import yaml
                data = yaml.safe_load(f)
                _RAW_DATA_CACHE = {k.lower(): v for k, v in data.get('entries', {}).items()}
        except:
            pass
    return _RAW_DATA_CACHE


def get_children(name: str) -> List[GlossaryEntry]:
    """Get all entries that have this entry as their parent.

    Works for both locations (via location_features.parent) and
    organizations (via top-level parent field).
    """
    name_lower = name.lower()
    children = []
    raw_data = _get_raw_data()

    for entry in ENTRIES.values():
        # Check location_features.parent
        if entry.location_features and entry.location_features.parent:
            if entry.location_features.parent.lower() == name_lower:
                children.append(entry)
                continue

        # Check top-level parent field (for organizations)
        raw_entry = raw_data.get(entry.term.lower(), {})
        if raw_entry.get('parent', '').lower() == name_lower:
            children.append(entry)

    return sorted(children, key=lambda e: e.term)


def get_parent(name: str) -> Optional[GlossaryEntry]:
    """Get the parent of an entry (location or organization)."""
    entry = lookup(name)
    if not entry:
        return None

    # Check location_features.parent
    if entry.location_features and entry.location_features.parent:
        return lookup(entry.location_features.parent)

    # Check top-level parent field using cached data
    raw_data = _get_raw_data()
    raw_entry = raw_data.get(entry.term.lower(), {})
    parent_name = raw_entry.get('parent', '')
    if parent_name:
        return lookup(parent_name)

    return None


def build_tree(name: str, depth: int = 3, _current_depth: int = 0) -> Dict[str, Any]:
    """Build a hierarchical tree from any entry (location or organization).

    Returns:
        {
            "name": str,
            "category": str,
            "short": str,
            "level": str (for locations),
            "children": [recursive tree nodes]
        }
    """
    entry = lookup(name)
    if not entry:
        return {"error": f"Entry '{name}' not found"}

    result = {
        "name": entry.term,
        "category": entry.category,
        "short": entry.short[:60] + "..." if len(entry.short) > 60 else entry.short,
        "children": []
    }

    # Add level for locations
    if entry.location_features:
        result["level"] = entry.location_features.level.value if entry.location_features.level else None
        result["type"] = entry.location_features.location_type.value if entry.location_features.location_type else None

    # Recursively add children
    if _current_depth < depth:
        children = get_children(entry.term)
        for child in children:
            child_tree = build_tree(child.term, depth, _current_depth + 1)
            if "error" not in child_tree:
                result["children"].append(child_tree)

    return result


def format_tree(tree: Dict[str, Any], indent: int = 0) -> str:
    """Format a tree dict as ASCII tree structure."""
    if "error" in tree:
        return tree["error"]

    lines = []
    prefix = "  " * indent

    # Format this node
    level_info = f" [{tree.get('level', tree.get('category', ''))}]" if tree.get('level') or tree.get('category') else ""
    lines.append(f"{prefix}{'└── ' if indent > 0 else ''}{tree['name']}{level_info}")

    # Format children
    for child in tree.get("children", []):
        lines.append(format_tree(child, indent + 1))

    return "\n".join(lines)


# =============================================================================
# REVERSE LOOKUP (WHO-REFERENCES)
# =============================================================================

def who_references(term: str) -> Dict[str, List[GlossaryEntry]]:
    """Find all entries that reference a given term.

    Searches:
    - related fields
    - location_features.parent, children, castes_present
    - top-level parent field

    Returns:
        {
            "in_related": [entries with term in their related field],
            "as_parent": [entries that have this as parent],
            "as_child": [entries that list this as child],
            "in_castes_present": [locations that list this caste],
            "in_details": [entries mentioning term in details text]
        }
    """
    term_lower = term.lower()
    results = {
        "in_related": [],
        "as_parent": [],
        "as_child": [],
        "in_castes_present": [],
        "in_details": []
    }

    # Use cached raw data for parent field access
    raw_data = _get_raw_data()

    for entry in ENTRIES.values():
        entry_term_lower = entry.term.lower()

        # Check related field
        for rel in entry.related:
            if rel.lower() == term_lower:
                results["in_related"].append(entry)
                break

        # Check location_features
        if entry.location_features:
            lf = entry.location_features

            # Parent
            if lf.parent and lf.parent.lower() == term_lower:
                results["as_parent"].append(entry)

            # Children
            for child in lf.children:
                if child.lower() == term_lower:
                    results["as_child"].append(entry)
                    break

            # Castes present
            for caste in lf.castes_present:
                if caste.lower() == term_lower:
                    results["in_castes_present"].append(entry)
                    break

        # Check top-level parent
        raw_entry = raw_data.get(entry.term, {})
        if raw_entry.get('parent', '').lower() == term_lower:
            if entry not in results["as_parent"]:
                results["as_parent"].append(entry)

        # Check details text
        if entry.details and term_lower in entry.details.lower():
            results["in_details"].append(entry)

    return results


# =============================================================================
# CONTEXT BUNDLE
# =============================================================================

def context_bundle(terms: List[str]) -> Dict[str, Any]:
    """Get definitions for multiple terms at once.

    Useful for scene setup where you need context on multiple entities.

    Returns:
        {
            "found": {term: GlossaryEntry},
            "not_found": [terms],
            "suggestions": {term: [similar terms]}
        }
    """
    found = {}
    not_found = []
    suggestions = {}

    for term in terms:
        entry = lookup(term.strip())
        if entry:
            found[entry.term] = entry
        else:
            not_found.append(term)
            result = check(term)
            if result["similar"]:
                suggestions[term] = result["similar"]

    return {
        "found": found,
        "not_found": not_found,
        "suggestions": suggestions
    }


def format_context_bundle(bundle: Dict[str, Any]) -> str:
    """Format a context bundle for display."""
    lines = []
    lines.append(f"\n{'=' * 60}")
    lines.append("  CONTEXT BUNDLE")
    lines.append(f"{'=' * 60}")

    if bundle["found"]:
        lines.append(f"\n  FOUND ({len(bundle['found'])} terms):")
        lines.append(f"  {'─' * 40}")
        for term, entry in bundle["found"].items():
            lines.append(f"\n  • {term} [{entry.category}]")
            lines.append(f"    {entry.short}")
            if entry.rag_pointer:
                lines.append(f"    📚 RAG: {entry.rag_pointer}")

    if bundle["not_found"]:
        lines.append(f"\n  NOT FOUND ({len(bundle['not_found'])} terms):")
        lines.append(f"  {'─' * 40}")
        for term in bundle["not_found"]:
            if term in bundle["suggestions"]:
                lines.append(f"  ✗ {term} → did you mean: {', '.join(bundle['suggestions'][term][:3])}")
            else:
                lines.append(f"  ✗ {term}")

    lines.append(f"\n{'=' * 60}")
    return "\n".join(lines)


# =============================================================================
# EXPAND (RECURSIVE RELATED TERMS)
# =============================================================================

def expand_term(term: str, depth: int = 2, _visited: Set[str] = None) -> Dict[str, Any]:
    """Recursively expand a term through its related terms.

    Returns:
        {
            "term": str,
            "entry": GlossaryEntry,
            "related": [recursive expand results]
        }
    """
    if _visited is None:
        _visited = set()

    entry = lookup(term)
    if not entry:
        return {"term": term, "error": "not found"}

    term_lower = entry.term.lower()
    if term_lower in _visited:
        return {"term": entry.term, "already_visited": True}

    _visited.add(term_lower)

    result = {
        "term": entry.term,
        "category": entry.category,
        "short": entry.short,
        "rag_pointer": entry.rag_pointer,
        "related": []
    }

    if depth > 0 and entry.related:
        for rel_term in entry.related:
            rel_result = expand_term(rel_term, depth - 1, _visited)
            result["related"].append(rel_result)

    return result


def format_expand(result: Dict[str, Any], indent: int = 0) -> str:
    """Format an expand result as indented tree."""
    lines = []
    prefix = "  " * indent

    if "error" in result:
        lines.append(f"{prefix}✗ {result['term']} (not found)")
        return "\n".join(lines)

    if result.get("already_visited"):
        lines.append(f"{prefix}↩ {result['term']} (see above)")
        return "\n".join(lines)

    cat_marker = f"[{result.get('category', '?')}]"
    lines.append(f"{prefix}• {result['term']} {cat_marker}")
    lines.append(f"{prefix}  {result.get('short', '')[:70]}...")

    for rel in result.get("related", []):
        lines.append(format_expand(rel, indent + 1))

    return "\n".join(lines)


# =============================================================================
# VALIDATE REFERENCES
# =============================================================================

def validate_refs(filepath: str) -> Dict[str, Any]:
    """Validate that glossary_terms in a document's front matter exist.

    Returns:
        {
            "file": str,
            "valid": [terms that exist],
            "invalid": [terms that don't exist],
            "suggestions": {term: [similar terms]}
        }
    """
    import re

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract front matter
    fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        return {"file": filepath, "error": "No front matter found"}

    import yaml
    try:
        front_matter = yaml.safe_load(fm_match.group(1))
    except yaml.YAMLError as e:
        return {"file": filepath, "error": f"Invalid YAML: {e}"}

    glossary_terms = front_matter.get('glossary_terms', [])
    if not glossary_terms:
        return {"file": filepath, "valid": [], "invalid": [], "suggestions": {}}

    valid = []
    invalid = []
    suggestions = {}

    for term in glossary_terms:
        entry = lookup(term)
        if entry:
            valid.append(entry.term)  # Use canonical name
        else:
            invalid.append(term)
            result = check(term)
            if result["similar"]:
                suggestions[term] = result["similar"]

    return {
        "file": filepath,
        "valid": valid,
        "invalid": invalid,
        "suggestions": suggestions
    }


def format_validate_refs(result: Dict[str, Any]) -> str:
    """Format validation results."""
    lines = []
    lines.append(f"\n{'=' * 60}")
    lines.append(f"  VALIDATING: {result['file']}")
    lines.append(f"{'=' * 60}")

    if "error" in result:
        lines.append(f"\n  ERROR: {result['error']}")
        return "\n".join(lines)

    if result["valid"]:
        lines.append(f"\n  ✓ VALID ({len(result['valid'])} terms):")
        for term in result["valid"]:
            lines.append(f"    • {term}")

    if result["invalid"]:
        lines.append(f"\n  ✗ INVALID ({len(result['invalid'])} terms):")
        for term in result["invalid"]:
            if term in result["suggestions"]:
                lines.append(f"    • {term} → try: {', '.join(result['suggestions'][term][:3])}")
            else:
                lines.append(f"    • {term}")

    if not result["invalid"]:
        lines.append(f"\n  ✓ All terms validated successfully!")

    lines.append(f"\n{'=' * 60}")
    return "\n".join(lines)


# =============================================================================
# VALIDATE ENTRY AGAINST SOURCE
# =============================================================================

def validate_entry(term: str) -> Dict[str, Any]:
    """Validate a glossary entry against its rag_pointer source documents.

    Searches the source document(s) for the term and related information,
    returning context to help verify accuracy.

    Returns:
        {
            "term": str,
            "entry": GlossaryEntry or None,
            "rag_pointer": str,
            "source_files": [paths found],
            "mentions": [{"file": str, "context": str}],
            "warnings": [str]
        }
    """
    import glob
    import re

    entry = lookup(term)
    if not entry:
        return {"term": term, "error": f"Entry '{term}' not found in glossary"}

    result = {
        "term": entry.term,
        "category": entry.category,
        "short": entry.short,
        "rag_pointer": entry.rag_pointer or "(none)",
        "source_files": [],
        "mentions": [],
        "warnings": []
    }

    # Find source files based on rag_pointer
    if entry.rag_pointer:
        pointers = [p.strip() for p in entry.rag_pointer.split(',')]
        for pointer in pointers:
            # Try to find matching files
            search_terms = pointer.replace(':', ' ').replace('-', ' ').split()
            # Look for .md files containing these terms
            for md_file in glob.glob("*.md"):
                file_lower = md_file.lower()
                matches = sum(1 for t in search_terms if t.lower() in file_lower)
                if matches >= len(search_terms) // 2:
                    result["source_files"].append(md_file)

    # Search for term mentions in source files
    if result["source_files"]:
        for source_file in result["source_files"]:
            try:
                with open(source_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if entry.term.lower() in line.lower():
                            # Get context (2 lines before and after)
                            start = max(0, i - 2)
                            end = min(len(lines), i + 3)
                            context = '\n'.join(lines[start:end])
                            result["mentions"].append({
                                "file": source_file,
                                "line": i + 1,
                                "context": context[:500]  # Truncate long contexts
                            })
                            if len(result["mentions"]) >= 5:
                                break
            except Exception as e:
                result["warnings"].append(f"Could not read {source_file}: {e}")

    # Check for potential issues
    if not result["source_files"]:
        result["warnings"].append(f"No source files found matching rag_pointer: {entry.rag_pointer}")

    if not result["mentions"] and result["source_files"]:
        result["warnings"].append(f"Term '{entry.term}' not found in source files")

    # Check related terms exist
    for rel in entry.related:
        if not lookup(rel):
            result["warnings"].append(f"Related term '{rel}' not found in glossary")

    return result


def format_validate_entry(result: Dict[str, Any]) -> str:
    """Format entry validation results."""
    lines = []
    lines.append(f"\n{'=' * 60}")
    lines.append(f"  VALIDATING ENTRY: {result.get('term', 'unknown')}")
    lines.append(f"{'=' * 60}")

    if "error" in result:
        lines.append(f"\n  ERROR: {result['error']}")
        return "\n".join(lines)

    lines.append(f"\n  Category: {result['category']}")
    lines.append(f"  Short: {result['short'][:60]}...")
    lines.append(f"  RAG Pointer: {result['rag_pointer']}")

    if result["source_files"]:
        lines.append(f"\n  SOURCE FILES FOUND ({len(result['source_files'])}):")
        for sf in result["source_files"]:
            lines.append(f"    • {sf}")

    if result["mentions"]:
        lines.append(f"\n  MENTIONS IN SOURCES ({len(result['mentions'])}):")
        for mention in result["mentions"][:3]:
            lines.append(f"\n    📄 {mention['file']}:{mention['line']}")
            for ctx_line in mention["context"].split('\n')[:3]:
                lines.append(f"       {ctx_line[:70]}")

    if result["warnings"]:
        lines.append(f"\n  ⚠️  WARNINGS ({len(result['warnings'])}):")
        for warn in result["warnings"]:
            lines.append(f"    • {warn}")
    else:
        lines.append(f"\n  ✓ No warnings")

    lines.append(f"\n{'=' * 60}")
    return "\n".join(lines)


# =============================================================================
# ENTRY INSERTION
# =============================================================================

def format_yaml_entry(name: str, data: Dict) -> str:
    """Format a glossary entry as YAML with markers."""
    import yaml
    
    lines = [f"  # ═══ {name} ═══"]
    lines.append(f"  {name}:")
    
    # Format each field with proper indentation
    for key, value in data.items():
        if isinstance(value, str):
            if '\n' in value or len(value) > 60:
                # Multi-line string
                lines.append(f"    {key}: |")
                for line in value.strip().split('\n'):
                    lines.append(f"      {line}")
            else:
                # Check if needs quoting
                if ':' in value or value.startswith('"') or value.startswith("'"):
                    lines.append(f'    {key}: "{value}"')
                else:
                    lines.append(f"    {key}: {value}")
        elif isinstance(value, list):
            if all(isinstance(x, str) and len(x) < 40 for x in value):
                # Inline list
                lines.append(f"    {key}: [{', '.join(value)}]")
            else:
                # Block list
                lines.append(f"    {key}:")
                for item in value:
                    lines.append(f"      - {item}")
        elif isinstance(value, dict):
            lines.append(f"    {key}:")
            for k, v in value.items():
                if isinstance(v, list):
                    lines.append(f"      {k}:")
                    for item in v:
                        lines.append(f"        - {item}")
                elif isinstance(v, dict):
                    lines.append(f"      {k}:")
                    for k2, v2 in v.items():
                        if isinstance(v2, list):
                            lines.append(f"        {k2}: [{', '.join(str(x) for x in v2)}]")
                        else:
                            lines.append(f"        {k2}: {v2}")
                else:
                    lines.append(f"      {k}: {v}")
        else:
            lines.append(f"    {key}: {value}")
    
    lines.append(f"  # ─── end {name} ───")
    return '\n'.join(lines)


def insert_entry(name: str, data: Dict, after: str = None) -> bool:
    """Insert a new entry into the glossary YAML file.
    
    Args:
        name: Name of the new entry
        data: Dict containing entry fields (category, short, details, etc.)
        after: Insert after this entry name. If None, appends before final entries.
    
    Returns:
        True if successful, False otherwise.
    """
    yaml_path = Path(__file__).parent / "glossary_data.yaml"
    
    with open(yaml_path, 'r') as f:
        content = f.read()
    
    # Check if entry already exists
    if f"  {name}:" in content:
        print(f"Entry '{name}' already exists")
        return False
    
    # Format the new entry
    new_entry = format_yaml_entry(name, data)
    
    if after:
        # Find the end marker of the 'after' entry
        marker = f"  # ─── end {after} ───"
        if marker not in content:
            # Try case-insensitive search
            for line in content.split('\n'):
                if '# ─── end' in line and after.lower() in line.lower():
                    marker = line.strip()
                    break
            else:
                print(f"Could not find entry '{after}'")
                return False
        
        # Insert after the marker
        content = content.replace(marker, f"{marker}\n\n{new_entry}")
    else:
        # Insert before a default marker (Armorers' Guild or end of entries)
        default_markers = [
            "  # ═══ Armorers' Guild ═══",
            "  # End of entries"
        ]
        inserted = False
        for marker in default_markers:
            if marker in content:
                content = content.replace(marker, f"{new_entry}\n\n{marker}")
                inserted = True
                break
        
        if not inserted:
            # Append before the final line
            lines = content.rstrip().split('\n')
            lines.insert(-1, '')
            lines.insert(-1, new_entry)
            content = '\n'.join(lines)
    
    # Validate YAML before writing
    try:
        import yaml
        yaml.safe_load(content)
    except yaml.YAMLError as e:
        print(f"YAML validation failed: {e}")
        return False
    
    with open(yaml_path, 'w') as f:
        f.write(content)
    
    # Reload glossary
    global ENTRIES
    ENTRIES = {}
    load_glossary()
    
    print(f"Inserted '{name}' successfully")
    return True


def bulk_insert(entries: List[Dict], after: str = None) -> int:
    """Insert multiple entries at once.
    
    Args:
        entries: List of dicts, each with 'name' key and entry data
        after: Insert after this entry name
    
    Returns:
        Number of entries successfully inserted.
    """
    count = 0
    current_after = after
    
    for entry_data in entries:
        name = entry_data.pop('name')
        if insert_entry(name, entry_data, after=current_after):
            current_after = name  # Chain insertions
            count += 1
    
    return count


def update_entry(name: str, updates: Dict) -> bool:
    """Update fields of an existing entry using surgical text replacement.
    
    Args:
        name: Name of entry to update
        updates: Dict of fields to update (supports nested keys like 'location_features.parent')
    
    Returns:
        True if successful, False otherwise.
    """
    import yaml
    import re
    
    yaml_path = Path(__file__).parent / "glossary_data.yaml"
    
    with open(yaml_path, 'r') as f:
        content = f.read()
    
    # Find the entry boundaries using markers
    start_marker = f"  # ═══ {name} ═══"
    end_marker = f"  # ─── end {name} ───"
    
    # Case-insensitive search for markers
    start_idx = -1
    end_idx = -1
    actual_name = name
    
    for line_idx, line in enumerate(content.split('\n')):
        if '# ═══' in line and name.lower() in line.lower():
            # Extract actual name from marker
            match = re.search(r'# ═══ (.+) ═══', line)
            if match:
                actual_name = match.group(1)
                start_marker = f"  # ═══ {actual_name} ═══"
                end_marker = f"  # ─── end {actual_name} ───"
                start_idx = content.find(start_marker)
                break
    
    if start_idx == -1:
        # Try finding entry without markers
        entry_line = f"  {name}:"
        for line in content.split('\n'):
            if line.strip().startswith(name + ':') or line.strip().startswith(f'"{name}":'):
                entry_line = line
                start_idx = content.find(line)
                break
        
        if start_idx == -1:
            print(f"Entry '{name}' not found")
            return False
    
    end_idx = content.find(end_marker)
    if end_idx == -1:
        print(f"Could not find end marker for '{actual_name}'")
        return False
    
    end_idx += len(end_marker)
    
    # Extract current entry text
    entry_text = content[start_idx:end_idx]
    
    # Parse the entry (just the YAML part, not markers)
    yaml_start = entry_text.find(f"  {actual_name}:")
    if yaml_start == -1:
        print(f"Could not find YAML for '{actual_name}'")
        return False
    
    yaml_end = entry_text.find(f"  # ─── end")
    entry_yaml = entry_text[yaml_start:yaml_end]
    
    # Parse to dict
    try:
        parsed = yaml.safe_load(entry_yaml)
        entry_data = parsed[actual_name]
    except Exception as e:
        print(f"Failed to parse entry: {e}")
        return False
    
    # Apply updates (supports dot notation for nested keys)
    for key, value in updates.items():
        if '.' in key:
            parts = key.split('.')
            target = entry_data
            for part in parts[:-1]:
                if part not in target:
                    target[part] = {}
                target = target[part]
            target[parts[-1]] = value
        else:
            entry_data[key] = value
    
    # Format new entry
    new_entry = format_yaml_entry(actual_name, entry_data)
    
    # Replace in content
    new_content = content[:start_idx] + new_entry + content[end_idx:]
    
    # Validate
    try:
        yaml.safe_load(new_content)
    except yaml.YAMLError as e:
        print(f"YAML validation failed: {e}")
        return False
    
    with open(yaml_path, 'w') as f:
        f.write(new_content)
    
    # Reload glossary
    global ENTRIES
    ENTRIES = {}
    load_glossary()
    
    print(f"Updated '{actual_name}'")
    return True


def set_parent(name: str, parent: str) -> bool:
    """Shortcut to set location_features.parent for an entry."""
    return update_entry(name, {'location_features.parent': parent})


# =============================================================================
# FORMATTING
# =============================================================================

def format_entry(entry: GlossaryEntry, verbose: bool = False) -> str:
    """Format an entry for display. If verbose=True, include aesthetic features."""
    lines = [f"\n{'=' * 60}"]
    lines.append(f"  {entry.term.upper()}  [{entry.category}]")
    lines.append(f"{'=' * 60}")
    lines.append(f"\n{entry.short}")
    
    if entry.details:
        lines.append(f"\n{entry.details}")
    
    if entry.rag_pointer:
        lines.append(f"\n  RAG: {entry.rag_pointer}")
    
    if entry.related:
        lines.append(f"\nðÃ…¸"— Related: {', '.join(entry.related)}")
    
    if entry.caste_features:
        cf = entry.caste_features
        lines.append(f"\n--- Caste Features ---")
        lines.append(f"  Morphology: {cf.morphology.value}")
        lines.append(f"  Scale: {cf.scale.value}")
        lines.append(f"  Compulsion: {cf.compulsion.value}")
        lines.append(f"  Lifespan: {cf.lifespan.value}")
        lines.append(f"  Cognition: {cf.cognition.value}")
        lines.append(f"  Population: {cf.population.value}")
        
        if cf.original_function:
            lines.append(f"  Original function: {cf.original_function}")
        if cf.current_role:
            lines.append(f"  Current role: {cf.current_role}")
        if cf.lifespan_note:
            lines.append(f"  Lifespan note: {cf.lifespan_note}")
        if cf.physical_traits:
            lines.append(f"  Physical traits:")
            for trait in cf.physical_traits:
                lines.append(f"    • {trait}")
        if cf.special:
            lines.append(f"  Special:")
            for s in cf.special:
                lines.append(f"    • {s}")
    
    if entry.location_features:
        lf = entry.location_features
        lines.append(f"\n--- Location Features ---")
        if lf.real_world_anchor:
            lines.append(f"    Real World: {lf.real_world_anchor}")
        if lf.level:
            lines.append(f"  Level: {lf.level.value}")
        if lf.location_type:
            lines.append(f"  Type: {lf.location_type.value}")
        if lf.parent:
            lines.append(f"  Parent: {lf.parent}")
        if lf.population:
            lines.append(f"  Population: {lf.population}")
        if lf.controlling_entity:
            lines.append(f"  Controller: {lf.controlling_entity}")
        if lf.primary_function:
            lines.append(f"  Function: {lf.primary_function}")
        if lf.temporal_effects:
            lines.append(f"  Temporal: {lf.temporal_effects}")
        if lf.children:
            lines.append(f"  Children: {', '.join(lf.children[:5])}")
            if len(lf.children) > 5:
                lines.append(f"    ... and {len(lf.children) - 5} more")
        if lf.borders:
            lines.append(f"  Borders:")
            for d, locs in lf.borders.items():
                lines.append(f"    {d}: {', '.join(locs)}")
        if lf.transit:
            lines.append(f"  Transit:")
            for t in lf.transit:
                route = t.get('route', '?')
                to = t.get('to', '?')
                ttype = t.get('type', '')
                notes = t.get('notes', '')
                line = f"    • {route} → {to}"
                if ttype:
                    line += f" [{ttype}]"
                lines.append(line)
                if notes and verbose:
                    lines.append(f"      {notes}")
    
    # Local aesthetic (simple instantiation note - always show for locations)
    if entry.local_aesthetic:
        lines.append(f"\n--- Local Aesthetic ---")
        lines.append(f"  {entry.local_aesthetic}")
    
    # Aesthetic features (verbose mode)
    if verbose and entry.aesthetic_features:
        af = entry.aesthetic_features
        lines.append(f"\n--- Aesthetic Features ---")
        if af.intention:
            lines.append(f"  Intention: \"{af.intention}\"")
        if af.environment:
            lines.append(f"  Environment: {af.environment}")
        if af.construction:
            lines.append(f"  Construction: {af.construction}")
        if af.visual_vocabulary:
            lines.append(f"  Visual References:")
            for v in af.visual_vocabulary:
                lines.append(f"    - {v}")
        if af.materials:
            lines.append(f"  Materials:")
            for m in af.materials:
                lines.append(f"    - {m}")
        if af.colors:
            lines.append(f"  Colors:")
            for c in af.colors:
                lines.append(f"    - {c}")
        if af.sensory:
            lines.append(f"  Sensory:")
            for s in af.sensory:
                lines.append(f"    - {s}")
        if af.key_elements:
            lines.append(f"  Key Elements:")
            for k in af.key_elements:
                lines.append(f"    - {k}")
    
    # NPCs in this location tree (verbose mode for locations)
    if verbose and entry.category == "location":
        persons_tree = persons_in_location_tree(entry.term)
        if persons_tree:
            lines.append(f"\n--- Notable Persons ---")
            for loc_name, persons in persons_tree.items():
                if loc_name.lower() == entry.term.lower():
                    # Direct persons at this location
                    for p in persons:
                        lines.append(f"  • {p.term}: {p.short[:60]}...")
                else:
                    # Persons in child locations
                    lines.append(f"  [{loc_name}]")
                    for p in persons:
                        lines.append(f"    • {p.term}: {p.short[:55]}...")
    
    lines.append(f"{'=' * 60}\n")
    return "\n".join(lines)


# =============================================================================
# CLI
# =============================================================================

def print_help():
    print("""
Post-Interdict Empire Glossary

Data file: glossary_data.yaml
Schema: GLOSSARY_SCHEMA.md

Commands:
    lookup <term> [-v]         - Look up a specific term (-v for aesthetics)
    search <query>             - Search all entries for query string
    category <category>        - List all entries in category
    check <term>               - Check if term exists, suggest similar
    related <term>             - Get term and its related entries
    aesthetics                 - List all entries with aesthetic data

    caste-feature <feat> <val> - Find castes by feature value
    caste-trait <trait>        - Find castes with trait in description
    caste-compare <c1> <c2>    - Compare two castes side by side

    tree <name> [depth]        - Show hierarchy tree (locations OR organizations)
    location-tree <name>       - Show location hierarchy (legacy)
    scene-setup <location> [-v]- Get scene setup info (-v for aesthetics)
    locations-by-level <lvl>   - List all locations at level
    locations-by-type <type>   - List all locations of type
    locations-with-caste <c>   - Find locations where caste present
    adjacent-to <location>     - Find adjacent locations
    neighbors <loc> [dir]      - Get neighbors in direction

    path <start> <end> [-v]    - Find shortest path between locations
    graph-stats                - Show location graph statistics
    graph-neighbors <loc>      - Show all graph connections for location

    who-references <term>      - Find all entries that reference a term
    context-bundle <t1,t2,...> - Get definitions for multiple terms
    expand <term> [depth]      - Recursively expand related terms
    validate-refs <filepath>   - Check glossary_terms in front matter
    validate-entry <term>      - Check entry against its rag_pointer sources

    insert <n> [--after <e>]   - Insert new entry (reads YAML from stdin)
    update <n> --set k=v       - Update entry field (or pipe YAML)
    set-parent <n> <parent>    - Shortcut to set location parent
    scan <filepath> [-v]       - Scan file for glossary terms

Examples:
    python glossary.py lookup Highborn
    python glossary.py tree "Bureau of the Lens"
    python glossary.py who-references "Highborn"
    python glossary.py validate-entry "Autofactory"
    python glossary.py expand "Lampblack Yards" 2
    python glossary.py validate-refs Religion_-_Oracle_Cult.md
""")


def main():
    if len(sys.argv) < 2:
        print_help()
        return
    
    cmd = sys.argv[1].lower()
    
    if cmd in ["help", "--help", "-h"]:
        print_help()
        return
    
    if cmd == "location-tree" and len(sys.argv) >= 3:
        name = " ".join(sys.argv[2:])
        result = location_tree(name)
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"\n{'=' * 60}")
            print(f"  LOCATION TREE: {result['name'].upper()}")
            print(f"{'=' * 60}")
            print(f"\n  Level: {result['level']}")
            print(f"  Type: {result['type']}")
            if result['population']:
                print(f"  Population: {result['population']}")
            if result['borders']:
                print(f"\n  Borders:")
                for direction, locs in result['borders'].items():
                    print(f"    {direction}: {', '.join(locs)}")
            if result['children']:
                print(f"\n  Contains ({len(result['children'])} locations):")
                for child in result['children']:
                    print(f"    • {child['name']} [{child['level']}/{child['type']}]")
            print(f"{'=' * 60}")
        return
    
    if cmd == "locations-by-level" and len(sys.argv) >= 3:
        level = sys.argv[2]
        results = locations_by_level(level)
        if results:
            print(f"\n{level.upper()} locations ({len(results)}):\n")
            for entry in results:
                print(f"  • {entry.term}: {entry.short[:50]}...")
        else:
            print(f"No locations at level '{level}'")
        return
    
    if cmd == "locations-by-type" and len(sys.argv) >= 3:
        loc_type = sys.argv[2]
        results = locations_by_type(loc_type)
        if results:
            print(f"\n{loc_type.upper()} locations ({len(results)}):\n")
            for entry in results:
                print(f"  • {entry.term}: {entry.short[:50]}...")
        else:
            print(f"No locations of type '{loc_type}'")
        return
    
    if cmd == "locations-with-caste" and len(sys.argv) >= 3:
        caste = " ".join(sys.argv[2:])
        results = locations_with_caste(caste)
        if results:
            print(f"\nLocations with {caste} present ({len(results)}):\n")
            for entry in results:
                print(f"  • {entry.term}")
        else:
            print(f"No locations found with '{caste}'")
        return
    
    if cmd == "adjacent-to" and len(sys.argv) >= 3:
        name = " ".join(sys.argv[2:])
        results = adjacent_to(name)
        if results:
            print(f"\nLocations adjacent to '{name}' ({len(results)}):\n")
            for entry in results:
                lf = entry.location_features
                ltype = lf.location_type.value if lf else "?"
                print(f"  • {entry.term} [{ltype}]")
        else:
            entry = location_lookup(name)
            if entry:
                print(f"No border information for '{name}'")
            else:
                print(f"Location '{name}' not found")
        return
    
    if cmd == "neighbors" and len(sys.argv) >= 3:
        name = sys.argv[2]
        direction = sys.argv[3] if len(sys.argv) >= 4 else None
        result = neighbors(name, direction)
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"\nNeighbors of '{name}':\n")
            for dir_name, locs in result.items():
                print(f"  {dir_name}: {', '.join(locs)}")
        return
    
    if cmd == "scene-setup" and len(sys.argv) >= 3:
        name = " ".join(sys.argv[2:])
        entry = location_lookup(name)
        if not entry:
            print(f"Location '{name}' not found")
            return
        
        lf = entry.location_features
        print(f"\n{'=' * 60}")
        print(f"  SCENE SETUP: {entry.term.upper()}")
        print(f"{'=' * 60}")
        print(f"\n{entry.short}")
        if entry.details:
            print(f"\n{entry.details}")
        
        # Show real world anchor prominently
        if lf and lf.real_world_anchor:
            print(f"\n  ðÃ…¸Ã…' REAL WORLD: {lf.real_world_anchor}")
        
        rag_docs = []
        if entry.rag_pointer:
            for doc in entry.rag_pointer.split(','):
                doc = doc.strip()
                if doc and doc not in rag_docs:
                    rag_docs.append(doc)
        
        ancestors = []
        if lf and lf.parent:
            parent = location_lookup(lf.parent)
            while parent:
                ancestors.append(parent.term)
                if parent.rag_pointer:
                    for doc in parent.rag_pointer.split(','):
                        doc = doc.strip()
                        if doc and doc not in rag_docs:
                            rag_docs.append(doc)
                parent_lf = parent.location_features
                if parent_lf and parent_lf.parent:
                    parent = location_lookup(parent_lf.parent)
                else:
                    break
        
        if ancestors:
            print(f"\n  HIERARCHY: {' → '.join(reversed(ancestors))} → {entry.term}")
        
        if rag_docs:
            print(f"\n  📚 RAG DOCUMENTS TO PULL:")
            for i, doc in enumerate(rag_docs, 1):
                print(f"     {i}. project_knowledge_search(\"{doc}\")")
        
        if lf and lf.castes_present:
            print(f"\n  👥 CASTES PRESENT: {', '.join(lf.castes_present)}")
        
        if lf and lf.borders:
            print(f"\n  🚪 EXITS:")
            for direction, locations in lf.borders.items():
                print(f"     {direction}: {', '.join(locations)}")
        
        if lf and lf.children:
            print(f"\n  📍 SUB-LOCATIONS:")
            for child in lf.children:
                child_entry = location_lookup(child)
                if child_entry and child_entry.location_features:
                    ctype = child_entry.location_features.location_type.value
                    print(f"     • {child} [{ctype}]")
                else:
                    print(f"     • {child}")
        
        if lf:
            if lf.hazards:
                print(f"\n  ⚠️ HAZARDS: {', '.join(lf.hazards)}")
            if lf.temporal_effects:
                print(f"\n  ⏰ TEMPORAL: {lf.temporal_effects}")
        
        # Show local aesthetic if present
        if entry.local_aesthetic:
            print(f"\n  ðÃ…¸Ã…½Â¨ LOCAL AESTHETIC:")
            print(f"     {entry.local_aesthetic}")
        
        # Show this entry's own aesthetic_features if present
        if entry.aesthetic_features:
            af = entry.aesthetic_features
            print(f"\n  ðÃ…¸Ã…½Â¨ AESTHETIC VOCABULARY:")
            print(f"     Intention: \"{af.intention}\"")
            if af.visual_vocabulary:
                print(f"     Visual references: {', '.join([v.split(':')[0] for v in af.visual_vocabulary[:4]])}")
            if af.materials:
                print(f"     Materials: {', '.join([m.split('(')[0].strip() for m in af.materials[:3]])}")
            if af.colors:
                print(f"     Colors: {', '.join([c.split('(')[0].strip() for c in af.colors[:3]])}")
        # Otherwise show parent's aesthetic vocabulary
        elif lf and lf.parent:
            parent_entry = location_lookup(lf.parent)
            while parent_entry:
                if parent_entry.aesthetic_features:
                    af = parent_entry.aesthetic_features
                    print(f"\n  ðÃ…¸Ã…½Â¨ PARENT AESTHETIC ({parent_entry.term}):")
                    print(f"     Intention: \"{af.intention}\"")
                    if af.visual_vocabulary:
                        print(f"     Visual vocabulary: {', '.join([v.split(':')[0] for v in af.visual_vocabulary[:3]])}")
                    break
                parent_lf = parent_entry.location_features
                if parent_lf and parent_lf.parent:
                    parent_entry = location_lookup(parent_lf.parent)
                else:
                    break
        
        print(f"\n{'=' * 60}")
        return
    
    if cmd == "caste-feature" and len(sys.argv) >= 4:
        feature = sys.argv[2]
        value = sys.argv[3]
        results = caste_by_feature(feature, value)
        if results:
            print(f"\nCastes with {feature}={value} ({len(results)}):\n")
            for entry in results:
                print(f"  • {entry.term}: {entry.short[:50]}...")
        else:
            print(f"No castes found with {feature}={value}")
        return
    
    if cmd == "caste-trait" and len(sys.argv) >= 3:
        trait = " ".join(sys.argv[2:])
        results = caste_by_trait(trait)
        if results:
            print(f"\nCastes with trait '{trait}' ({len(results)}):\n")
            for entry in results:
                print(f"  • {entry.term}: {entry.short[:50]}...")
        else:
            print(f"No castes found with trait '{trait}'")
        return
    
    if cmd == "caste-compare" and len(sys.argv) >= 4:
        c1 = sys.argv[2]
        c2 = sys.argv[3]
        result = caste_compare(c1, c2)
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"\n{'=' * 60}")
            print(f"  COMPARING: {result['caste1']} vs {result['caste2']}")
            print(f"{'=' * 60}\n")
            for feat, (v1, v2) in result['comparison'].items():
                match = "âÃÆ'Æ'…""" if v1 == v2 else "≠"
                print(f"  {feat:15} {v1:15} {match} {v2}")
            print(f"\n  Original function:")
            print(f"    {result['caste1']}: {result['original_function'][0]}")
            print(f"    {result['caste2']}: {result['original_function'][1]}")
            print(f"\n  Current role:")
            print(f"    {result['caste1']}: {result['current_role'][0]}")
            print(f"    {result['caste2']}: {result['current_role'][1]}")
            print(f"{'=' * 60}")
        return
    
    # Random command - can work with or without argument
    if cmd == "random":
        cat = sys.argv[2] if len(sys.argv) >= 3 else None
        entry = random_entry(cat=cat)
        if entry:
            print(f"\n{'=' * 60}")
            print(f"  RANDOM: {entry.term}")
            print(f"{'=' * 60}")
            print(format_entry(entry))
        else:
            if cat:
                print(f"No entries found in category '{cat}'")
            else:
                print("No entries found")
        return
    
    # Aesthetics command - list all entries with aesthetic data
    if cmd == "aesthetics":
        entries_with_aesthetics = [e for e in ENTRIES.values() if e.aesthetic_features]
        if entries_with_aesthetics:
            print(f"\nEntries with aesthetic data ({len(entries_with_aesthetics)}):\n")
            for entry in sorted(entries_with_aesthetics, key=lambda e: e.term):
                af = entry.aesthetic_features
                intention = f' - "{af.intention}"' if af.intention else ""
                print(f"  {entry.term} [{entry.category}]{intention}")
        else:
            print("No entries with aesthetic data found")
        return
    
    # Graph stats command - no argument required
    if cmd == "graph-stats":
        stats = graph_stats()
        print(f"\n{'=' * 50}")
        print("  LOCATION GRAPH STATISTICS")
        print(f"{'=' * 50}\n")
        print(f"  Nodes (locations): {stats['nodes']}")
        print(f"  Edges (connections): {stats['edges']}")
        print(f"  Graph components: {stats['components']}")
        print(f"  Largest component: {stats['largest_component']} nodes")
        print(f"\n  Most connected locations:")
        for name, count in stats['hubs']:
            print(f"    {name}: {count} connections")
        if stats['isolated']:
            print(f"\n  Isolated locations ({len(stats['isolated'])}):")
            for name in stats['isolated'][:10]:
                print(f"    - {name}")
            if len(stats['isolated']) > 10:
                print(f"    ... and {len(stats['isolated']) - 10} more")
        print(f"\n{'=' * 50}")
        return

    # Tree command - unified hierarchy for locations AND organizations
    if cmd == "tree" and len(sys.argv) >= 3:
        # Parse depth if provided
        depth = 3
        name_parts = []
        for a in sys.argv[2:]:
            if a.isdigit():
                depth = int(a)
            elif not a.startswith("-"):
                name_parts.append(a)
        name = " ".join(name_parts)

        tree = build_tree(name, depth=depth)
        if "error" in tree:
            print(f"Error: {tree['error']}")
        else:
            print(f"\n{'=' * 60}")
            print(f"  HIERARCHY TREE: {tree['name'].upper()}")
            print(f"{'=' * 60}\n")
            print(format_tree(tree))
            print(f"\n{'=' * 60}")
        return

    # Who-references command
    if cmd == "who-references" and len(sys.argv) >= 3:
        term = " ".join(sys.argv[2:])
        results = who_references(term)

        total = sum(len(v) for v in results.values())
        print(f"\n{'=' * 60}")
        print(f"  WHO REFERENCES: {term}")
        print(f"  Total: {total} entries")
        print(f"{'=' * 60}")

        if results["as_parent"]:
            print(f"\n  Has '{term}' as PARENT ({len(results['as_parent'])}):")
            for entry in results["as_parent"]:
                print(f"    • {entry.term} [{entry.category}]")

        if results["as_child"]:
            print(f"\n  Lists '{term}' as CHILD ({len(results['as_child'])}):")
            for entry in results["as_child"]:
                print(f"    • {entry.term} [{entry.category}]")

        if results["in_related"]:
            print(f"\n  In RELATED field ({len(results['in_related'])}):")
            for entry in results["in_related"]:
                print(f"    • {entry.term} [{entry.category}]")

        if results["in_castes_present"]:
            print(f"\n  In CASTES_PRESENT ({len(results['in_castes_present'])}):")
            for entry in results["in_castes_present"]:
                print(f"    • {entry.term} [{entry.category}]")

        if results["in_details"]:
            print(f"\n  Mentioned in DETAILS ({len(results['in_details'])}):")
            for entry in results["in_details"][:10]:
                print(f"    • {entry.term} [{entry.category}]")
            if len(results["in_details"]) > 10:
                print(f"    ... and {len(results['in_details']) - 10} more")

        print(f"\n{'=' * 60}")
        return

    # Context-bundle command
    if cmd == "context-bundle" and len(sys.argv) >= 3:
        # Terms can be comma-separated or space-separated
        raw_terms = " ".join(sys.argv[2:])
        terms = [t.strip() for t in raw_terms.split(",")]

        bundle = context_bundle(terms)
        print(format_context_bundle(bundle))
        return

    # Expand command
    if cmd == "expand" and len(sys.argv) >= 3:
        # Parse depth if provided
        depth = 2
        name_parts = []
        for a in sys.argv[2:]:
            if a.isdigit():
                depth = int(a)
            elif not a.startswith("-"):
                name_parts.append(a)
        term = " ".join(name_parts)

        result = expand_term(term, depth=depth)
        print(f"\n{'=' * 60}")
        print(f"  EXPAND: {term} (depth={depth})")
        print(f"{'=' * 60}\n")
        print(format_expand(result))
        print(f"\n{'=' * 60}")
        return

    # Validate-refs command
    if cmd == "validate-refs" and len(sys.argv) >= 3:
        filepath = sys.argv[2]
        try:
            result = validate_refs(filepath)
            print(format_validate_refs(result))
        except FileNotFoundError:
            print(f"Error: File not found: {filepath}")
        except Exception as e:
            print(f"Error validating file: {e}")
        return

    # Validate-entry command - check entry against source documents
    if cmd == "validate-entry" and len(sys.argv) >= 3:
        term = " ".join(sys.argv[2:])
        result = validate_entry(term)
        print(format_validate_entry(result))
        return

    if len(sys.argv) < 3:
        print(f"Error: {cmd} requires an argument")
        return

    # Check for -v/--verbose flag
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    args = [a for a in sys.argv[2:] if not a.startswith("-")]
    arg = " ".join(args)
    
    if cmd == "lookup":
        entry = lookup(arg)
        if not entry:
            entry = location_lookup(arg)
        if entry:
            print(format_entry(entry, verbose=verbose))
        else:
            result = check(arg)
            print(f"Term '{arg}' not found.")
            if result["similar"]:
                print(f"Similar: {', '.join(result['similar'])}")
    
    elif cmd == "search":
        results = search(arg)
        if results:
            print(f"Found {len(results)} results for '{arg}':\n")
            for entry in results[:10]:
                print(f"  • {entry.term} [{entry.category}]: {entry.short[:50]}...")
        else:
            print(f"No results for '{arg}'")
    
    elif cmd == "category":
        results = category(arg)
        if results:
            print(f"\n{arg.upper()} ({len(results)} entries):\n")
            for entry in sorted(results, key=lambda e: e.term):
                print(f"  • {entry.term}: {entry.short[:50]}...")
        else:
            print(f"No entries in category '{arg}'")
    
    elif cmd == "check":
        result = check(arg)
        if result["exists"]:
            print(f"âÃÆ'Æ'…"" '{arg}' exists")
            print(format_entry(result["entry"]))
        else:
            print(f"✗ '{arg}' not found")
            if result["similar"]:
                print(f"  Did you mean: {', '.join(result['similar'])}")
    
    elif cmd == "related":
        results = related(arg)
        if results:
            print(f"'{arg}' and related terms:\n")
            for entry in results:
                print(format_entry(entry))
        else:
            print(f"Term '{arg}' not found")
    
    elif cmd == "scan":
        # Check for -v/--verbose flag
        verbose = "-v" in sys.argv or "--verbose" in sys.argv
        # Get filepath (skip flags)
        filepath = None
        for a in sys.argv[2:]:
            if not a.startswith("-"):
                filepath = a
                break
        
        if not filepath:
            print("Error: scan requires a filepath")
            print("Usage: glossary.py scan <filepath> [-v|--verbose]")
            return
        
        try:
            result = scan_file(filepath)
            print(format_scan_report(result, verbose=verbose))
        except FileNotFoundError:
            print(f"Error: File not found: {filepath}")
        except Exception as e:
            print(f"Error scanning file: {e}")
    
    elif cmd == "scan-text":
        # Read from stdin for piped content
        import sys as sys_mod
        if sys_mod.stdin.isatty():
            print("Error: scan-text reads from stdin")
            print("Usage: cat document.txt | glossary.py scan-text [-v]")
            return
        text = sys_mod.stdin.read()
        verbose = "-v" in sys.argv or "--verbose" in sys.argv
        result = scan_document(text)
        print(format_scan_report(result, verbose=verbose))
    
    elif cmd == "path":
        # Find path between two locations
        # Usage: glossary.py path "start" "end" [-v]
        if len(args) < 2:
            print("Error: path requires two location names")
            print("Usage: glossary.py path <start> <end> [-v|--verbose]")
            return
        
        start = args[0]
        end = args[1]
        
        path = find_path(start, end)
        if path:
            print(format_path(path, verbose=verbose))
        else:
            # Check if locations exist
            glossary = load_glossary()
            name_map = {n.lower(): n for n in glossary.keys()}
            start_exists = start.lower() in name_map
            end_exists = end.lower() in name_map
            
            if not start_exists:
                print(f"Location '{start}' not found.")
                similar = [n for n in glossary.keys() if start.lower() in n.lower()][:5]
                if similar:
                    print(f"  Similar: {', '.join(similar)}")
            elif not end_exists:
                print(f"Location '{end}' not found.")
                similar = [n for n in glossary.keys() if end.lower() in n.lower()][:5]
                if similar:
                    print(f"  Similar: {', '.join(similar)}")
            else:
                print(f"No path found between '{start}' and '{end}'.")
                print("  (These locations may be in disconnected graph components)")
    
    elif cmd == "graph-neighbors":
        # Show all graph connections for a location
        graph = build_location_graph()
        name_map = {n.lower(): n for n in graph.keys()}
        loc_key = name_map.get(arg.lower())
        
        if not loc_key:
            print(f"Location '{arg}' not found.")
            return
        
        neighbor_set = graph.get(loc_key, set())
        if neighbor_set:
            print(f"\n{loc_key} has {len(neighbor_set)} graph connections:\n")
            for n in sorted(neighbor_set):
                print(f"  • {n}")
        else:
            print(f"{loc_key} has no connections in the graph.")
    
    elif cmd == "insert":
        # Insert a new entry
        # Usage: glossary.py insert <name> [--after <entry>] < entry.yaml
        # Or: glossary.py insert <name> --category <cat> --short "description"
        import sys as sys_mod
        
        if len(args) < 1:
            print("Error: insert requires entry name")
            print("Usage: glossary.py insert <name> [--after <entry>] < entry.yaml")
            print("   or: glossary.py insert <name> --category <cat> --short \"desc\"")
            return
        
        name = args[0]
        after = None
        
        # Parse --after flag
        if "--after" in sys.argv:
            idx = sys.argv.index("--after")
            if idx + 1 < len(sys.argv):
                after = sys.argv[idx + 1]
        
        # Check if reading from stdin
        if not sys_mod.stdin.isatty():
            import yaml
            yaml_text = sys_mod.stdin.read()
            try:
                data = yaml.safe_load(yaml_text)
                if insert_entry(name, data, after=after):
                    print(f"Entry '{name}' inserted successfully")
            except yaml.YAMLError as e:
                print(f"Invalid YAML: {e}")
        else:
            # Build entry from command line args
            data = {}
            
            if "--category" in sys.argv:
                idx = sys.argv.index("--category")
                if idx + 1 < len(sys.argv):
                    data["category"] = sys.argv[idx + 1]
            
            if "--short" in sys.argv:
                idx = sys.argv.index("--short")
                if idx + 1 < len(sys.argv):
                    data["short"] = sys.argv[idx + 1]
            
            if "--parent" in sys.argv:
                idx = sys.argv.index("--parent")
                if idx + 1 < len(sys.argv):
                    data["location_features"] = {"parent": sys.argv[idx + 1]}
            
            if not data.get("category") or not data.get("short"):
                print("Error: --category and --short required when not reading from stdin")
                return
            
            if insert_entry(name, data, after=after):
                print(f"Entry '{name}' inserted successfully")
    
    elif cmd == "update":
        # Update an existing entry
        # Usage: glossary.py update <n> --set key=value [--set key2=value2]
        # Or: glossary.py update <n> < updates.yaml
        import sys as sys_mod
        
        if len(args) < 1:
            print("Error: update requires entry name")
            print("Usage: glossary.py update <n> --set key=value")
            print("   or: glossary.py update <n> < updates.yaml")
            return
        
        name = args[0]
        
        # Check if reading from stdin
        if not sys_mod.stdin.isatty():
            import yaml
            yaml_text = sys_mod.stdin.read()
            try:
                updates = yaml.safe_load(yaml_text)
                if update_entry(name, updates):
                    print(f"Entry '{name}' updated successfully")
            except yaml.YAMLError as e:
                print(f"Invalid YAML: {e}")
        else:
            # Parse --set flags
            updates = {}
            i = 0
            while i < len(sys.argv):
                if sys.argv[i] == "--set" and i + 1 < len(sys.argv):
                    kv = sys.argv[i + 1]
                    if '=' in kv:
                        k, v = kv.split('=', 1)
                        updates[k] = v
                    i += 2
                else:
                    i += 1
            
            if not updates:
                print("Error: --set key=value required when not reading from stdin")
                return
            
            if update_entry(name, updates):
                print(f"Entry '{name}' updated successfully")
    
    elif cmd == "set-parent":
        # Shortcut: glossary.py set-parent <entry> <parent>
        if len(args) < 2:
            print("Usage: glossary.py set-parent <entry> <parent>")
            return
        
        if set_parent(args[0], args[1]):
            print(f"Set parent of '{args[0]}' to '{args[1]}'")
    
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()

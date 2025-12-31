#!/usr/bin/env python3
"""
Glossary Entry Revision Stepper

Steps through glossary entries one by one for revision according to
the design principles. Prints a reminder every 10 entries.

USAGE
=====
    python3 glossary_stepper.py                    # Start from beginning
    python3 glossary_stepper.py --start 50         # Start from entry 50
    python3 glossary_stepper.py --category caste   # Only castes
    python3 glossary_stepper.py --needs-work       # Only entries with empty/short details

OUTPUT
======
    Prints entries one at a time. For each entry, shows:
    - Entry name and category
    - Current short description
    - Current details (if any)
    - Structured features (if any)

    After viewing, you revise externally and run again with --start N
    to continue from where you left off.
"""

import yaml
import sys
import argparse
from pathlib import Path

# =============================================================================
# THE EIGENVECTOR - Print every 10 entries
# =============================================================================

REMINDER = """
═══════════════════════════════════════════════════════════════════════════════
REVISION PRINCIPLES
═══════════════════════════════════════════════════════════════════════════════

WHAT TO EDIT: Only `short` and `details`. Leave subsections (material_culture,
caste_features, location_features, etc.) alone.

WHAT DETAILS SHOULD CONTAIN:
  • Physical reality — what do outsiders see? Bodies, spaces, artifacts.
  • Lived experience — what is it like to BE this? To live here? To do this work?
  • Social position — where do they fit? What is their life? Who do they deal with?

  Do NOT repeat content that belongs in subsections. If there's a material_culture
  section, don't summarize it in details—that's what the section is for.

THE POSITIONS (every entry conveys coherent internal perspective):
  • Inheritors caring for what they didn't build
  • Makers certain they were finalizing
  • Things continuing their function past their audience
  • People doing harm with their justification
  • People creating within inherited constraints

THE QUALITY:
  • Care persisting where understanding has failed
  • Endurance and transcendence amidst impenetrable mystery
  • Someone is doing their best here, and it matters

THE STYLE:
  • Patterns, not specific instances (instances get recycled as canonical examples)
  • Prose, not fragments
  • Don't be too literal about the design framework—no winking at the meta-level
  • Show the internal logic that makes apparent absurdity make sense
  • For governments: what it's like to work within the forms
  • For architecture: what it's like to move through the spaces
  • For technology: what it's like to depend on what you can't comprehend

THE QUESTION: "How do we live inside it?" — never "How do we fix it?"
═══════════════════════════════════════════════════════════════════════════════
"""

# =============================================================================
# LOADER
# =============================================================================

def load_glossary(path: str = "glossary_data.yaml") -> dict:
    """Load glossary data from YAML file."""
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data.get('entries', {})

# =============================================================================
# ENTRY DISPLAY
# =============================================================================

def display_entry(name: str, entry: dict, index: int, total: int):
    """Display a single entry for review."""
    print(f"\n{'─' * 79}")
    print(f"ENTRY {index + 1} of {total}: {name}")
    print(f"{'─' * 79}")

    category = entry.get('category', 'unknown')
    short = entry.get('short', '')
    details = entry.get('details', '')
    rag_pointer = entry.get('rag_pointer', '')
    related = entry.get('related', [])

    print(f"\nCATEGORY: {category}")
    print(f"\nSHORT:\n  {short}")

    if details:
        print(f"\nDETAILS:")
        for line in details.strip().split('\n'):
            print(f"  {line}")
    else:
        print(f"\nDETAILS: [EMPTY - needs work]")

    # Show category-specific features
    if 'caste_features' in entry:
        print(f"\nCASTE FEATURES:")
        cf = entry['caste_features']
        for key, value in cf.items():
            if isinstance(value, list):
                print(f"  {key}:")
                for item in value[:3]:  # Show first 3
                    print(f"    - {item}")
                if len(value) > 3:
                    print(f"    ... and {len(value) - 3} more")
            else:
                print(f"  {key}: {value}")

    if 'location_features' in entry:
        print(f"\nLOCATION FEATURES:")
        lf = entry['location_features']
        for key, value in lf.items():
            print(f"  {key}: {value}")

    if 'material_culture' in entry:
        print(f"\n[Has material_culture section - {len(entry['material_culture'])} fields]")

    if related:
        print(f"\nRELATED: {', '.join(related[:5])}", end='')
        if len(related) > 5:
            print(f" ... and {len(related) - 5} more")
        else:
            print()

    if rag_pointer:
        print(f"\nRAG POINTER: {rag_pointer}")

# =============================================================================
# ASSESSMENT
# =============================================================================

def needs_work(entry: dict) -> bool:
    """Check if an entry likely needs revision."""
    details = entry.get('details', '')
    if not details or len(details.strip()) < 50:
        return True
    # Check if details is just a category description rather than inhabited
    short = entry.get('short', '')
    if details.strip() == short.strip():
        return True
    return False

def get_work_assessment(entry: dict) -> str:
    """Return a brief assessment of what work the entry needs."""
    details = entry.get('details', '')
    short = entry.get('short', '')

    issues = []
    if not details:
        issues.append("NO DETAILS")
    elif len(details.strip()) < 50:
        issues.append("MINIMAL DETAILS")

    # Check for "is" patterns suggesting external description
    if short and short.strip().split()[0:2] == ['A', 'type']:
        issues.append("ENCYCLOPEDIC SHORT")

    if 'material_culture' in entry:
        issues.append("HAS MATERIAL_CULTURE (may have specific instances)")

    return " | ".join(issues) if issues else "OK"

# =============================================================================
# MAIN STEPPER
# =============================================================================

def step_through(entries: dict, start: int = 0, category: str = None,
                 needs_work_only: bool = False):
    """Step through entries one by one."""

    # Filter entries
    items = list(entries.items())

    if category:
        items = [(k, v) for k, v in items if v.get('category') == category]

    if needs_work_only:
        items = [(k, v) for k, v in items if needs_work(v)]

    total = len(items)

    if start >= total:
        print(f"Start index {start} exceeds total entries ({total})")
        return

    print(f"\nTotal entries to review: {total}")
    if category:
        print(f"Filtered to category: {category}")
    if needs_work_only:
        print(f"Filtered to entries needing work")

    # Print initial reminder
    print(REMINDER)

    for i, (name, entry) in enumerate(items[start:], start=start):
        # Print reminder every 10 entries
        if i > start and i % 10 == 0:
            print(REMINDER)

        display_entry(name, entry, i, total)

        assessment = get_work_assessment(entry)
        if assessment != "OK":
            print(f"\n⚠ ASSESSMENT: {assessment}")

        print(f"\n[Press Enter for next, 'q' to quit, 's' to skip 10, or entry number to jump]")

        try:
            response = input("> ").strip().lower()
            if response == 'q':
                print(f"\nStopped at entry {i}. Resume with: --start {i}")
                break
            elif response == 's':
                # Skip ahead is handled by continuing
                continue
            elif response.isdigit():
                jump_to = int(response)
                if jump_to < total:
                    # This is a simple stepper, so we just note it
                    print(f"Note: Restart with --start {jump_to} to jump")
        except EOFError:
            print(f"\nEOF at entry {i}. Resume with: --start {i}")
            break
        except KeyboardInterrupt:
            print(f"\n\nInterrupted at entry {i}. Resume with: --start {i}")
            break

# =============================================================================
# STATS
# =============================================================================

def show_stats(entries: dict):
    """Show statistics about the glossary."""
    total = len(entries)
    by_category = {}
    needs_work_count = 0

    for name, entry in entries.items():
        cat = entry.get('category', 'unknown')
        by_category[cat] = by_category.get(cat, 0) + 1
        if needs_work(entry):
            needs_work_count += 1

    print(f"\nGLOSSARY STATISTICS")
    print(f"{'─' * 40}")
    print(f"Total entries: {total}")
    print(f"Entries needing work: {needs_work_count}")
    print(f"\nBy category:")
    for cat, count in sorted(by_category.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Step through glossary entries for revision")
    parser.add_argument('--start', type=int, default=0, help="Start from entry N")
    parser.add_argument('--category', type=str, help="Filter to category (caste/location/organization/concept)")
    parser.add_argument('--needs-work', action='store_true', help="Only show entries needing work")
    parser.add_argument('--stats', action='store_true', help="Show statistics only")
    parser.add_argument('--file', type=str, default='glossary_data.yaml', help="Glossary file path")

    args = parser.parse_args()

    # Find glossary file
    glossary_path = Path(args.file)
    if not glossary_path.exists():
        # Try common locations
        for try_path in ['/home/user/ya-Sattra/glossary_data.yaml',
                         '/mnt/project/glossary_data.yaml',
                         'glossary_data.yaml']:
            if Path(try_path).exists():
                glossary_path = Path(try_path)
                break

    if not glossary_path.exists():
        print(f"Could not find glossary file: {args.file}")
        sys.exit(1)

    print(f"Loading: {glossary_path}")
    entries = load_glossary(str(glossary_path))

    if args.stats:
        show_stats(entries)
    else:
        step_through(entries, start=args.start, category=args.category,
                    needs_work_only=args.needs_work)

if __name__ == '__main__':
    main()

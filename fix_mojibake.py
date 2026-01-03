#!/usr/bin/env python3
"""
Fix mojibake encoding issues in project files.

The mojibake pattern: UTF-8 bytes decoded as Windows-1252/CP1252,
then re-encoded as UTF-8.

Usage:
    python fix_mojibake.py                    # Fix all .md and .yaml in current dir
    python fix_mojibake.py file.md            # Fix specific file
    python fix_mojibake.py --dir /path/to/dir # Fix all in directory
    python fix_mojibake.py --dry-run          # Show what would change
"""

import argparse
import sys
from pathlib import Path


def build_replacements():
    """
    Build replacement patterns from byte sequences.
    
    When UTF-8 text is decoded as Windows-1252 then re-encoded as UTF-8,
    each original UTF-8 byte becomes a CP1252 character, which then becomes
    1-3 UTF-8 bytes. We construct the patterns by simulating this process.
    """
    originals = {
        '\u2014': 'em-dash',
        '\u2013': 'en-dash',
        '\u2019': 'right single quote',
        '\u2018': 'left single quote',
        '\u201c': 'left double quote',
        '\u201d': 'right double quote',
        '\u2026': 'ellipsis',
        '\u00e9': 'e-acute',
        '\u00e8': 'e-grave',
        '\u00fc': 'u-umlaut',
        '\u00f6': 'o-umlaut',
        '\u00e4': 'a-umlaut',
        '\u00f1': 'n-tilde',
        '\u00e1': 'a-acute',
        '\u00ed': 'i-acute',
        '\u00f3': 'o-acute',
        '\u00fa': 'u-acute',
    }
    
    replacements = []
    
    for char, name in originals.items():
        utf8_bytes = char.encode('utf-8')
        try:
            mojibake = b''.join(
                bytes([b]).decode('cp1252').encode('utf-8')
                for b in utf8_bytes
            ).decode('utf-8')
            replacements.append((mojibake, char))
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass
    
    # Sort by length descending to avoid partial matches
    replacements.sort(key=lambda x: len(x[0]), reverse=True)
    return replacements


REPLACEMENTS = build_replacements()
EXTENSIONS = {'.md', '.yaml', '.yml', '.txt'}


def fix_content(content: str) -> tuple[str, int]:
    """Apply all replacements, return fixed content and count of changes."""
    changes = 0
    for old, new in REPLACEMENTS:
        count = content.count(old)
        if count:
            content = content.replace(old, new)
            changes += count
    return content, changes


def fix_file(filepath: Path, dry_run: bool = False, verbose: bool = False) -> int:
    """Fix a single file. Returns number of replacements made."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        print(f"  SKIP (not UTF-8): {filepath}", file=sys.stderr)
        return 0
    except Exception as e:
        print(f"  ERROR reading {filepath}: {e}", file=sys.stderr)
        return 0

    fixed, changes = fix_content(content)
    
    if changes == 0:
        if verbose:
            print(f"  OK: {filepath}")
        return 0
    
    if dry_run:
        print(f"  WOULD FIX: {filepath} ({changes} replacements)")
    else:
        try:
            filepath.write_text(fixed, encoding='utf-8')
            print(f"  FIXED: {filepath} ({changes} replacements)")
        except Exception as e:
            print(f"  ERROR writing {filepath}: {e}", file=sys.stderr)
            return 0
    
    return changes


def find_files(directory: Path) -> list[Path]:
    """Find all fixable files in directory."""
    files = []
    for ext in EXTENSIONS:
        files.extend(directory.rglob(f'*{ext}'))
    return sorted(files)


def main():
    parser = argparse.ArgumentParser(
        description='Fix mojibake encoding issues in markdown and yaml files.'
    )
    parser.add_argument(
        'files', nargs='*', 
        help='Specific files to fix (default: all .md/.yaml in current dir)'
    )
    parser.add_argument(
        '--dir', '-d', type=Path, default=None,
        help='Directory to scan for files'
    )
    parser.add_argument(
        '--dry-run', '-n', action='store_true',
        help='Show what would be changed without modifying files'
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Show all files, including those with no changes'
    )
    parser.add_argument(
        '--show-patterns', action='store_true',
        help='Show the replacement patterns and exit'
    )
    
    args = parser.parse_args()
    
    if args.show_patterns:
        print("Replacement patterns (mojibake -> correct):")
        for old, new in REPLACEMENTS:
            print(f"  {repr(old):30} -> {repr(new)} ({new})")
        return 0
    
    if args.files:
        files = [Path(f) for f in args.files]
    elif args.dir:
        files = find_files(args.dir)
    else:
        files = find_files(Path.cwd())
    
    if not files:
        print("No files found to process.")
        return 0
    
    mode = " (dry run)" if args.dry_run else ""
    print(f"Scanning {len(files)} file(s)...{mode}")
    
    total_changes = 0
    files_fixed = 0
    
    for filepath in files:
        if not filepath.exists():
            print(f"  SKIP (not found): {filepath}", file=sys.stderr)
            continue
        changes = fix_file(filepath, args.dry_run, args.verbose)
        if changes:
            total_changes += changes
            files_fixed += 1
    
    print(f"\nDone. {files_fixed} file(s), {total_changes} total replacements.")
    return 0


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""Fix mojibake encoding issues in markdown files."""
import codecs
import sys
import os

SOURCE_FILE = '/mnt/project/The_Emperor.md'
DEST_FILE = '/home/claude/Post-Interdict Empire/Mysteries - The Emperor and the Singularity.md'

# Fix mojibake
REPLACEMENTS = [
    ('â€"', '—'),
    (''', "'"),
    ('"', '"'),
    ('â€', '"'),
    ('é', 'é'),
    ('è', 'è'),
    ('ü', 'ü'),
    ('ö', 'ö'),
    ('ä', 'ä'),
]


def fix_mojibake():
    """Read source file, fix mojibake issues, and write to destination."""
    # Read source file
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"ERROR: Source file not found: {SOURCE_FILE}", file=sys.stderr)
        return 1
    except PermissionError:
        print(f"ERROR: Permission denied reading: {SOURCE_FILE}", file=sys.stderr)
        return 1
    except UnicodeDecodeError as e:
        print(f"ERROR: Failed to decode file as UTF-8: {SOURCE_FILE}", file=sys.stderr)
        print(f"  Details: {e}", file=sys.stderr)
        return 1
    except IOError as e:
        print(f"ERROR: Failed to read file: {SOURCE_FILE}", file=sys.stderr)
        print(f"  Details: {e}", file=sys.stderr)
        return 1

    # Apply replacements
    for old, new in REPLACEMENTS:
        content = content.replace(old, new)

    # Ensure destination directory exists
    dest_dir = os.path.dirname(DEST_FILE)
    try:
        os.makedirs(dest_dir, exist_ok=True)
    except PermissionError:
        print(f"ERROR: Permission denied creating directory: {dest_dir}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"ERROR: Failed to create directory: {dest_dir}", file=sys.stderr)
        print(f"  Details: {e}", file=sys.stderr)
        return 1

    # Write destination file
    try:
        with open(DEST_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
    except PermissionError:
        print(f"ERROR: Permission denied writing: {DEST_FILE}", file=sys.stderr)
        return 1
    except IOError as e:
        print(f"ERROR: Failed to write file: {DEST_FILE}", file=sys.stderr)
        print(f"  Details: {e}", file=sys.stderr)
        return 1

    print('Fixed mojibake')
    return 0


if __name__ == '__main__':
    sys.exit(fix_mojibake())

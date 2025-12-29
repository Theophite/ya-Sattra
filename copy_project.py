#!/usr/bin/env python3
"""
Copy project files to working directory, fixing mojibake in the process.

This script is ASCII-safe - all unicode literals use escape sequences.
Handles the common case of UTF-8 bytes misread as CP1252 then re-saved as UTF-8.

Usage:
    python3 copy_project.py                    # Copy all .py, .md, and .yaml files
    python3 copy_project.py --ext .py .md .txt # Specify extensions
    python3 copy_project.py --file foo.py      # Copy specific file(s)
    python3 copy_project.py --dry-run          # Show what would be copied
"""

import os
import sys
import shutil
import argparse

# Mojibake fixes: corrupted sequence -> correct character
# All values use \u or \U escapes to keep this file ASCII-safe
MOJIBAKE_FIXES = {
    # Arrows - right arrow is by far most common in these docs
    "\u00e2\u2020\u2019": "\u2192",           # -> right arrow (U+2192)
    "\u00e2\u0086\u2019": "\u2192",           # -> right arrow (variant)
    "\u00e2\u2020\u0091": "\u2191",           # up arrow (U+2191)
    "\u00e2\u2020\u0093": "\u2193",           # down arrow (U+2193)
    "\u00e2\u2020\u0090": "\u2190",           # <- left arrow (U+2190)
    
    # Dashes
    "\u00e2\u20ac\u201d": "\u2014",           # -- em dash
    "\u00e2\u20ac\u201c": "\u2013",           # - en dash
    
    # Bullets and misc punctuation
    "\u00e2\u20ac\u00a2": "\u2022",           # bullet
    "\u00e2\u20ac\u00a6": "\u2026",           # ellipsis
    
    # Quotes
    "\u00e2\u20ac\u2122": "\u2019",           # right single quote
    "\u00e2\u20ac\u2018": "\u2018",           # left single quote
    "\u00e2\u20ac\u0153": "\u201c",           # left double quote
    "\u00e2\u20ac\u009d": "\u201d",           # right double quote
    "\u00e2\u20ac\u201c": "\u201c",           # left double quote (variant)
    
    # Emoji (4-byte UTF-8 sequences get especially mangled)
    "\u00f0\u0178\u2019\u00a1": "\U0001F4A1", # 💡 lightbulb
    "\u00f0\u0178\u201c\u0161": "\U0001F4DA", # 📚 books
    "\u00f0\u0178\u2018\u00a5": "\U0001F465", # 👥 busts in silhouette
    "\u00f0\u0178\u0161\u00aa": "\U0001F6AA", # 🚪 door
    "\u00f0\u0178\u201c\u008d": "\U0001F4CD", # 📍 round pushpin
    
    # 3-byte symbols
    "\u00e2\u0161\u00a0\u00ef\u00b8\u008f": "\u26a0\ufe0f", # ⚠️ warning with variant selector
    "\u00e2\u0161\u00a0": "\u26a0",           # âÅ¡  warning sign alone
    "\u00e2\u0153\u201c": "\u2714",           # âÃƒ…"" check mark
    "\u00e2\u0153\u2014": "\u2717",           # ✗ cross mark
    "\u00e2\u008f\u00b0": "\u23f0",           # ⏰ alarm clock
    "\u00ef\u00b8\u008f": "\ufe0f",           # variation selector (clean up orphans)
    
    # Box drawing - horizontal lines
    "\u00e2\u201d\u20ac": "\u2500",           # ─ horizontal line (U+2500)
    "\u00e2\u2022\u0090": "\u2550",           # ═ double horizontal (U+2550) - common header decoration
    "\u00c3\u00a2\u00e2\u20ac\u00a2\u00c2\u0090": "\u2550", # triple-encoded double horizontal
    
    # Control characters that appear in mangled box-drawing (strip them)
    "\u00c2\u0090": "",                        # mangled control char DCS (U+0090) - remove
    "\u00c2\u0091": "",                        # mangled control char (U+0091) - remove  
    "\u00c2\u0092": "",                        # mangled control char (U+0092) - remove
    "\u00c2\u0093": "",                        # mangled control char (U+0093) - remove
    "\u00c2\u0094": "",                        # mangled control char (U+0094) - remove
    "\u00c2\u0095": "",                        # mangled control char (U+0095) - remove
    
    # Geometric shapes (E2 97 xx sequence)
    "\u00e2\u2014\u2020": "\u25c6",           # â—â€  black diamond
    "\u00e2\u2014\u2021": "\u25c7",           # â—â€¡ white diamond
    "\u00e2\u2014\u2039": "\u25cb",           # â—â€¹ white circle
    "\u00e2\u2014\u008f": "\u25cf",           # ● black circle
    "\u00e2\u02dc\u2026": "\u2605",           # ★ black star
    
    # Accented characters - macrons (common in Imperial language)
    "\u00c4\u0081": "\u0101",                 # a with macron
    "\u00c4\u0093": "\u0113",                 # e with macron
    
    # Triple-encoded macrons (found in some markdown files)
    "\u00c3\u201e\u00c2\u0081": "\u0101",     # ā triple-encoded
    "\u00c3\u201e\u00c2\u00ab": "\u012b",     # ī triple-encoded
    "\u00c3\u2026\u00c2\u008d": "\u014d",     # ō triple-encoded
    "\u00c3\u2026\u00c2\u00ab": "\u016b",     # ū triple-encoded
    
    # Common Latin-1 misreadings (C3 xx pattern = UTF-8 for U+00xx read as CP1252)
    "\u00c2\u00a0": "\u00a0",                 # nbsp
    "\u00c2\u00ab": "\u00ab",                 # left guillemet
    "\u00c2\u00bb": "\u00bb",                 # right guillemet
    "\u00c2\u00b0": "\u00b0",                 # degree
    "\u00c2\u00b7": "\u00b7",                 # middle dot
    "\u00c3\u00a0": "\u00e0",                 # a grave
    "\u00c3\u00a1": "\u00e1",                 # a acute
    "\u00c3\u00a2": "\u00e2",                 # a circumflex
    "\u00c3\u00a8": "\u00e8",                 # e grave
    "\u00c3\u00a9": "\u00e9",                 # e acute
    "\u00c3\u00aa": "\u00ea",                 # e circumflex
    "\u00c3\u00ab": "\u00eb",                 # e umlaut
    "\u00c3\u00ac": "\u00ec",                 # i grave
    "\u00c3\u00ad": "\u00ed",                 # i acute
    "\u00c3\u00ae": "\u00ee",                 # i circumflex
    "\u00c3\u00af": "\u00ef",                 # i umlaut
    "\u00c3\u00b1": "\u00f1",                 # n tilde
    "\u00c3\u00b2": "\u00f2",                 # o grave
    "\u00c3\u00b3": "\u00f3",                 # o acute
    "\u00c3\u00b4": "\u00f4",                 # o circumflex
    "\u00c3\u00b6": "\u00f6",                 # o umlaut
    "\u00c3\u00b9": "\u00f9",                 # u grave
    "\u00c3\u00ba": "\u00fa",                 # u acute
    "\u00c3\u00bb": "\u00fb",                 # u circumflex
    "\u00c3\u00bc": "\u00fc",                 # u umlaut
    "\u00c3\u00bf": "\u00ff",                 # y umlaut
    "\u00c3\u2039": "\u00cb",                 # E umlaut (Ë)
    "\u00c5\u00bb": "\u017b",                 # Z dot above
    
    # More macrons (C4/C5 range)
    "\u00c4\u201c": "\u0113",                 # e macron (variant encoding)
    "\u00c4\u00ab": "\u012b",                 # i macron
    "\u00c5\u008d": "\u014d",                 # o macron
    "\u00c5\u00ab": "\u016b",                 # u macron
    "\u00c7\u201d": "\u01d4",                 # u with caron (Ã‡")
}

# Additional single-character fixes (less certain, applied second)
SINGLE_CHAR_FIXES = {
    "\u0178": "\u00ff",                       # y with diaeresis (if standalone)
}


def fix_mojibake(text):
    """Apply all mojibake fixes to text."""
    result = text
    fixes_applied = 0
    
    # Apply multi-character fixes first (longer sequences first for safety)
    for bad, good in sorted(MOJIBAKE_FIXES.items(), key=lambda x: -len(x[0])):
        count = result.count(bad)
        if count > 0:
            result = result.replace(bad, good)
            fixes_applied += count
    
    return result, fixes_applied


def copy_file_with_fixes(src, dst, dry_run=False):
    """Copy a file, applying mojibake fixes to text files.

    Returns:
        int: Number of fixes applied, or -1 on error.
    """
    # Determine if this is a text file we should process
    text_extensions = {".py", ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".rst"}
    _, ext = os.path.splitext(src)
    is_text = ext.lower() in text_extensions

    if dry_run:
        print(f"  {src} -> {dst}" + (" [text, will fix]" if is_text else " [binary, copy only]"))
        return 0

    # Ensure destination directory exists
    dst_dir = os.path.dirname(dst)
    if dst_dir:
        try:
            os.makedirs(dst_dir, exist_ok=True)
        except PermissionError:
            print(f"ERROR: Permission denied creating directory: {dst_dir}", file=sys.stderr)
            return -1
        except OSError as e:
            print(f"ERROR: Failed to create directory: {dst_dir}", file=sys.stderr)
            print(f"  Details: {e}", file=sys.stderr)
            return -1

    if is_text:
        try:
            with open(src, "r", encoding="utf-8") as f:
                content = f.read()

            fixed_content, fixes = fix_mojibake(content)

            with open(dst, "w", encoding="utf-8") as f:
                f.write(fixed_content)

            return fixes
        except UnicodeDecodeError:
            # Fall back to binary copy if UTF-8 decode fails
            try:
                shutil.copy2(src, dst)
            except (PermissionError, IOError, shutil.Error) as e:
                print(f"ERROR: Failed to copy file {src}: {e}", file=sys.stderr)
                return -1
            return 0
        except FileNotFoundError:
            print(f"ERROR: Source file not found: {src}", file=sys.stderr)
            return -1
        except PermissionError as e:
            print(f"ERROR: Permission denied: {e}", file=sys.stderr)
            return -1
        except IOError as e:
            print(f"ERROR: I/O error copying {src} to {dst}: {e}", file=sys.stderr)
            return -1
    else:
        # Binary copy for non-text files
        try:
            shutil.copy2(src, dst)
        except FileNotFoundError:
            print(f"ERROR: Source file not found: {src}", file=sys.stderr)
            return -1
        except PermissionError as e:
            print(f"ERROR: Permission denied: {e}", file=sys.stderr)
            return -1
        except (IOError, shutil.Error) as e:
            print(f"ERROR: Failed to copy {src} to {dst}: {e}", file=sys.stderr)
            return -1
        return 0


def find_project_files(extensions):
    """Find all files with given extensions in /mnt/project/

    Returns:
        list: Sorted list of matching file paths, or empty list on error.
    """
    project_dir = "/mnt/project"
    files = []

    try:
        entries = os.listdir(project_dir)
    except FileNotFoundError:
        print(f"ERROR: Project directory not found: {project_dir}", file=sys.stderr)
        return []
    except PermissionError:
        print(f"ERROR: Permission denied accessing: {project_dir}", file=sys.stderr)
        return []
    except OSError as e:
        print(f"ERROR: Failed to list directory: {project_dir}", file=sys.stderr)
        print(f"  Details: {e}", file=sys.stderr)
        return []

    for entry in entries:
        path = os.path.join(project_dir, entry)
        try:
            if os.path.isfile(path):
                _, ext = os.path.splitext(entry)
                if ext.lower() in extensions:
                    files.append(path)
        except OSError:
            # Skip files we can't stat
            continue

    return sorted(files)


def main():
    parser = argparse.ArgumentParser(description="Copy project files with mojibake fixes")
    parser.add_argument("--ext", nargs="+", default=[".py", ".md", ".yaml"],
                        help="File extensions to copy (default: .py .md .yaml)")
    parser.add_argument("--file", nargs="+", dest="files",
                        help="Specific files to copy (relative to /mnt/project/)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be copied without copying")
    parser.add_argument("--dest", default="/home/claude",
                        help="Destination directory (default: /home/claude)")
    
    args = parser.parse_args()
    
    # Ensure destination exists
    try:
        os.makedirs(args.dest, exist_ok=True)
    except PermissionError:
        print(f"ERROR: Permission denied creating destination directory: {args.dest}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"ERROR: Failed to create destination directory: {args.dest}", file=sys.stderr)
        print(f"  Details: {e}", file=sys.stderr)
        return 1

    # Determine which files to copy
    if args.files:
        src_files = [os.path.join("/mnt/project", f) for f in args.files]
    else:
        extensions = set(e if e.startswith(".") else "." + e for e in args.ext)
        src_files = find_project_files(extensions)

    if not src_files:
        print("No files found to copy.")
        return 0

    print(f"{'Would copy' if args.dry_run else 'Copying'} {len(src_files)} files:")

    total_fixes = 0
    errors = 0
    for src in src_files:
        filename = os.path.basename(src)
        dst = os.path.join(args.dest, filename)
        fixes = copy_file_with_fixes(src, dst, dry_run=args.dry_run)

        if fixes == -1:
            errors += 1
        elif not args.dry_run:
            status = f" ({fixes} fixes)" if fixes > 0 else ""
            print(f"  {filename}{status}")
            total_fixes += fixes

    if not args.dry_run:
        if errors > 0:
            print(f"\nCompleted with {errors} error(s). {total_fixes} total mojibake sequences fixed.", file=sys.stderr)
            return 1
        else:
            print(f"\nDone. {total_fixes} total mojibake sequences fixed.")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)

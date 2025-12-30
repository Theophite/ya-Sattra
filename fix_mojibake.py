#!/usr/bin/env python3
import codecs

with open('/mnt/project/The_Emperor.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix mojibake
replacements = [
    ('â€"', '—'),
    ('â€™', "'"),
    ('â€œ', '"'),
    ('â€', '"'),
    ('Ã©', 'é'),
    ('Ã¨', 'è'),
    ('Ã¼', 'ü'),
    ('Ã¶', 'ö'),
    ('Ã¤', 'ä'),
]

for old, new in replacements:
    content = content.replace(old, new)

with open('/home/claude/Post-Interdict Empire/Mysteries - The Emperor and the Singularity.md', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed mojibake')

# Stepper Skill

Step through glossary entries systematically using `glossary_stepper.py`.

```bash
python3 glossary_stepper.py --category location   # Step through locations
python3 glossary_stepper.py --start 50            # Resume from entry 50
python3 glossary_stepper.py --stats               # Check progress
```

Edit **both** `short` and `details`. Leave subsections alone.

## Tools

**DO NOT use grep or other raw search commands.** Use the provided tools:

- `python3 glossary_stepper.py` — step through entries systematically
- `python3 glossary.py lookup "Entry Name"` — view a single entry formatted
- `python3 glossary.py search "term"` — find entries containing a term

The stepper and glossary.py exist for this purpose. Use them.

## The Eigenvector

Every entry conveys the coherent internal perspective of its subject.

The question is not "what is it" or "how did it happen." The question is **"how do we live inside it?"**

That question forces the inhabited perspective. A caste entry is about bodies and what it's like to have that body. A location entry is about spaces and what it's like to move through them. An organization entry is about structure and what it's like to work within it. Drift into the wrong level and you're writing the wrong entry.

Patterns generate fiction; instances constrain it. Describe what generates instances, not specific examples that become canonical and get recycled.

The entry should make sense from inside without explaining the meta-structure. Don't announce design principles. Embody them.

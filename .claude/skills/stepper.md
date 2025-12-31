# Stepper Skill

Step through **all 683 glossary entries**, editing **every single one**.

## Workflow

1. Read position from `.stepper_position`
2. Show entry: `python3 glossary_stepper.py --show N`
3. **Edit both `short` and `details`** (leave subsections alone)
4. Commit the revision
5. Increment `.stepper_position`
6. Repeat

**Edit every single entry.** No skipping. No "this one looks fine." Every entry gets touched. If an entry is already good, make it better. If it's great, find something to improve anyway. The goal is 683 commits, one per entry.

## Tools

**DO NOT use grep or other raw search commands.** Use:

- `python3 glossary_stepper.py --show N` — show entry N (all categories)
- `python3 glossary_stepper.py --show N --category location` — filter by category
- `python3 glossary.py lookup "Entry Name"` — view entry formatted
- `cat .stepper_position` — check current position

## The Eigenvector

Every entry conveys the coherent internal perspective of its subject.

The question is not "what is it" or "how did it happen." The question is **"how do we live inside it?"**

That question forces the inhabited perspective. A caste entry is about bodies and what it's like to have that body. A location entry is about spaces and what it's like to move through them. An organization entry is about structure and what it's like to work within it. Drift into the wrong level and you're writing the wrong entry.

Patterns generate fiction; instances constrain it. Describe what generates instances, not specific examples that become canonical and get recycled.

The entry should make sense from inside without explaining the meta-structure. Don't announce design principles. Embody them.

# Stepper Command

Step through **all 683 glossary entries**, editing **every single one**.

## The Eigenvector

Every entry conveys the coherent internal perspective of its subject.

The question is not "what is it" or "how did it happen." The question is **"how do we live inside it?"**

That question forces the inhabited perspective:
- **Caste:** bodies and what it's like to have that body
- **Location:** spaces and what it's like to move through them
- **Organization:** structure and what it's like to work within it
- **Technology:** what it's like to depend on what you can't comprehend

Patterns generate fiction; instances constrain it. Describe what generates instances, not specific examples that become canonical and get recycled.

The entry should make sense from inside without explaining the meta-structure. Don't announce design principles. Embody them.

## Workflow

1. Read position: `cat .stepper_position`
2. Show entry: `python3 glossary_stepper.py --show N`
3. **Edit both `short` and `details`** (leave subsections alone)
4. Commit the revision
5. Increment position: `echo "N+1" > .stepper_position`
6. Repeat

## Rules

- **Edit every single entry.** No skipping. No "this one looks fine."
- **No first person.** Locations describe spaces, not communities speaking.
- **No grep.** Use `glossary_stepper.py` and `glossary.py lookup`.
- **The goal is 683 commits**, one per entry.

## Tools

```bash
python3 glossary_stepper.py --show N              # Show entry N
python3 glossary_stepper.py --show N --category location  # Filter by category
python3 glossary.py lookup "Entry Name"           # View entry formatted
cat .stepper_position                             # Check current position
```

## Current Position

Read `.stepper_position` to see where you are. Continue from there.

# Stepper Skill: Systematic Glossary Entry Revision

Use `glossary_stepper.py` to systematically revise glossary entries according to the eigenvector principle.

## The Eigenvector

Every entry conveys the coherent internal perspective of its subject.

**THE QUESTION:** "How do we live inside it?"

## What To Edit

Edit **BOTH** `short` AND `details` fields. Leave all subsections (`caste_features`, `location_features`, `material_culture`, etc.) alone.

## Stepper Commands

```bash
python3 glossary_stepper.py                    # Start from beginning
python3 glossary_stepper.py --start 50         # Start from entry 50
python3 glossary_stepper.py --category caste   # Only castes
python3 glossary_stepper.py --category location # Only locations
python3 glossary_stepper.py --needs-work       # Only entries with empty/short details
python3 glossary_stepper.py --stats            # Show statistics
```

## Details Should Contain

1. **Physical reality** — what do outsiders see?
2. **Lived experience** — what is it like to BE this?
3. **The internal logic** that makes apparent absurdity make sense

## Stay at the Appropriate Level

Each category has its proper scope:

- **Caste:** Bodies and what it's like to have that body
- **Location:** Spaces and what it's like to move through them
- **Organization:** Structure and what it's like to work within it
- **Technology:** What it's like to depend on what you can't comprehend

**CRITICAL:** Don't describe culture in caste entries (that's organization). Don't describe bodies in organization entries (that's caste). Stay at the right level.

## Patterns, Not Instances

Specific examples become canonical and get recycled. Describe the **pattern that generates instances**, not the instances themselves.

**WRONG:** "The Temple of the Seventh Silence stands at the corner of Market Street"
**RIGHT:** "Temples cluster at major crossroads, their bells marking quarter-hours"

## Don't Invent

No terminology, places, or concepts that don't exist in the setting. Each entry should be interpretable on its own.

**WRONG:** "pillar-cities and sky-bridges connect the upper districts"
**RIGHT:** Reference only terms that exist in the glossary

If you need to reference setting terms, put them in the `related` field, not inline in the prose.

## Don't Wink

Embody the design principles without announcing them. No meta-commentary.

**WRONG:** "Engineers stop sorting—they know what each sound means"
**RIGHT:** "Each sound has a meaning engineers learn to read"

The winking version draws attention to the principle ("look, I'm showing expertise!"). The correct version simply demonstrates expertise.

## The Quality

Care persisting where understanding has failed. Endurance and transcendence amidst impenetrable mystery. Someone is doing their best here, and it matters.

## Workflow

1. **Run the stepper** for your target category
2. **Read each entry** as displayed
3. **Revise the entry** in glossary_data.yaml:
   - Rewrite `short` to be inhabited, not encyclopedic
   - Rewrite `details` with physical reality, lived experience, internal logic
   - Put proper nouns in `related` field
4. **Commit after each entry** with message format: "Revise [Entry Name] entry: [brief description of change]"
5. **Continue systematically** through all entries

## Common Mistakes

### Encyclopedic Openings
**WRONG:** "Population 50,000. A major trading hub."
**RIGHT:** "The crowd never thins. You learn to read currents—when the tide of bodies shifts toward the docks, a ship has come in."

### External Description for Castes
**WRONG:** "Beamcrawlers are a tall caste with long limbs adapted for climbing."
**RIGHT:** "The ground is wrong. Too flat, too stable. Your hands find nothing to grip."

### Cultural Details in Caste Entries
**WRONG:** "Akama maintain records and serve as scribes in government offices."
**RIGHT:** "Four hands write simultaneously. Eight eyes scan separate columns."

### Invented Terminology
**WRONG:** "The megastructures of the Old Empire..."
**RIGHT:** Use only terms that exist in the glossary

## Progress Tracking

The stepper shows entry count and prints reminders every 10 entries. Use `--start N` to resume from where you left off.

Current status:
- Caste entries: DONE (44 entries completed)
- Location entries: IN PROGRESS
- Organization entries: PENDING
- Other categories: PENDING

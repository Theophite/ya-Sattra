"""
Morning Generator for The Lattice Translator scenario.

Generates 2-3 atmospheric elements for the opening scene when the player wakes up.
"""

import random

MORNING_EVENTS = {
    "children": [
        "Vero is already awake, talking to himself in the other room.",
        "Maret had a nightmare. Senna is soothing him.",
        "The boys are arguing over something. It escalates, then stops.",
        "The children are still asleep. The apartment is quiet.",
        "Vero wants to show you something he found. It can wait, but he doesn't think so.",
        "Maret is standing in the doorway, watching you. He doesn't say anything.",
        "The boys are awake, playing some game that involves a lot of whispering.",
    ],
    "senna": [
        "Senna is at her workbench already, bent over something small. Quiet swearing.",
        "Senna is making breakfast downstairs. You smell it.",
        "Senna is getting the children dressed. She needs you to leave.",
        "Senna is still in bedÃ¢Ã¢â€šÂ¬â€unusual. She says she's fine.",
        "Senna has already left for an early errand. A note on the table.",
        "Senna is talking quietly to a neighbor at the door.",
        "The smell of coca tea brewing. Senna set some steeping before you woke.",
        "A warning tone from the lector on Senna's workbench. It's booting. That's what woke you.",
        "Senna is rewinding a coil of copper wire, measuring lengths against her forearm.",
        "Senna is cleaning a component you don't recognize. It gleams in the lamplight.",
    ],
    "building_sounds": [
        "The orb-lights outside are flickering on, one by one. The hum rises.",
        "Mutterers in the walls. Scratching, then a faint whirr. Fixing something.",
        "Water rushing through pipes somewhereÃ¢Ã¢â€šÂ¬â€more than usual.",
        "A deep thrum from below. Machinery powering up. You've heard it before.",
        "A sound you don't recognize. Metallic. Rhythmic. Then it stops.",
        "Footsteps on the stairs. Someone going to work early.",
        "The building's morning hum is different today. Lower. You can't say why.",
        "A thunk from the pneumatic tube. The White Sheet has arrived, compliments of the Lens.",
    ],
    "outside": [
        "The market is already loud. Vendors setting up.",
        "Fog today. The air is thickÃ¢Ã¢â€šÂ¬â€too many bodies, too much water boiling for noodles. It has to go somewhere. Water beads on your window.",
        "Someone is shouting in the terrace below. An argument.",
        "The bronze column across the gap is catching the morning light. Beautiful, actually.",
        "A beamcrawler hangs from a harness right outside your window, fixing one of the orbs. You can see the soles of their feet.",
        "Birds have gotten into the Fourth Whorl again. A whole flock of pigeons on the skybridge visible from your window, squalling and cooing. They're not supposed to be in here.",
        "Water dripping from above, outside. Condensation collecting on the bronze ceiling of the Whorl, finding the texture, falling past your window. It's that kind of morning.",
    ],
    "visitors": [
        "A knock at the door. Keloreth from 2-B, taking up a collection for a bribe to fix the water pressure.",
        "A knock at the door. Neighbor asking if you've seen their child's missing toy.",
        "A knock at the door. Building coordinator reminding everyone about the stairwell inspection.",
        "A message slipped under the door. Folded paper, no signature.",
        "No visitors. Just the building's sounds.",
        "A knock at the door. Someone looking for the previous tenant. They've been gone for years.",
    ],
}


def generate_morning(count=None):
    """Generate 2-3 morning elements.
    
    Args:
        count: Optional fixed number of elements (2-3). If None, randomly chosen.
    
    Returns:
        List of morning event strings.
    """
    if count is None:
        count = random.randint(2, 3)
    count = max(2, min(3, count))
    
    categories = random.sample(list(MORNING_EVENTS.keys()), k=count)
    elements = []
    for cat in categories:
        elements.append(random.choice(MORNING_EVENTS[cat]))
    return elements


def format_morning(elements):
    """Format morning elements for display."""
    lines = ["THIS MORNING:", ""]
    for element in elements:
        lines.append(f"Ã¢Ã¢â€šÂ¬Ã‚Â¢ {element}")
    return "\n".join(lines)


if __name__ == "__main__":
    elements = generate_morning()
    print(format_morning(elements))

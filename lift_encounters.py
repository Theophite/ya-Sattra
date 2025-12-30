#!/usr/bin/env python3
"""
Lift Encounters Generator for the Lattice Translator Scenario

FOR USE IN THINKING BLOCK ONLY. Run this script to generate encounter ideas,
then synthesize the results into natural prose for the actual response. 
Do not output the raw generator results to the user.

Generates random encounters Rivan might have on his daily lift commute
from the Fourth Whorl to the depths. 

Key notes:
- Enekef Namali (Kef) is Rivan's supervisor - Highborn, from the Namali clone line
- The Namali have perfect memory and identical faces - when Rivan sees one on the 
  lift, he literally cannot know if it's Kef or a different Namali
- Kef is formal, rigid, not unfriendly but not warm - he's transferring Devra 
  because the work is killing her, and he's probably right, which makes it worse
- Warborn are ALWAYS military/combat roles (Bureau of the Sword) - never laborers
- The lift station was built for thousands; now serves dozens
- Graffiti dates back to Record of Black Star and earlier
"""

import random
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Passenger:
    description: str
    bureau: Optional[str] = None
    notes: Optional[str] = None

@dataclass 
class LiftEncounter:
    passengers: List[Passenger]
    graffiti_detail: Optional[str] = None
    ambient_detail: Optional[str] = None
    namali_present: bool = False


# Clone lines that might appear
CLONE_LINES = {
    "Namali": {
        "description": "A Namali clerk",
        "features": "the same broad face, the same close-cropped hair, the same expression of distant focus",
        "bureau": "Lens",
        "note": "Enekef Namali (Kef) is Rivan's supervisor. The Namali are Highborn with perfect memory. "
                "Rivan cannot tell Kef from any of his clonebrothers. They all look the same."
    },
    "Ket": {
        "description": "A Ket administrator", 
        "features": "enhanced pattern recognition visible in the way their eyes track movement",
        "bureau": "Various",
        "note": "Ket clones serve across multiple Bureaus."
    },
}

# Regular passengers by type
ROD_WORKERS = [
    Passenger("Three Rod workers in heavy boots, tools on their belts, heading to the climate control stations", "Rod"),
    Passenger("A Rod maintenance crew, five of them, silent and tired, carrying equipment bags", "Rod"),
    Passenger("Two Rod technicians arguing quietly about pressure differentials", "Rod"),
    Passenger("A lone Rod inspector with a clipboard, making notes about something", "Rod"),
    Passenger("Rod workers with copper wire coiled over their shoulders, heading somewhere deep", "Rod"),
]

ARCHIVISTS = [
    Passenger("An archivist clutching a pneumatic cylinder like it contains something precious", "Lens"),
    Passenger("Two archivists from upper storage, their robes dusty with something that isn't dust", "Lens"),
    Passenger("An elderly archivist who has been making this commute longer than you've been alive", "Lens"),
]

CLERKS = [
    Passenger("Junior clerks in robes newer than yours, still learning the route", "Various"),
    Passenger("A clerk you've seen before but never spoken to, reading a folded White Sheet", "Various"),
    Passenger("Senior clerk with the geometric embroidery of someone two ranks above you", "Lens"),
    Passenger("Echo clerks heading to the upper levels, their work less classified than yours", "Lens"),
]

SWORD_PERSONNEL = [
    Passenger("A Sword officer in dress uniform, probably heading to the Second Whorl for administrative duties", "Sword", 
              "Not Warborn - baseline or near-baseline, the kind who commands rather than fights"),
    Passenger("Two Sword gendarmes escorting someone in plain clothes who doesn't look at anyone", "Sword",
              "The gendarmes are near-baseline. Warborn don't do escort duty."),
    Passenger("A Sword logistics clerk with the harried look of someone who can't get ordnance requisitions approved", "Sword"),
]

WARBORN_ENCOUNTERS = [
    Passenger("A Warborn in full kit, nine feet tall, taking up space meant for four. Heat radiates off them. "
              "They're heading somewhere with purpose - escort duty, garrison rotation, something military. "
              "No one looks at them directly.", "Sword",
              "Warborn are always soldiers. Always. This one will be dead of cancer before forty."),
    Passenger("Two Warborn, standard infantry phenotype, in the corner of the lift. The heat is oppressive. "
              "They speak to each other in low voices about someone named Korath.", "Sword",
              "Warborn only appear in military contexts. These are probably rotating between garrison posts."),
]

DEPTH_DWELLERS = [
    Passenger("Someone in clothes you don't recognize - depth-dweller fashion, heading further down than you go"),
    Passenger("A family of depth-dwellers, three generations, speaking a dialect you can barely follow"),
    Passenger("A depth-dweller merchant with a cart of pale mushrooms, heading to one of the deep markets"),
]

OTHER = [
    Passenger("No one. The lift is empty. You ride alone with the graffiti and the hum of cables."),
    Passenger("A Companion in their grey robes, heading somewhere you don't want to think about", "Companions Guild"),
    Passenger("Someone who might be Aureate - the proportions are slightly off, the neck slightly long - but they wear no sigil"),
    Passenger("A courier with a sealed pouch, practically vibrating with the importance of whatever they're carrying"),
]

# Graffiti details - things Rivan might notice
GRAFFITI = [
    "Someone carved 'VENN WAS HERE - BLACK STAR 3' into the bronze near the door. The letters are worn almost smooth.",
    "A crude drawing of something with too many limbs. You've seen it before. You've never looked closely.",
    "Names layered over names, generations of passengers marking their passage. The oldest are illegible.",
    "A date in notation you don't recognize. Older than Black Star. Older than anything you can read.",
    "Someone wrote 'THE EMPEROR PROTECTS' and someone else scratched it out and wrote 'FROM WHAT'",
    "A love note, or what might be a love note, in a dialect that hasn't been spoken in centuries.",
    "Tally marks. Hundreds of them. You don't know what they're counting.",
    "A symbol you've seen in documents from the Archive. You don't know what it means there either.",
    "The words 'STILL WAITING' in fresh scratches. Recent. This week, maybe.",
    "A map of something. Not the lift routes you know. Somewhere else. Somewhere deeper.",
]

# Ambient details
AMBIENT = [
    "The lift shudders. One of the Rod workers mutters about the counterweight.",
    "The cables groan. No one looks up.",
    "A light panel flickers, dies, comes back. Standard.",
    "The lift stops between floors. Waits. Continues. No one comments.",
    "You can feel the heat from the Warborn six rows away.",
    "Someone is humming. You can't tell who.",
    "The lift smells like machine oil and old bronze and too many bodies over too many years.",
    "The empty brackets pass by outside the grate - dozens of them, hundreds, waiting for lifts that don't come.",
    "You count the floors by the change in pressure in your ears.",
    "The graffiti slides past. You've memorized it. You still read it every time.",
]


def generate_namali_encounter() -> Passenger:
    """Generate a Namali clone encounter with the ambiguity of whether it's Kef"""
    variants = [
        Passenger(
            "A Namali stands near the door. The same broad face as Kef. The same close-cropped hair. "
            "The same expression of distant focus that suggests a mind cataloguing everything it perceives. "
            "You don't know if this is Kef Namali or one of his clonebrothers. You've never been able to tell.",
            "Lens",
            "Is this your boss? You literally cannot know."
        ),
        Passenger(
            "Two Namalis board at the Third Whorl junction. They don't acknowledge each other - or maybe they do, "
            "in some way you can't perceive, some clone-line communication beneath the threshold of your awareness. "
            "Either of them could be Kef. Neither of them could be Kef.",
            "Lens", 
            "Multiple Namalis. The ambiguity compounds."
        ),
        Passenger(
            "A Namali glances at you as they exit. The perfect memory means they remember you. "
            "They remember every time they've seen you. If this is Kef, he's catalogued every interaction you've had. "
            "If it isn't Kef, this stranger knows your face now, forever.",
            "Lens",
            "The Namali perfect memory - they never forget a face."
        ),
        Passenger(
            "You see a Namali on the platform as the lift doors open. They don't board. "
            "They're waiting for something, or someone, with that patient stillness the clone-line shares. "
            "You wonder if Kef is watching you leave, or if this is someone else entirely.",
            "Lens",
            "The paranoia of clone-line ubiquity."
        ),
        Passenger(
            "A Namali in senior clerk's embroidery rides three stops in silence. "
            "Kef wears senior clerk's embroidery. So do his clonebrothers in supervisory roles. "
            "The Namali exits without looking at you. You don't know if you've just been observed by your boss.",
            "Lens",
            "Kef Namali is Rivan's supervisor. The Namali are a Highborn clone line with perfect memory."
        ),
    ]
    return random.choice(variants)


def generate_encounter() -> LiftEncounter:
    """Generate a complete lift encounter"""
    
    passengers = []
    namali_present = False
    
    # Determine how many passengers (usually 0-8)
    num_passengers = random.choices(
        [0, 1, 2, 3, 4, 5, 6, 7, 8],
        weights=[5, 15, 25, 25, 15, 8, 4, 2, 1]  # Usually 2-4 passengers
    )[0]
    
    if num_passengers == 0:
        passengers.append(Passenger("The lift is empty. Just you and the graffiti and the hum of ancient cables."))
    else:
        # Chance of Namali (creates the "is this my boss?" tension)
        if random.random() < 0.15:  # 15% chance
            passengers.append(generate_namali_encounter())
            namali_present = True
            num_passengers -= 1
        
        # Chance of Warborn (rare, always notable)
        if random.random() < 0.05 and num_passengers > 0:  # 5% chance
            passengers.append(random.choice(WARBORN_ENCOUNTERS))
            num_passengers -= 1
        
        # Fill remaining slots
        all_regular = ROD_WORKERS + ARCHIVISTS + CLERKS + SWORD_PERSONNEL + DEPTH_DWELLERS + OTHER
        for _ in range(num_passengers):
            passengers.append(random.choice(all_regular))
    
    # Maybe notice specific graffiti
    graffiti_detail = random.choice(GRAFFITI) if random.random() < 0.3 else None
    
    # Ambient detail
    ambient_detail = random.choice(AMBIENT) if random.random() < 0.4 else None
    
    return LiftEncounter(
        passengers=passengers,
        graffiti_detail=graffiti_detail,
        ambient_detail=ambient_detail,
        namali_present=namali_present
    )


def format_encounter(encounter: LiftEncounter) -> str:
    """Format an encounter for display"""
    lines = []
    
    lines.append("=" * 60)
    lines.append("LIFT ENCOUNTER")
    lines.append("=" * 60)
    
    if encounter.namali_present:
        lines.append("\nâš ï¸  NAMALI PRESENT - Is this Kef? You cannot know.\n")
    
    lines.append("\nPASSENGERS:")
    for p in encounter.passengers:
        lines.append(f"\nâ€¢ {p.description}")
        if p.bureau:
            lines.append(f"  [Bureau: {p.bureau}]")
        if p.notes:
            lines.append(f"  Note: {p.notes}")
    
    if encounter.graffiti_detail:
        lines.append(f"\nGRAFFITI: {encounter.graffiti_detail}")
    
    if encounter.ambient_detail:
        lines.append(f"\nAMBIENT: {encounter.ambient_detail}")
    
    lines.append("\n" + "=" * 60)
    
    return "\n".join(lines)


def main():
    """Generate and display a lift encounter"""
    print("\nGenerating lift encounter for Rivan's commute...\n")
    encounter = generate_encounter()
    print(format_encounter(encounter))
    
    # Generate a few more for variety
    print("\n\nADDITIONAL SAMPLES:")
    for i in range(3):
        print(f"\n--- Sample {i+2} ---")
        encounter = generate_encounter()
        print(format_encounter(encounter))


if __name__ == "__main__":
    main()

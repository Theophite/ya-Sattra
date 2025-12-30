#!/usr/bin/env python3
"""
Market Encounters Generator for the Lattice Translator Scenario

FOR USE IN THINKING BLOCK ONLY. Run this script to generate encounter ideas,
then synthesize the results into natural prose for the actual response.
Do not output the raw generator results to the user.

Generates random encounters for Fourth Whorl market scenesâ€”the Terrace market
Rivan passes on his commute, guild shops, food vendors, the commerce that
fills the enclosed arcology.

Key context:
- The Fourth Whorl is INSIDE the arcology. There is no sky, no outside.
- Light comes from orb-fixtures in the distant ceiling, casting golden glow.
- Bronze columns (40 feet tall, 4 feet diameter) fill the space with geometric 
  patterns worn smooth where hands touch.
- Awnings in ochre and ecru with batik patterns stretch between columns.
- Guild shops (white market) operate under ancient charters.
- Temporary stalls (gray market) have uncertain legal status.
- Prices in obols: 1 obol = a day's unskilled labor.
- Westerners are NEVER seen. Their identical ships dock in the Rift, never open,
  and cargo (including Westerner tea) appears/disappears without contact.
  No Westerner characters should ever appear.
"""

import random
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Vendor:
    description: str
    goods: str
    price_note: Optional[str] = None
    market_type: str = "white"  # white, gray, or black

@dataclass
class MarketCharacter:
    description: str
    activity: str
    notes: Optional[str] = None

@dataclass
class MarketEncounter:
    vendors: List[Vendor]
    characters: List[MarketCharacter]
    physical_detail: Optional[str] = None
    ambient_detail: Optional[str] = None
    time_of_day: str = "morning"


# === VENDORS ===

FOOD_VENDORS = [
    Vendor(
        "A flatbread seller with a portable griddle",
        "Flatbread charring at the edges, sold in stacks of six",
        "Half-obol for a stackâ€”cheaper than baking your own fuel",
        "gray"
    ),
    Vendor(
        "The egg merchant from the Seventh Terrace",
        "Eggs in ceramic holders, sorted by size",
        "Quarter-obol for four. She knows when you're in a hurry.",
        "white"
    ),
    Vendor(
        "A noodle stall sending steam into the bronze air",
        "Noodles with fish, noodles with vegetables, noodles with both",
        "Quarter-obol a bowl. No seatingâ€”eat standing or carry it.",
        "gray"
    ),
    Vendor(
        "The marru seller whose shop has occupied this corner for two centuries",
        "Ceramic vessels of fermented fish paste, the smell escaping despite wax seals",
        "Half-obol for a household vessel. The smell never leaves the building.",
        "white"
    ),
    Vendor(
        "A vendor with a cart of pale mushrooms from the depths",
        "Mushrooms grown somewhere below, where light doesn't reach",
        "Two obols for a basket. Depth-dweller produce, technically legal.",
        "gray"
    ),
    Vendor(
        "The coca leaf merchant near the junction",
        "Dried coca in paper twists, the bitter smell mixing with bronze",
        "Quarter-obol for enough to last a week. Everyone buys here.",
        "white"
    ),
    Vendor(
        "A grilled-meat cart working the morning crowd",
        "Goat on skewers, peppered and charred",
        "Eighth-obol per skewer. No licenseâ€”the vendor moves when gendarmes appear.",
        "gray"
    ),
    Vendor(
        "The pickle vendor whose jars line a permanent stall",
        "Fermented greens in brine, fermented radish, something purple and pungent",
        "Quarter-obol for a jar. The purple ones are an acquired taste.",
        "white"
    ),
]

GUILD_SHOPS = [
    Vendor(
        "A Clothiers' Guild shop with the seven-pointed star above its door",
        "Maguey-silk in boltsâ€”cream, ochre, rust, teal, indigo",
        "Prices chalked on slate. The teal costs twice the ochre.",
        "white"
    ),
    Vendor(
        "The copper-workers' display, vessels stacked to the ceiling",
        "Bowls, cups, plates in various stages of oxidationâ€”red-gold to full green patina",
        "Three obols for a decent bowl. The green ones are 'antique.'",
        "white"
    ),
    Vendor(
        "A lens-grinders' shop, the Alley of Lenses guild chapter",
        "Spectacles, magnifying glasses, lector components in sealed cases",
        "Fifty obols for reading spectacles. The components are priced by consultation.",
        "white"
    ),
    Vendor(
        "The Booksellers' Guild outpost, smaller than the Row proper",
        "Approved texts, Bureau publications, religious materials, blank ledgers",
        "Two obols for a blank ledger. The approved texts are cheaper than the alternatives.",
        "white"
    ),
    Vendor(
        "A Metalworkers' Guild shop with tools hung from every surface",
        "Hammers, chisels, files, specialized implements whose purposes aren't obvious",
        "Quality guaranteed by charter. Prices to match.",
        "white"
    ),
]

ARCHAEOTECH_VENDORS = [
    Vendor(
        "A gray-market stall with 'documentation pending' on everything",
        "Salvaged lector components, power cells of uncertain origin, something that glows faintly",
        "Prices negotiable. Provenance not discussed.",
        "gray"
    ),
    Vendor(
        "A certified salvage dealer with Rod inspection stamps",
        "Pre-Interdict lighting panels (50 obols each), tools that never dull, fabric that won't tear",
        "Everything documented. Everything expensive. Everything works.",
        "white"
    ),
    Vendor(
        "A vendor who sells 'historical artifacts' from a locked case",
        "Items you don't look at too closely. The vendor doesn't explain what they do.",
        "If you have to ask the price, you can't afford it.",
        "black"
    ),
]

TEXTILE_AND_GOODS = [
    Vendor(
        "A temporary stall selling wool from the eastern territories",
        "Rough-woven fabric in natural colorsâ€”cream, grey, brown",
        "Half the price of guild cloth. Half the quality.",
        "gray"
    ),
    Vendor(
        "An awning-maker repairing canvas between sales",
        "Canvas panels, bamboo frames, rope, the batik stamps for patterns",
        "Thirty obols for a proper awning. Repairs are cheaper.",
        "white"
    ),
    Vendor(
        "A Ganati trader with goods from the Republic",
        "Destrier-leather goods, copper jewelry with organic patterns, maguey products",
        "Sold through the Liaison Office. Prices include 'facilitation fees.'",
        "white"
    ),
]


# === MARKET CHARACTERS ===

CLERKS_SHOPPING = [
    MarketCharacter(
        "A junior clerk in new black robes, obviously lost",
        "Comparing prices on a slate, calculating something",
        "First week in the Bureau, probably. Hasn't learned where to shop yet."
    ),
    MarketCharacter(
        "An elderly clerk whose robes have been mended many times",
        "Buying flatbread in bulk, the routine of decades",
        "Keloreth Block, maybe. Same commute as Rivan."
    ),
    MarketCharacter(
        "Two clerks from the Archive, still arguing about something from work",
        "Walking through the market without seeing it, gesturing at each other",
        "The argument involves classification protocols. They don't notice anyone else."
    ),
]

MERCHANTS_AND_ARTISANS = [
    MarketCharacter(
        "A textile merchant examining a competitor's goods",
        "Rubbing fabric between fingers, checking weave and dye",
        "Not buying. Assessing."
    ),
    MarketCharacter(
        "A copper-smith delivering finished goods to a customer",
        "Carrying a crate of vessels, the green patina showing through cloth wrapping",
        "The delivery is worth more than a clerk's monthly salary."
    ),
    MarketCharacter(
        "A master artisan from the Chronometer-Makers' Guild",
        "Moving through the crowd with purpose, people making way",
        "The guild badge is visible. The deference is automatic."
    ),
    MarketCharacter(
        "A young apprentice running an errand",
        "Carrying something wrapped in cloth, moving fast, looking nervous",
        "Whatever's in the package, it's fragile and expensive."
    ),
]

FOREIGN_TRADERS = [
    MarketCharacter(
        "A Ganati factor in Republican dress",
        "Negotiating with a guild representative, both speaking careful Imperial",
        "The cultural distance is visible in every gesture."
    ),
    MarketCharacter(
        "A trader from ya-Don, the accent obvious",
        "Selling something from a caseâ€”jewelry, maybe, or small tools",
        "Provincial goods for provincial prices."
    ),
    MarketCharacter(
        "A Ranga merchant with the scarification marking southern origin",
        "Examining textiles, comparing quality to what they know",
        "The Ranga trade through Aureate intermediaries. This one has connections."
    ),
]

OTHERS = [
    MarketCharacter(
        "A Companion in grey robes, shopping like anyone else",
        "Buying vegetables, ordinary as that is",
        "Even Companions eat. The grey robes get more space than they need."
    ),
    MarketCharacter(
        "A minor Aureate with the es- in their name and nothing else",
        "Haggling over prices they can't really afford",
        "The particle doesn't pay the bills."
    ),
    MarketCharacter(
        "Children chasing each other between stalls",
        "Playing a game with rules only they understand",
        "The vendors know them. The parents are somewhere nearby."
    ),
    MarketCharacter(
        "A gendarme walking a patrol route, not really looking",
        "The presence of authority, not its exercise",
        "Gray-market vendors watch the route and time their exposure."
    ),
    MarketCharacter(
        "Maintenance workers with push brooms, sweeping bronze",
        "The endless work of keeping the Fourth Whorl clean",
        "By morning the floor is scuffed again. They sweep anyway."
    ),
]


# === PHYSICAL ENVIRONMENT ===

PHYSICAL_DETAILS = [
    "A bronze column rises through the market, its geometric patterns worn smooth at hand-height. "
    "Above, an awning in ochre canvas provides shade that doesn't quite reach the ground.",
    
    "The ceiling is lost in golden hazeâ€”orb-fixtures casting light that has no source you can see. "
    "Banners hang from sky-bridges fifty feet up, teal and burgundy with geometric patterns.",
    
    "Buildings crowd between the ancient columns, never quite touching them. The gap is five feet, "
    "maybe tenâ€”enough for people to pass, enough for the columns to be maintained. Someone is "
    "polishing one now, standing on a ladder, the bronze gleaming where the cloth touches.",
    
    "A sky-bridge crosses overhead, its underside decorated with carved reliefs too high to read. "
    "People cross itâ€”silhouettes against the golden lightâ€”heading somewhere Rivan has never been.",
    
    "The floor is bronze tile, warped slightly from millennia of thermal cycling, worn into paths "
    "where generations have walked the same routes. The path to the junction is visible in the polish.",
    
    "An industrial building hums somewhere nearbyâ€”the sound of presses, machinery, something being made. "
    "The sound is constant. You stop hearing it after a while.",
    
    "The Terrace market isn't a buildingâ€”it's a section of the Fourth Whorl where stalls accumulate. "
    "The boundaries are informal, marked by where vendors set up and where they don't.",
]

AMBIENT_DETAILS = [
    "The smell: frying flatbread, machine oil, human sweat, incense from a shrine-stall. "
    "The sharp metallic scent of bronze itself, underlying everything.",
    
    "Ten thousand conversations at once, a murmur that never stops. Hammering from repair stalls. "
    "The sizzle of cooking. Footsteps on bronze, thousands of footsteps, a continuous rustling.",
    
    "A vendor calls out prices in a singsong patternâ€”three for an obol, two for an obolâ€”the words "
    "blurring into rhythm. Someone else is arguing, their voice rising, then subsiding.",
    
    "The crowd flows around obstacles like water. A dropped crate causes an eddy; people adjust "
    "without looking, their bodies knowing the rhythm of the market.",
    
    "A gust of warm air from a ventilation grilleâ€”the Rod's climate systems still function, mostly. "
    "The temperature stays constant. The humidity does not.",
    
    "Someone is playing music somewhereâ€”a string instrument, something with a drone. "
    "The sound comes from above, maybe from a sky-bridge platform. It stops, then starts again.",
    
    "The morning rush is building. In an hour the market will be crowded. Now there's still room "
    "to move, still time to browse. The vendors are setting up, arranging goods, preparing for the day.",
]


# === TIME OF DAY ===

TIME_EFFECTS = {
    "dawn": "The market is quiet. Vendors set up stalls, arranging goods in patterns refined over years. "
            "The orb-lights are dimmer nowâ€”simulating dawn, though no sun rises here.",
    
    "morning": "The morning crowd fills the passages between stalls. Clerks buy breakfast before heading "
               "to the inner whorls. The flatbread sellers are busiest now.",
    
    "midday": "The market is packed. Everyone who works in the Fourth Whorl seems to be here at once. "
              "Movement is slow, negotiation is quick, the ambient noise is overwhelming.",
    
    "afternoon": "The crowd thins as workers return to their posts. The food vendors rest; the goods "
                 "vendors work harder, catching customers with time to browse.",
    
    "evening": "The market is emptying. Vendors pack unsold goods, collapse temporary stalls, count "
               "the day's take. The lights dim toward night-cycle. Tomorrow it starts again.",
}


def generate_encounter(time: str = "morning") -> MarketEncounter:
    """Generate a complete market encounter"""
    
    vendors = []
    characters = []
    
    # Usually 1-3 vendors noticed
    num_vendors = random.choices([1, 2, 3], weights=[40, 40, 20])[0]
    
    # Weight toward food and guild shops
    all_vendors = (
        FOOD_VENDORS * 3 + 
        GUILD_SHOPS * 2 + 
        ARCHAEOTECH_VENDORS + 
        TEXTILE_AND_GOODS
    )
    vendors = random.sample(all_vendors, min(num_vendors, len(all_vendors)))
    
    # Usually 1-2 characters noticed
    num_characters = random.choices([0, 1, 2, 3], weights=[10, 40, 35, 15])[0]
    
    all_characters = (
        CLERKS_SHOPPING * 2 +
        MERCHANTS_AND_ARTISANS * 2 +
        FOREIGN_TRADERS +
        OTHERS * 2
    )
    if num_characters > 0:
        characters = random.sample(all_characters, min(num_characters, len(all_characters)))
    
    physical_detail = random.choice(PHYSICAL_DETAILS) if random.random() < 0.5 else None
    ambient_detail = random.choice(AMBIENT_DETAILS) if random.random() < 0.6 else None
    
    return MarketEncounter(
        vendors=vendors,
        characters=characters,
        physical_detail=physical_detail,
        ambient_detail=ambient_detail,
        time_of_day=time
    )


def format_encounter(encounter: MarketEncounter) -> str:
    """Format an encounter for display"""
    lines = []
    
    lines.append("=" * 70)
    lines.append("MARKET ENCOUNTER")
    lines.append("=" * 70)
    
    lines.append(f"\nTIME: {encounter.time_of_day.upper()}")
    lines.append(TIME_EFFECTS.get(encounter.time_of_day, ""))
    
    lines.append("\n--- VENDORS ---")
    for v in encounter.vendors:
        lines.append(f"\n[{v.market_type.upper()}] {v.description}")
        lines.append(f"  Goods: {v.goods}")
        if v.price_note:
            lines.append(f"  Price: {v.price_note}")
    
    if encounter.characters:
        lines.append("\n--- CHARACTERS ---")
        for c in encounter.characters:
            lines.append(f"\nâ€¢ {c.description}")
            lines.append(f"  Activity: {c.activity}")
            if c.notes:
                lines.append(f"  Notes: {c.notes}")
    
    if encounter.physical_detail:
        lines.append(f"\n--- PHYSICAL DETAIL ---\n{encounter.physical_detail}")
    
    if encounter.ambient_detail:
        lines.append(f"\n--- AMBIENT ---\n{encounter.ambient_detail}")
    
    lines.append("\n" + "=" * 70)
    
    return "\n".join(lines)


def main():
    """Generate and display market encounters"""
    print("\nGenerating market encounter...\n")
    
    # Morning encounter (Rivan's commute time)
    encounter = generate_encounter("morning")
    print(format_encounter(encounter))
    
    # Show samples at different times
    print("\n\nSAMPLES AT DIFFERENT TIMES:")
    for time in ["dawn", "midday", "evening"]:
        print(f"\n--- {time.upper()} ---")
        encounter = generate_encounter(time)
        print(format_encounter(encounter))


if __name__ == "__main__":
    main()

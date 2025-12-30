"""
Soldier's Kit Generator for the Post-Interdict Empire.

Generates equipment loadouts by soldier function across all major polities.
Each kit includes: primary weapon, secondary weapon, armor, equipment, 
personal items, and condition/wear details.

Manufacturer information is embedded - each named producer has specific output.
"""

import random

# =============================================================================
# MANUFACTURERS - What each producer actually makes
# =============================================================================

MANUFACTURERS = {
    # IMPERIAL MANUFACTURERS - Individual guild craftsmen with extreme variance
    "imperial": {
        "Master Kavek Ossoreth": {
            "location": "Medina Quarter, ya-Sattra",
            "specialty": "Rifles, traditional patterns",
            "products": [
                "Kavek-pattern chemical rifle (.42 caliber, brass furniture)",
                "carbines (shortened cavalry variant)",
                "heavy rifles (.55 caliber, tripod-mounted)",
            ],
            "notes": "Armorers' Guild master, third generation. His workshop produces perhaps forty rifles yearly. Quality excellent but availability limited. Contracts with specific battalions going back centuries."
        },
        "Journeyman Thess Morain": {
            "location": "Seventh Terrace, ya-Sattra",
            "specialty": "Precision components",
            "products": [
                "rifle sights (adjustable windage)",
                "trigger assemblies",
                "barrel linings (extends service life)",
            ],
            "notes": "Should have made master a decade ago; politics. His sights are worth their weight in silver. Works alone—no apprentices, no assistants."
        },
        "Master Vos-Dhal and Sons": {
            "location": "Iron Yards, ya-Sattra",
            "specialty": "Heavy equipment and crew-served weapons",
            "products": [
                "field pieces (chemical-propellant artillery)",
                "siege guns (requires ox-team transport)",
                "heavy weapon mounts and tripods",
            ],
            "notes": "Three generations, twelve workers. Work closely with Ironback units who can handle the weight. Reliable over innovative."
        },
        "The Ironmongers Collective": {
            "location": "Threshold district, ya-Don",
            "specialty": "Ammunition production",
            "products": [
                "rifle cartridges (sixteen different bore sizes)",
                "pistol rounds (twelve standard calibers)",
                "artillery shells (chemical propellant)",
            ],
            "notes": "Penitent-aligned cooperative, not a traditional guild operation. Quality varies by shift supervisor—the good batches are marked with blue dye."
        },
        "Apprentice Lorshan (under Master Tessoran)": {
            "location": "Fourth Whorl, ya-Sattra",
            "specialty": "Barrel work",
            "products": [
                "rifle barrels (adequate quality)",
                "barrel repairs",
                "bore enlargements for worn weapons",
            ],
            "notes": "Cheap. Fast. Adequate. When the real armorers have a six-month wait, soldiers come here."
        },
        "Master Keloreth the Elder": {
            "location": "Antediluvian Quarter, ya-Sattra",
            "specialty": "Ancient patterns and restorations",
            "products": [
                "reproduction archaeotech (non-functional display)",
                "antique weapon restoration",
                "ceremonial pieces for Aureate families",
            ],
            "notes": "Seventy-three years old. His apprentices do the work; he does the signatures. The name still commands premium prices."
        },
        "Journeyman Torven Garris": {
            "location": "Iron Yards, ya-Sattra (mobile)",
            "specialty": "Field repairs",
            "products": [
                "emergency repairs",
                "parts fabrication from salvage",
                "bore conversions between calibers",
            ],
            "notes": "No fixed workshop. Works from a cart. Goes where the work is. Soldiers know his name."
        },
    },
    
    # AKAMA / THOUSAND KINGDOMS - Individual craftsmen and salvage operations
    "akama": {
        "Dzoragh Ironhand": {
            "location": "Malpais village (mobile forge)",
            "specialty": "Traditional smithing, destrier equipment",
            "products": [
                "destrier tack (harness, saddle frames)",
                "gouges (distinctive blood-channel fuller)",
                "sabers (single-edge, moderate curve)",
                "spearheads and lance tips",
            ],
            "notes": "Third generation. Travels between villages. His gouges have a distinctive fuller that channels blood away from the grip."
        },
        "Grandmother Vurda Eleven-Sage": {
            "location": "Southern Malpais",
            "specialty": "Legendary blades",
            "products": [
                "gouges (master quality, months-long wait)",
                "sabers (pattern-welded, exceptional edge retention)",
                "daggers (ceremonial and functional)",
                "lance heads (for khans only)",
            ],
            "notes": "Seventy-three. No apprentice has matched her work. Waiting list measured in years. Her gouges are heirlooms."
        },
        "Khorat the Deserter": {
            "location": "Thavek district, Ogon",
            "specialty": "Chemical-propellant rifles",
            "products": [
                "hunting rifle (.38 caliber, accurate to 400 yards)",
                "carbine (cavalry length)",
                "heavy rifle (.50 caliber)",
            ],
            "notes": "Ganati Republican Guard deserter. Uses captured Imperial tooling. Quality approaches Republican standards. Doesn't talk about his past."
        },
        "Imek Stone-Foot": {
            "location": "Thavek district, Ogon",
            "specialty": "Electromagnetic weapons (emerging)",
            "products": [
                "light rail carbine (Imek-pattern, recent development)",
                "capacitor packs (portable)",
                "coil assemblies for weapon repair",
            ],
            "notes": "Purchased a coil-winder from Avouvar traders. First Akama-repairable rail weapons. Revolutionary development."
        },
        "Old Tseng and his boys": {
            "location": "Ogon outskirts",
            "specialty": "Infantry equipment",
            "products": [
                "infantry shields (laminated wood, leather facing)",
                "spears (ash shafts, iron heads)",
                "leather armor (boiled, reinforced)",
                "arrows (bulk production, consistent quality)",
            ],
            "notes": "Tseng is dead. His sons run the forge. Everyone still calls it Old Tseng's. Reliable but not exceptional."
        },
        "Gorvan Salvage": {
            "location": "Ogon harbor district",
            "specialty": "Captured equipment evaluation and bypass",
            "products": [
                "authentication bypass (Imperial weapons)",
                "equipment evaluation and certification",
                "parts harvesting from damaged equipment",
            ],
            "notes": "Gorvan himself handles the neural-lock bypass. His apprentices do the rest. If it was captured, they can tell you if it works."
        },
        "Whoever's working the Tama forge today": {
            "location": "Ogon, varies",
            "specialty": "Basic metalwork",
            "products": [
                "horseshoes",
                "knife repairs",
                "whatever you need",
            ],
            "notes": "The Tama family has outlasted every Khan for four centuries. Be useful. Never threaten power."
        },
    },
    
    # GANATI MANUFACTURERS - Merchant houses (Dusk) and syndicalist cooperatives (Dawn)
    "ganati": {
        "Dam Workers' Armorers Assembly": {
            "location": "Inside the Dam, chambers adjacent to turbine halls",
            "specialty": "Mass production",
            "products": [
                "rifle barrels (machine-turned, consistent bore)",
                "cartridge cases (brass, standardized)",
                "bayonets (triangular, socket-mount)",
                "uniform fittings (buttons, buckles)",
            ],
            "notes": "Dawn-aligned cooperative. 24-hour production. Quality varies by shift committee. Free power means experimentation is cheap.",
            "political": "Dawn"
        },
        "House Tal-Omir": {
            "location": "Merchant Terraces, Taho—workshops overlooking the harbor",
            "specialty": "Quality weapons for merchant guards",
            "products": [
                "Tal-Omir rifle (.40 caliber, blued steel, walnut stock)",
                "carbines (caravan guard variant)",
                "matched officer pistol pairs",
                "presentation weapons (engraved, for diplomacy)",
            ],
            "notes": "Old merchant family, Dusk-aligned. Higher prices, better quality. Their guards carry their own weapons.",
            "political": "Dusk"
        },
        "Khen-Masot Rifle Works": {
            "location": "Near Wall workshop district, Ganat proper",
            "specialty": "Standardized infantry weapons",
            "products": [
                "infantry rifle (.40 caliber, Guard standard)",
                "replacement parts (standardized)",
                "training rifles (reduced charge)",
            ],
            "notes": "Compound name, old merchant family, but maintains careful neutrality. Contracts predate the Revolution. Supplies the Guard regardless of who holds the Consulates.",
            "political": "neutral"
        },
        "Taho Metalworkers' Collective": {
            "location": "Industrial terraces, Taho—former textile mills converted after the War",
            "specialty": "Dragoon equipment",
            "products": [
                "culverin components (seventy percent domestic)",
                "rail carbines (reverse-engineered)",
                "charging equipment",
            ],
            "notes": "Syndicalist cooperative, Dawn-aligned. Their reverse-engineered rail weapons don't require Imperial authentication.",
            "political": "Dawn"
        },
        "Ghesam Optical (Sefka Ghesam, proprietor)": {
            "location": "Near Wall, Ganat proper",
            "specialty": "Precision optics",
            "products": [
                "rifle scopes (4x magnification)",
                "artillery ranging equipment",
                "signal mirrors (heliograph quality)",
                "binoculars (field grade)",
            ],
            "notes": "Single-name family—no kilit marker, but wealthy anyway. Forty workers, irreplaceable expertise. Waiting list for military contracts.",
            "political": "neutral"
        },
        "High Junction Armorers' Congress": {
            "location": "High Junction, northern frontier",
            "specialty": "Frontier equipment",
            "products": [
                "cold-weather gear (insulated, layered)",
                "cavalry equipment (saddles, tack)",
                "portable field forges",
                "ammunition (local production)",
            ],
            "notes": "Frontier cooperative. Six years of grid power transformed this garrison town. Dawn-aligned, supplies frontier kilits.",
            "political": "Dawn"
        },
        "House Kel el-Marwen (Salvage Division)": {
            "location": "Vegas Springs",
            "specialty": "Captured Imperial equipment",
            "products": [
                "refurbished Imperial rifles",
                "captured ammunition (sorted by caliber)",
                "Imperial armor (ceramic plates, fitted)",
                "authentication bypass services",
            ],
            "notes": "The Dusk Consul's family business. Every border action produces salvage. They buy, evaluate, resell. The el- particle means ancient Imperial descent.",
            "political": "Dusk"
        },
        "Academy Experimental Section": {
            "location": "Far Wall, Ganat proper",
            "specialty": "Reverse-engineering research",
            "products": [
                "prototype weapons",
                "technical documentation",
                "proof-of-concept designs",
            ],
            "notes": "Not a commercial producer—a laboratory. Where captured culverins go to be understood. State-funded.",
            "political": "state"
        },
    },
    
    # AVOUVAR MANUFACTURERS - Terminal outputs and trade interfaces
    "avouvar": {
        "Vesztraëlin Terminal Alpha": {
            "location": "Garrison District, Asovoë",
            "specialty": "Armor alloys",
            "products": [
                "armor alloy ingots (Warborn-grade, stops penetrators)",
                "pressure-rated tubes (pneumatic/hydraulic)",
            ],
            "notes": "Autofactory terminal, not conventional manufacturing. Production follows Medial schedules. May run for years, then stop for a decade."
        },
        "Vesztraëlin Terminal Gamma": {
            "location": "Garrison District, Asovoë",
            "specialty": "Volatile compounds",
            "products": [
                "oxidizers and propellants",
                "specialized storage containers",
                "chemical precursors",
            ],
            "notes": "Smaller and more erratic than Alpha. Requires careful handling."
        },
        "Droëvan Primary Terminal": {
            "location": "Garrison District, Asovoë",
            "specialty": "Electromagnetic components",
            "products": [
                "capacitors (railgun grade)",
                "electromagnets (various sizes)",
                "charging systems",
            ],
            "notes": "Essential for railgun maintenance throughout Asovoë. When this terminal stops, everyone's weapons degrade."
        },
        "Czernaël Factor-House": {
            "location": "San Juan Islands (trade interface)",
            "specialty": "Export processing",
            "products": [
                "armor alloy (sized for non-Avouvar customers)",
                "weapon components (adapted for larger hands)",
                "authentication certificates",
            ],
            "notes": "Where Avouvar goods meet the outside world. Akama are the primary customers. Significant markup. Neutral in the feud."
        },
    },
}

# =============================================================================
# SOLDIER TYPES BY POLITY AND FUNCTION
# =============================================================================

SOLDIER_KITS = {
    # =========================================================================
    # UNDYING EMPIRE
    # =========================================================================
    "imperial_warborn_infantry": {
        "name": "Warborn Infantry",
        "polity": "Undying Empire",
        "function": "Shock troops, breakthrough operations",
        "primary_weapons": [
            "Warborn railgun (60kg, electromagnetic acceleration, requires two baseline handlers)",
            "heavy chemical rifle (.55 caliber, reinforced stock for Warborn grip)",
            "Warborn-pattern pike (12 feet, counterweighted for their strength)",
        ],
        "secondary_weapons": [
            "combat knife (18-inch blade, bone handle)",
            "fists (bone-reinforced knuckles)",
            "teeth (filed sharp, tradition)",
        ],
        "armor": [
            "partial plate (ceramic over synthetic fiber, covers vitals only—regeneration handles the rest)",
            "bone armor (natural calcium plates visible through skin, no external covering)",
            "heavy coat (synthetic fiber, ablative layer, symbolic more than protective)",
        ],
        "equipment": [
            "ammunition harness (200 rounds or capacitor pack)",
            "nutrient concentrate (six meals daily requirement)",
            "stimulant injectors (Creche-issued, combat enhancement)",
            "cohort identification tags (forty names, most crossed out)",
        ],
        "personal_items": [
            "letters to crèche-nurse (never sent)",
            "bone dice (carved from a cohort-brother's remains)",
            "Oracle prayer beads (every battlefield decision recorded)",
            "nothing (possessions are sentiment; sentiment is weakness)",
        ],
        "condition": [
            "Equipment immaculate—Mutterer maintenance, Companion supervision",
            "Weapon shows heat scoring from recent action",
            "Armor bears impact craters that would have killed baseline soldiers",
            "Everything functional; Warborn don't keep broken equipment or broken soldiers",
        ],
    },
    
    "imperial_warborn_scout": {
        "name": "Warborn Scout-Assassin",
        "polity": "Undying Empire",
        "function": "Reconnaissance, elimination, terror operations",
        "primary_weapons": [
            "suppressed chemical rifle (.32 caliber, subsonic rounds)",
            "light railgun (30kg, reduced signature)",
            "composite bow (silent, recoverable ammunition)",
        ],
        "secondary_weapons": [
            "garrote (monofilament, Thess family manufacture)",
            "throwing knives (balanced, ceramic, invisible to detectors)",
            "poisoned needles (Creche-supplied paralytic)",
        ],
        "armor": [
            "stealth suit (synthetic fiber, thermal dampening, reduces their constant heat output)",
            "light ceramic plates (vitals only, mobility prioritized)",
            "face wrap (hides the inhuman features during infiltration)",
        ],
        "equipment": [
            "enhanced optics (night vision, thermal)",
            "climbing gear (grapples, rope rated for their weight)",
            "communication device (encrypted, short-range)",
            "nutrient concentrate (compressed, three days supply)",
        ],
        "personal_items": [
            "trophy collection (ears, fingers, identification tags)",
            "journal (targets eliminated, methods used)",
            "nothing traceable (doctrine)",
            "single photograph (cohort at decanting, eight of forty remain)",
        ],
        "condition": [
            "Equipment worn but functional—field maintenance",
            "Everything matte black, non-reflective",
            "Blood stains that won't quite wash out",
            "Weapon cleaning kit more used than the weapon itself",
        ],
    },
    
    "imperial_ironback_heavy": {
        "name": "Ironback Heavy Weapons",
        "polity": "Undying Empire",
        "function": "Crew-served weapons, defensive positions",
        "primary_weapons": [
            "Vos-Dhal heavy weapon (crew-served, carried by one Ironback)",
            "heavy chemical rifle (.55 caliber, extended barrel)",
            "siege crossbow (mechanical advantage, penetrates armor)",
        ],
        "secondary_weapons": [
            "entrenching tool (doubles as weapon)",
            "weighted club (lead-filled, one-handed use)",
            "bare hands (calcium-reinforced bones)",
        ],
        "armor": [
            "heavy plate (covers torso and head, the rest is bone)",
            "integrated helmet (bolted to skull anchor points)",
            "synthetic fiber undersuit (cushioning for the constant calcification)",
        ],
        "equipment": [
            "weapon maintenance kit (specific to heavy weapons)",
            "ammunition crate (carries what would require two baselines)",
            "medical supplies (painkillers for the headaches)",
            "insurance pool documentation (tendon snap preparation)",
        ],
        "personal_items": [
            "savings ledger (front-loading the career)",
            "apprenticeship inquiry letters (planning for after)",
            "bone carvings (keeping the fingers flexible)",
            "nothing personal (the body is enough burden)",
        ],
        "condition": [
            "Equipment scratched and dented—absorbs the recoil others can't",
            "Weapon stock shaped to fit arthritic grip",
            "Armor modified as the body calcified",
            "Everything reinforced; they know what's coming",
        ],
    },
    
    "imperial_springheel_scout": {
        "name": "Springheel Scout",
        "polity": "Undying Empire",
        "function": "Reconnaissance, flanking, pursuit",
        "primary_weapons": [
            "Kavek carbine (.38 caliber, shortened for mobility)",
            "repeating crossbow (near-silent, quick reload)",
            "javelins (three, throwing optimized for their arm extension)",
        ],
        "secondary_weapons": [
            "fighting knife (curved, designed for their reach)",
            "weighted bolas (for entanglement)",
            "signal whistle (ultrasonic, coordinates with other Springheels)",
        ],
        "armor": [
            "light leather (doesn't restrict the joints)",
            "ceramic inserts (vitals only)",
            "reinforced boots (carbon-fiber tendon support)",
        ],
        "equipment": [
            "climbing equipment (their physiology is the climbing equipment)",
            "signal flags (visual communication across distances)",
            "ration pouch (light, high-calorie)",
            "stretching kit (obsessive maintenance of those tendons)",
        ],
        "personal_items": [
            "insurance pool token (every Springheel pays in)",
            "love letters (life is uncertain; say it now)",
            "lucky charm (tendon snap has no correlation with anything)",
            "running journal (logging every stretch, looking for patterns)",
        ],
        "condition": [
            "Everything lightweight and secured—nothing can rattle",
            "Worn smooth from constant movement",
            "Straps adjusted for perfect fit",
            "Tendons either hold or they don't; the kit won't change that",
        ],
    },
    
    "imperial_caste_levy": {
        "name": "Caste Levy Infantry",
        "polity": "Undying Empire",
        "function": "Line infantry, holding positions",
        "primary_weapons": [
            "chemical rifle (Master Kavek pattern, .42 caliber, if your unit has the contract)",
            "chemical rifle (.45 caliber, older than the soldier, maker's mark worn away)",
            "chemical rifle (.38 caliber, Apprentice Lorshan work—cheap, adequate)",
            "chemical rifle (no maker's mark, assembled from three different weapons)",
        ],
        "secondary_weapons": [
            "bayonet (triangular, socket-mount)",
            "fighting knife (personal purchase)",
            "entrenching tool (also a weapon)",
        ],
        "armor": [
            "synthetic fiber vest (the good units have these)",
            "uniform that looks like armor (designed to resemble the real thing)",
            "leather vest with ceramic inserts (personal purchase)",
            "nothing (supply hasn't arrived)",
        ],
        "equipment": [
            "ammunition pouch (60 rounds, standard load)",
            "canteen and mess kit",
            "blanket roll",
            "identification papers (always keep these on your person)",
        ],
        "personal_items": [
            "letters from home (mother, mostly)",
            "guild rejection notice (why he's here)",
            "dice and cards (army currency)",
            "small idol (Oracle or Penitent, usually both)",
        ],
        "condition": [
            "Equipment mismatched—different procurement batches",
            "Rifle bore worn but functional",
            "Uniform patched in three places",
            "Everything carried has a story; nothing was issued that didn't require effort to acquire",
        ],
    },
    
    "imperial_gendarme": {
        "name": "Gendarme",
        "polity": "Undying Empire",
        "function": "Urban patrol, law enforcement",
        "primary_weapons": [
            "carbine (.38 caliber, urban length)",
            "shotgun (crowd control, less-lethal option)",
            "truncheon (primary tool, really)",
        ],
        "secondary_weapons": [
            "pistol (.32 caliber, holstered)",
            "knife (utility more than combat)",
            "weighted gloves (for when the truncheon isn't enough)",
        ],
        "armor": [
            "leather vest with ceramic plates",
            "helmet (protects against thrown objects)",
            "reinforced uniform (shows the badge)",
        ],
        "equipment": [
            "restraints (rope and metal)",
            "whistle (calling for backup)",
            "notebook (documentation protects you)",
            "small bribe (solves most problems)",
        ],
        "personal_items": [
            "list of which laws to enforce (learned over twenty years)",
            "family photograph (why he doesn't take risks)",
            "territory map (who to avoid, who to pressure)",
            "second small bribe (the first one doesn't always work)",
        ],
        "condition": [
            "Equipment well-maintained—inspection happens",
            "Truncheon shows impact wear",
            "Boots resoled twice",
            "Everything practical; flash draws attention from supervisors and criminals both",
        ],
    },
    
    # =========================================================================
    # THOUSAND KINGDOMS (AKAMA)
    # =========================================================================
    "akama_destrier_cavalry": {
        "name": "Destrier Cavalry",
        "polity": "Thousand Kingdoms",
        "function": "Primary strike force, mobile warfare",
        "primary_weapons": [
            "gouge (village-made, adequate, tells its story through notches and repairs)",
            "gouge (Dzoragh Ironhand work, distinctive blood-channel fuller)",
            "gouge (Grandmother Vurda master-work, pattern-welded, heirloom quality)",
            "lance (10-foot, reinforced for the impact of a leaping mount)",
        ],
        "secondary_weapons": [
            "brace of pistols (2-4 high-caliber breach-loaders)",
            "saber (single-edge, moderate curve, for when dismounted)",
            "composite bow (traditional, for harassment fire)",
            "Ganati pistol (import, better quality, status symbol)",
        ],
        "armor": [
            "autofactory alloy plate (Czernaël Factor-House import, heavy but stops penetrators)",
            "ceramic plates over destrier-leather (traditional, lighter)",
            "boiled leather with iron reinforcement (Old Tseng's boys, adequate)",
            "salvaged Imperial ceramic (Gorvan Salvage fitting, works anyway)",
        ],
        "equipment": [
            "destrier tack (saddle, harness, feed bag, grooming tools)",
            "ammunition pouch (50 pistol rounds)",
            "bedroll and tent (one-person, weatherproof)",
            "fire-starting kit and camp cookware",
        ],
        "personal_items": [
            "money pouch (sending to mother three weeks' ride south)",
            "gambling bones (obligatory redistribution, also entertainment)",
            "trophy from first kill (or first significant kill)",
            "destrier tooth (bonded at fourteen, this one fell out naturally)",
        ],
        "condition": [
            "Armor tells a story through damage and repair",
            "Gouge notched from use, edge recently touched up",
            "Equipment weathered but cared for—Akama aesthetic",
            "Destrier tack immaculate (you neglect your mount, you die)",
        ],
    },
    
    "akama_infantry": {
        "name": "Akama Infantry",
        "polity": "Thousand Kingdoms",
        "function": "Holding ground, fortification duty (those who can't bond with destriers)",
        "primary_weapons": [
            "Khorat rifle (.38 caliber, the Deserter's work)",
            "spear and shield (Old Tseng's boys, standard infantry kit)",
            "heavy crossbow (for fortification work)",
            "captured Imperial rifle (Gorvan Salvage bypass)",
        ],
        "secondary_weapons": [
            "hand axe (utility and combat)",
            "fighting knife (personal)",
            "sling (for when ammunition runs out)",
        ],
        "armor": [
            "leather armor (boiled, Old Tseng's pattern)",
            "shield (laminated wood, leather facing)",
            "salvaged ceramic plates (strapped over leather)",
            "helmet (iron, open-face)",
        ],
        "equipment": [
            "ammunition pouch (40 rounds)",
            "entrenching tool",
            "ration bag (three days)",
            "rope (fifty feet, always useful)",
        ],
        "personal_items": [
            "letter of recommendation (hoping for cavalry assignment, eventually)",
            "destrier rejection memory (the mount wouldn't accept him)",
            "savings (land purchase, someday)",
            "Khan's favor token (for distinguished service)",
        ],
        "condition": [
            "Equipment functional, not fancy—infantry don't get the good stuff",
            "Shield shows sword cuts",
            "Rifle borrowed from a dead cavalry rider",
            "Everything carried, nothing pretty",
        ],
    },
    
    "akama_scout": {
        "name": "Akama Scout",
        "polity": "Thousand Kingdoms",
        "function": "Reconnaissance, pathfinding",
        "primary_weapons": [
            "carbine (Khorat cavalry pattern, shortened)",
            "composite bow (traditional, quiet)",
            "javelins (three, light, any smith's work)",
        ],
        "secondary_weapons": [
            "knife (multipurpose)",
            "sling (supplementary, for small game)",
            "garrote (for sentries)",
        ],
        "armor": [
            "leather vest (mobility over protection)",
            "no armor (speed is armor)",
            "camouflage cloak (local vegetation pattern)",
        ],
        "equipment": [
            "map case (often empty—knowledge is in the head)",
            "signal mirror",
            "fire-starting kit",
            "minimal rations (forage supplemented)",
        ],
        "personal_items": [
            "territory journal (routes, water sources, danger points)",
            "first kill memory (still dreams about his face)",
            "mentor's gift (a scout who survived)",
            "nothing extra (weight is enemy)",
        ],
        "condition": [
            "Everything muted colors, nothing shiny",
            "Well-worn but not worn-out",
            "Bow string recently replaced",
            "Carries less than infantry, moves faster",
        ],
    },
    
    "akama_dragoon": {
        "name": "Akama Dragoon",
        "polity": "Thousand Kingdoms",
        "function": "Mounted infantry, dismounted firepower",
        "primary_weapons": [
            "heavy rifle (Khorat .50 caliber, the Deserter's elephant gun)",
            "heavy rifle with bayonet (lance conversion for mounted work)",
            "Imek Stone-Foot light rail carbine (new, expensive, Akama-repairable)",
        ],
        "secondary_weapons": [
            "pistol (single, reload takes too long for a brace)",
            "saber (for emergencies)",
            "bayonet-lance (fixed, used mounted or dismounted)",
        ],
        "armor": [
            "ceramic plates over leather (need protection when dismounted)",
            "autofactory alloy breastplate (Czernaël import, expensive, worth it)",
            "heavy leather with iron studs (traditional, adequate)",
        ],
        "equipment": [
            "ammunition bandolier (60 heavy rifle rounds)",
            "cleaning kit (heavy rifles foul quickly)",
            "horse tack (regular horse, not destrier)",
            "picket equipment (must secure mount during dismounted action)",
        ],
        "personal_items": [
            "marksman badge (if earned)",
            "horse bond token (not the same as destrier, still matters)",
            "family weapon (if inherited)",
            "Imperial casualty tally (professional pride)",
        ],
        "condition": [
            "Rifle shows careful maintenance",
            "Ammunition counted obsessively",
            "Horse equipment as good as personal gear",
            "Everything optimized for the dismount-fire-remount cycle",
        ],
    },
    
    # =========================================================================
    # REPUBLIC OF GANAT
    # =========================================================================
    "ganati_guard_cavalry": {
        "name": "Republican Guard Cavalry",
        "polity": "Republic of Ganat",
        "function": "Rapid response, frontier patrol",
        "primary_weapons": [
            "House Tal-Omir carbine (.40 caliber, cavalry length, Dusk quality)",
            "Khen-Masot rifle (.40 caliber, Guard standard issue)",
            "captured Imperial rifle (House Kel el-Marwen refurbishment, status symbol)",
        ],
        "secondary_weapons": [
            "saber (Republican Guard pattern, slightly curved)",
            "pistol (.38 caliber, Taho Arsenal)",
            "lance (for charge work, rarely used)",
        ],
        "armor": [
            "ceramic vest (Republican manufacture, standardized)",
            "synthetic fiber vest (Furnace-Annex material, imported)",
            "leather with ceramic inserts (frontier modification)",
        ],
        "equipment": [
            "ammunition pouch (80 rounds)",
            "canteen (desert operations require more water)",
            "compass and map",
            "signal flags (cavalry communication)",
        ],
        "personal_items": [
            "voting card (citizenship through service)",
            "kilit membership token",
            "land grant documentation (future homestead)",
            "family correspondence (building connections for after service)",
        ],
        "condition": [
            "Equipment standardized—Republican logistics work",
            "Well-maintained (professional force)",
            "Uniform shows service years through wear patterns",
            "Horse equipment matches rider quality—the Guard provides",
        ],
    },
    
    "ganati_guard_infantry": {
        "name": "Republican Guard Infantry",
        "polity": "Republic of Ganat",
        "function": "Fixed positions, urban operations",
        "primary_weapons": [
            "rifle (.40 caliber, Dam Workers' Assembly production)",
            "rifle with Ghesam scope (designated marksman)",
            "shotgun (urban operations)",
        ],
        "secondary_weapons": [
            "bayonet (socket-mount, Dam Industrial)",
            "pistol (.32 caliber)",
            "trench knife (close quarters)",
        ],
        "armor": [
            "ceramic vest (Republican standard issue)",
            "helmet (composite, protects against fragmentation)",
            "reinforced uniform",
        ],
        "equipment": [
            "ammunition pouch (100 rounds)",
            "entrenching tool",
            "gas mask (chemical warfare preparation)",
            "first aid kit",
        ],
        "personal_items": [
            "voting card",
            "kilit dues receipt",
            "hookah shop regular's token",
            "political pamphlet (Dawn or Dusk, always one)",
        ],
        "condition": [
            "Equipment uniform—Republican standardization",
            "Everything numbered and tracked",
            "Replacement parts available through proper channels",
            "Professional maintenance; the Guard has logistics that work",
        ],
    },
    
    "ganati_kilit_militia": {
        "name": "Kilit Militia",
        "polity": "Republic of Ganat",
        "function": "Reserve force, territorial defense",
        "primary_weapons": [
            "rifle (.40 caliber, older pattern)",
            "rifle (family weapon, maintained privately)",
            "rifle (kilit armory issue, variable quality)",
        ],
        "secondary_weapons": [
            "bayonet",
            "knife (work tool pressed into service)",
            "nothing (sixty days a year isn't enough to justify a sidearm)",
        ],
        "armor": [
            "vest (kilit issue, may or may not have inserts)",
            "work clothes (that's what they showed up in)",
            "family armor (if wealthy enough)",
        ],
        "equipment": [
            "ammunition pouch (40 rounds, kilit supply)",
            "canteen",
            "personal food (army food is bad)",
            "bedroll (army bedding is worse)",
        ],
        "personal_items": [
            "voting card (this is why they're here)",
            "farm or shop accounting (what they'd rather be doing)",
            "calendar (counting days until release)",
            "grandfather's war stories (why this matters, allegedly)",
        ],
        "condition": [
            "Equipment varies wildly by kilit wealth",
            "Rifle may not have been fired since last year's training",
            "Personal items reveal real life—this is obligation, not career",
            "Uniform doesn't quite fit (it's communal)",
        ],
    },
    
    "ganati_merchant_guard": {
        "name": "Merchant House Guard",
        "polity": "Republic of Ganat",
        "function": "Caravan protection, house security",
        "primary_weapons": [
            "House Tal-Omir rifle (.40 caliber, best quality)",
            "carbine (house pattern, caravan work)",
            "shotgun (close protection)",
        ],
        "secondary_weapons": [
            "pistol (House Tal-Omir matched pair)",
            "saber (decorative and functional)",
            "knife (utility)",
        ],
        "armor": [
            "ceramic vest (merchant grade, better than military)",
            "armored coat (concealed protection)",
            "light armor (mobility for caravan escort)",
        ],
        "equipment": [
            "ammunition (private supply, no shortages)",
            "communication gear (semaphore flags, signal rockets)",
            "merchant house identification (opens doors)",
            "expense account documentation",
        ],
        "personal_items": [
            "bonus documentation (good pay)",
            "merchant house loyalty oath",
            "route maps (proprietary, valuable)",
            "retirement fund statement (merchant houses pay well)",
        ],
        "condition": [
            "Equipment best quality—merchant profit buys good gear",
            "Uniform shows house colors",
            "Everything maintained by house armorers",
            "Professional appearance required; representing the house",
        ],
    },
    
    # =========================================================================
    # AVOUVAR
    # =========================================================================
    "avouvar_house_fighter": {
        "name": "Avouvar House Fighter",
        "polity": "Asovoë",
        "function": "House defense, feud operations",
        "primary_weapons": [
            "carbine (scaled for Avouvar hands, custom manufacture)",
            "crossbow (mechanical advantage, silent)",
            "pistol (primary weapon for corridor fighting)",
        ],
        "secondary_weapons": [
            "knife (fighting and utility)",
            "garrote (feud operations)",
            "acid vials (area denial)",
        ],
        "armor": [
            "autofactory alloy vest (local production, excellent quality)",
            "ceramic plates (Vesztraëlin terminal output)",
            "light armor (mobility in corridors)",
        ],
        "equipment": [
            "climbing gear (multi-level operations)",
            "communication whistle (complex codes)",
            "medical kit (radiation exposure treatment)",
            "house identification (friend-or-foe)",
        ],
        "personal_items": [
            "house genealogy card (proving membership)",
            "feud kill tally (house honor)",
            "radiation dosimeter (everyone carries one)",
            "antique from better times (house heirloom)",
        ],
        "condition": [
            "Equipment excellent—autofactory terminals provide",
            "Sized for Avouvar frames (smaller than baseline)",
            "Everything adapted from Warborn originals",
            "Maintained obsessively; equipment failure is death",
        ],
    },
    
    "avouvar_emplacement_crew": {
        "name": "Avouvar Railgun Crew",
        "polity": "Asovoë",
        "function": "Fixed emplacement operation",
        "primary_weapons": [
            "Warborn railgun (fixed mount, crew of three)",
        ],
        "secondary_weapons": [
            "pistol (backup)",
            "knife (always)",
            "nothing (the railgun is everything)",
        ],
        "armor": [
            "heavy vest (protects against debris)",
            "hearing protection (railgun discharge)",
            "gloves (capacitor handling)",
        ],
        "equipment": [
            "railgun maintenance kit",
            "capacitor test equipment",
            "ammunition inventory",
            "Droëvan terminal requisition forms",
        ],
        "personal_items": [
            "firing log (every shot recorded)",
            "crew photograph (you fight together, you die together)",
            "house commendation (if earned)",
            "targeting calculations (passed down through crews)",
        ],
        "condition": [
            "Personal equipment secondary to weapon system",
            "Railgun immaculate—house survival depends on it",
            "Capacitors tested daily",
            "Ammunition counted, recounted, counted again",
        ],
    },
    
    # =========================================================================
    # FRONTIER
    # =========================================================================
    "frontier_garrison": {
        "name": "Frontier Garrison Cavalry",
        "polity": "Imperial Frontier",
        "function": "Border patrol, estate defense",
        "primary_weapons": [
            "carbine (cavalry pattern, variable manufacture)",
            "rifle (inherited, Colonel-Hereditary armory)",
            "lance (ceremonial and functional)",
        ],
        "secondary_weapons": [
            "saber (estate standard)",
            "pistol (personal purchase)",
            "bow (for hunting, sometimes for war)",
        ],
        "armor": [
            "leather with metal reinforcement",
            "ceramic vest (if the Colonel-Hereditary provides)",
            "family armor (handed down)",
        ],
        "equipment": [
            "horse tack (estate supplied)",
            "patrol rations",
            "signal flares",
            "estate identification documents",
        ],
        "personal_items": [
            "payment record (estate scrip, partially redeemable)",
            "transfer request (everyone wants to transfer)",
            "local map (personal knowledge)",
            "Akama phrase book (practical necessity)",
        ],
        "condition": [
            "Equipment varies by Colonel-Hereditary wealth",
            "Maintained by garrison armorer (if there is one)",
            "Horse better cared for than soldier",
            "Everything shows the frontier—patched, adapted, adequate",
        ],
    },
}

# =============================================================================
# GENERATION FUNCTIONS
# =============================================================================

def generate_kit(soldier_type=None):
    """Generate a complete kit for a soldier type.
    
    Args:
        soldier_type: Specific type key, or None for random selection.
        
    Returns:
        Dictionary containing soldier information and equipment.
    """
    if soldier_type is None:
        soldier_type = random.choice(list(SOLDIER_KITS.keys()))
    
    if soldier_type not in SOLDIER_KITS:
        raise ValueError(f"Unknown soldier type: {soldier_type}")
    
    kit_template = SOLDIER_KITS[soldier_type]
    
    return {
        "type": soldier_type,
        "name": kit_template["name"],
        "polity": kit_template["polity"],
        "function": kit_template["function"],
        "primary_weapon": random.choice(kit_template["primary_weapons"]),
        "secondary_weapon": random.choice(kit_template["secondary_weapons"]),
        "armor": random.choice(kit_template["armor"]),
        "equipment": random.sample(kit_template["equipment"], 
                                   min(3, len(kit_template["equipment"]))),
        "personal_item": random.choice(kit_template["personal_items"]),
        "condition": random.choice(kit_template["condition"]),
    }


def generate_kit_formatted(soldier_type=None):
    """Generate a formatted kit description.
    
    Args:
        soldier_type: Specific type key, or None for random selection.
        
    Returns:
        Formatted string describing the kit.
    """
    kit = generate_kit(soldier_type)
    
    equipment_list = "\n".join(f"  - {item}" for item in kit["equipment"])
    
    return f"""**{kit['name']}** ({kit['polity']})
*Function: {kit['function']}*

Primary Weapon: {kit['primary_weapon']}
Secondary: {kit['secondary_weapon']}
Armor: {kit['armor']}

Equipment:
{equipment_list}

Personal: {kit['personal_item']}

Condition: {kit['condition']}"""


def list_soldier_types():
    """Return list of all soldier types organized by polity."""
    by_polity = {}
    for key, kit in SOLDIER_KITS.items():
        polity = kit["polity"]
        if polity not in by_polity:
            by_polity[polity] = []
        by_polity[polity].append((key, kit["name"]))
    return by_polity


def get_manufacturer_info(manufacturer_name, polity=None):
    """Get detailed information about a manufacturer.
    
    Args:
        manufacturer_name: Name of the manufacturer
        polity: Optional polity to search within
        
    Returns:
        Dictionary of manufacturer information, or None if not found.
    """
    search_polities = [polity] if polity else MANUFACTURERS.keys()
    
    for p in search_polities:
        if p in MANUFACTURERS:
            for name, info in MANUFACTURERS[p].items():
                if manufacturer_name.lower() in name.lower():
                    return {"name": name, "polity": p, **info}
    return None


def list_manufacturers():
    """Return all manufacturers organized by polity."""
    result = {}
    for polity, manufacturers in MANUFACTURERS.items():
        result[polity] = list(manufacturers.keys())
    return result


# =============================================================================
# MAIN - Command line interface
# =============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--list":
            print("SOLDIER TYPES BY POLITY:\n")
            for polity, types in list_soldier_types().items():
                print(f"{polity}:")
                for key, name in types:
                    print(f"  {key}: {name}")
                print()
        elif sys.argv[1] == "--manufacturers":
            print("MANUFACTURERS BY POLITY:\n")
            for polity, names in list_manufacturers().items():
                print(f"{polity.upper()}:")
                for name in names:
                    info = MANUFACTURERS[polity][name]
                    print(f"  {name}")
                    print(f"    Location: {info['location']}")
                    print(f"    Specialty: {info['specialty']}")
                    print(f"    Products: {', '.join(info['products'][:3])}...")
                print()
        elif sys.argv[1] == "--manufacturer" and len(sys.argv) > 2:
            name = " ".join(sys.argv[2:])
            info = get_manufacturer_info(name)
            if info:
                print(f"\n{info['name'].upper()} ({info['polity']})")
                print(f"Location: {info['location']}")
                print(f"Specialty: {info['specialty']}")
                print("\nProducts:")
                for product in info['products']:
                    print(f"  - {product}")
                print(f"\nNotes: {info['notes']}")
            else:
                print(f"Manufacturer '{name}' not found.")
        else:
            # Generate specific soldier type
            soldier_type = sys.argv[1]
            if soldier_type in SOLDIER_KITS:
                print(generate_kit_formatted(soldier_type))
            else:
                print(f"Unknown type: {soldier_type}")
                print("Use --list to see available types.")
    else:
        # Random soldier kit
        print("RANDOM SOLDIER KIT:\n")
        print(generate_kit_formatted())
        print("\n---")
        print("Usage:")
        print("  python soldier_kit_generator.py              # Random kit")
        print("  python soldier_kit_generator.py TYPE         # Specific type")
        print("  python soldier_kit_generator.py --list       # List all types")
        print("  python soldier_kit_generator.py --manufacturers  # List manufacturers")
        print("  python soldier_kit_generator.py --manufacturer NAME  # Manufacturer detail")

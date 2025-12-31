#!/usr/bin/env python3
"""
Name Generator for the Post-Interdict Empire

Generates names by region and class/type. Use for NPCs during play or to
pre-populate scenario documents with name stubs.

USAGE
=====
    name_generator.py <region> [options]
    name_generator.py stub <region> <type>    # Output a stub for later replacement
    name_generator.py fill <file>             # Replace all [NAME:...] stubs in file
    name_generator.py list                    # Show all regions and types

REGIONS
=======
    imperial    - Core Imperial territories, ya-Sattra, ya-Don
    tsatsan     - Ya-Tsatsa (Oracle cult city, Jargon-derived names)
    ganati      - Republic of Ganat (former Southwest)
    akama       - Thousand Kingdoms (Pacific Northwest interior)
    avouvar     - Asovoe / ya-Tsovez (far north, diacritical marks)

TYPES (vary by region)
======================
    Imperial:
        personal        - Given names only
        aureate         - Highborn with es- lineage
        bureau          - Bureau family names (-saren/-giren)
        professional    - Working class (-sīr, -ir)
        management      - Administrative families (-mar)
        lower           - Lower class (non-Imperial, detached suffix)
        clone           - Clone naming patterns
        homiletic       - Penitent Church liturgical names
    
    Tsatsan:
        personal        - Jargon-derived monosyllables
        aureate         - Local Aureate (Ezh marker)
        family          - Non-Aureate family names
        full            - Personal + family combined
    
    Ganati:
        personal        - Given names only
        unmarked        - Revolutionary default (no kilit marker)
        compound        - Old aristocracy (kilit-lineage compound)
        scaled          - Desert-adapted caste naming
    
    Akama:
        personal        - Personal name only (back-vowel default)
        malpais         - Traditional: personal + astrological (e.g., Khol Thirteen-Hawk)
        ogon            - Urban/warband: personal + epithet (e.g., Tsoka Red Deer)
        kmadhol         - Kma-Dhol: front-vowel personal + astrological
        astrological    - Astrological surname only (Number-Phase)
        epithet         - Epithet only (e.g., Stonefoot, Iron-Rain)
    
    Avouvar:
        personal        - Personal names with diacriticals (ë, ö, ż, sz)
        full            - Personal + precinct/house name
        precinct        - House/precinct name only

CANONICAL NAMES
===============
Some names are CANONICAL - they belong to established organizations or
characters and should not be randomly generated. Currently canonical:

    Sewer-fisher clans: Loak, Benru, Venn, Hasket, Sarn, Cho
    Hanged Men: Fen
    Aureate lineages: Ysalar, Lahun, Vadrin, Tariq, Ophar, Thabit, etc.
    Ganati leaders: Dhal-Setil, Khen-Masot, el-Marwen
    Tsatsan organizations: Yen Tam, Ma-Oro, Ezh Tan, Ahn-Tam
    Avouvar characters: Czenovaë, Teszvorath, Szëlvoram, Koratvel

Use glossary.py to look up canonical organizations before inventing new ones.

STUB FORMAT
===========
    [NAME:region:type]           - e.g., [NAME:imperial:lower]
    [NAME:region:type:gender]    - e.g., [NAME:imperial:personal:f]

EXAMPLES
========
    name_generator.py imperial lower
    name_generator.py imperial lower --count 5
    name_generator.py ganati unmarked --gender f
    name_generator.py stub imperial professional
    name_generator.py fill scenario.md
"""

import sys
import os
import re
import random
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict

# =============================================================================
# NAME DATA
# =============================================================================
# Extracted from Name_Generator_*.md files
# CANONICAL names (established organizations) are EXCLUDED from random generation

# Names that should NOT be randomly generated - they're canonical
CANONICAL_NAMES = {
    # Sewer-fisher clans (Middens organizations)
    'Loak', 'Benru', 'Venn', 'Hasket', 'Sarn', 'Cho',
    # Hanged Men family
    'Fen',
    
    # Aureate lineages (es- names from Satara and major houses)
    'Ysalar', 'Lahun', 'Vadrin', 'Tariq', 'Ophar', 'Thabit',
    'Tsays', 'Voren', 'Kiral', 'Orem', 'Morai',
    # These appear as es-X in Aureate names
    
    # Ganati canonical compound surnames (established characters)
    'Dhal-Setil', 'Khen-Masot', 'Khen-Toukh', 'el-Marwen',
    
    # Tsatsan canonical (established organizations)
    'Yen Tam', 'Ma-Oro', 'Ezh Tan', 'Ahn-Tam',
    
    # Avouvar canonical (established characters from Asovoe doc)
    'Czenovaë', 'Teszvorath', 'Szëlvoram', 'Koratvel', 'Völtrevan',
}

# -----------------------------------------------------------------------------
# IMPERIAL NAMES
# -----------------------------------------------------------------------------

IMPERIAL_PERSONAL = {
    # Patterns from Name_Generator_-_Imperial.md:
    # - Open ending (-a): liquid/nasal consonants + a
    # - Nasal ending (-an/-en): two syllables ending in nasal
    # - Liquid ending (-ar/-ir): two syllables ending in liquid
    # - Sibilant ending (-is/-es): two syllables ending in sibilant
    # - Vowel-initial: starts with vowel
    # - Monosyllabic: Keth, Vor pattern
    # - With -th-: distinctive Imperial sound
    
    'neutral': [
        # Canonical (from doc)
        'Keth', 'Vor', 'Iro', 'Orin', 'Isen', 'Evar', 'Amis', 'Calis', 'Miris',
        'Tene', 'Dima', 'Sahir', 'Varan', 'Kalen', 'Morai', 'Tariq', 'Ophar',
        'Aram', 'Omar', 'Peyor', 'Dorian', 'Thabit', 'Orath', 'Theron', 'Elin',
        'Ilar',
        # Vowel-initial additions
        'Avar', 'Orel', 'Emer', 'Elar', 'Uren', 'Alin', 'Oran',
        # Nasal ending (-an/-en)
        'Thoren', 'Dalen', 'Soren', 'Taren', 'Moren',
        # Liquid ending (-ir/-ar)  
        'Korir', 'Velar', 'Temir',
        # Sibilant ending (-is)
        'Teris', 'Velis', 'Koris',
        # With -th-
        'Kethar', 'Therin', 'Othar',
        # Monosyllabic
        'Kel', 'Thar', 'Ren', 'Sen',
    ],
    'f': [
        # Canonical (from doc) - mostly open endings (-a)
        'Lira', 'Avira', 'Sera', 'Kira', 'Vaida', 'Mena', 'Mira', 'Tara', 
        'Vela', 'Nora', 'Shera', 'Kasha', 'Vasha', 'Betha', 'Zoraya', 'Mesca',
        'Rila', 'Dessa', 'Yenna', 'Benna', 'Avra', 'Phen', 'Mara', 'Sela',
        # Open ending additions (following Lira/Sera/Kira pattern)
        'Thera', 'Kela', 'Dara', 'Ora', 'Reva', 'Tola', 'Vera', 'Sira',
        'Asha', 'Vora', 'Thela', 'Nira', 'Dena',
        # Vowel-initial (following Avira pattern)
        'Alira', 'Elira', 'Ovira', 'Anira', 'Emira',
        # With -th-
        'Thora', 'Ethira', 'Athena',
    ],
    'm': [
        # Canonical (from doc)
        'Ravi', 'Kori', 'Perseval', 'Kollis', 'Dorian',
        # From story vignettes and scenarios
        'Jarek', 'Garren', 'Luka', 'Torr', 'Pol', 'Tam', 'Cren', 'Kav', 'Rem',
        # Nasal ending (-an/-en, following Varan/Kalen)
        'Daren', 'Toren', 'Saven', 'Koren', 'Valen',
        # Liquid ending (following Sahir pattern)
        'Talir', 'Korir', 'Dalir',
        # With -th- (following Thabit pattern)
        'Thoren', 'Kethan', 'Othar',
        # Three-syllable (following Perseval/Dorian)
        'Korvian', 'Taloran', 'Seviran',
    ],
}

IMPERIAL_AUREATE_LINEAGES = [
    # Canonical lineages (Satara members, major houses) excluded:
    # Ysalar, Lahun, Vadrin, Tariq, Ophar, Thabit, Tsays, Voren, Kiral, Orem, Morai
    # 
    # Pattern analysis from canonical: two syllables, ending in -ar/-ir/-ath/-al/-un/-em
    # Etaie is unusual (three syllables, -ie ending)
    
    # From doc (non-Satara)
    'Etaie', 'Vorath', 'Vorel', 'Andrel', 'Verlaus', 'Kelthen',
    # -ath endings (like Vorath)
    'Kelath', 'Serrath', 'Torrath', 'Delath', 'Morrath',
    # -ar/-ir endings (like Kiral but not Kiral itself)
    'Velar', 'Selir', 'Korar', 'Themir', 'Dalir',
    # -al/-el endings (like Vorel)
    'Torel', 'Senal', 'Korel', 'Thelal', 'Daral',
    # -un/-en endings (like Lahun but not Lahun itself)
    'Velun', 'Koren', 'Theren', 'Selun', 'Doren',
    # -em/-im endings (like Orem but not Orem itself)
    'Velem', 'Serim', 'Kolem', 'Therim',
]

IMPERIAL_BUREAU_FAMILIES = [
    'Taasaren', 'Sharsaren', 'Pelamsaren', 'Orathsaren', 'Themalsaren', 
    'Varemgiren', 'Kengiren', 'Kelasaren', 'Thevaren', 'Morasaren',
]

IMPERIAL_PROFESSIONAL_FULL = [
    # Pattern: [root]-da-sīr or [root]-sīr (respectable working class)
    # From doc: Vordasīr (dock), Kemdasīr (mine), Masdasīr (mason), Talessīr (assessor)
    'Vordasīr', 'Kemdasīr', 'Masdasīr', 'Talessīr',
    # Additions following pattern (root + -dasīr)
    'Teldasīr', 'Kordasīr', 'Seldasīr', 'Mordasīr', 'Veldasīr',
    'Thelasīr', 'Kelasīr', 'Serasīr', 'Torasīr',
]

IMPERIAL_PROFESSIONAL_REDUCED = [
    # Pattern: [root]-ir (reduced form, common)
    # From doc: Sahir, Talir, Dalir, Kelir
    'Sahir', 'Talir', 'Kelir', 'Dalir',
    # Additions following pattern
    'Thevir', 'Morir', 'Selair', 'Korir', 'Velir', 'Torir', 
    'Senir', 'Kalir', 'Dorir', 'Temir', 'Varir', 'Thenir',
]

IMPERIAL_MANAGEMENT = [
    'Donmar', 'Velmar', 'Adelmar', 'Delmar', 'Kevelmar', 'Tavelmar',
    'Kelmar', 'Thevamar', 'Selamar',
]

IMPERIAL_ARCHAIC = [
    'Imeten', 'Brennam', 'Orath',
]

# Lower class - excluding canonical names (Loak, Benru, Venn, Hasket, Sarn, Cho, Fen)
# These explicitly DON'T follow Imperial phonology - absorbed populations, rougher sounds

IMPERIAL_LOWER_NONIMPERIAL = [
    # Canonical patterns: Hasket, Loak, Brend, Ostir, Kavven, Polm, Thurrick
    # Can have consonant clusters, different vowel patterns, feel "rougher"
    'Brend', 'Ostir', 'Kavven', 'Polm', 'Thurrick', 'Tisker', 'Osley',
    'Durren', 'Ritt', 'Marsh',
    # Additions following these patterns (consonant clusters, -ck/-sk endings, etc.)
    'Grenn', 'Stovak', 'Bremm', 'Korst', 'Drask', 'Tolvak', 'Krennik',
    'Gresh', 'Vosker', 'Dremm', 'Storn', 'Brekk', 'Thorvik', 'Galsk',
]

IMPERIAL_LOWER_DETACHED = [
    # Single-syllable affixes that were once attached to personal names
    # Pattern: monosyllabic, simple sounds
    # Canonical excluded: Venn, Cho, Fen
    'Kar', 'Pol', 'Eth', 'Ren', 'Thos', 'Tal', 'Vor', 'Ket',
    # Additions (monosyllabic, simple)
    'Vel', 'Kem', 'Sar', 'Dol', 'Ter', 'Kol', 'Sen', 'Mer', 'Bren', 'Tol',
]

IMPERIAL_LOWER_TRUNCATED = [
    # Truncated from -dasīr/-masīr forms
    # Pattern: [root]-dal or [root]-mal
    'Vordal', 'Kemdal', 'Masdal',
    # Additions following the truncation pattern
    'Teldal', 'Seldal', 'Theldal', 'Kordal', 'Mordal', 'Vendal',
    'Telmal', 'Selmal', 'Kormal', 'Morval', 'Thormal',
]

# Homiletic (Penitent Church) name components
IMPERIAL_HOMILETIC_VIRTUE = [
    'Common-Task', 'Burden-Bearer', 'Faithful-Labor', 'Steadfast-Hand',
    'Patient-Service', 'Quiet-Duty', 'Simple-Faith',
]

IMPERIAL_HOMILETIC_ASPIRATION = [
    'Gates-of-Heaven', 'Dawn-of-Ascension', 'Light-Before-Dawn',
    'Road-of-Mercy', 'Wheel-and-Way',
]

IMPERIAL_HOMILETIC_PENITENTIAL = [
    'Ashes-of-Pride', 'Weight-of-Error', 'Memory-of-Fault',
    'Foundation-Stones',
]

IMPERIAL_HOMILETIC_LABOR = [
    'Fire-Keeper', 'Forge-Tender', 'Iron-Shaper', 'Coal-Bearer',
]

# -----------------------------------------------------------------------------
# TSATSAN NAMES (Ya-Tsatsa, Jargon-derived)
# Monosyllabic elements from doc: An, Bei, Beb, Mir, Tam, Dho, Fen, Gat, Kho, 
# Neb, Ol, Pek, Tok, Yen, Zho
# These do NOT mix with Imperial morphology
# -----------------------------------------------------------------------------

TSATSAN_ELEMENTS = [
    'An', 'Bei', 'Beb', 'Mir', 'Tam', 'Dho', 'Gat', 'Kho', 'Neb', 
    'Ol', 'Pek', 'Tok', 'Zho', 'Vel', 'Kee', 'To', 'Fen',
]

# Local Tsatsan Aureate families (Ezh marker)
TSATSAN_AUREATE_NAMES = ['Tan', 'Ot', 'Dhol', 'Ghen', 'Khel']

# Non-Aureate family patterns (two-element or hyphenated)
# Canonical excluded: Yen Tam, Ma-Oro, Ahn-Tam
TSATSAN_FAMILIES = [
    ('Gat', 'Neb'), ('Kho', 'Tam'), ('Mir', 'Kee'), ('Beb', 'Kee'), 
    ('Tam', 'Vel'), ('Dho', 'Tam'), ('Pek', 'Vel'), ('Tok', 'Bei'),
    ('Zho', 'Kee'), ('Neb', 'Vel'), ('Ol', 'Tam'), ('Bei', 'Kho'),
]

# Canonical Tsatsan names (from Ya-Tsatsa doc) - established characters
TSATSAN_CANONICAL = {
    'Yen Tam',  # Beneficial Society
    'Ma-Oro',   # Criminal operations  
    'Ezh Tan',  # Major Aureate family
    'Ahn-Tam',  # Tomb carvers
}

# -----------------------------------------------------------------------------
# GANATI NAMES
# -----------------------------------------------------------------------------

GANATI_GIVEN_STARTERS = [
    'You', 'Tse', 'Khe', 'Gha', 'Lho', 'Ma', 'Na', 'Da', 'Sa', 'Ta',
    'Fa', 'Ka', 'Ba', 'Ra', 'Wa', 'Ya', 'Ou', 'El', 'Al',
]

GANATI_GIVEN_COMPLETIONS = [
    'la', 'li', 'lu', 'na', 'ni', 'ra', 'ri', 'sa', 'si', 'ta', 'ti',
    'ma', 'mi', 'ka', 'ki', 'ba', 'bi', 'da', 'di', 'fa', 'fi',
    'ssa', 'kka', 'tta', 'mma', 'nna', 'lla',  # geminated
]

GANATI_KILIT_MARKERS = [
    'Dhal', 'Khen', 'Tsel', 'Ghou', 'Masot', 'Elou', 'Kheri', 'Tsefa',
]

GANATI_LINEAGE_ENDINGS = [
    'oun', 'akh', 'eikh', 'oum', 'alh', 'ets', 'our',
]

GANATI_LINEAGES = [
    'Masot', 'Kheroun', 'Tselakh', 'Ghoueikh', 'Dhaloun', 'Eloum',
    'Youmalh', 'Kheriets', 'Tsefour', 'Setil', 'Toukh', 'Omir', 
    'Kemari', 'Beleikh', 'Ghaloun',
]

# -----------------------------------------------------------------------------
# AKAMA NAMES (Thousand Kingdoms)
# Tibetan/Turkic/Mayan influenced. Vowel harmony (back: a,o,u OR front: e,i)
# Harsh, throat-focused sound. Consonant clusters: ts-, kh-, gh-, dh-, br-
# -----------------------------------------------------------------------------

# Back-vowel personal names (standard Akama pattern)
AKAMA_BACK_MONO = ['Som', 'Gan', 'Khol', 'Tam', 'Ghor', 'Dhal', 'Bron', 'Krom', 'Vur', 'Tsang', 'Drok', 'Khur', 'Tsom']
AKAMA_BACK_DI = ['Tsoka', 'Ataru', 'Ghom', 'Gorin', 'Koram', 'Torakh', 'Dulang', 'Tsamar', 'Dharam', 'Ghulom', 'Bortam', 'Dhalang', 'Kromakh']
AKAMA_BACK_TRI = ['Buragh', 'Khoram', 'Tsalkor', 'Dharung', 'Ghulang', 'Bromakh', 'Tsamarak', 'Ghorunal', 'Khalomur']

# Front-vowel personal names (Kma-Dhol/regional pattern)
AKAMA_FRONT_MONO = ['Vey', 'Sev', 'Khen', 'Tsen', 'Drel', 'Ghel', 'Brek', 'Khel']
AKAMA_FRONT_DI = ['Imek', 'Sevek', 'Dherim', 'Kelim', 'Tselek', 'Gherim', 'Vremin', 'Drelikh']
AKAMA_FRONT_TRI = ['Kherzen', 'Tselker', 'Gherimel', 'Breshen', 'Dherikhen', 'Tselekim']

# Phase elements for astrological names (Number + Phase)
AKAMA_PHASE_ANIMALS = ['Hawk', 'Bear', 'Elk', 'Salmon', 'Deer', 'Blackfish', 'Owl', 'Raven', 'Wolf', 'Otter', 'Hare', 'Serpent', 'Toad', 'Eagle', 'Crane', 'Birds']
AKAMA_PHASE_DESTRIERS = ['Gnasher', 'Trills', 'Coralhorn', 'Blackeye']
AKAMA_PHASE_PLANTS = ['Reed', 'Yarrow', 'Cedar', 'Sage', 'Willow', 'Thornbush', 'Bunchgrass', 'Root', 'Pine', 'Moss']
AKAMA_PHASE_PHENOMENA = ['Wind', 'Stone', 'Rain', 'Thunder', 'Frost', 'Ember', 'Ash', 'Smoke', 'Cloud', 'Star', 'River', 'Snow']
AKAMA_NUMBERS = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen']

# Epithet components - organized by generative pattern
# AVOID: agent nouns (-er), fantasy tropes (-Touched), job descriptions
# PREFER: past tense, ongoing states, specific moments, implied stories

# Physical markers (distinctive features, injuries - simple folk terms, not clinical)
# Remember: Akama phenotype is different. No big noses. Crude/direct naming.
AKAMA_EPITHET_PHYSICAL = [
    'Long-Arm', 'Harelip', 'Three-Finger', 'Burnt-Face', 'White-Hair',
    'Cutthroat', 'One-Eye', 'Bent-Back', 'No-Ear', 'Bleeder', 'Pox-Face',
    'Club-Foot', 'Hunchback', 'Squint', 'Limp-Wrist',
]

# Misfortune epithets (conditions that limit/define - simple, often cruel)
AKAMA_EPITHET_MISFORTUNE = [
    'Toothless', 'Half-Hand', 'Falls-Twice', 'The Eunuch', 'Limps',
    'Stone-Deaf', 'Blind', 'Shakes', 'Mute', 'Simpleton', 'Drools',
]

# Survival markers (the point is they lived - past tense, states)
AKAMA_EPITHET_SURVIVAL = [
    'Left-Behind', 'Ransomed-Cheap', 'Kindling', 'Came-Back', 'Still-Standing',
    'Twice-Buried', 'Unkilled', 'Sold-Young', 'Walked-Out-Burning',
    'Starved-Out', 'Ate-the-Horses', 'Drank-the-Sea-Water', 'Crawled-Home',
]

# Deed-based (implies a specific story - past tense preferred)
AKAMA_EPITHET_DEED = [
    'Burnt-the-Bridge', 'Held-the-Gate', 'Broke-the-Truce', 'Horse-Thief',
    'Salted-the-Well', 'Killed-His-Captain', 'Took-the-Flag', 'Paid-in-Blood',
    'Opened-the-Gate', 'Fed-Them-to-Dogs',
]

# Behavioral (how they consistently act - present tense patterns)
AKAMA_EPITHET_BEHAVIORAL = [
    'Never-Runs', 'Speaks-Little', 'Eats-Last', 'Laughs-Bleeding', 'Sleeps-Light',
    'Counts-Fingers', 'Walks-Alone', 'Shares-Nothing', 'Forgives-None', 
    'Waits-Too-Long', 'Hits-First', 'Asks-Twice',
]

# Contested/ironic (meaning depends on who speaks it and how)
AKAMA_EPITHET_CONTESTED = [
    'First-Strike', 'Captain-Killer', 'Giant-Feller', 'Hero-of-the-Retreat',
    'Last-to-Fight', 'Found-the-Banner', 'Volunteer', 'The-Brave-One',
]

# Circumstantial (what happened to/around them - origin moments, mundane tragedy)
AKAMA_EPITHET_CIRCUMSTANTIAL = [
    'Born-in-Snow', 'River-Found', 'Storm-Child', 'Night-Came', 'Star-Fell', 
    'Wolves-Passed', 'Mother-Died', 'Father-Unknown', 'Doorstep',
    'Stillborn', 'Wrong-Twin', 'Seventh-Son',
]

# Animal-connection (relationship/omen - events, not abilities or marks)
AKAMA_EPITHET_ANIMAL = [
    'Crows-Follow-Him', 'Crows-Follow-Her', 'Wolf-Fed', 'Bear-Took-His-Eye',
    'Serpent-Bit', 'Wolves-Let-Him-Pass', 'Dogs-Wont-Bite-Her',
    'Horse-Threw-Him', 'Thrown-Thrice', 'Hawk-Circled', 'Owl-Called',
    'Found-with-Wolves', 'Elk-Gored',
]

# Elemental (metaphorical - what they bring, atmospheric)
AKAMA_EPITHET_ELEMENTAL = [
    'Iron-Rain', 'Thunder-Voice', 'Smoke-Behind-Him', 'Brings-the-Frost',
    'Dust-and-Ashes', 'Cold-Wind', 'Dry-River', 'Black-Sky',
]

# Simple color + animal (traditional omen-based - kept but used sparingly)
AKAMA_EPITHET_COLORS = ['Red', 'Black', 'Grey', 'White', 'Pale']
AKAMA_EPITHET_OMEN_ANIMALS = ['Deer', 'Wolf', 'Crane', 'Hawk', 'Elk', 'Owl']

# Material + body (physical quality metaphor)
AKAMA_EPITHET_MATERIALS = ['Stone', 'Iron', 'Bone', 'Salt', 'Ice', 'Oak']
AKAMA_EPITHET_BODY = ['foot', 'Hand', 'Back', 'Heart', 'Jaw', 'Spine']

# Canonical Akama names (from docs)
AKAMA_CANONICAL = {
    'Tsoka Red Deer',  # Junta member
    'Khol Thirteen-Hawk',
    'Vey Nine Birds',
    'Iron-Rain',  # warband leader
    'Imek Stonefoot',
}

# -----------------------------------------------------------------------------
# AVOUVAR NAMES (Asovoe, ya-Tsovez)
# Distinctive diacritical marks: ë, ö, ż, sz, cz
# Structure: [personal name] [precinct/house name]
# Children unnamed until Anointing at 13 (or 30 for Lavoëran)
# -----------------------------------------------------------------------------

AVOUVAR_PRECINCTS = [
    # Major house/precinct names - some are canonical (established characters)
    'Vroëszka', 'Sztoavel', 'Czernaël', 'Kolaëvin', 'Żelovin', 
    'Lavoëran', 'Kraëlosz', 'Vesztraëlin', 'Droëvan', 'Dravoëtsin',
]

# Personal name components - can combine
AVOUVAR_NAME_STARTS = [
    'Czen', 'Tesz', 'Szël', 'Kor', 'Drav', 'Völ', 'Kol', 'Vel', 'Sztr',
    'Lav', 'Kra', 'Vesz', 'Dro', 'Żel', 'Czern', 'Szt', 'Vör', 'Tël',
]

AVOUVAR_NAME_ENDS = [
    'ovaë', 'vorath', 'voram', 'atvel', 'ötsz', 'trevan', 'tvel',
    'ëvan', 'ovel', 'aël', 'evin', 'ëran', 'ëlosz', 'aëlin', 'ëtsin',
    'ovan', 'avel', 'ëszka', 'orath', 'ëvon', 'atsch', 'ëvel',
]

# Canonical Avouvar names (established characters from Asovoe doc)
AVOUVAR_CANONICAL = {
    'Czenovaë Vroëszka',     # theologian matriarch
    'Teszvorath Kolaëvin',   # absolutist patriarch
    'Szëlvoram Żelovin',     # Witness-Paramount
    'Koratvel Lavoëran',     # the Chancellor
    'Völtrevan',             # Witness (461 years old)
}


# =============================================================================
# GENERATION FUNCTIONS
# =============================================================================

def pick(lst: List[str], exclude: set = None) -> str:
    """Pick a random item, optionally excluding canonical names."""
    if exclude is None:
        exclude = CANONICAL_NAMES
    available = [x for x in lst if x not in exclude]
    if not available:
        available = lst  # Fallback if all are canonical
    return random.choice(available)


def generate_imperial_personal(gender: str = None) -> str:
    """Generate an Imperial personal name."""
    if gender == 'f':
        return pick(IMPERIAL_PERSONAL['f'])
    elif gender == 'm':
        return pick(IMPERIAL_PERSONAL['m'])
    else:
        # Mix of all
        all_names = (IMPERIAL_PERSONAL['neutral'] + 
                     IMPERIAL_PERSONAL['f'] + 
                     IMPERIAL_PERSONAL['m'])
        return pick(all_names)


def generate_imperial_aureate(gender: str = None) -> str:
    """Generate an Aureate name with es- lineage."""
    personal = generate_imperial_personal(gender)
    lineage = pick(IMPERIAL_AUREATE_LINEAGES)
    return f"{personal} es-{lineage}"


def generate_imperial_bureau(gender: str = None) -> str:
    """Generate a Bureau family name."""
    personal = generate_imperial_personal(gender)
    family = pick(IMPERIAL_BUREAU_FAMILIES)
    return f"{personal} {family}"


def generate_imperial_professional(gender: str = None) -> str:
    """Generate a professional-class name."""
    personal = generate_imperial_personal(gender)
    if random.random() < 0.4:
        family = pick(IMPERIAL_PROFESSIONAL_FULL)
    else:
        family = pick(IMPERIAL_PROFESSIONAL_REDUCED)
    return f"{personal} {family}"


def generate_imperial_management(gender: str = None) -> str:
    """Generate a management-class name."""
    personal = generate_imperial_personal(gender)
    family = pick(IMPERIAL_MANAGEMENT)
    return f"{personal} {family}"


def generate_imperial_lower(gender: str = None) -> str:
    """Generate a lower-class name."""
    personal = generate_imperial_personal(gender)
    roll = random.random()
    if roll < 0.4:
        family = pick(IMPERIAL_LOWER_NONIMPERIAL)
    elif roll < 0.7:
        family = pick(IMPERIAL_LOWER_DETACHED)
    else:
        family = pick(IMPERIAL_LOWER_TRUNCATED)
    return f"{personal} {family}"


def generate_imperial_clone() -> str:
    """Generate a clone name."""
    roll = random.random()
    if roll < 0.5:
        # Personal + cloneline
        personal = pick(IMPERIAL_PERSONAL['neutral'])
        cloneline = pick(IMPERIAL_LOWER_DETACHED)
        return f"{personal} {cloneline}"
    else:
        # Batch + number
        batch = pick(IMPERIAL_PERSONAL['neutral']) + pick(['eth', 'al', 'ov', 'im', 'an'])
        number = random.randint(1, 12)
        return f"{batch}-{number}"


def generate_imperial_homiletic(gender: str = None) -> str:
    """Generate a Penitent Church homiletic name."""
    roll = random.random()
    if roll < 0.3:
        homiletic = pick(IMPERIAL_HOMILETIC_VIRTUE)
    elif roll < 0.5:
        homiletic = pick(IMPERIAL_HOMILETIC_ASPIRATION)
    elif roll < 0.7:
        homiletic = pick(IMPERIAL_HOMILETIC_PENITENTIAL)
    else:
        homiletic = pick(IMPERIAL_HOMILETIC_LABOR)
    
    # Sometimes add a family name
    if random.random() < 0.5:
        family = pick(IMPERIAL_BUREAU_FAMILIES + IMPERIAL_ARCHAIC)
        return f"{homiletic} {family}"
    return homiletic


def generate_tsatsan_personal() -> str:
    """Generate a Tsatsan personal name (Jargon-derived monosyllables)."""
    # Can be single element or multi-element
    if random.random() < 0.7:
        return pick(TSATSAN_ELEMENTS)
    else:
        # Two-element personal name
        return f"{pick(TSATSAN_ELEMENTS)} {pick(TSATSAN_ELEMENTS)}"


def generate_tsatsan_aureate() -> str:
    """Generate a Tsatsan Aureate name (Ezh marker)."""
    personal = generate_tsatsan_personal()
    house = pick(TSATSAN_AUREATE_NAMES)
    # Tsatsan uses family-first ordering locally
    return f"Ezh {house} {personal}"


def generate_tsatsan_family() -> str:
    """Generate a Tsatsan non-Aureate family name."""
    pair = random.choice(TSATSAN_FAMILIES)
    if random.random() < 0.3:
        return f"{pair[0]}-{pair[1]}"
    else:
        return f"{pair[0]} {pair[1]}"


def generate_tsatsan_full() -> str:
    """Generate a full Tsatsan name (personal + family)."""
    personal = generate_tsatsan_personal()
    family = generate_tsatsan_family()
    return f"{personal} {family}"


def generate_ganati_personal(gender: str = None) -> str:
    """Generate a Ganati given name."""
    starter = pick(GANATI_GIVEN_STARTERS)
    completion = pick(GANATI_GIVEN_COMPLETIONS)
    return starter + completion


def generate_ganati_unmarked(gender: str = None) -> str:
    """Generate an unmarked (revolutionary default) Ganati name."""
    personal = generate_ganati_personal(gender)
    lineage = pick(GANATI_LINEAGES)
    return f"{personal} {lineage}"


def generate_ganati_compound(gender: str = None) -> str:
    """Generate a compound (old aristocracy) Ganati name."""
    personal = generate_ganati_personal(gender)
    
    # Try up to 10 times to avoid canonical compound surnames
    for _ in range(10):
        kilit = pick(GANATI_KILIT_MARKERS)
        lineage = pick(GANATI_LINEAGES)
        compound = f"{kilit}-{lineage}"
        if compound not in CANONICAL_NAMES:
            return f"{personal} {compound}"
    
    # Fallback: just use what we got
    return f"{personal} {kilit}-{lineage}"


def generate_ganati_scaled(gender: str = None) -> str:
    """Generate a scaled-caste Ganati name."""
    # Scaled castes often use simpler, shorter names
    personal = generate_ganati_personal(gender)
    # Lineage might be abbreviated
    lineage = pick(GANATI_LINEAGES)
    if random.random() < 0.5:
        lineage = lineage[:4]  # Truncate
    return f"{personal} {lineage}"


def generate_akama_personal(front_vowel: bool = False) -> str:
    """Generate an Akama personal name.
    
    Args:
        front_vowel: If True, use Kma-Dhol/regional front-vowel pattern (e, i).
                     If False (default), use standard back-vowel pattern (a, o, u).
    """
    if front_vowel:
        # Front-vowel (Kma-Dhol) pattern
        pools = [AKAMA_FRONT_MONO, AKAMA_FRONT_DI, AKAMA_FRONT_TRI]
    else:
        # Back-vowel (standard) pattern
        pools = [AKAMA_BACK_MONO, AKAMA_BACK_DI, AKAMA_BACK_TRI]
    
    # Weight toward disyllabic (most common)
    weights = [0.25, 0.55, 0.20]
    pool = random.choices(pools, weights=weights)[0]
    return pick(pool)


def generate_akama_astrological() -> str:
    """Generate an Akama astrological surname (Number + Phase Element)."""
    number = random.choice(AKAMA_NUMBERS)
    # Weight toward animals (most common)
    phase_pools = [
        (AKAMA_PHASE_ANIMALS, 0.5),
        (AKAMA_PHASE_PHENOMENA, 0.25),
        (AKAMA_PHASE_PLANTS, 0.15),
        (AKAMA_PHASE_DESTRIERS, 0.10),
    ]
    pool = random.choices([p[0] for p in phase_pools], weights=[p[1] for p in phase_pools])[0]
    phase = random.choice(pool)
    return f"{number}-{phase}"


def generate_akama_epithet_only() -> str:
    """Generate an Akama epithet (without personal name).
    
    Draws from multiple categories:
    - Physical markers (states, not descriptions)
    - Misfortune (injuries/lacks that define)
    - Survival (the point is they lived)
    - Deed-based (implies a story)
    - Behavioral (how they act)
    - Contested/ironic (meaning depends on speaker)
    - Circumstantial (origin moments)
    - Animal-connection (omens, not abilities)
    - Elemental (metaphorical/atmospheric)
    - Color + Animal (traditional, sparingly)
    - Material + Body (physical metaphor)
    """
    # Weight different categories
    categories = [
        (AKAMA_EPITHET_SURVIVAL, 0.15),      # "Ate-the-Horses"
        (AKAMA_EPITHET_DEED, 0.15),          # "Burnt-the-Bridge"
        (AKAMA_EPITHET_MISFORTUNE, 0.12),    # "Toothless"
        (AKAMA_EPITHET_BEHAVIORAL, 0.12),    # "Never-Runs"
        (AKAMA_EPITHET_PHYSICAL, 0.10),      # "Three-Finger"
        (AKAMA_EPITHET_ANIMAL, 0.10),        # "Crows-Follow-Him"
        (AKAMA_EPITHET_CONTESTED, 0.08),     # "Hero-of-the-Retreat"
        (AKAMA_EPITHET_CIRCUMSTANTIAL, 0.08),# "Born-in-Snow"
        (AKAMA_EPITHET_ELEMENTAL, 0.05),     # "Iron-Rain"
        (None, 0.05),  # Material + Body compound
    ]
    
    pools = [c[0] for c in categories]
    weights = [c[1] for c in categories]
    
    selected_pool = random.choices(pools, weights=weights)[0]
    
    if selected_pool is None:
        # Material + Body compound
        material = random.choice(AKAMA_EPITHET_MATERIALS)
        body = random.choice(AKAMA_EPITHET_BODY)
        if body[0].isupper():
            return f"{material}-{body}"
        else:
            return f"{material}{body}"
    else:
        return random.choice(selected_pool)


def generate_akama_malpais() -> str:
    """Generate a traditional Malpais name (personal + astrological surname)."""
    personal = generate_akama_personal(front_vowel=False)
    astro = generate_akama_astrological()
    return f"{personal} {astro}"


def generate_akama_ogon() -> str:
    """Generate an urban Ogon/warband name (personal + epithet)."""
    personal = generate_akama_personal(front_vowel=False)
    epithet = generate_akama_epithet_only()
    return f"{personal} {epithet}"


def generate_akama_kmadhol() -> str:
    """Generate a Kma-Dhol name (front-vowel personal + astrological)."""
    personal = generate_akama_personal(front_vowel=True)
    astro = generate_akama_astrological()
    return f"{personal} {astro}"


def generate_avouvar_personal() -> str:
    """Generate an Avouvar personal name."""
    # Combine start and end components
    # Avoid canonical names
    for _ in range(10):
        start = pick(AVOUVAR_NAME_STARTS)
        end = pick(AVOUVAR_NAME_ENDS)
        name = start + end
        if name not in CANONICAL_NAMES:
            return name
    return name


def generate_avouvar_full() -> str:
    """Generate a full Avouvar name (personal + precinct)."""
    personal = generate_avouvar_personal()
    precinct = pick(AVOUVAR_PRECINCTS)
    return f"{personal} {precinct}"


def generate_avouvar_precinct() -> str:
    """Generate just a precinct/house name (for references)."""
    return pick(AVOUVAR_PRECINCTS)


# =============================================================================
# MAIN INTERFACE
# =============================================================================

GENERATORS = {
    'imperial': {
        'personal': generate_imperial_personal,
        'aureate': generate_imperial_aureate,
        'bureau': generate_imperial_bureau,
        'professional': generate_imperial_professional,
        'management': generate_imperial_management,
        'lower': generate_imperial_lower,
        'clone': generate_imperial_clone,
        'homiletic': generate_imperial_homiletic,
    },
    'tsatsan': {
        'personal': generate_tsatsan_personal,
        'aureate': generate_tsatsan_aureate,
        'family': generate_tsatsan_family,
        'full': generate_tsatsan_full,
    },
    'ganati': {
        'personal': generate_ganati_personal,
        'unmarked': generate_ganati_unmarked,
        'compound': generate_ganati_compound,
        'scaled': generate_ganati_scaled,
    },
    'akama': {
        'personal': generate_akama_personal,
        'malpais': generate_akama_malpais,
        'ogon': generate_akama_ogon,
        'kmadhol': generate_akama_kmadhol,
        'astrological': generate_akama_astrological,
        'epithet': generate_akama_epithet_only,
    },
    'avouvar': {
        'personal': generate_avouvar_personal,
        'full': generate_avouvar_full,
        'precinct': generate_avouvar_precinct,
    },
}


def generate_name(region: str, name_type: str, gender: str = None) -> str:
    """Generate a name for the given region and type."""
    region = region.lower()
    name_type = name_type.lower()
    
    if region not in GENERATORS:
        raise ValueError(f"Unknown region: {region}. Use: {', '.join(GENERATORS.keys())}")
    
    if name_type not in GENERATORS[region]:
        types = ', '.join(GENERATORS[region].keys())
        raise ValueError(f"Unknown type for {region}: {name_type}. Use: {types}")
    
    gen_func = GENERATORS[region][name_type]
    
    # Check if generator accepts gender
    import inspect
    sig = inspect.signature(gen_func)
    if 'gender' in sig.parameters:
        return gen_func(gender=gender)
    return gen_func()


def make_stub(region: str, name_type: str, gender: str = None) -> str:
    """Create a stub string for later replacement."""
    if gender:
        return f"[NAME:{region}:{name_type}:{gender}]"
    return f"[NAME:{region}:{name_type}]"


def fill_stubs(text: str) -> str:
    """Replace all [NAME:...] stubs in text with generated names."""
    pattern = r'\[NAME:([a-z]+):([a-z]+)(?::([mf]))?\]'
    
    def replace(match):
        region = match.group(1)
        name_type = match.group(2)
        gender = match.group(3)
        try:
            return generate_name(region, name_type, gender)
        except ValueError as e:
            return f"[ERROR: {e}]"
    
    return re.sub(pattern, replace, text, flags=re.IGNORECASE)


def fill_file(filepath: str) -> None:
    """Replace all stubs in a file."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Count stubs
    pattern = r'\[NAME:[^\]]+\]'
    stubs = re.findall(pattern, content)
    
    if not stubs:
        print(f"No [NAME:...] stubs found in {filepath}")
        return
    
    filled = fill_stubs(content)
    
    with open(filepath, 'w') as f:
        f.write(filled)
    
    print(f"Replaced {len(stubs)} name stubs in {filepath}")


def list_all():
    """List all available regions and types."""
    print("\nAVAILABLE NAME GENERATORS")
    print("=" * 50)
    for region, types in GENERATORS.items():
        print(f"\n{region.upper()}")
        for name_type in types:
            print(f"  {name_type}")
    
    print("\n\nCANONICAL NAMES (excluded from generation)")
    print("=" * 50)
    print("These names belong to established organizations.")
    print("Look them up in glossary.py before using:")
    for name in sorted(CANONICAL_NAMES):
        print(f"  {name}")


def main():
    args = sys.argv[1:]
    
    if not args or '-h' in args or '--help' in args:
        print(__doc__)
        return
    
    if args[0] == 'list':
        list_all()
        return
    
    if args[0] == 'stub':
        if len(args) < 3:
            print("Usage: name_generator.py stub <region> <type> [gender]")
            return
        region = args[1]
        name_type = args[2]
        gender = args[3] if len(args) > 3 else None
        print(make_stub(region, name_type, gender))
        return
    
    if args[0] == 'fill':
        if len(args) < 2:
            print("Usage: name_generator.py fill <file>")
            return
        fill_file(args[1])
        return
    
    # Default: generate name
    region = args[0]
    name_type = args[1] if len(args) > 1 else 'personal'
    
    # Parse options
    count = 1
    gender = None
    
    i = 2
    while i < len(args):
        if args[i] == '--count' and i + 1 < len(args):
            count = int(args[i + 1])
            i += 2
        elif args[i] == '--gender' and i + 1 < len(args):
            gender = args[i + 1]
            i += 2
        elif args[i] in ('m', 'f'):
            gender = args[i]
            i += 1
        else:
            i += 1
    
    try:
        for _ in range(count):
            print(generate_name(region, name_type, gender))
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

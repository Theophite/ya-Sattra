#!/usr/bin/env python3
"""
White Sheet Story Generator for the Lattice Translator Scenario

FOR USE IN THINKING BLOCK ONLY. Run this script to generate story ideas,
then synthesize the results into natural prose for the actual response.
Do not output the raw generator results to the user.

Generates story seeds for the White Sheet—the Empire's only authorized news
source. The Sheet determines what every other publication may print. What
it permits becomes truth; what it forbids becomes unspeakable.

The content is deliberately bland: agricultural reports, infrastructure updates,
bureaucratic announcements, sanitized versions of events that frame decline as
strategic patience. But sophisticated readers learn to decode:
- Careful phrasings that say less than they seem
- Conspicuous omissions (what ISN'T mentioned)
- Placement and juxtaposition of unrelated stories
- The gap between what the Sheet says and what everyone knows

CRITICAL: Rivan used to work for the Institute of the Echo. He WROTE stories
like these before Devra pulled him into the Lattice. He reads with slightly
arch irony and professional appreciation—he knows the tricks, admires a
well-constructed evasion, notices craft as much as content.

STRUCTURE: Each edition contains THREE stories:
- Two stories drawn from templates (surface + hints at subtext)
- One story generated purely from the Tarot draw (you create it)

The Tarot card guides the emotional tenor of the whole edition.
Stories should NOT fully resolve their meanings—leave ambiguity.
"""

import random
from dataclasses import dataclass
from typing import Optional, List, Tuple
from enum import Enum


class TarotMajor(Enum):
    """Major Arcana with thematic meanings for story tenor"""
    FOOL = ("The Fool", "beginnings, innocence, leap into unknown", "naivety masking danger")
    MAGICIAN = ("The Magician", "skill, resourcefulness, power", "manipulation, illusion")
    HIGH_PRIESTESS = ("The High Priestess", "mystery, hidden knowledge, intuition", "secrets withheld")
    EMPRESS = ("The Empress", "abundance, nurturing, fertility", "smothering, stagnation")
    EMPEROR = ("The Emperor", "authority, structure, control", "rigidity, tyranny")
    HIEROPHANT = ("The Hierophant", "tradition, conformity, institutions", "dogma, empty ritual")
    LOVERS = ("The Lovers", "relationships, choices, alignment", "disharmony, misalignment")
    CHARIOT = ("The Chariot", "willpower, determination, triumph", "aggression, lack of direction")
    STRENGTH = ("The Strength", "courage, patience, inner power", "self-doubt, weakness")
    HERMIT = ("The Hermit", "introspection, solitude, guidance", "isolation, withdrawal")
    WHEEL = ("The Wheel of Fortune", "cycles, fate, turning points", "bad luck, resistance to change")
    JUSTICE = ("The Justice", "fairness, truth, law", "unfairness, dishonesty")
    HANGED_MAN = ("The Hanged Man", "suspension, letting go, new perspective", "stalling, resistance")
    DEATH = ("The Death", "endings, transformation, transition", "resistance to change, stagnation")
    TEMPERANCE = ("The Temperance", "balance, moderation, patience", "imbalance, excess")
    DEVIL = ("The Devil", "bondage, materialism, shadow self", "release, breaking free")
    TOWER = ("The Tower", "sudden change, upheaval, revelation", "disaster, chaos")
    STAR = ("The Star", "hope, faith, renewal", "despair, disconnection")
    MOON = ("The Moon", "illusion, fear, the unconscious", "confusion, deception")
    SUN = ("The Sun", "joy, success, vitality", "temporary happiness, false optimism")
    JUDGEMENT = ("The Judgement", "reflection, reckoning, awakening", "self-doubt, refusal to learn")
    WORLD = ("The World", "completion, integration, accomplishment", "incompletion, shortcuts")

    @property
    def name_str(self) -> str:
        return self.value[0]
    
    @property
    def upright(self) -> str:
        return self.value[1]
    
    @property
    def reversed(self) -> str:
        return self.value[2]


@dataclass
class WhiteSheetStory:
    """A single White Sheet story with surface and hints"""
    headline: str
    surface_content: str
    what_to_notice: str  # Hints for the reader, not definitive meanings
    placement_note: Optional[str] = None


@dataclass
class WhiteSheetEdition:
    """A complete White Sheet edition for the day"""
    template_stories: List[WhiteSheetStory]  # Two from templates
    tarot_card: Tuple[TarotMajor, bool]  # (card, is_upright)
    editorial_note: Optional[str] = None


# === STORY TEMPLATES ===
# These are LESS specific than before. They hint at subtext without resolving it.

AGRICULTURAL_STORIES = [
    WhiteSheetStory(
        "EASTERN GRANARIES REPORT ADEQUATE RESERVES",
        "Provincial administrators confirm grain storage meets projected requirements for the coming season.",
        "The word 'adequate' is doing a lot of work. No actual figures given. 'Projected requirements' can mean anything.",
    ),
    WhiteSheetStory(
        "WEATHER-RELATED AGRICULTURAL ADJUSTMENTS IN SOUTHERN TERRITORIES",
        "Farmers implement seasonal modifications to planting schedules in response to atmospheric conditions.",
        "No mention of what the 'conditions' are. 'Adjustments' and 'modifications' are deliberately vague.",
    ),
    WhiteSheetStory(
        "IRRIGATION INFRASTRUCTURE RECEIVES SCHEDULED ATTENTION",
        "Bureau of the Rod personnel conduct work on water distribution systems in agricultural districts.",
        "Is this maintenance or emergency repair? The passive voice obscures who decided this was necessary and why.",
    ),
    WhiteSheetStory(
        "FISHERIES YIELD CONSISTENT WITH EXPECTATIONS",
        "Harbor authorities report maritime harvests continue at sustainable levels.",
        "'Consistent with expectations' only means something if you know what the expectations were.",
    ),
]

INFRASTRUCTURE_STORIES = [
    WhiteSheetStory(
        "ROUTINE MAINTENANCE SCHEDULED FOR THIRD WHORL WATER SYSTEMS",
        "Residents may experience temporary pressure fluctuations during overnight hours.",
        "How temporary? Which areas? The vagueness suggests they don't want people asking questions.",
    ),
    WhiteSheetStory(
        "LIFT SERVICES OPTIMIZED IN COMMERCIAL DISTRICTS",
        "Bureau of the Rod announces efficiency improvements to vertical transport systems.",
        "'Optimized' and 'improvements' without baseline comparisons. Is service getting better or are they redefining success?",
    ),
    WhiteSheetStory(
        "LIGHTING PANEL REPLACEMENT PROGRAM CONTINUES",
        "The ongoing initiative to modernize illumination systems proceeds according to projections.",
        "Which projections? The original ones or revised ones? 'Continues' is not the same as 'progresses.'",
    ),
    WhiteSheetStory(
        "PNEUMATIC MESSAGING NETWORK ACHIEVES RELIABILITY TARGETS",
        "Interdepartmental communication systems demonstrate consistent performance metrics.",
        "Targets can be lowered until anything achieves them. No mention of delivery times or coverage.",
    ),
]

BUREAUCRATIC_STORIES = [
    WhiteSheetStory(
        "PERSONNEL TRANSITIONS IN BUREAU OF THE SCALE",
        "Several experienced administrators accept positions in provincial offices.",
        "'Accept' is an interesting word choice. The provinces mentioned are far from the capital.",
    ),
    WhiteSheetStory(
        "EXAMINATION RESULTS DEMONSTRATE CONTINUED EXCELLENCE",
        "This year's Seven-Cornered Examination produces candidates meeting established criteria.",
        "No numbers. No comparison to previous years. 'Meeting criteria' is the minimum, not excellence.",
    ),
    WhiteSheetStory(
        "INTER-BUREAU COOPERATION INITIATIVE ANNOUNCED",
        "Senior administrators gather to coordinate approaches to shared challenges.",
        "When Bureaus announce 'cooperation,' it usually means a dispute has become too visible to ignore.",
    ),
    WhiteSheetStory(
        "DOCUMENT PROCESSING PROCEDURES UPDATED",
        "Bureau of the Scale implements revised protocols for petition handling.",
        "Updated how? Faster? Slower? More requirements? The lack of detail suggests the changes aren't improvements.",
    ),
]

MILITARY_SECURITY_STORIES = [
    WhiteSheetStory(
        "GARRISON ROTATIONS PROCEED IN EASTERN TERRITORIES",
        "Bureau of the Sword announces scheduled personnel movements among defensive installations.",
        "'Rotations' and 'movements' are carefully neutral. No mention of where troops are going versus where they're leaving.",
    ),
    WhiteSheetStory(
        "UNUSUAL ACTIVITY REPORTED NEAR TRADE ROUTES",
        "Travelers advised to coordinate with Bureau escort services when transiting certain highways.",
        "The word 'unusual' covers everything from bandits to something the Sheet can't name directly.",
    ),
    WhiteSheetStory(
        "SECURITY RECRUITMENT MEETS ANNUAL TARGETS",
        "Bureau of the Sword reports successful completion of this year's intake for civil forces.",
        "Targets can be adjusted. 'Meets' is not 'exceeds.' No mention of retention or experience levels.",
    ),
    WhiteSheetStory(
        "MARITIME SECURITY EXERCISES CONDUCTED",
        "Naval elements demonstrate readiness through coordinated maneuvers in coastal waters.",
        "How many ships? Which waters? 'Exercises' can mean anything from fleet operations to a single patrol.",
    ),
]

FOREIGN_AFFAIRS_STORIES = [
    WhiteSheetStory(
        "MARITIME TRADERS OPERATING UNDER UNUSUAL PROTOCOLS",
        "Harbor authorities note continued commercial activity from vessels employing non-standard procedures.",
        "The Westerners, presumably. The Sheet can't say more because no one knows more.",
    ),
    WhiteSheetStory(
        "TEMPORARY ADJUSTMENTS IN EASTERN COMMERCIAL RELATIONSHIPS",
        "Merchants report modifications to traditional trade patterns with inland territories.",
        "'Temporary' and 'adjustments' are doing a lot of work. No timeline. No specifics on what changed.",
    ),
    WhiteSheetStory(
        "ADMINISTRATIVE ARRANGEMENTS IN NORTHEASTERN PROVINCES",
        "Provincial boundaries undergo adjustment to optimize efficiency.",
        "Boundaries don't change for efficiency. Something has shifted that requires new maps.",
    ),
    WhiteSheetStory(
        "DELEGATION RETURNS FROM SOUTHERN OBSERVATION",
        "Personnel complete scheduled assessment of regional conditions.",
        "Who went where to observe what? The vagueness is the point.",
    ),
]

RELIGIOUS_CULTURAL_STORIES = [
    WhiteSheetStory(
        "ORACLE OBSERVANCES PROCEED WITH TRADITIONAL DIGNITY",
        "Faithful mark the contemplation period with appropriate ceremonies.",
        "'Traditional dignity' suggests nothing noteworthy happened. Or nothing they want to report.",
    ),
    WhiteSheetStory(
        "TESTAMENT INTERPRETATIONS RECEIVE SCHOLARLY ATTENTION",
        "Bureau of the Lens announces publication of updated commentary.",
        "When the Lens publishes 'updated' interpretation, someone's previous interpretation just became wrong.",
    ),
    WhiteSheetStory(
        "THEATRICAL PRODUCTIONS DEMONSTRATE ARTISTIC VITALITY",
        "Licensed venues report public interest in approved offerings.",
        "The word 'approved' is present. The word 'popular' is not.",
    ),
]

ECONOMIC_STORIES = [
    WhiteSheetStory(
        "PATENT AUTHENTICATION SYSTEMS PERFORM WITHIN PARAMETERS",
        "Bureau of the Coin confirms continued functionality of verification infrastructure.",
        "Parameters can be widened. 'Continued functionality' is not 'optimal performance.'",
    ),
    WhiteSheetStory(
        "AUREATE SUCCESSION PROCEEDS ACCORDING TO PROVISIONS",
        "Patent transition completes required formalities.",
        "Which family? The omission of the name might be significant, or might be routine.",
    ),
    WhiteSheetStory(
        "GUILD CHARTERS RENEWED IN CEREMONY",
        "Commercial privileges receive formal confirmation from Bureau of the Scale.",
        "Renewal is routine. The fact that it's newsworthy suggests someone thought it might not happen.",
    ),
    WhiteSheetStory(
        "COMMODITY PRICES REFLECT SEASONAL PATTERNS",
        "Market observers note fluctuations consistent with historical expectations.",
        "'Fluctuations' in which direction? 'Consistent with expectations' depends entirely on what was expected.",
    ),
]


# === PLACEMENT NOTES ===

PLACEMENT_NOTES = [
    "Placed prominently, displacing something.",
    "Buried in the middle pages.",
    "Adjacent to an unrelated story—the juxtaposition feels deliberate.",
    "Repeated from last week with minor changes.",
    "Given unusual length for such thin content.",
    "Formatted identically to a story from months ago about a different region.",
    "Truncated, as if the compositor ran out of approved text.",
    "Headline larger than the story warrants.",
]


# === EDITORIAL NOTES ===

EDITORIAL_NOTES = [
    "The edition feels thinner than usual.",
    "The paper quality is worse this week.",
    "A correction notice for an old story that changes nothing of substance.",
    "An unusually prominent reminder about unauthorized news distribution.",
    "A new regular feature no one asked for.",
    "The weather report is suspiciously detailed.",
    "An obituary for a minor functionary given strange prominence.",
]


# === TAROT-BASED STORY PROMPTS ===
# These give you seeds to CREATE a third story based on the card

TAROT_STORY_SEEDS = {
    TarotMajor.FOOL: [
        "A story about a new initiative or program, presented with optimism that feels unearned",
        "Something beginning—a project, a posting, a construction—without mention of what it replaces",
        "An announcement of 'fresh approaches' to old problems",
    ],
    TarotMajor.MAGICIAN: [
        "A story crediting someone's skill or intervention for a positive outcome",
        "Technical achievement presented without context for what it cost",
        "A profile of capability that feels like it's selling something",
    ],
    TarotMajor.HIGH_PRIESTESS: [
        "A story that hints at classified information without revealing it",
        "References to 'sources' or 'assessments' that can't be named",
        "Something about the Lattice or the Academy, carefully vague",
    ],
    TarotMajor.EMPRESS: [
        "A story about harvests, fertility, or production—abundance language",
        "The Creche announcing something about population or lineage",
        "Nurturing language applied to institutional programs",
    ],
    TarotMajor.EMPEROR: [
        "A story emphasizing hierarchy, proper procedure, or chain of command",
        "The Emperor mentioned, however obliquely",
        "Authority structures being reinforced or clarified",
    ],
    TarotMajor.HIEROPHANT: [
        "Something about Oracle observances or Testament interpretation",
        "Traditional practices being affirmed or defended",
        "Institutional continuity emphasized",
    ],
    TarotMajor.LOVERS: [
        "A story about alliances, agreements, or partnerships",
        "Something about marriage patterns or family arrangements",
        "A choice being presented as though there were no alternatives",
    ],
    TarotMajor.CHARIOT: [
        "Military success or 'progress' described in triumphant language",
        "Movement, expansion, or advance—even if the direction is unclear",
        "Willpower or determination celebrated",
    ],
    TarotMajor.STRENGTH: [
        "Endurance celebrated—surviving something difficult",
        "Patience or forbearance praised as virtue",
        "Quiet strength in the face of unnamed challenges",
    ],
    TarotMajor.HERMIT: [
        "A story about isolated communities or individuals",
        "Withdrawal framed positively—'focusing,' 'consolidating'",
        "Wisdom attributed to someone removed from events",
    ],
    TarotMajor.WHEEL: [
        "A story about cycles—seasonal, economic, historical",
        "Fortune changing, for better or worse",
        "Fate or destiny invoked",
    ],
    TarotMajor.JUSTICE: [
        "Legal proceedings or Scale Bureau announcements",
        "Fairness or balance emphasized",
        "Someone getting what they 'deserve'",
    ],
    TarotMajor.HANGED_MAN: [
        "Something suspended, delayed, or put on hold",
        "Waiting presented as strategy",
        "A different perspective offered on an old issue",
    ],
    TarotMajor.DEATH: [
        "An ending—retirement, closure, conclusion",
        "Transformation language: 'reorganization,' 'transition'",
        "Something old making way for something new",
    ],
    TarotMajor.TEMPERANCE: [
        "Balance, moderation, or patience emphasized",
        "Mixing or combining—mergers, integrations",
        "Slow, careful progress praised",
    ],
    TarotMajor.DEVIL: [
        "Something about dependencies or constraints",
        "Material concerns—prices, resources, debts",
        "Bonds that can't easily be broken",
    ],
    TarotMajor.TOWER: [
        "Sudden change, even if minimized",
        "An accident, disaster, or unexpected event",
        "Old structures failing, however the Sheet frames it",
    ],
    TarotMajor.STAR: [
        "Hope or renewal language",
        "Recovery from something difficult",
        "Distant goals or aspirations",
    ],
    TarotMajor.MOON: [
        "Uncertainty, ambiguity, things unclear",
        "Fears addressed or dismissed",
        "Something happening at night or in darkness",
    ],
    TarotMajor.SUN: [
        "Success, achievement, celebration",
        "Children or youth featured",
        "Brightness and optimism, possibly false",
    ],
    TarotMajor.JUDGEMENT: [
        "Reckoning or assessment",
        "Past actions being evaluated",
        "Calls to account or reflection",
    ],
    TarotMajor.WORLD: [
        "Completion or achievement",
        "Integration of disparate elements",
        "Cycles closing, new ones beginning",
    ],
}


def draw_tarot() -> Tuple[TarotMajor, bool]:
    """Draw a random Major Arcana card, upright or reversed"""
    card = random.choice(list(TarotMajor))
    is_upright = random.random() > 0.4  # Slightly favor upright
    return (card, is_upright)


def generate_edition() -> WhiteSheetEdition:
    """Generate a complete White Sheet edition: 2 template stories + 1 tarot-based"""
    
    # Draw the guiding tarot card
    tarot_card = draw_tarot()
    
    # Collect all story categories
    all_categories = [
        AGRICULTURAL_STORIES,
        INFRASTRUCTURE_STORIES,
        BUREAUCRATIC_STORIES,
        MILITARY_SECURITY_STORIES,
        FOREIGN_AFFAIRS_STORIES,
        RELIGIOUS_CULTURAL_STORIES,
        ECONOMIC_STORIES,
    ]
    
    # Select TWO stories from different categories
    selected_stories = []
    cat1, cat2 = random.sample(all_categories, 2)
    
    story1 = random.choice(cat1)
    story2 = random.choice(cat2)
    
    # Maybe add placement notes
    if random.random() < 0.4:
        story1 = WhiteSheetStory(
            headline=story1.headline,
            surface_content=story1.surface_content,
            what_to_notice=story1.what_to_notice,
            placement_note=random.choice(PLACEMENT_NOTES)
        )
    if random.random() < 0.4:
        story2 = WhiteSheetStory(
            headline=story2.headline,
            surface_content=story2.surface_content,
            what_to_notice=story2.what_to_notice,
            placement_note=random.choice(PLACEMENT_NOTES)
        )
    
    selected_stories = [story1, story2]
    
    # Maybe add editorial note
    editorial = random.choice(EDITORIAL_NOTES) if random.random() < 0.3 else None
    
    return WhiteSheetEdition(
        template_stories=selected_stories,
        tarot_card=tarot_card,
        editorial_note=editorial
    )


def format_edition(edition: WhiteSheetEdition) -> str:
    """Format an edition for display"""
    lines = []
    
    card, is_upright = edition.tarot_card
    orientation = "upright" if is_upright else "reversed"
    meaning = card.upright if is_upright else card.reversed
    
    lines.append("=" * 75)
    lines.append("WHITE SHEET EDITION")
    lines.append("=" * 75)
    
    lines.append(f"\nðŸŽ´ TAROT: {card.name_str} ({orientation})")
    lines.append(f"   Meaning: {meaning}")
    lines.append(f"   (This colors the emotional tenor of Rivan's reading)")
    
    if edition.editorial_note:
        lines.append(f"\nðŸ“° EDITION NOTE: {edition.editorial_note}")
    
    lines.append(f"\n{'─' * 75}")
    lines.append("TEMPLATE STORIES (use these two)")
    lines.append(f"{'─' * 75}")
    
    for i, story in enumerate(edition.template_stories, 1):
        lines.append(f"\n**STORY {i}**: {story.headline}")
        lines.append(f"   Surface: {story.surface_content}")
        lines.append(f"   Notice: {story.what_to_notice}")
        if story.placement_note:
            lines.append(f"   Placement: {story.placement_note}")
    
    lines.append(f"\n{'─' * 75}")
    lines.append("TAROT-GENERATED STORY (create this one)")
    lines.append(f"{'─' * 75}")
    
    seeds = TAROT_STORY_SEEDS.get(card, ["A story reflecting the card's themes"])
    lines.append(f"\n   Card: {card.name_str} ({orientation})")
    lines.append(f"   Theme: {meaning}")
    lines.append(f"\n   Possible directions:")
    for seed in seeds:
        lines.append(f"   • {seed}")
    
    lines.append(f"\n   CREATE a third story based on these themes.")
    lines.append(f"   It should feel like it belongs in the Sheet—bland surface,")
    lines.append(f"   but the tarot theme colors what Rivan notices or feels about it.")
    
    lines.append("\n" + "=" * 75)
    lines.append("SYNTHESIS NOTES:")
    lines.append("- Rivan USED TO WORK FOR THE ECHO. He wrote stories like these.")
    lines.append("- He reads with slightly arch irony and professional appreciation.")
    lines.append("- He knows the tricks: the careful word choices, the meaningful omissions.")
    lines.append("- He notices craft as much as content—admiring a well-constructed evasion.")
    lines.append("- He's sophisticated but not paranoid; he doesn't assume conspiracy.")
    lines.append("- The tarot card is for YOU, not for Rivan—it shapes mood, not content.")
    lines.append("- A sentence or two about the Sheet is usually enough.")
    lines.append("=" * 75)
    
    return "\n".join(lines)


def main():
    """Generate and display White Sheet editions"""
    print("\nGenerating White Sheet edition...\n")
    
    edition = generate_edition()
    print(format_edition(edition))
    
    # One more sample
    print("\n\n" + "â”" * 75)
    print("ADDITIONAL SAMPLE")
    print("â”" * 75)
    edition = generate_edition()
    print(format_edition(edition))


if __name__ == "__main__":
    main()

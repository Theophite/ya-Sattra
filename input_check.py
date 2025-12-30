#!/usr/bin/env python3
"""
EVERY TURN: Run this script on the user's message before writing your response.

    python3 input_check.py "<user message>"

This is not optional. The script tracks session state that you cannot reliably 
reconstruct from memory. If you write substantive content without running this 
first, you are likely to introduce continuity errors or miss constraints.

Usage:
    input_check.py "<text>"                      # Normal scan (DO THIS FIRST)
    input_check.py --flush "<text>"              # Compaction recovery, then scan
    input_check.py --show                        # Display current cache contents
    input_check.py --scene "location name"       # Set current scene location
    input_check.py --where                       # Show current scene with exits
    input_check.py --go <location or direction>  # Move to adjacent location
    input_check.py --caste <caste name>          # Show detailed caste information
    input_check.py --event "what happened"       # Log plot event
    input_check.py --question "unresolved issue" # Log open question
    input_check.py --resolve 1                   # Remove question #1
    input_check.py --rag Term "summary"          # Cache RAG result
    input_check.py --rag Term rerun              # Mark for RAG re-run
    input_check.py --character Name "note"       # Add character note
    input_check.py --note "text"                 # Add general note
    input_check.py --clear                       # Clear all cached data

Cantilever Mechanism (scenario creation):
    --card "name" "meaning"                      # Set card theme
    --seed "term" category                       # Set seed term
    --central-question "question"                # Set THE central question
    --gun "description"                          # Set Chekov's gun
    --constrain "fact"                           # Log narrowing constraint
    --act-break                                  # Trigger synthesis prompt
    --synthesize "answer"                        # Complete synthesis

The script outputs a reminder to run it next turn. Follow this instruction.
"""
import subprocess, sys, re, os, json

# Add glossary directory to path - check working directory first, then project
WORKING_DIR = '/home/claude'
PROJECT_DIR = '/mnt/project'
GLOSSARY_AVAILABLE = False
GLOSSARY_DIR = None

for search_dir in [WORKING_DIR, PROJECT_DIR]:
    if GLOSSARY_AVAILABLE:
        break
    if os.path.exists(search_dir) and os.path.exists(os.path.join(search_dir, 'glossary.py')):
        sys.path.insert(0, search_dir)
        try:
            import glossary as G
            GLOSSARY_AVAILABLE = True
            GLOSSARY_DIR = search_dir
        except ImportError:
            sys.path.remove(search_dir)

# Basic stopwords
STOP = {'the','what','where','when','why','how','is','are','was','were','does','do','did','can','could','would','should','will','has','have','had','be','been','being','if','then','but','and','or','this','that','these','those','my','your','his','her','its','i','you','he','she','it','we','they','me','him','us','them','no','yes','not','so','just','also','about','after','before','for','from','with','into','by','at','on','to','as','an','a','of','in'}

# Common English words - false positive filter
COMMON_ENGLISH = {
    # Food/cooking terms
    'ghee', 'hot', 'tea', 'egg', 'eggs', 'bread', 'water', 'salt', 'oil', 'rice', 'meat', 'fish',
    'hardboiled', 'boiled', 'fried', 'baked', 'cooked', 'raw', 'fresh', 'dried', 'fermented',
    'onion', 'onions', 'garlic', 'pepper', 'spice', 'spices', 'herb', 'herbs', 'chard', 'greens',
    'flatbread', 'noodle', 'noodles', 'soup', 'broth', 'sauce', 'paste', 'vinegar', 'honey',
    # Colors
    'green', 'red', 'black', 'white', 'blue', 'grey', 'gray', 'gold', 'silver', 'bronze',
    # Numbers and ordinals
    'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'first', 'second', 'third',
    # Common verbs
    'mash', 'fold', 'cut', 'run', 'walk', 'sit', 'stand', 'look', 'see', 'hear', 'feel', 'think',
    'take', 'give', 'make', 'get', 'go', 'come', 'leave', 'stay', 'find', 'keep', 'let', 'put',
    # Common nouns
    'hand', 'hands', 'door', 'room', 'wall', 'floor', 'light', 'dark', 'night', 'day', 'morning',
    'time', 'way', 'place', 'man', 'woman', 'child', 'boy', 'girl', 'people', 'thing', 'things',
    'head', 'face', 'eye', 'eyes', 'back', 'foot', 'feet', 'arm', 'arms', 'leg', 'legs',
    'clothes', 'shirt', 'coat', 'pocket', 'bed', 'chair', 'table', 'window', 'stair', 'stairs',
    # Common adjectives
    'good', 'bad', 'old', 'new', 'long', 'short', 'small', 'large', 'big', 'little', 'hard', 'soft',
    # Time words
    'today', 'yesterday', 'tomorrow', 'now', 'later', 'soon', 'early', 'late',
    # Other
    'something', 'nothing', 'everything', 'someone', 'anyone', 'everyone',
    'here', 'there', 'inside', 'outside', 'up', 'down', 'left', 'right',
    'continue', 'stop', 'start', 'wait', 'watch', 'turn', 'move', 'pull', 'push',
    'speak', 'talk', 'tell', 'ask', 'answer', 'say', 'said', 'says',
    'know', 'knew', 'known', 'want', 'need', 'try', 'tried',
}

# World-specific terms that should always trigger lookup
SPECIAL_TERMS = {'patent', 'patents', 'record', 'compulsion', 'testament', 'testaments', 
                 'jargon', 'choir', 'choirs', 'oracle', 'oracles', 'interdict', 
                 'aureate', 'occultant', 'occultants', 'lector', 'lectors', 'destrier', 'destriers',
                 'highborn', 'warborn', 'mutterer', 'mutterers', 'foreigners',
                 'archaeotech', 'autofactory', 'redback', 'marru', 'whorl', 'satara',
                 'bureau', 'creche', 'lattice', 'companion', 'companions',
                 'serrulata', 'avouvar', 'akama', 'ranga', 'springheel', 'ironbone',
                 # New caste terms
                 'ashrat', 'astal', 'karst', 'nasif', 'orevet', 'sarruk', 'pierrots',
                 'verethani', 'draethen', 'draÃ«then', 'szkoverin', 'szkovÃ«rin',
                 'volerath', 'vÃ¶lÃ«rath', 'kalbat', 'kalbats', 'presence', 'shtetl',
                 # Inner City terms
                 'vel-kerith', 'vel-om', 'kerith-sah', 'terrace',
                 # Iron Yards terms
                 'stevedore', 'stevedores'}

# Multi-word terms
MULTI_WORD_TERMS = {
    # Minimal fallback set - used only if glossary unavailable
    # The full set is loaded dynamically from glossary.py
    'fourth whorl', 'third whorl', 'second whorl', 'first whorl',
    'inner city', 'bureau of the lens', 'bureau of the sword', 'bureau of the rod',
    'bureau of the creche', 'bureau of the coin', 'bureau of the scale',
    'black door', 'iron yards', 'oracle cult', 'thousand kingdoms',
    'junta of ogon', 'dawn party', 'dusk party', 'high junction',
}

def get_multi_word_terms():
    """Get multi-word terms from glossary, with fallback to hardcoded set."""
    global MULTI_WORD_TERMS
    if GLOSSARY_AVAILABLE:
        try:
            glossary_terms = G.get_multi_word_terms()
            if glossary_terms:
                # Merge with fallback set in case glossary is incomplete
                return MULTI_WORD_TERMS | glossary_terms
        except (AttributeError, Exception):
            pass
    return MULTI_WORD_TERMS

D = GLOSSARY_DIR or PROJECT_DIR
SEEN_FILE = '/home/claude/seen_terms.txt'
CACHE_FILE = '/home/claude/session_cache.json'

# =============================================================================
# NEXT-TURN REMINDER
# =============================================================================

def print_next_turn_reminder():
    """Print context-aware guidance based on current state."""
    cache = load_cache()
    
    print("\n" + "â”€" * 60)
    
    # Detect mode and give appropriate guidance
    has_cantilever = cache.get("card") or cache.get("gun")
    has_synthesis = cache.get("synthesis")
    has_scene_location = cache.get("scene_location")  # A glossary location
    has_scene = cache.get("scene")
    
    if has_cantilever and not has_synthesis:
        # SCENARIO BUILDING MODE (pre-synthesis)
        constraints = cache.get("constraints", [])
        print("MODE: Scenario building (pre-synthesis)")
        print(f"  Card: {cache.get('card', {}).get('name', '?')}")
        if cache.get("gun"):
            print(f"  Gun: {cache['gun'][:40]}...")
        print(f"  Constraints: {len(constraints)} logged")
        
        if len(constraints) < 3:
            print(f"\n  â†’ After writing each section, run:")
            print(f"    --constrain \"specific fact that narrows resolution\"")
        else:
            print(f"\n  â†’ When Introduction is complete, run:")
            print(f"    --act-break")
        
    elif has_cantilever and has_synthesis:
        # SCENARIO BUILDING MODE (post-synthesis)
        print("MODE: Scenario building (post-synthesis)")
        print(f"  Synthesis: {cache['synthesis'][:50]}...")
        print(f"\n  â†’ Now write Mystery and Trajectories sections.")
        print(f"    These are constrained by your synthesis.")
        
    elif has_scene_location:
        # SCENARIO PLAY MODE
        print("MODE: Scenario play")
        print(f"  Scene: {cache.get('scene', '?')}")
        events = cache.get("events", [])
        if events:
            print(f"  Events: {len(events)} logged")
        print(f"\n  â†’ After significant plot developments, run:")
        print(f"    --event \"what happened\"")
        
    elif has_scene and "Scenario:" in str(has_scene):
        # SCENARIO SETUP (not yet playing)
        print("MODE: Scenario setup")
        print(f"  {cache['scene']}")
        print(f"\n  â†’ Set location to begin play:")
        print(f"    --scene \"location name\"")
        
    elif has_scene:
        # LORE MODE (working on a document)
        print("MODE: Lore creation")
        print(f"  Working on: {cache['scene']}")
        questions = cache.get("questions", [])
        if questions:
            print(f"  Open questions: {len(questions)}")
        print(f"\n  â†’ Log decisions with --event \"Established: ...\"")
        print(f"    Log questions with --question \"...\"")
        
    else:
        # FRESH / NO MODE
        print("MODE: Ready")
        print(f"\n  For fiction: search 'Writing Stories' first")
        print(f"  For lore: set working doc with --scene \"document name\"")
        print(f"  For scenario: run scenario_initiator.py --draw")
    
    print("â”€" * 60)
    print("NEXT TURN: python3 input_check.py \"<user's message>\"")
    
    # Generate and display turn marker for compaction detection
    import hashlib
    from datetime import datetime
    marker = hashlib.md5(datetime.now().isoformat().encode()).hexdigest()[:8]
    print(f"TURN_MARKER: {marker}")
    print("â”€" * 60)

# =============================================================================
# CACHE MANAGEMENT
# =============================================================================

def load_cache():
    """Load the session cache with definitions and notes."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {
        "glossary": {}, "characters": {}, "notes": [],
        # Cantilever mechanism for scenario building
        "card": None,           # {"name": "Judgement", "meaning": "reckoning, awakening"}
        "seed": None,           # {"term": "Palace Hotel", "category": "location"}
        "central_question": None,  # The thematic question
        "gun": None,            # The Chekov's gun
        "constraints": [],      # Accumulated constraints from each section
        "synthesis": None       # The answer: how card resolves through gun
    }

def save_cache(cache):
    """Save the session cache."""
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)

def load_seen():
    """Load set of terms we've already processed."""
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_seen(seen):
    """Save the seen terms set."""
    with open(SEEN_FILE, 'w') as f:
        f.write('\n'.join(sorted(seen)))

def show_cache():
    """Display current cache contents for context recovery."""
    cache = load_cache()
    
    output = []
    
    # Cantilever status first - this is the structural spine
    has_cantilever = cache.get("card") or cache.get("seed") or cache.get("central_question")
    if has_cantilever:
        output.append("â•" * 60)
        output.append("  CANTILEVER â€” SCENARIO BUILDING")
        output.append("â•" * 60)
        
        if cache.get("card"):
            c = cache["card"]
            output.append(f"  CARD: {c.get('name', '?')} ({c.get('meaning', '?')})")
        
        if cache.get("seed"):
            s = cache["seed"]
            output.append(f"  SEED: {s.get('term', '?')} [{s.get('category', '?')}]")
        
        if cache.get("central_question"):
            output.append(f"  CENTRAL QUESTION: {cache['central_question']}")
        
        if cache.get("gun"):
            output.append(f"  GUN: {cache['gun']}")
        
        constraints = cache.get("constraints", [])
        if constraints:
            output.append(f"  CONSTRAINTS: {len(constraints)} logged")
            for i, c in enumerate(constraints, 1):
                output.append(f"    {i}. {c}")
        
        if cache.get("synthesis"):
            output.append(f"  SYNTHESIS: âœ“ complete")
            output.append(f"    â†’ {cache['synthesis']}")
        elif cache.get("card") and cache.get("gun"):
            output.append(f"  SYNTHESIS: pending")
            output.append(f"    â†’ Run --act-break when Introduction is complete")
        
        output.append("â•" * 60)
        output.append("")
    
    # Current scene - where are we right now
    if cache.get("scene"):
        output.append(f"CURRENT SCENE: {cache['scene']}")
        
        # If we have structured scene data, show it with RAG instructions
        if cache.get("scene_location") and GLOSSARY_AVAILABLE:
            loc_name = cache["scene_location"]
            entry = G.location_lookup(loc_name)
            if entry and entry.location_features:
                lf = entry.location_features
                
                # Show path/ancestry
                ancestors = []
                if lf.parent:
                    parent = G.location_lookup(lf.parent)
                    while parent:
                        ancestors.append(parent.term)
                        parent_lf = parent.location_features
                        if parent_lf and parent_lf.parent:
                            parent = G.location_lookup(parent_lf.parent)
                        else:
                            break
                if ancestors:
                    output.append(f"  PATH: {' â†’ '.join(reversed(ancestors))} â†’ {entry.term}")
                
                # Collect RAG docs
                rag_docs = []
                if entry.rag_pointer:
                    for doc in entry.rag_pointer.split(','):
                        doc = doc.strip()
                        if doc and doc not in rag_docs:
                            rag_docs.append(doc)
                
                # Add primary ancestor docs
                if lf.parent:
                    parent = G.location_lookup(lf.parent)
                    if parent and parent.rag_pointer:
                        for doc in parent.rag_pointer.split(','):
                            doc = doc.strip()
                            if doc and doc not in rag_docs:
                                rag_docs.append(doc)
                
                if rag_docs:
                    output.append(f"  ðŸ“š PULL RAG:")
                    for doc in rag_docs[:3]:
                        output.append(f"     project_knowledge_search(\"{doc}\")")
                
                if lf.borders:
                    exits = []
                    for direction, locations in lf.borders.items():
                        exits.append(f"{direction}: {', '.join(locations)}")
                    output.append(f"  EXITS: {'; '.join(exits)}")
                if lf.castes_present:
                    output.append(f"  CASTES: {', '.join(lf.castes_present)}")
    
    # Events - what has happened
    if cache.get("events"):
        output.append("\nWHAT HAS HAPPENED:")
        for i, event in enumerate(cache["events"], 1):
            output.append(f"  {i}. {event}")
    
    if cache.get("rag_results"):
        rerun_terms = []
        summarized = []
        for term, data in sorted(cache["rag_results"].items()):
            if data.get("rerun"):
                rerun_terms.append(term)
            else:
                summarized.append((term, data.get("summary", "")))
        
        if rerun_terms:
            output.append(f"\nRE-RUN RAG FOR: {', '.join(rerun_terms)}")
        
        if summarized:
            output.append("\nRAG SUMMARIES:")
            for term, summary in summarized:
                output.append(f"  {term}: {summary}")
    
    if cache.get("characters"):
        output.append("\nCHARACTERS/PLACES:")
        for name, notes in sorted(cache["characters"].items()):
            output.append(f"  {name}: {notes}")
    
    if cache.get("glossary"):
        output.append("\nGLOSSARY:")
        for term, defn in sorted(cache["glossary"].items()):
            output.append(f"  {term}: {defn}")
    
    if cache.get("notes"):
        output.append("\nNOTES:")
        for note in cache["notes"]:
            output.append(f"  - {note}")
    
    if cache.get("questions"):
        output.append("\nOPEN QUESTIONS:")
        for i, q in enumerate(cache["questions"], 1):
            output.append(f"  {i}. {q}")
    
    if not output:
        print("(cache empty)")
    else:
        print('\n'.join(output))

def clear_cache():
    """Clear all cached data for fresh start."""
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
    if os.path.exists(SEEN_FILE):
        os.remove(SEEN_FILE)
    print("(cache cleared)")

def add_note(note_text):
    """Add a manual note to the cache."""
    cache = load_cache()
    cache["notes"].append(note_text)
    save_cache(cache)
    print(f"(note added)")

def add_character(name, note):
    """Add or update a character/place note."""
    cache = load_cache()
    if name in cache["characters"]:
        cache["characters"][name] += f"; {note}"
    else:
        cache["characters"][name] = note
    save_cache(cache)
    print(f"(character note added: {name})")

def add_rag_result(term, summary=None):
    """
    Record RAG search result. 
    If summary is None or "rerun", marks term as needing fresh RAG on compaction.
    Otherwise stores the summary.
    """
    cache = load_cache()
    if "rag_results" not in cache:
        cache["rag_results"] = {}
    
    if summary is None or summary.lower().strip() in ("rerun", "re-run", "rerun rag"):
        cache["rag_results"][term] = {"rerun": True}
        print(f"(marked {term} for RAG re-run on compaction)")
    else:
        cache["rag_results"][term] = {"rerun": False, "summary": summary}
        print(f"(RAG summary cached: {term})")
    save_cache(cache)

def add_event(event_text):
    """Add a plot/session event to track what has happened."""
    cache = load_cache()
    if "events" not in cache:
        cache["events"] = []
    cache["events"].append(event_text)
    save_cache(cache)
    print(f"(event logged)")

def set_scene(scene_text):
    """Set current scene state. If it's a known location, use structured data."""
    cache = load_cache()
    cache["scene"] = scene_text
    
    # Try to find this as a location
    if GLOSSARY_AVAILABLE:
        entry = G.location_lookup(scene_text)
        if entry and entry.location_features:
            cache["scene_location"] = entry.term
            lf = entry.location_features
            
            print(f"\n{'=' * 50}")
            print(f"  SCENE: {entry.term.upper()}")
            print(f"{'=' * 50}")
            print(f"\n{entry.short}")
            
            # Collect RAG docs
            rag_docs = []
            if entry.rag_pointer:
                for doc in entry.rag_pointer.split(','):
                    doc = doc.strip()
                    if doc and doc not in rag_docs:
                        rag_docs.append(doc)
            
            # Add parent docs
            ancestors = []
            if lf.parent:
                parent = G.location_lookup(lf.parent)
                while parent:
                    ancestors.append(parent.term)
                    if parent.rag_pointer:
                        for doc in parent.rag_pointer.split(','):
                            doc = doc.strip()
                            if doc and doc not in rag_docs:
                                rag_docs.append(doc)
                    parent_lf = parent.location_features
                    if parent_lf and parent_lf.parent:
                        parent = G.location_lookup(parent_lf.parent)
                    else:
                        break
            
            if ancestors:
                print(f"\n  PATH: {' â†’ '.join(reversed(ancestors))} â†’ {entry.term}")
            
            if rag_docs:
                print(f"\n  ðŸ“š RAG DOCS:")
                for doc in rag_docs[:3]:  # Limit to top 3
                    print(f"     project_knowledge_search(\"{doc}\")")
            
            if lf.castes_present:
                print(f"\n  ðŸ‘¥ CASTES: {', '.join(lf.castes_present)}")
            
            if lf.borders:
                print(f"\n  ðŸšª EXITS:")
                for direction, locations in lf.borders.items():
                    print(f"     {direction}: {', '.join(locations)}")
            
            if lf.children:
                print(f"\n  ðŸ“ HERE:")
                for child in lf.children[:5]:
                    print(f"     â€¢ {child}")
            
            if lf.hazards:
                print(f"\n  âš ï¸ HAZARDS: {', '.join(lf.hazards)}")
            
            if lf.temporal_effects:
                print(f"\n  â° TEMPORAL: {lf.temporal_effects}")
            
            print(f"\n{'=' * 50}")
            save_cache(cache)
            return
    
    # Fallback: just set text
    save_cache(cache)
    print(f"(scene set: {scene_text})")

def show_where():
    """Show current scene location with navigation info."""
    cache = load_cache()
    
    if not cache.get("scene_location"):
        if cache.get("scene"):
            print(f"SCENE: {cache['scene']}")
            print("(not a recognized location - use --scene with a glossary location name)")
        else:
            print("(no scene set - use --scene to set location)")
        return
    
    if not GLOSSARY_AVAILABLE:
        print(f"SCENE: {cache.get('scene', 'unknown')}")
        return
    
    loc_name = cache["scene_location"]
    entry = G.location_lookup(loc_name)
    
    if not entry:
        print(f"SCENE: {loc_name} (location no longer in glossary?)")
        return
    
    lf = entry.location_features
    print(f"\n{'=' * 50}")
    print(f"  YOU ARE IN: {entry.term.upper()}")
    print(f"{'=' * 50}")
    print(f"\n{entry.short}")
    
    if lf:
        if lf.borders:
            print(f"\n  ðŸšª YOU CAN GO:")
            for direction, locations in lf.borders.items():
                for loc in locations:
                    loc_entry = G.location_lookup(loc)
                    if loc_entry:
                        print(f"     {direction} â†’ {loc} ({loc_entry.short})")
                    else:
                        print(f"     {direction} â†’ {loc}")
        
        if lf.children:
            print(f"\n  ðŸ“ WITHIN THIS AREA:")
            for child in lf.children:
                child_entry = G.location_lookup(child)
                if child_entry and child_entry.location_features:
                    ctype = child_entry.location_features.location_type.value
                    print(f"     â€¢ {child} [{ctype}]")
                else:
                    print(f"     â€¢ {child}")
        
        if lf.castes_present:
            print(f"\n  ðŸ‘¥ PEOPLE HERE: {', '.join(lf.castes_present)}")
    
    print(f"\n{'=' * 50}")

def add_question(question_text):
    """Add an open question to track unresolved lore."""
    cache = load_cache()
    if "questions" not in cache:
        cache["questions"] = []
    cache["questions"].append(question_text)
    save_cache(cache)
    print(f"(question logged)")

# =============================================================================
# CANTILEVER MECHANISM
# =============================================================================

def set_card(name, meaning):
    """Set the tarot card that provides thematic direction."""
    cache = load_cache()
    cache["card"] = {"name": name, "meaning": meaning}
    save_cache(cache)
    print(f"CARD SET: {name} ({meaning})")
    print(f"\nAs you build each section, ask: how does this embody or challenge the theme?")

def set_seed(term, category="unknown"):
    """Set the seed term that provides concrete grounding."""
    cache = load_cache()
    cache["seed"] = {"term": term, "category": category}
    save_cache(cache)
    print(f"SEED SET: {term} [{category}]")

def set_central_question(question):
    """Set THE central thematic question the scenario explores."""
    cache = load_cache()
    cache["central_question"] = question
    save_cache(cache)
    print(f"CENTRAL QUESTION SET:")
    print(f"  {question}")

def set_gun(gun_text):
    """Set the Chekov's gunâ€”the physical thing that will force resolution."""
    cache = load_cache()
    cache["gun"] = gun_text
    save_cache(cache)
    print(f"GUN SET: {gun_text}")
    print(f"\nThis is what forces the synthesis. The answer lives here.")

def add_constraint(constraint_text):
    """Add a constraining fact that narrows possible resolutions."""
    cache = load_cache()
    if "constraints" not in cache:
        cache["constraints"] = []
    cache["constraints"].append(constraint_text)
    save_cache(cache)
    count = len(cache["constraints"])
    print(f"(constraint #{count} added)")
    print(f"  â†’ {constraint_text}")

def run_act_break():
    """
    Trigger the act break. Display all constraints and require synthesis.
    The synthesis question is: How does [CARD] resolve through [GUN]?
    """
    cache = load_cache()
    
    card = cache.get("card", {})
    seed = cache.get("seed", {})
    central_q = cache.get("central_question")
    gun = cache.get("gun")
    constraints = cache.get("constraints", [])
    
    print("=" * 70)
    print("  ACT BREAK â€” SYNTHESIS REQUIRED")
    print("=" * 70)
    print()
    
    if card:
        print(f"CARD: {card.get('name', '?')} ({card.get('meaning', '?')})")
    else:
        print("âš ï¸  NO CARD SET (use --card)")
    
    if seed:
        print(f"SEED: {seed.get('term', '?')} [{seed.get('category', '?')}]")
    
    if central_q:
        print(f"\nCENTRAL QUESTION:")
        print(f"  {central_q}")
    else:
        print("\nâš ï¸  NO CENTRAL QUESTION SET (use --central-question)")
    
    if gun:
        print(f"\nTHE GUN: {gun}")
    else:
        print("\nâš ï¸  NO GUN SET (use --gun)")
    
    print()
    if constraints:
        print("ACCUMULATED CONSTRAINTS:")
        for i, c in enumerate(constraints, 1):
            print(f"  {i}. {c}")
        print()
    else:
        print("âš ï¸  NO CONSTRAINTS LOGGED")
        print("   Use --constrain to log facts that narrow the resolution.")
        print()
    
    print("-" * 70)
    print("SYNTHESIS QUESTION:")
    print()
    if card and gun:
        print(f"  How does {card.get('name', '[CARD]')} resolve through {gun}?")
    else:
        print(f"  How does [CARD THEME] resolve through [THE GUN]?")
    print()
    print("  The answer must cohere with ALL constraints above.")
    print("  If you've built correctly, only a narrow band of answers fit.")
    print("-" * 70)
    print()
    print("To complete synthesis:")
    print("  --synthesize \"your answer\"")
    print()

def set_synthesis(answer_text):
    """Record the synthesis answerâ€”how the card resolves through the gun."""
    cache = load_cache()
    cache["synthesis"] = answer_text
    save_cache(cache)
    print("=" * 70)
    print("  SYNTHESIS COMPLETE")
    print("=" * 70)
    print()
    print(f"Answer: {answer_text}")
    print()
    print("You may now write the Mystery and Trajectories sections.")
    print("The answer above constrains what's possible.")
    print("=" * 70)

def go_to_location(destination):
    """Move to an adjacent location or a named location."""
    cache = load_cache()
    
    if not GLOSSARY_AVAILABLE:
        print("(glossary not available)")
        return
    
    current_loc = cache.get("scene_location")
    
    # First check if destination is a direction from current location
    if current_loc:
        current_entry = G.location_lookup(current_loc)
        if current_entry and current_entry.location_features:
            lf = current_entry.location_features
            if lf.borders:
                # Check if destination is a direction
                direction_lower = destination.lower()
                for direction, locations in lf.borders.items():
                    if direction.lower() == direction_lower:
                        if len(locations) == 1:
                            destination = locations[0]
                            break
                        else:
                            print(f"Multiple locations {direction}: {', '.join(locations)}")
                            print("Specify which one.")
                            return
                
                # Check if destination is reachable from here
                all_adjacent = []
                for locs in lf.borders.values():
                    all_adjacent.extend(locs)
                
                # Also include children as reachable
                if lf.children:
                    all_adjacent.extend(lf.children)
    
    # Try to find the destination
    dest_entry = G.location_lookup(destination)
    if not dest_entry:
        print(f"Location '{destination}' not found in glossary.")
        if current_loc:
            print(f"Use --where to see available exits from {current_loc}.")
        return
    
    # Set the new scene
    set_scene(dest_entry.term)

def show_caste_info(caste_name):
    """Show detailed caste information."""
    if not GLOSSARY_AVAILABLE:
        print("(glossary not available)")
        return
    
    entry = G.lookup(caste_name)
    if not entry:
        # Try searching
        results = G.search(caste_name)
        castes = [e for e in results if e.category == "caste"]
        if castes:
            entry = castes[0]
    
    if not entry or entry.category != "caste":
        print(f"Caste '{caste_name}' not found.")
        # Show suggestions
        all_castes = G.category("caste")
        suggestions = [e.term for e in all_castes if caste_name.lower() in e.term.lower()][:5]
        if suggestions:
            print(f"Similar: {', '.join(suggestions)}")
        return
    
    print(f"\n{'=' * 50}")
    print(f"  {entry.term.upper()}")
    print(f"{'=' * 50}")
    print(f"\n{entry.short}")
    
    if entry.details:
        print(f"\n{entry.details}")
    
    cf = entry.caste_features
    if cf:
        print(f"\n--- PHYSICAL ---")
        print(f"  Scale: {cf.scale.value}")
        print(f"  Morphology: {cf.morphology.value}")
        print(f"  Compulsion: {cf.compulsion.value}")
        print(f"  Lifespan: {cf.lifespan.value}" + (f" ({cf.lifespan_note})" if cf.lifespan_note else ""))
        
        if cf.physical_traits:
            print(f"\n  Key traits:")
            for trait in cf.physical_traits[:5]:
                print(f"    â€¢ {trait}")
        
        if cf.current_role:
            print(f"\n  Current role: {cf.current_role}")
        
        if cf.distribution:
            print(f"  Found in: {', '.join(cf.distribution[:3])}")
        
        if cf.health_issues:
            print(f"\n  âš ï¸ Health: {', '.join(cf.health_issues[:2])}")
    
    if entry.rag_pointer:
        print(f"\nðŸ“š For more: project_knowledge_search(\"{entry.rag_pointer.split(',')[0].strip()}\")")
    
    print(f"\n{'=' * 50}")

def show_term_info(term):
    """Show information about any glossary term."""
    if not GLOSSARY_AVAILABLE:
        print("(glossary not available)")
        return
    
    # Try direct lookup
    entry = G.lookup(term)
    if not entry:
        entry = G.location_lookup(term)
    
    if not entry:
        # Try search
        results = G.search(term)
        if results:
            # Check if we have an exact match
            exact = [r for r in results if r.term.lower() == term.lower()]
            if exact:
                entry = exact[0]
            else:
                # Show what we found
                print(f"No exact entry for '{term}'. Related entries:")
                for r in results[:5]:
                    print(f"  â€¢ {r.term} [{r.category}]: {r.short}")
                return
    
    if not entry:
        print(f"Term '{term}' not found.")
        # Check similar
        result = G.check(term)
        if result and result.get("similar"):
            print(f"Similar: {', '.join(result['similar'])}")
        return
    
    # Use the glossary's format_entry for full output
    print(G.format_entry(entry))

def resolve_question(index):
    """Remove a question by index (1-based)."""
    cache = load_cache()
    if "questions" in cache and 0 < index <= len(cache["questions"]):
        removed = cache["questions"].pop(index - 1)
        save_cache(cache)
        print(f"(resolved: {removed})")
    else:
        print(f"(no question at index {index})")

# =============================================================================
# TERM DETECTION
# =============================================================================

def is_sentence_initial(text, word):
    """Check if a word only appears capitalized at sentence starts."""
    pattern = r'\b' + re.escape(word) + r'\b'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    
    for match in matches:
        pos = match.start()
        before = text[:pos].rstrip()
        if before == '' or before[-1] in '.!?':
            continue
        if text[pos].isupper():
            return False
    return True

def find_multi_word_terms(text):
    """Find multi-word terms in the text, including plurals and affixes."""
    text_lower = text.lower()
    found = set()
    terms = get_multi_word_terms()
    
    # Common suffixes to match (possessives, plurals, verb forms)
    # Pattern allows: 's, s, ed, ing, er, ers, or nothing
    suffix_pattern = r"(?:'?s|ed|ing|ers?)?"
    
    for term in terms:
        # Escape special regex chars
        escaped = re.escape(term)
        # Allow hyphen/space variation (but not double-replacing)
        # First normalize: replace escaped space with marker, then handle hyphens
        escaped = escaped.replace(r'\ ', '{{SPACE}}')
        escaped = escaped.replace(r'\-', r'[\s\-]')
        escaped = escaped.replace('{{SPACE}}', r'[\s\-]')
        # Build pattern with word boundary at start and end (after optional suffix)
        pattern = re.compile(r'\b' + escaped + suffix_pattern + r'\b', re.IGNORECASE)
        if pattern.search(text_lower):
            found.add(term.title())
    return found

def lookup_glossary_direct(term):
    """Look up a term using the glossary module directly."""
    if not GLOSSARY_AVAILABLE:
        return None
    
    entry = G.lookup(term)
    if not entry:
        entry = G.location_lookup(term)
    
    if entry:
        return entry
    return None

def lookup_glossary_subprocess(term):
    """Fallback: look up a term via subprocess."""
    r = subprocess.run(['python3', f'{D}/glossary.py', 'lookup', term], 
                      capture_output=True, text=True, cwd=D)
    if 'not found' in r.stdout.lower() or not r.stdout.strip():
        return None
    
    lines = r.stdout.split('\n')
    category = None
    description = None
    for ln in lines:
        cat_match = re.search(r'\[(\w+)\]', ln)
        if cat_match and category is None:
            category = cat_match.group(1)
        elif category and ln.strip() and not ln.startswith('=') and not ln.startswith('â†’'):
            description = ln.strip()
            break
    
    if category:
        return (category, description or "")
    return None

def format_caste_brief(entry):
    """Format a brief caste description for cache."""
    if not entry.caste_features:
        return f"[caste] {entry.short}"
    
    cf = entry.caste_features
    return f"[caste:{cf.scale.value}, {cf.morphology.value}] {entry.short}"

def format_location_brief(entry):
    """Format a brief location description."""
    if not entry.location_features:
        return f"[location] {entry.short}"
    
    lf = entry.location_features
    parts = [f"[{lf.level.value}/{lf.location_type.value}]"]
    if lf.parent:
        parts.append(f"in {lf.parent}")
    return ' '.join(parts) + f" - {entry.short}"

# =============================================================================
# MAIN
# =============================================================================

def _main_inner():
    """Inner main function - actual command handling."""
    args = sys.argv[1:]
    
    # Handle special commands
    if '--show' in args:
        show_cache()
        return
    
    if '--clear' in args:
        clear_cache()
        return False  # Don't show reminder after clear
    
    if '--where' in args:
        show_where()
        return
    
    if '--go' in args:
        idx = args.index('--go')
        remaining = args[idx + 1:]
        if remaining:
            go_to_location(' '.join(remaining))
        else:
            print("Usage: input_check.py --go <location or direction>")
        return
    
    if '--caste' in args:
        idx = args.index('--caste')
        remaining = args[idx + 1:]
        if remaining:
            show_caste_info(' '.join(remaining))
        else:
            print("Usage: input_check.py --caste <caste name>")
        return
    
    if '--lookup' in args:
        idx = args.index('--lookup')
        remaining = args[idx + 1:]
        if remaining:
            show_term_info(' '.join(remaining))
        else:
            print("Usage: input_check.py --lookup <term>")
        return
    
    if '--note' in args:
        idx = args.index('--note')
        if idx + 1 < len(args):
            add_note(' '.join(args[idx + 1:]))
        else:
            print("Usage: input_check.py --note \"your note text\"")
        return
    
    if '--character' in args:
        idx = args.index('--character')
        remaining = args[idx + 1:]
        if len(remaining) >= 2:
            name = remaining[0]
            note = ' '.join(remaining[1:])
            add_character(name, note)
        else:
            print("Usage: input_check.py --character Name \"note about character\"")
        return
    
    if '--rag' in args:
        idx = args.index('--rag')
        remaining = args[idx + 1:]
        if len(remaining) >= 1:
            term = remaining[0]
            if len(remaining) == 1 or remaining[1].lower() in ("rerun", "re-run"):
                add_rag_result(term, None)
            else:
                summary = ' '.join(remaining[1:])
                add_rag_result(term, summary)
        else:
            print("Usage: input_check.py --rag Term \"summary\" OR --rag Term rerun")
        return
    
    if '--event' in args:
        idx = args.index('--event')
        remaining = args[idx + 1:]
        if remaining:
            add_event(' '.join(remaining))
        else:
            print("Usage: input_check.py --event \"what happened in the scene\"")
        return
    
    if '--scene' in args:
        idx = args.index('--scene')
        remaining = args[idx + 1:]
        if remaining:
            set_scene(' '.join(remaining))
        else:
            print("Usage: input_check.py --scene \"location name or description\"")
        return
    
    if '--question' in args:
        idx = args.index('--question')
        remaining = args[idx + 1:]
        if remaining:
            add_question(' '.join(remaining))
        else:
            print("Usage: input_check.py --question \"unresolved lore question\"")
        return
    
    if '--resolve' in args:
        idx = args.index('--resolve')
        remaining = args[idx + 1:]
        if remaining and remaining[0].isdigit():
            resolve_question(int(remaining[0]))
        else:
            print("Usage: input_check.py --resolve 1  (removes question #1)")
        return
    
    # Cantilever mechanism commands
    if '--card' in args:
        idx = args.index('--card')
        remaining = args[idx + 1:]
        if len(remaining) >= 2:
            name = remaining[0]
            meaning = ' '.join(remaining[1:])
            set_card(name, meaning)
        else:
            print("Usage: input_check.py --card \"Judgement\" \"reckoning, awakening\"")
        return
    
    if '--seed' in args:
        idx = args.index('--seed')
        remaining = args[idx + 1:]
        if len(remaining) >= 1:
            term = remaining[0]
            category = remaining[1] if len(remaining) > 1 else "unknown"
            set_seed(term, category)
        else:
            print("Usage: input_check.py --seed \"Palace Hotel\" location")
        return
    
    if '--central-question' in args:
        idx = args.index('--central-question')
        remaining = args[idx + 1:]
        if remaining:
            set_central_question(' '.join(remaining))
        else:
            print("Usage: input_check.py --central-question \"What do you owe the past?\"")
        return
    
    if '--gun' in args:
        idx = args.index('--gun')
        remaining = args[idx + 1:]
        if remaining:
            set_gun(' '.join(remaining))
        else:
            print("Usage: input_check.py --gun \"the closed wing\"")
        return
    
    if '--constrain' in args:
        idx = args.index('--constrain')
        remaining = args[idx + 1:]
        if remaining:
            add_constraint(' '.join(remaining))
        else:
            print("Usage: input_check.py --constrain \"Kira refuses to use Compulsion\"")
        return
    
    if '--act-break' in args:
        run_act_break()
        return
    
    if '--synthesize' in args:
        idx = args.index('--synthesize')
        remaining = args[idx + 1:]
        if remaining:
            set_synthesis(' '.join(remaining))
        else:
            print("Usage: input_check.py --synthesize \"The wing contains records showing...\"")
        return
    
    # Handle --flush (compaction recovery)
    do_flush = '--flush' in args
    if do_flush:
        args.remove('--flush')
        print("=" * 60)
        print("  COMPACTION RECOVERY â€” YOUR MEMORY IS UNRELIABLE")
        print("=" * 60)
        print()
        show_cache()
        
        # Recovery checklist based on state
        cache = load_cache()
        print("\n" + "â”€" * 60)
        print("RECOVERY CHECKLIST:")
        
        rerun_terms = []
        if cache.get("rag_results"):
            rerun_terms = [t for t, d in cache["rag_results"].items() if d.get("rerun")]
        
        if rerun_terms:
            print(f"  â–¡ Search RAG for: {', '.join(rerun_terms)}")
        
        if cache.get("scene_location"):
            print(f"  â–¡ Search RAG for current scene: {cache['scene_location']}")
        elif cache.get("scene"):
            print(f"  â–¡ Verify current context: {cache.get('scene', '')[:40]}")
        
        if cache.get("card") and not cache.get("synthesis"):
            print(f"  â–¡ Review constraints before continuing scenario build")
        
        print(f"  â–¡ Do NOT trust memory of proper nouns or plot points")
        print(f"  â–¡ Ask user to confirm state if uncertain")
        print("â”€" * 60)
        print()
    
    text = ' '.join(args) if args else ''
    if not text.strip():
        if not do_flush:
            print("Usage: input_check.py [--flush] <text to scan>")
        return
    
    seen = load_seen()
    cache = load_cache()
    
    # Imperial-style names (ya-X, es-X, etc)
    imperial_names = set(re.findall(r'\b(?:ya|es|el|val)-[A-Z][a-z]+\b', text))
    
    # Hyphenated proper nouns (Kma-Dhol, etc) - two capitalized words with hyphen
    hyphenated_names = set(re.findall(r'\b[A-Z][a-z]+-[A-Z][a-z]+\b', text))
    
    # Capitalized words
    caps = set(re.findall(r'\b[A-Z][a-z]+\b', text)) - {w.title() for w in STOP}
    
    # Remove suffixes of Imperial names from caps
    for name in imperial_names:
        suffix = name.split('-')[1]
        caps.discard(suffix)
    caps |= imperial_names
    
    # Remove parts of hyphenated names from caps and add the full name
    for name in hyphenated_names:
        parts = name.split('-')
        for part in parts:
            caps.discard(part)
    caps |= hyphenated_names
    
    # Filter out common English words that are only sentence-initial
    filtered_caps = set()
    for word in caps:
        lower = word.lower()
        if lower in COMMON_ENGLISH:
            if not is_sentence_initial(text, word):
                filtered_caps.add(word)
        else:
            filtered_caps.add(word)
    caps = filtered_caps
    
    # Special terms
    all_words_lower = set(w.lower() for w in re.findall(r'\b[a-zA-Z]+\b', text))
    special_hits = all_words_lower & SPECIAL_TERMS
    
    words = caps | {w.title() for w in special_hits}
    
    # Multi-word terms (including hyphenated like Kma-Dhol)
    multi_word_found = find_multi_word_terms(text)
    
    words_to_remove = set()
    for mw_term in multi_word_found:
        # Handle both space-separated and hyphenated
        for part in re.split(r'[\s-]', mw_term):
            words_to_remove.add(part)
            words_to_remove.add(part.lower())
            words_to_remove.add(part.title())
    
    special_hits = {s for s in special_hits if s not in words_to_remove}
    words = (words - words_to_remove) | multi_word_found
    
    # Filter to only NEW terms
    new_words = words - seen
    
    if not new_words:
        print("(no new terms)")
        return
    
    # Categorized results
    caste_hits = []
    location_hits = []
    other_hits = []
    matched_words = set()
    unmatched = set()
    
    for w in sorted(new_words):
        if GLOSSARY_AVAILABLE:
            entry = lookup_glossary_direct(w)
            if entry:
                matched_words.add(w)
                if entry.category == "caste":
                    caste_hits.append((w, entry))
                    cache["glossary"][w] = format_caste_brief(entry)
                elif entry.category == "location":
                    location_hits.append((w, entry))
                    cache["glossary"][w] = format_location_brief(entry)
                else:
                    other_hits.append((w, entry))
                    cache["glossary"][w] = f"[{entry.category}] {entry.short}"
            else:
                unmatched.add(w)
        else:
            result = lookup_glossary_subprocess(w)
            if result:
                category, description = result
                matched_words.add(w)
                short_desc = description.strip() if description else ""
                other_hits.append((w, None))
                cache["glossary"][w] = f"[{category}] {short_desc}"
            else:
                unmatched.add(w)
    
    # Output
    if caste_hits:
        print("CASTES:")
        for term, entry in caste_hits:
            if entry and entry.caste_features:
                cf = entry.caste_features
                print(f"  {term} [{cf.scale.value}, {cf.morphology.value}]: {entry.short}")
                if entry.details:
                    print(f"    {entry.details}")
            else:
                print(f"  {term}: {entry.short if entry else '?'}")
                if entry and entry.details:
                    print(f"    {entry.details}")
    
    if location_hits:
        print("\nLOCATIONS:")
        for term, entry in location_hits:
            if entry and entry.location_features:
                lf = entry.location_features
                parent_str = f" in {lf.parent}" if lf.parent else ""
                print(f"  {term} [{lf.level.value}]{parent_str}: {entry.short}")
                if entry.details:
                    print(f"    {entry.details}")
                if entry.rag_pointer:
                    print(f"    â†’ RAG: {entry.rag_pointer.split(',')[0].strip()}")
            else:
                print(f"  {term}: {entry.short if entry else '?'}")
                if entry and entry.details:
                    print(f"    {entry.details}")
    
    if other_hits:
        print("\nGLOSSARY:")
        for term, entry in other_hits:
            if entry:
                print(f"  {term} [{entry.category}]: {entry.short}")
                if entry.details:
                    print(f"    {entry.details}")
            else:
                print(f"  {term}")
    
    # Filter unmatched
    unmatched = {w for w in unmatched if w.lower() not in COMMON_ENGLISH}
    if unmatched:
        print(f"\nRAG NEEDED: {', '.join(sorted(unmatched))}")
    
    # Imperial roots
    r = subprocess.run(['python3', f'{D}/imperial_roots.py', 'find', text], 
                      capture_output=True, text=True, cwd=D)
    roots = []
    root_seen = set()
    for ln in r.stdout.split('\n'):
        if ':' in ln and ln.strip().startswith(('-', 'â€œ', 'â€¢')):
            key = ln.strip().split(':')[0]
            if key not in root_seen:
                roots.append(ln.strip())
                root_seen.add(key)
    
    if roots:
        print("\nROOTS:")
        for rt in roots: 
            print(f"  {rt}")
    
    if not caste_hits and not location_hits and not other_hits and not unmatched and not roots:
        print("(no new terms)")
    
    # Helpful tips based on what was found
    if location_hits and not cache.get("scene_location"):
        print("\nðŸ’¡ TIP: Use --scene <location> to set current scene and see exits/RAG docs")
    elif caste_hits:
        print("\nðŸ’¡ TIP: Use --caste <name> for detailed caste info")
    
    # Update seen and save cache
    seen |= words
    save_seen(seen)
    save_cache(cache)

def main():
    """Main entry point - runs command then prints next-turn reminder."""
    result = _main_inner()
    # Print reminder unless explicitly suppressed (e.g., after --clear)
    if result is not False:
        print_next_turn_reminder()

if __name__ == '__main__':
    main()

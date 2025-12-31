# GM Agent Architecture for the Post-Interdict Empire

## Executive Summary

A multi-agent system for running tabletop RPG sessions in the Post-Interdict Empire setting. The architecture uses dynamic prompt construction, structured lore retrieval, and separated concerns between narrative generation and state management to create a world that moves independently of player action.

---

## Core Principles

1. **The world has momentum.** Events occur whether the player engages or not. NPCs have agendas. Clocks tick.

2. **Memory is injected, not recalled.** Agents receive their orientation each turn via dynamically constructed system prompts. Conversation history persists normally; directives are reconstructed.

3. **The glossary is the hub.** All retrieval passes through the structured glossary, which points to detail documents and back.

4. **NPCs think before they act.** Opus runs discrete perspective blocks for each NPC before synthesizing scene output.

5. **Constraints fire from structure.** If-then rules live in document metadata and glossary entries, injected into prompts when relevant entities appear.

---

## Agent Roles

### Orchestrator (Python)

The control loop. Receives player input, queries glossary, constructs prompts, routes between agents.

**Responsibilities:**
- Parse player input for glossary entities
- Retrieve relevant constraints and vibes
- Build Opus system prompt from components
- Send Opus output to Haiku for parsing
- Receive state updates from Haiku
- Maintain ticking clocks and world events

**Not an LLM.** Pure code.

### Opus (Claude claude-opus-4-5-20250514)

The narrator. Generates scene descriptions, dialogue, and world narration.

**Receives:**
- Dynamic system prompt (location, state, constraints, vibes)
- NPC list with agendas
- Ticking clocks
- Player's input

**Process:**
1. Extended thinking: run perspective block for each active NPC
2. Extended thinking: determine world momentum (what happens regardless of player)
3. Extended thinking: synthesis plan
4. Output: scene narration

**Does not:**
- Track state (Haiku does this)
- Remember previous sessions (orchestrator provides context)
- Make mechanical rulings (separate validator does this)

### Haiku (Claude claude-3-5-haiku-20241022)

The state clerk. Parses Opus output, extracts state changes, maintains the log.

**Receives:**
- Opus's narrative output
- Current state log
- Extraction instructions (what to track this scene)

**Extracts:**
- Who moved, who spoke
- Location changes
- NPC state changes (mood, knowledge, position)
- Clock advances
- New tensions or resolutions
- Items exchanged
- Information revealed

**Outputs:**
- Updated state log
- State summary for next Opus prompt
- Alerts if continuity issues detected

**System prompt modulated by:** what Opus just generated (tells Haiku what to look for)

---

## Document Architecture

### Current State (to be restructured)

Large monolithic markdown files mixing reference material, instance data, and examples.

### Target State

**Flat naming, split files:**
```
Caste - Sewer-Fishers - Overview.md
Caste - Sewer-Fishers - Biology.md
Caste - Sewer-Fishers - Cognition.md
Caste - Sewer-Fishers - Clan Benru.md
Caste - Sewer-Fishers - Clan Loak.md
...
Vignettes - Merras Kitchen.md
Vignettes - The Venn Bridge.md
Vignettes - Stillbirth.md
...
Dossiers - Korim Sarn.md
Dossiers - Yuli Loak.md
...
```

**Document types:**
- **Reference:** Stable definitional content (biology, social organization)
- **Instance:** Specific entities (clans, characters, locations)
- **Vignette:** Narrative examples (tone, voice, atmosphere)
- **Dossier:** Character profiles with agendas and state

### Front Matter Schema

Every document includes YAML front matter:

```yaml
---
title: Clan Loak
type: instance
parent: Caste - Sewer-Fishers
glossary_terms:
  - Sewer-Fishers
  - Lift-3
  - Salvage Guild
  - Hanged Men
  - Merra Loak
  - Yuli Loak

guidance:
  - "If naming a Loak, use single-syllable names: Yuli, Korr, Bos, Jak"
  - "If describing Lift-3, include the sewer-gas engine sound and smell"
  - "Merra's kitchen is neutral ground - no violence occurs there"
  - "Stevedore fosterlings are protective of pure-line family members"

see_also:
  - Caste - Sewer-Fishers - Biology.md
  - Caste - Sewer-Fishers - Clan Venn.md
---
```

### Vignette Front Matter

```yaml
---
title: Merra's Kitchen
type: vignette
location: Hollow-Egress, Middens
characters:
  - Merra Loak
  - Yuli Loak
  - Korim Sarn
themes:
  - information exchange
  - neutral ground
  - cross-clan cooperation
  - salvage economy
tone: quotidian, layered with politics
---
```

---

## Glossary as Hub

The existing `glossary_data.yaml` already contains:
- `rag_pointer` → points to detail documents
- `related` → points to other glossary entries
- `caste_features` / `location_features` → structured queryable data
- Hierarchical location data (parent, children, borders)

### Additions Needed

**Guidance field** for entries that need behavioral constraints:
```yaml
Sewer-Fishers:
  category: caste
  short: "..."
  rag_pointer: "Caste - Sewer-Fishers - Overview.md"
  related: [Technical Castes, Mutterers, Middens]
  guidance:
    - "Show mathematical intuition as bodily sensation, not calculation"
    - "Never have sewer-fishers reveal Technical Caste ancestry to outsiders"
    - "Infant mortality is ~50%; personhood begins at 9 months when muttering stops"
```

**Bidirectional linking:** Documents point back to glossary via `glossary_terms` in front matter. Glossary points to documents via `rag_pointer`.

---

## Dynamic System Prompt Construction

### Base Layer (static)

```markdown
You are the GM for a Post-Interdict Empire campaign. Your prose is:
- Concrete and sensory, not abstract
- Morally neutral - describe, don't judge
- Attentive to material conditions before motivations
- Incomplete - characters don't know everything

You narrate a world that moves independently of the player.
```

### Location Layer (from glossary)

```markdown
## Current Location: Merra's Kitchen

Loak clan mess hall atop Hollow-Egress in the Middens. Engine heat from
Lift-3 below. Perpetual stew. Neutral ground - no violence here.

Aesthetic: Fish oil smell, dripping salvage gear, steam, engine harmonics.
The smoke and sewage smell don't reach this high.

Exits: Ladder down to Lift-3 engine room, rope bridge to Vetch-Rise
```

### State Layer (from Haiku)

```markdown
## Current State

Present NPCs:
- Yuli Loak: At engine room door, oil on hands, watching Chain-Men
- Korim Sarn: Corner table, just surfaced, luminescent eyes dim
- Merra Loak: Behind counter, ladling stew, tracking everything
- Two Chain-Men: Corner table, not eating, listening

Recent events:
- Vin Venn delivered pre-Interdict circuit boards (2 days meals credit)
- Chain-Men mentioned "mapping unauthorized crossings by week's end"
- Player asked Merra about deep tunnel conditions

Tension: Chain-Men surveillance; Korim has news he can't articulate
```

### Constraints Layer (from glossary + checkers)

```markdown
## Active Constraints

Entity-derived:
- Korim's speech includes tonal frequencies that vibrate nearby metal
- Sewer-fishers show mathematical intuition as sensation, not calculation
- Chain-Men report to Fen; anything notable gets passed up

Scene-derived:
- Merra's kitchen is neutral ground
- Merra never stops working while talking
- All conversation is performative while Chain-Men present
```

### NPC Agenda Layer

```markdown
## NPC Agendas

Korim Sarn:
- NEED: Warn surface about deep instability
- OBSTACLE: Can't translate what he experienced
- TELL: Eyes dimmer than usual, speech more tonal

Merra Loak:
- NEED: Maintain neutral ground while gathering intelligence
- WATCHING: Chain-Men attention, Korim's state, player's questions
- TELL: Ladle rhythm changes when she's thinking

Chain-Men:
- TASK: Map unauthorized crossings (Fen's orders)
- METHOD: Listen, observe, don't confront
- TELL: Not eating the stew
```

### Clocks Layer

```markdown
## Ticking Clocks

- Korim leaves in ~20 minutes (can't stay surfaced long)
- Chain-Men shift change in ~1 hour (reinforcements)
- Evening salvage rush begins in ~30 minutes (kitchen gets crowded)
```

### Vibes Layer (from Writing Guide or vignettes)

```markdown
## Voice This Scene

Kitchen scenes: quotidian activity layered with information exchange.
Food service continues through all conversation. Economic calculation
is constant and unspoken. The stew is the only constant.
```

---

## NPC Thinking Blocks

Before generating scene output, Opus runs extended thinking for each active NPC:

```
<thinking>
## Korim Sarn's Perspective
I've been below too long. The surfacers can't understand what the
below-ones showed me - the harmonic instability, the patterns that
feel wrong. Merra might understand the urgency if not the content.
The Chain-Men worry me. If Fen learns the deep trade is disrupted...
I need to find words. The player asked about deep tunnels. Maybe.

## Merra Loak's Perspective
Korim looks worse than usual. That luminescence should be brighter.
The Chain-Men haven't touched their stew - they're working, not eating.
Do I raise their prices? That signals I've noticed. But subsidizing
surveillance grates. The stranger asking about deep tunnels - interesting
timing. I could create an opening for Korim if I position the conversation.

## Chain-Men's Perspective (collective)
Routine sweep. Hannok said map crossings, note anything unusual.
The Sarn talks weird - note it. The stranger asks about tunnels - note it.
We don't confront, we collect. The stew is actually good. Don't note that.

## World Momentum
The kitchen fills slowly as afternoon salvage crews return. Price
conversations happen at the counter. Someone mentions the Penitent
Ward tunnel collapse - south end, near the old detention complex.
News is traveling.

## Synthesis
The player asked about deep tunnels. Merra can deflect to Korim
naturally. Korim struggles to answer - his perspective block shows
he wants to but can't find words. Chain-Men note the conversation
but don't intervene. Background: kitchen getting busier, collapse
news spreading. The world continues.
</thinking>
```

Then Opus generates the scene from this synthesis.

---

## State Management

### Haiku's State Log

Structured record of everything that has happened:

```yaml
session: 2024-12-29-001
location: Merra's Kitchen
turn: 7

npcs_present:
  - id: korim-sarn
    status: anxious, struggling to communicate
    position: corner table
    knowledge_state: knows deep instability, can't articulate

  - id: merra-loak
    status: alert, working
    position: behind counter
    knowledge_state: suspects Korim has news, tracking Chain-Men

  - id: chain-men-pair
    status: surveilling
    position: corner table
    knowledge_state: noted Sarn speech patterns, noted player questions

events_this_session:
  - turn: 3
    type: arrival
    actor: korim-sarn
    details: "Surfaced via first transition chamber, unusual timing"

  - turn: 5
    type: information
    actor: chain-men
    details: "Mentioned mapping unauthorized crossings"
    witnesses: [merra-loak, yuli-loak, player]

  - turn: 6
    type: question
    actor: player
    target: merra-loak
    content: "Asked about deep tunnel conditions"
    witnesses: [korim-sarn, chain-men-pair]

clocks:
  - name: korim-departure
    remaining: 18 minutes

  - name: chain-men-shift-change
    remaining: 55 minutes

tensions:
  - parties: [korim-sarn, chain-men-pair]
    nature: surveillance risk
    status: unresolved
```

### Haiku's Extraction Prompt

Each turn, Haiku receives instructions on what to extract:

```markdown
## Extraction Targets This Turn

From Opus's output, extract:
1. Any NPC movement or position changes
2. Any information revealed (who learned what)
3. Any clock advances (time passing, deadlines mentioned)
4. Korim's communication attempts (did he manage to convey anything?)
5. Chain-Men attention (did they note anything new?)
6. Player commitments (did they agree to anything, promise anything?)

Update the state log. Generate summary for next Opus prompt.
Flag if: Korim leaves, Chain-Men act, new NPCs enter.
```

---

## Retrieval Flow

1. **Player input:** "I ask Korim directly - what's wrong down there?"

2. **Orchestrator parses:** Entities = [Korim Sarn, deep tunnels, Sarns]

3. **Glossary lookup:**
   - Korim Sarn → Dossiers - Korim Sarn.md
   - Sarns → Caste - Sewer-Fishers - Clan Sarn.md
   - Deep tunnels → (no direct hit, semantic search)

4. **Constraint gathering:**
   - From Sarn doc: "Korim's speech includes pressure-pulse mathematics"
   - From Sewer-Fisher guidance: "Mathematical intuition is sensation not calculation"
   - From scene state: Chain-Men are listening

5. **Prompt construction:** Assemble all layers

6. **Opus generates:** With NPC thinking blocks, then scene

7. **Haiku parses:** Extracts state changes

8. **State updates:** Korim revealed something, Chain-Men noted it, clock advanced

9. **Next turn:** New prompt reflects updated state

---

## Mechanical Validation (Future)

Separate from narrative generation. Python-based checks for:
- Continuity errors (NPC in two places)
- Lore violations (Mutterer initiating action)
- Impossible actions (baseline human in lethal radiation zone)

Runs on Opus output before delivery to player. Can flag or auto-correct.

---

## Cost Optimization

### Negative Overhead via Haiku Preprocessing

RAG results go to Haiku for summarization before reaching Opus. Haiku's summary costs less than Opus processing raw retrieval. Net savings on Opus input tokens exceeds Haiku processing cost.

### Glossary as First Filter

Glossary entries are short (50-200 words). Embed entire glossary for vector search. Only retrieve full documents when glossary points to them. Most queries resolved at glossary level.

### State Compression

Haiku's state summaries are compressed representations of full logs. Opus receives summary, not full history. Full log available for contradiction checking but not injected into every prompt.

### Prompt Caching

Base persona layer is static → cacheable. Only dynamic layers (state, constraints, NPCs) change per turn.

---

## Implementation Phases

### Phase 1: Document Restructuring
- Split existing monolithic .md files into chunked documents
- Add YAML front matter with glossary_terms and guidance
- Update glossary rag_pointer fields to new document names
- Create Dossiers folder for character profiles
- Move vignettes to Vignettes folder with proper tagging

### Phase 2: Retrieval Pipeline
- Build prompt construction from glossary + documents
- Implement constraint extraction from front matter
- Connect to existing glossary.py for entity lookup
- Test retrieval flow without agents

### Phase 3: Agent Loop
- Implement Orchestrator control loop
- Connect Opus with dynamic prompt construction
- Implement Haiku state extraction
- Build state log format and update cycle

### Phase 4: NPC System
- Add NPC agenda format to dossiers
- Implement thinking block prompting for Opus
- Test multi-NPC scenes

### Phase 5: World Momentum
- Add ticking clocks system
- Implement off-screen event generation
- Connect world state to prompt injection

---

## Open Questions

1. **Local model for state clerk?** Haiku works, but a local 7B might be sufficient and cheaper for structured extraction.

2. **How aggressive on document splitting?** Each clan as own file seems right. Each Satara member? Maybe overkill.

3. **Vignette retrieval trigger?** When does a vignette get pulled for vibes? Location match? Theme match? Explicit request?

4. **Clock granularity?** Real-time minutes? Abstract "turns"? Narrative beats?

5. **Multi-session persistence?** State log format for save/load across sessions?

---

## File Locations

- Glossary: `glossary_data.yaml`
- Glossary tool: `glossary.py`
- This design doc: `DESIGN - GM Agent Architecture.md`
- Documents: `*.md` (to be restructured per Phase 1)

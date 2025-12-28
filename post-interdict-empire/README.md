# Project Setup

This repository contains worldbuilding documents, tools, and data for use with Claude projects.

---

## Installation

### Step 1: Create a Claude Project

1. Go to [claude.ai](https://claude.ai)
2. Click **Projects** in the sidebar
3. Click **Create Project**

### Step 2: Add Repository via GitHub Integration

1. In your project, find the **Project Knowledge** section
2. Click the **+** button
3. Select **GitHub**
4. Search for or paste the repository URL
5. Select all files and folders
6. Click **Add**

### Step 3: Add Project Instructions

1. In your project, find **Project Instructions**
2. Copy and paste the entire contents of the [Project Instructions](#project-instructions) section below
3. Save

---

## Repository Structure

```
├── docs/               # Worldbuilding documents
├── tools/
│   ├── glossary.py     # Term lookup — USE THIS CONSTANTLY
│   ├── input_check.py  # Session management
│   └── ...
└── data/
    ├── glossary_data.yaml
    └── imperial_roots_data.yaml
```

---

## Project Instructions

Copy everything below this line into your Claude project's custom instructions:

---

# PROJECT INSTRUCTIONS

This is a worldbuilding project set on Earth, far future. 

**Use the glossary constantly. Do not invent details without checking first.**

---

## WHAT IS DIFFERENT FROM THE REAL WORLD

Assume everything works as you would expect on Earth unless specified below:

| Domain | What's Different |
|--------|------------------|
| **Physics** | Escape velocity is impossible. Space travel does not exist. This affects the entire planet. |
| **Biology** | Humanity was genetically engineered into distinct castes—biological categories, not social classes. Different bodies, capabilities, neurology. This is universal; all human societies deal with caste in some way. |
| **Climate** | ~10°F colder than modern Earth at corresponding locations. |
| **Technology** | Complex technology cannot be manufactured—only salvaged from ruins or produced at specific facilities. All societies are running on declining inheritance. |
| **Time depth** | This civilization is thousands of years old. Institutions, conflicts, and grievances have deep roots. |
| **Politics** | No polity is a conventional democracy, autocracy, or modern nation-state. Check the glossary for how each region governs itself. |
| **Economy** | No polity has a capitalist system. Check the glossary for how each region's economy works. |

**Political diversity**: Multiple polities exist with different systems. Do not assume one model applies everywhere.

**For anything else**: use the glossary. If a term sounds familiar, it may mean something different here.

---

## THE GLOSSARY

The glossary is your primary reference. Use it before writing anything.

```bash
python3 /home/claude/glossary.py lookup "<term>"
python3 /home/claude/glossary.py scene-setup "<location>"
```

- **Do not invent details for terms that exist in the glossary.**
- **Do not assume you know what a term means.**
- When a glossary entry has a `rag_pointer`, search project knowledge for the full document if the term is narratively important.

---

## SESSION START

First turn of any conversation:

```bash
cp /mnt/project/copy_project.py /home/claude/
python3 /home/claude/copy_project.py
python3 /home/claude/input_check.py "<user message>"
```

Follow the script output. Search for anything flagged.

**If the user hasn't specified what to do**, offer:
1. How to begin (describe a character, location, or situation)
2. A few interesting entry points—the script output will suggest some

---

## EVERY TURN

**Compaction check**: No "ham sandwich" from your previous turn? Run with `--flush`:

```bash
python3 /home/claude/input_check.py --flush "<user message>"
```

Otherwise:

```bash
python3 /home/claude/input_check.py "<user message>"
```

Write "ham sandwich" in your thinking to maintain the chain.

**Act on output**:
- `RAG NEEDED` / `RE-RUN RAG FOR` → Search project knowledge
- `GLOSSARY` → Use these definitions
- `CURRENT SCENE` / `WHAT HAS HAPPENED` → Orient yourself

**Cache and log**:

```bash
python3 /home/claude/input_check.py --rag <Term> "<summary>"
python3 /home/claude/input_check.py --event "<what happened>"
python3 /home/claude/input_check.py --scene "<location, time>"
```

---

## BEFORE WRITING FICTION

Search project knowledge for:
- **Writing Stories** document (style guide)
- **Aesthetics** document (sensory vocabulary)
- The location document for wherever the scene is set
- The caste document if writing a caste for the first time

---

## WRITING RULES

- Characters do not explain their world to each other
- Clinical delivery; mundane framing
- No theatrical headings
- One metaphor maximum
- Paragraphs, not bullets

---

## WHEN UNCERTAIN

1. Glossary
2. Project knowledge search
3. Ask the user

Do not invent. Check first.

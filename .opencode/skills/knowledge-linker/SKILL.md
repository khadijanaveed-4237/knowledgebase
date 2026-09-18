---
name: knowledge-linker
description: Identifies meaningful relationships between existing knowledge notes and suggests links between them. Uses observable evidence from note content, tags, and existing links. Trigger keywords: link knowledge, connect notes, find relationships, suggest links, knowledge graph, link notes.
---

# Knowledge Linker

## Purpose

Identify meaningful relationships between existing knowledge notes in the PKM vault and suggest links between them. Helps connect related knowledge without modifying notes.

## When to Use

- "Find related knowledge notes"
- "Suggest links between my notes"
- "What notes relate to X?"
- "Build a knowledge graph from my notes"
- "Discover connections in my PKM"

## What It Does

- Reads knowledge notes from `pkm/Knowledge/`
- Identifies candidate relationships using observable evidence
- Suggests meaningful links with confidence and evidence
- Distinguishes existing links from new suggestions
- Reports when evidence is insufficient

## What It Does Not Do

- Modify, delete, merge, or rename notes
- Analyze software architecture → use **architecture-analysis**
- Find project bugs or code quality issues → use **project-analysis**
- Create or organize PKM notes → use **pkm**
- Invent relationships without evidence
- Replace manual curation

---

## How It Works

1. **Locate notes** — Scan `pkm/Knowledge/` for markdown files
2. **Extract metadata** — Title, tags, summary, notes, existing wikilinks
3. **Identify concepts** — Key terms from titles, headings, tags, content
4. **Compare notes** — Find pairs with meaningful evidence
5. **Check existing links** — Avoid suggesting links that already exist
6. **Classify relationship** — Assign type (see Relationship Types)
7. **Gather evidence** — Tag each claim as [FACT], [INTERPRETATION], or [INSUFFICIENT EVIDENCE]
8. **Assign confidence** — High / Medium / Low based on evidence strength
9. **Present suggestions** — Clear, human-readable output

---

## Relationship Types

| Type | Meaning |
|------|---------|
| **broader concept** | Target is a more general category |
| **narrower concept** | Target is a more specific sub-topic |
| **related concept** | Topics are meaningfully related |
| **prerequisite** | Target should be understood first |
| **example of** | Source is an instance of target |
| **depends on** | Source requires target |
| **contrasts with** | Topics are usefully compared |
| **extends** | Source builds upon target |

---

## Evidence Rules

- **[FACT]** — Directly observed: matching tags, explicit wikilinks, shared terminology in content
- **[INTERPRETATION]** — Reasonable inference from multiple evidence points
- **[INSUFFICIENT EVIDENCE]** — Cannot establish meaningful relationship

**A single shared word does NOT prove a relationship.** Requires multiple evidence points or clear semantic connection.

- Title similarity + tag overlap + content references → stronger evidence
- Same tag only → weak evidence, report [INSUFFICIENT EVIDENCE] unless supported

---

## Output Format

```
# Knowledge Link Suggestions

## Note: `Note Title`

### Existing Links
- `[[Existing Note]]` — already linked

### Suggested Links

#### Target: `Related Note`
- Relationship: broader concept
- Confidence: High
- [FACT] Both notes share tags: `python`, `web-framework`
- [FACT] `Note Title` contains wikilink to `Related Note` in References
- [INTERPRETATION] `Related Note` is a broader category

#### Target: `Another Note`
- Relationship: related concept
- Confidence: Medium
- [FACT] Both discuss async patterns
- [INTERPRETATION] Concepts are complementary

#### Target: `Unrelated Note`
- Relationship: [INSUFFICIENT EVIDENCE]
- Only shared word: "Python" — no semantic connection

---
```

---

## Limitations

- Static analysis only — cannot infer intent
- Only operates on `pkm/Knowledge/` by default
- Weak evidence → [INSUFFICIENT EVIDENCE] (not a failure)
- Does not modify notes — suggestions only
- May miss relationships requiring domain knowledge
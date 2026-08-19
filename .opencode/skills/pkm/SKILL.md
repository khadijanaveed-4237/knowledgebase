---
name: pkm
description: Manages the PKM knowledge base — captures ideas into pkm/Ideas, creates knowledge notes in pkm/Knowledge, tracks projects in pkm/Projects, and logs research in pkm/Research, using the templates in pkm/Templates. Use when the user wants to capture an idea, write or save a note, add knowledge, start or update a project, begin or record research, or organize the vault. Trigger keywords: idea, note, knowledge, capture, save this, research, project, PKM, vault, template. Use ONLY for notes inside the pkm/ folder, not for general tasks.
---

# PKM Skill

Manage the personal knowledge management (PKM) vault at `pkm/`.

## Purpose

Keep the vault consistent and maintainable:

- **Ideas** — capture raw, unprocessed ideas (`pkm/Ideas/`).
- **Knowledge** — distilled, permanent knowledge notes (`pkm/Knowledge/`).
- **Projects** — project goals, tasks, and progress logs (`pkm/Projects/`).
- **Research** — research questions, hypotheses, and findings (`pkm/Research/`).
- **Templates** — canonical note skeletons in `pkm/Templates/`. Never invent a
  new structure; always derive from the matching template.

## When to invoke

Invoke when the request involves creating, updating, or organizing PKM notes:

- "Capture this idea" → Idea note.
- "Write a note about X" / "Save this knowledge" → Knowledge note.
- "Set up a project log" / "Update the project" → Project note.
- "Research X" / "Log findings" → Research note.
- "Organize / fix / review the vault" → Organization or review workflow.

Do NOT invoke for unrelated coding or chat requests.

## Actions (workflow)

### 1. Classify the request

Map the request to exactly one note type: Idea, Knowledge, Project, or Research.
If it fits several, choose the dominant one and note the others in
`references` or `related`.

### 2. Read the template

Read the matching file from `pkm/Templates/`:

| Type      | Template                | Target folder       |
| --------- | ----------------------- | ------------------- |
| Idea      | `pkm/Templates/ideas.md`     | `pkm/Ideas/`        |
| Knowledge | `pkm/Templates/knowledge.md` | `pkm/Knowledge/`    |
| Project   | `pkm/Templates/projects.md`  | `pkm/Projects/`     |
| Research  | `pkm/Templates/research.md`  | `pkm/Research/`     |

### 3. Create the note

- Filename: `YYYY-MM-DD-kebab-case-slug.md` (e.g. `2026-08-19-fastapi-deployment.md`).
- Copy the template verbatim; keep every section heading and comment.
- Replace `{{title}}` with the note title and `{{date}}` with today's date
  (YYYY-MM-DD).
- Fill all frontmatter fields: `tags` (kebab-case), `status`, `author`,
  `sources`, `references`, plus type-specific fields (`mood`, `related`,
  `aliases`, `deadline`, `priority`, `milestones`, `lead`, `findings`).
- Set `last_audited` to today's date when creating or editing.

### 4. Fill the body

- Idea: raw description, "Why now", and smallest next steps.
- Knowledge: one-paragraph `Summary`, distilled `Notes`, and references.
- Project: `Objective`, actionable `Tasks`, `Milestones`, and `Notes / Log`.
- Research: `Question`, `Hypothesis`, chronological `Log / Findings`, `Sources`.

### 5. Cross-link

- Link related notes with `[[wikilink]]` in `references` / `related`.
- Before linking, search the vault to avoid duplicating an existing note; if a
  note already covers the topic, update it instead of creating a new one.

### 6. Update changelog

Append an entry to `Changelog` for every change:

```
- `YYYY-MM-DD` — Created. / Updated: <what changed>.
```

### 7. Review (only when asked)

For architecture or quality review, delegate to the `kb-architect`,
`kb-editor`, or `kb-tech-lead` subagents (they review only and never edit).
The skill itself creates and edits notes directly.

## Output

Report concisely:

1. What was created or updated (path, type, status).
2. Any frontmatter decisions worth noting (tags, status, links).
3. Duplicates found and how they were handled.
4. Suggested next steps (e.g. "review when the idea matures").

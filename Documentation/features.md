# Features

## Major Project Features

### 1. Personal Knowledge Management Vault
- **Structured note templates** — Four canonical template types (ideas, knowledge, projects, research) with YAML frontmatter ensuring consistency
- **Status tracking** — Each note supports status field (seed/sprouting/evergreen for ideas; fleeting/literature/permanent for knowledge; planning/active/done/archived for projects; active/on-hold/completed for research)
- **Wikilink support** — Notes can reference other notes using `[[wikilink]]` format, enabling knowledge graph construction
- **Category organization** — Notes are stored in dedicated subdirectories (Ideas, Knowledge, Projects, Research) for natural categorization
- **Searchability** — All notes are plain Markdown, making them searchable with standard tools

### 2. Deterministic Project Analysis Pipeline
- **8-stage evidence-based pipeline** — Inspect structure → Identify project type → Understand architecture → Find problems → Find causes → Evaluate impact → Recommend solutions → Create analysis report
- **Fact-first ordering** — Facts are reported before evidence, verification is computed before human-readable explanations
- **No guesses as facts** — Insufficient evidence is explicitly reported as "insufficient", never invented
- **Deterministic output** — Directory traversal and report lists are sorted; identical input produces byte-identical JSON and Markdown on every system
- **Read-only operation** — The target project is never modified, written to, or had dependencies installed

### 3. Technology Detection and Recognition
- **Manifest-based type detection** — Recognizes ecosystems from actual manifest files (package.json, pyproject.toml, Cargo.toml, go.mod, etc.) — never from prose or docs
- **Import-based technology recognition** — Identifies known libraries and frameworks from import statements in source code
- **Language detection by file extension** — Maps file extensions to programming languages
- **Multiple ecosystem handling** — When multiple ecosystems are detected, the primary is heuristically chosen with explicit confidence labeling

### 4. Comprehensive Problem Detection
- **Missing documentation** — Detects absent README.md and LICENSE files at project root
- **Large file identification** — Flags source files exceeding 200KB threshold, with function/class/import counts and responsibility detection
- **Code marker detection** — Finds TODO, FIXME, HACK markers and bare/silent exception handlers (`except: pass`)
- **Possible secret detection** — Heuristically identifies credential-like assignments (e.g., `api_key = "..."`) with strength classification (placeholder/possible_credential/strong_credential_signature)
- **Never exposes actual secrets** — Only reports metadata: file, line number, key name, value length, strength category — the secret value itself is never printed

### 5. Evidence-Classified Findings
- **Plausibility tags** — Each claim is labeled as `fact` (directly observed), `assumption` (heuristic inference), or `insufficient` (not verifiable)
- **Confidence levels** — `high` (multiple strong observations), `medium` (supported by observations), `low` (weak heuristic/single observation)
- **Verification status** — `verified` (evidence supports claim), `partially_verified` (some evidence, gaps remain), `unverified` (insufficient evidence)
- **Structured evidence items** — Each finding contains typed evidence with descriptions and line numbers

### 6. Cause Analysis with Conservative Classification
- **Evidence-supported causes** — Directly observable from the project (e.g., "File not found in project root listing")
- **Possible causes** — Plausible but not established by static inspection (e.g., "Tests may exist outside detected naming patterns")
- **Unknown/insufficient** — Cause cannot be determined from static inspection alone
- **No historical speculation** — The analyzer does not state reasons like "responsibilities grew over time"

### 7. Heuristic Impact Assessment
- **Severity estimation** — Heuristic severity labels (high/medium/low) based on category, evidence strength, and context
- **Explicit hedging** — Severity reasoning explicitly states what static inspection cannot determine
- **Assumption capping** — If plausibility is "assumption", severity is capped at medium and reasoning notes the cap
- **Strong credential signatures** — May reach high severity; placeholder patterns default to low

### 8. Recommendations Connected to Findings
- **Finding-backed recommendations** — Each recommendation is connected to a specific finding category
- **Verification-step statements** — Each recommendation states the next human verification step
- **Insufficient evidence guidance** — Recommendations for uncertain cases suggest verification rather than assuming a solution
- **Category-specific advice** — Recommendations tailored to missing documentation, large files, code markers, possible secrets, etc.

### 9. Dual Output Formats
- **JSON (machine-readable source of truth)** — Pure structured JSON printed to stdout with `--json` flag; also written as report JSON in the analysis output
- **Markdown (human-readable rendering)** — Formatted report written to `ANALYSIS.md` in the output directory
- **Consistency guarantee** — JSON and Markdown must not contain conflicting information
- **Summary rendering** — Additional Markdown summary with project type, languages, technologies, symbols, testing, and limitations

### 10. AI Agent Routing
- **AGENTS.md skill routing** — User questions are directed to the appropriate skill (pkm, project-analysis, architecture-analysis, knowledge-linker)
- **Seven specialized agents** — Project Detective, What-If Simulator, Chaos Tester, Assignment Reviewer, KB Architect, KB Editor, KB Tech Lead
- **Read-only agent behavior** — All agents deny edit, bash, webfetch, and websearch permissions
- **Evidence-based routing** — Agent descriptions and trigger keywords guide users to the right skill for their question

## How These Features Help Users

| Feature | User Benefit |
|---|---|
| Knowledge vault templates | Reduces cognitive overhead of deciding how to capture new information |
| 8-stage analysis pipeline | Provides comprehensive, structured project assessment without manual effort |
| Technology detection | Quickly understands what a project uses without reading documentation |
| Problem detection | Automatically flags common maintainability and security concerns |
| Evidence classification | Helps users distinguish what's observed from what's inferred |
| Conservative cause analysis | Prevents incorrect assumptions about why problems exist |
| Heuristic impact assessment | Gives a sense of relative priority without overclaiming |
| Finding-backed recommendations | Provides actionable next steps connected to specific observations |
| JSON + Markdown output | Shareable reports in both human-readable and machine-parseable formats |
| Agent routing | Knows which AI skill to invoke for different types of questions |
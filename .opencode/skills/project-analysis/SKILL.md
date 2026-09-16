---
name: project-analysis
description: Analyzes a software project read-only and produces an evidence-based, structured report. Use when the user asks to audit, review, analyze, inspect, or understand a codebase, or mentions the project-analysis workflow. Every finding must distinguish observed fact from inference, carry a confidence level, and pass verification before claims are made. Trigger keywords: project analysis, analyze project, codebase review, architecture review, audit code, find bugs, review repo, understand this project.
---

# Project Analysis

Analyze a target project **read-only** and produce a structured, evidence-based report. The Python analyzer answers **"What did we actually observe?"** and the LLM interprets **"What does this evidence mean?"**

## Purpose

This skill performs deterministic, read-only analysis of a software project. It collects observable evidence (files, sizes, patterns, imports, manifests), distinguishes facts from inferences, attaches confidence levels, verifies claims before explanations are produced, and produces both machine-readable JSON and human-readable Markdown reports.

## When to Invoke

Use this skill when the user asks to:

- Analyze, audit, review, or inspect a project or codebase
- Understand project architecture, structure, or technology stack
- Find problems, bugs, or code smells
- Review a repository or codebase
- Assess project health or code quality

## Inputs

- `<target-directory>`: The project root to analyze (read-only)
- `--output <dir>`: Output directory for the report (default: cwd)
- `--json`: Print structured JSON to stdout

## Pipeline

The analyzer implements an 8-stage pipeline that follows an evidence-first ordering:

1. **Inspect files and structure** — Walk the tree, count files/dirs/sizes, group by extension (deterministic facts only)
2. **Identify project type** — Detect ecosystem from manifest files; primary type is heuristic when multiple ecosystems are present
3. **Understand architecture** — Language breakdown, entry-point candidates, likely directory roles, config/test/db files; no architectural pattern is claimed unless strongly supported
4. **Find problems** — Detect missing files, large files, code markers, and possible secrets; each finding carries typed evidence items
5. **Find causes** — Determine evidence-supported causes versus possible causes; unknown or insufficient causes are explicitly stated
6. **Evaluate impact** — Conservative severity estimate; severity is never measured, only heuristically estimated
7. **Recommend solutions** — Connected to findings; each recommendation states what it depends on and what the next verification step should be
8. **Create analysis report** — Assemble JSON (source of truth) and render Markdown

The key ordering is: **facts first → evidence attached → verification computed → human-readable explanation produced last**.

## Strict Rules (MANDATORY)

### Evidence Rules

1. **Every finding must have evidence.** Each finding contains structured evidence items with type and description. Never present a claim without at least one evidence item.
2. **Never present assumptions as facts.** Every claim must be tagged with its plausibility: `fact` (directly observed), `assumption` (heuristic inference), or `insufficient` (not verifiable).
3. **Never invent files, dependencies, architecture, causes, or behavior.** If evidence is insufficient, explicitly say so.
4. **Never upgrade an assumption to a fact** without new, real evidence.
5. **Recommendations must be based on findings.** Do not recommend fixes for problems that were not established. Each recommendation states what it depends on (`based_on`) and the expected next verification step.
6. **Causes must be conservative.** Only call something an evidence-supported cause when the project actually contains evidence for it. If the cause cannot be established from static inspection, say so.
7. **Security findings require manual verification** unless confirmed by external tooling. Heuristic secret detection produces candidates, not confirmations.
8. **Never print actual secret values** in any output. Only expose safe metadata: file, line number, key name, value length, detection type, confidence.

### Read-Only Rules

9. **The target project is read-only.** The analyzer never creates, modifies, or deletes files inside the target.
10. **Reports are written outside the target project.** Output defaults to cwd; `--output` overrides.
11. **Preserve the target untouched.** Only the report path is written to.

### Interpretation Rules

12. **Severity is estimated, never measured.** Severity labels are heuristic estimates, not facts. Severity reasoning explicitly states what the analyzer cannot determine from static inspection.
13. **A lone marker (TODO/FIXME/HACK) is not proof of high impact.** These are informational signals, not measured defects.
14. **When multiple ecosystems are present**, the primary type is a heuristic assumption. State the confidence and note the coexistence.
15. **Missing files are observations, not automatically confirmed defects.** "README.md not found" is a fact. "Documentation is inadequate" is NOT automatically a fact.

### What the Python Analyzer Does NOT Do

16. **It does not understand business intent, historical reasons, or runtime behavior.** These require human review.
17. **It does not claim architectural patterns** (MVC, layered, microservices) unless supported by strong structural evidence.
18. **It does not diagnose what caused a file to grow.** "Responsibilities grew over time" is NOT stated by the analyzer.
19. **Different LLMs reviewing the same analyzer output should arrive at similar conclusions**, because the output is evidence-grounded, not interpretation-dependent.

## Evidence Model

Every finding carries structured evidence items. Each item has:

- **type**: What was observed (e.g., `file_absent`, `file_size`, `matched_pattern`, `function_count`, `class_count`, `multiple_responsibilities`)
- **description**: Human-readable description of the observation (e.g., includes file name and line number where available)

Examples:
- `[file_absent] README.md not found in project root file listing`
- `[file_size] File size is 350000 bytes (threshold: 200000 bytes)`
- `[matched_pattern] Credential-like assignment for key 'api_key' in config.py at line 5`
- `[multiple_responsibilities] File appears to contain: application_setup, api_routes, data_model`

**Never invent evidence.** Only record what the analyzer actually observed.

## Confidence Model

Every finding carries a confidence level:

| Level | Meaning |
|---|---|
| `high` | Directly verified from multiple strong observations |
| `medium` | Supported by observations but not fully confirmed |
| `low` | Weak heuristic; single observation or inference-based |
| `insufficient` | No meaningful evidence available for this claim |

Confidence is an **analyzer estimate**, not a scientific measurement. It reflects the strength of the evidence, not the certainty of the conclusion.

## Verification Model

Each finding passes through verification **before any explanation is produced**:

| Status | Meaning |
|---|---|
| `verified` | Evidence directly supports the claim |
| `partially_verified` | Some evidence exists, but gaps remain |
| `unverified` | Insufficient evidence to confirm the claim |

Verification is determined from plausibility, confidence, and evidence presence alone. It does not depend on the interpretation layer (causes, impact, or recommendations).

## Cause Analysis

Causes are conservative. Each cause is classified as:

- **Evidence-supported**: directly observable from the project (e.g., "File not found in the project root listing")
- **Possible**: plausible explanation but not established by static inspection (e.g., "Tests may exist outside the detected naming patterns")
- **Unknown / insufficient evidence**: the analyzer cannot determine the cause from static inspection alone

**Do not state historical or intentional explanations as causes.** For example, for large files, the analyzer does NOT claim "responsibilities grew over time." It states the size was observed and the actual historical cause is unknown from static inspection.

## Output Format

### JSON (Machine-Readable Source of Truth)

The JSON output contains structured information for:

- `target`: Project root path
- `pipeline`: Pipeline description (evidence-first flow)
- `read_only_target`: Confirmation of read-only behavior
- `stages.1_structure`: File counts, sizes, extensions, directory tree
- `stages.2_project_type`: Ecosystems, evidence files, primary type, confidence
- `stages.3_architecture`: Languages, entry points, likely directories, config/test/db files
- `stages.4_findings`: Array of findings, each containing:
  - `problem`: Title, category, plausibility, confidence, evidence items (including line numbers for secrets), context
  - `causes`: Verified/possible/unknown causes with explicit classification
  - `verification`: verified / partially_verified / unverified
  - `impact`: Severity, severity confidence, reasoning (hedged)
  - `recommendations`: Recommendation text, confidence, based_on, next step
- `summary`: Total findings, severity counts, verification counts

### Markdown (Human-Readable Rendering)

The Markdown report is a rendering of the same JSON data. It includes:

- Scope and method
- Project facts with verification status
- Findings with evidence, causes, impact, and recommendations
- Code summary (project type, languages, technologies, symbols, testing)
- Legend explaining plausibility, confidence, and verification

**JSON and Markdown must not contain conflicting information.**

## How an LLM Should Interpret the JSON

1. **Read the evidence items first.** What did the analyzer actually observe?
2. **Check the plausibility.** Is this a fact, assumption, or insufficient evidence?
3. **Check the confidence.** How strong is the evidence?
4. **Check the verification.** Was the claim verified, partially verified, or unverified?
5. **Read the causes.** Are they evidence-supported, possible, or unknown?
6. **Read the impact reasoning.** Why was this severity assigned? What could make this reasoning wrong?
7. **Read the recommendations.** Are they connected to established findings? Do they state what the next verification step is?
8. **Add your own reasoning** on top of the evidence, but preserve the tags and never upgrade assumptions to facts without new evidence.

## Limitations

- The analyzer uses heuristic pattern matching, not deep semantic analysis.
- Secret detection is heuristic and produces candidates, not confirmations.
- Architecture patterns (MVC, layered, microservices) are NOT claimed unless strongly evidenced.
- The analyzer cannot determine business impact, runtime behavior, code correctness, or historical reasons for code structure.
- Large file analysis counts functions/classes approximately via regex, not AST parsing.
- The analyzer only reads files; it cannot run the project or execute tests.
- Developer intentions, why a file was structured a certain way, and manual testing practices outside the repository cannot be determined statically.

## Examples

### Example: Missing README

```json
{
  "title": "No README/README.md at project root",
  "category": "missing_documentation",
  "plausibility": "fact",
  "confidence": "high",
  "evidence": [
    {"type": "file_absent", "description": "README.md not found in project root file listing"},
    {"type": "file_absent", "description": "README not found in project root file listing"}
  ],
  "verification": "verified"
}
```

**What this means:** The analyzer confirmed the file is absent. Whether this is actually a problem depends on context (the LLM should interpret this, not the analyzer).

### Example: Possible Secret

```json
{
  "title": "Possible hardcoded secret in config.py",
  "category": "possible_secret",
  "plausibility": "fact",
  "confidence": "medium",
  "evidence": [
    {"type": "matched_pattern", "description": "Credential-like assignment for key 'api_key' in config.py at line 5", "line": 5}
  ],
  "context": {
    "matched_key": "api_key",
    "value_length": 42,
    "strength": 1,
    "category": "possible_credential",
    "line": 5,
    "note": "Requires manual review; never print the actual secret value."
  },
  "verification": "partially_verified"
}
```

**What this means:** A credential-like pattern was detected. The analyzer cannot determine if it is a real secret. Manual verification is required. The secret value itself is never exposed.

### Example: Large File with Multiple Responsibilities

```json
{
  "title": "Large file: src/app.py",
  "category": "large_file",
  "plausibility": "fact",
  "confidence": "medium",
  "evidence": [
    {"type": "file_size", "description": "File size is 350000 bytes (threshold: 200000 bytes)"},
    {"type": "function_count", "description": "Approximately 45 function definitions"},
    {"type": "class_count", "description": "Approximately 3 class definitions"},
    {"type": "multiple_responsibilities", "description": "File appears to contain: application_setup, api_routes, data_model"}
  ],
  "context": {
    "function_count": 45,
    "class_count": 3,
    "likely_responsibilities": ["application_setup", "api_routes", "data_model"]
  },
  "verification": "partially_verified"
}
```

**What this means:** The file exceeds the size threshold and appears to handle multiple responsibilities. The analyzer does NOT claim to know why the file grew. Whether refactoring would help depends on project context (the LLM should interpret this).

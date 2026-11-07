# Project Analysis Workflow

This project implements a complete **eight-stage evidence-based analysis workflow**. The workflow is deterministic, read-only, and follows an evidence-first ordering: facts are reported before evidence, verification is computed before human-readable explanations, and recommendations are connected to established findings.

## The Eight-Stage Workflow

### Stage 1: Inspect Files and Structure

**What it does:**
- Walks the project tree read-only, pruning ignored directories (`.git`, `node_modules`, `__pycache__`, `venv`, `dist`, `build`, etc.)
- Counts files, directories, and total size in bytes
- Lists top-level items and builds a directory tree
- Groups files by extension
- Records file paths and directory structure

**Output:**
- File count, directory count, total size in bytes
- Top-level directory and file listing
- Files grouped by extension
- Directory tree for structure analysis
- **Plausibility:** fact (directly observed)
- **Confidence:** high (fully deterministic directory traversal)
- **Verification:** verified (tree is directly observed)

**Evidence collected:**
- Absolute path of the target root
- Sorted list of all files relative to root
- Sorted list of all directories
- File count and directory count
- Total size in bytes
- Top-level items (files and directories at root level)
- Files grouped by extension (e.g., Python .py files, JavaScript .js files)
- Directory tree structure

---

### Stage 2: Identify Project Type

**What it does:**
- Recursively scans for manifest files that indicate project ecosystem
- Manifest files detected: `package.json`, `pyproject.toml`, `setup.py`, `Cargo.toml`, `go.mod`, `Gemfile`, `composer.json`, `pom.xml`, `build.gradle`, etc.
- Reports all detected ecosystems with their evidence files
- Determines a primary type heuristic when multiple ecosystems are present

**Output:**
- Verdict: "detected" or "INSUFFICIENT EVIDENCE"
- Evidence: list of manifest file paths found
- Ecosystems: list of detected ecosystems with name, evidence file, and plausibility
- Types: list of technology labels detected
- Primary: heuristic primary language/ecosystem choice
- Primary confidence: high if single ecosystem, low if multiple ecosystems
- Multiple ecosystems flag: boolean

**Evidence collected:**
- Manifest file paths found (e.g., `package.json`, `pyproject.toml`)
- Ecosystem names (e.g., "Node.js / JavaScript / TypeScript", "Python")
- Technology labels from manifest hints
- Whether multiple ecosystems were detected

**Plausibility:** fact (if manifests found) or assumption (if multiple ecosystems)
**Confidence:** high (single ecosystem) or low (multiple ecosystems, heuristic primary)
**Verification:** verified (if single ecosystem) or partially_verified (if multiple ecosystems)

---

### Stage 3: Understand Architecture

**What it does:**
- Summarizes languages by file extension count
- Counts source files (files with recognized source extensions)
- Identifies likely entry-point candidates (common filenames like `main.py`, `app.py`, `index.js`, `server.js`, `main.go`, `manage.py`, `cli.py`)
- Groups source files by top-level directory (e.g., `api/`, `frontend/`, `backend/`, `model/`, `util/`)
- Heuristically detects likely directory roles from directory names (api, route, controller, frontend, backend, model, util, config, test, database, doc, script)
- Identifies config files (`.yml`, `.yaml`, `.toml`, `.ini`, `.cfg`, `.env`, `Makefile`, `Dockerfile`, `.editorconfig`, etc.)
- Identifies test files (files with "test" or "spec" in the name)
- Identifies database files (`.sql`, `.sqlite`, `.db`, files with "migration" in the name)
- Identifies manifest files already found in stage 2

**Output:**
- Language breakdown (language name → count)
- Source file count
- Entry-point candidates (list of detected filenames)
- Source grouping by top-level directory
- Likely directory roles (e.g., `{"backend": ["src/"], "config": ["config/"]}`)
- Config files list
- Test files list
- Database files list
- Manifest files list

**Evidence collected:**
- File extensions and their counts
- Source file paths
- Entry-point candidate filenames
- Directory names and their mapped roles
- Configuration file paths
- Test file paths
- Database file paths

**Plausibility:** fact (directly observed from file extensions and names)
**Confidence:** high (fully observed counts and names)
**Verification:** verified (all entries directly from file listing)

---

### Stage 4: Find Problems

**What it does:**
- Heuristic scan for common project issues:
  - **Missing README/LICENSE/.gitignore** at project root
  - **No test files detected** (when source files exist but no test/spec files)
  - **Large source files** exceeding 200KB threshold, with function/class/import counts and responsibility detection
  - **Code markers** — TODO, FIXME, HACK comments and bare/silent exception handlers (`except: pass`)
  - **Possible hardcoded secrets** — Credential-like assignments (e.g., `api_key = "..."`) with strength classification
- Each finding carries typed evidence items with descriptions and line numbers
- Secret values are **never** printed; only safe metadata is exposed (key name, value length, strength category)

**Output:**
- Array of problem findings, each containing:
  - Title (e.g., "Large file: src/app.py")
  - Category (e.g., `large_file`, `code_marker`, `possible_secret`, `missing_documentation`)
  - Plausibility (fact/assumption/insufficient)
  - Confidence (high/medium/low)
  - Evidence items (typed observations with descriptions)
  - Context (safe metadata only — no secret values)
  - Verification status (computed in stage 6)
  - Impact (computed in stage 5)
  - Recommendations (computed in stage 7)

**Evidence types observed:**
- `file_absent` — "README.md not found in project root file listing"
- `file_size` — "File size is 350000 bytes (threshold: 200000 bytes)"
- `function_count` — "Approximately 45 function definitions"
- `class_count` — "Approximately 3 class definitions"
- `import_count` — "23 import statements"
- `multiple_responsibilities` — "File appears to contain: application_setup, api_routes, data_model"
- `matched_pattern` — "Credential-like assignment for key 'api_key' in config.py at line 5"
- `pattern_absent` — "No test/spec directory or files found in N source files"

**Plausibility:** fact (for all heuristic detections based on observed code)
**Confidence:** varies (high for direct observations, medium for single patterns, low for weak heuristics)
**Verification:** computed in stage 6 (verified/partially_verified/unverified based on evidence and confidence)

---

### Stage 5: Find Causes (Conservative)

**What it does:**
- Determines evidence-supported causes versus possible causes for each problem
- Classifies causes as:
  - **Evidence-supported** — Directly observable from the project (e.g., "File not found in the project root listing")
  - **Possible** — Plausible but not established by static inspection (e.g., "Tests may exist outside the detected naming/location patterns")
  - **Unknown/insufficient** — The cause cannot be determined from static inspection alone
- Explicitly states when the cause cannot be determined
- Does NOT state historical or intentional explanations (e.g., does NOT claim "responsibilities grew over time for a large file")

**Output for each problem:**
- Verified cause (directly observable)
- Possible causes (plausible but unestablished)
- Plausibility (fact/assumption/insufficient)
- Confidence (high/medium/low)
- Verification status (verified/partially_verified/unverified)
- Evidence supporting the cause classification

**Classification rules:**
- `missing_documentation`/`missing_configuration`: "File not found in project root listing" + possible alternative explanations
- `missing_tests`: "No test files or test dirs found" + possible causes (tests may exist outside detected patterns; testing may be manual/external)
- `large_file`: Size confirmed; if multiple responsibilities, notes that static inspection cannot establish how/why the file evolved
- `code_marker`: Pattern matched confirmed; marker type (TODO/FIXME/HACK) noted with its meaning
- `possible_secret`: Credential-like key assignment confirmed; possible causes (real credential; test/development value; placeholder missed by filters)
- Default: "No verified cause from available evidence" with "Unknown" classification

**Plausibility:** fact (for evidence-supported), assumption (for possible), insufficient (for unknown)
**Confidence:** varies (high/medium/low based on evidence strength)
**Verification:** verified (evidence directly supports), partially_verified (some evidence, gaps), unverified (insufficient)

---

### Stage 6: Evaluate Impact

**What it does:**
- Assigns a heuristic severity label (high/medium/low) to each problem
- Provides reasoning for the severity assignment
- Explicitly states what static inspection **cannot** determine
- Notes when severity is based on assumption and caps it appropriately

**Severity assignment logic:**
- `possible_secret` with strength >= 2 → high severity ("Strong credential signature; potential security risk")
- `possible_secret` with strength == 1 → medium severity ("Possible credential; requires manual review")
- `large_file` with multiple responsibilities → medium severity ("Large file with multiple likely responsibilities; actual maintenance impact is not measurable statically")
- `large_file` without multiple responsibilities → low severity ("Large file; static inspection cannot establish the maintenance impact")
- `code_marker` with silent exception → medium severity ("Silent exceptions may mask errors")
- `code_marker` without silent exception → low severity ("Markers are informational signals, not measured defects")
- `missing_tests` → medium severity ("No tests detected; maintainability risk is potential, not measured")
- `missing_documentation`/`missing_configuration` → low severity ("Missing file is a concern, not a confirmed defect")
- Assumption capping: if plausibility is "assumption", severity is capped at medium and reasoning notes the cap
- Severity confidence: M if analyzer confidence is H, otherwise L

**Output:**
- Severity (high/medium/low)
- Severity confidence (high/medium/low — based on the analyzer's confidence level)
- Reasoning (why this severity was assigned, with explicit hedging about what cannot be determined)
- Plausibility (always "assumption" for severity)
- Confidence (M or L based on analyzer confidence)
- Verification (always "unverified" — severity is estimated, not measured)
- Evidence ("Severity is a heuristic estimate.")

**Important notes on severity:**
- Severity is **estimated, never measured** — the report explicitly states this
- Strong credential signatures may reach high severity, but this requires manual verification
- A lone TODO/FIXME/HACK is NOT proof of high impact — these are informational signals
- Missing files are observations, not automatically confirmed defects
- Reasoning explicitly states what the analyzer **cannot** determine from static inspection

**Plausibility:** assumption (severity is always a heuristic estimate)
**Confidence:** M if the problem's confidence is H, otherwise L
**Verification:** unverified (severity is estimated, not measured from evidence)

---

### Stage 7: Recommend Solutions

**What it does:**
- Generates evidence-based recommendations connected to specific findings
- Each recommendation states what it depends on (`based_on`)
- Each recommendation states the expected next verification step
- For insufficient evidence cases, recommends verification rather than assuming a solution is certain

**Recommendation rules by category:**
- `missing_documentation`: "Add a README.md describing purpose and usage" or "Add a LICENSE appropriate to the project"
- `missing_configuration`: "Add a .gitignore for the detected language/deps"
- `missing_tests`: "Inspect the repository's testing conventions; add tests for critical behavior if testing is genuinely absent"
- `large_file`: "Review and, if appropriate, split the file; it may serve multiple responsibilities" or "Review whether the file size is justified; splitting is only worthwhile if maintainability is affected"
- `code_marker`: "Replace bare/silent exception handlers with targeted handling and logging" or "Resolve or track the TODO/FIXME/HACK item in the issue tracker"
- `possible_secret`: "Verify whether the credential-like value is a real secret; if so, rotate it and move it to a secret manager"
- Insufficient evidence: "Manual review of findings needed"

**Output per finding:**
- Recommendation text
- Confidence (M if responsibilities detected, L otherwise, for large_file; L for most other categories)
- Verification (always "unverified" at this stage — recommendations depend on human verification)
- Severity (from stage 6)
- `based_on` field explaining what the recommendation depends on (e.g., "File absence observed", "Size observed", "Heuristic match; manual verification needed")
- Plausibility (assumption for most recommendations)

**Plausibility:** assumption (recommendations are proposals, not established facts)
**Confidence:** varies (M/L based on evidence strength and category)
**Verification:** unverified (recommendations depend on human verification step)

---

### Stage 8: Create Analysis Report

**What it does:**
- Assembles the complete analysis report from all prior stages
- **Per-finding order:** facts and evidence (stages 1-4) come first, then verification (stage 6), then human-readable explanation (causes, impact, recommendations) produced last
- This ordering ensures that explanations never influence verification
- Includes a legend for plausibility, confidence, and verification
- Guarantees: read_only_target, no_guess_fill, evidence_required_for_fact, no_secret_values_exposed, structured_evidence, verification_per_finding, conservative_causes, deterministic_ordering, json_source_of_truth

**Output formats:**
- **ANALYSIS.md** — Human-readable Markdown report written to the output directory (defaults to cwd)
- **JSON (with `--json`)** — Pure structured JSON printed to stdout; the machine-readable source of truth
- **Summary** — Total findings, severity counts, verification counts

**Report sections:**
1. Target and pipeline
2. Inspect files and structure
3. Identify project type
4. Understand architecture
5. Findings (problem / causes / verification / impact / recommendations)
6. Code summary (project type, languages, technologies, symbols, data flow, dependencies, configuration, testing)
7. Legend (plausibility | confidence | verification)

**Guarantees:**
- `read_only_target: true` — Target project is never modified
- `no_guess_fill: true` — Insufficient evidence is reported as such, never invented
- `evidence_required_for_fact: true` — Every finding must have evidence; facts require evidence
- `no_secret_values_exposed: true` — Actual secret values are never printed
- `structured_evidence: true` — Findings contain typed evidence items (including line numbers)
- `verification_per_finding: true` — Each finding has a verification status
- `conservative_causes: true` — Causes are only "evidence-supported" when directly observable
- `deterministic_ordering: true` — Identical input produces identical output on every system
- `json_source_of_truth: true` — JSON and Markdown must not contain conflicting information

**Plausibility:** mixed (facts from stages 1-4, assumptions from stages 5-7)
**Confidence:** mixed (high for observed facts, medium/low for assumptions)
**Verification:** mixed (verified for facts, partially_verified/unchecked for assumptions/unverified)
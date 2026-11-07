# Usage Guide

This section explains how to use the project, interact with agents, run available scripts, and understand generated reports.

## Running the Project Analyzer

The core analysis tool is the Python script `analyze.py`, located at:

```
.popencode/skills/project-analysis/scripts/analyze.py
```

### Basic Usage

```bash
# From the project root, analyze a target directory:
python3 .opencode/skills/project-analysis/scripts/analyze.py <target-directory>
```

### Command-Line Options

| Option | Short | Description |
|---|---|---|
| `--output` / `-o` | | Specify output directory for the Markdown report (defaults to current working directory) |
| `--json` / `-j` | | Print structured JSON to stdout; also written as machine-readable JSON in the report output |
| `<target-directory>` | | The project root path to analyze (required) |

### Examples

**1. Basic analysis (Markdown report in current directory):**

```bash
python3 .opencode/skills/project-analysis/scripts/analyze.py ./my-project
```

**2. Basic analysis with custom output directory:**

```bash
python3 .opencode/skills/project-analysis/scripts/analyze.py ./my-project --output ./analysis-reports
```

**3. JSON output (machine-readable):**

```bash
python3 .opencode/skills/project-analysis/scripts/analyze.py ./my-project --json
```

**4. JSON + Markdown both:**

```bash
python3 .opencode/skills/project-analysis/scripts/analyze.py ./my-project --output ./analysis-reports --json
```

This produces:
- `./analysis-reports/ANALYSIS.md` — Human-readable Markdown report
- JSON printed to stdout
- Summary information on stderr

### Interpreting the Output

#### Markdown Report (`ANALYSIS.md`)

The Markdown report includes these sections:

1. **Target and pipeline** — Project root path, pipeline name, read-only confirmation
2. **Inspect files and structure** — File counts, directory counts, total size, extension breakdown, top-level items, directory tree
3. **Identify project type** — Primary type detected, ecosystems found, confidence level, plausibility (fact/assumption/insufficient)
4. **Understand architecture** — Language breakdown, source file count, entry-point candidates, likely directory roles, config/test/db files
5. **Findings** — All detected problems with:
   - Problem title and category
   - Plausibility (fact/assumption/insufficient)
   - Confidence (high/medium/low)
   - Verification status (verified/partially_verified/unverified)
   - Severity (high/medium/low, estimated)
   - Evidence (typed observations with file:line references)
   - Causes (evidence-supported, possible, or unknown)
   - Impact reasoning (why severity was assigned)
   - Recommendations (connected to findings, with next verification step)
6. **Code summary** — Project type, languages, technologies (observed imports), symbols (functions/classes), testing info, limitations
7. **Legend** — Explanation of plausibility, confidence, and verification tags

#### JSON Output

The JSON output is the **machine-readable source of truth**. It contains the same information as the Markdown report but in structured JSON format. Key top-level keys:

- `target` — Project root path
- `pipeline` — Pipeline description ("facts -> evidence -> verification -> explanation -> report (8 stages)")
- `read_only_target` — Boolean confirming read-only behavior
- `stages` — Object with keys `1_structure`, `2_project_type`, `3_architecture`, `4_findings`
- `summary` — Object with `total_findings`, `severity_counts` (high/medium/low), `verification_counts` (verified/partially_verified/unverified)
- `code_summary` — Object with project type, languages, technologies, symbols, testing, and limitations

Each finding in `stages[4_findings]` contains:
- `problem` — Title, category, plausibility, confidence, evidence, verification
- `causes` — Verified cause, possible causes, plausibility, confidence, verification
- `verification` — verified/partially_verified/unverified
- `impact` — Severity, severity_confidence, reasoning, plausibility, confidence, verification, evidence
- `recommendations` — Recommendation text, plausibility, confidence, verification, severity, based_on

## Interacting with AI Agents

This project includes seven specialized AI agents routed through `AGENTS.md`. Each agent is designed for a specific type of question or task.

### Accessing Agents

Agents are accessed through the OpenCode framework. When you ask a question, the system routes it to the appropriate agent based on trigger keywords.

### Agent Trigger Keywords

| User Question | Use Skill/Agent |
|---|---|
| "What problems does my project have?" | project-analysis / Project Detective |
| "Find bugs in my code" | project-analysis / Chaos Tester |
| "Review my codebase for issues" | project-analysis / Chaos Tester |
| "Analyze my project" | project-analysis (full 8-stage pipeline) |
| "What is the architecture of my project?" | architecture-analysis |
| "Explain the system structure" | architecture-analysis |
| "What are the components and how do they relate?" | architecture-analysis |
| "Show me the data flow" | architecture-analysis |
| "What architectural pattern does this follow?" | architecture-analysis |
| "How are responsibilities separated?" | architecture-analysis |
| "Find related knowledge notes" | knowledge-linker |
| "Suggest links between my notes" | knowledge-linker |
| "What notes relate to X?" | knowledge-linker |
| "Capture this idea" | pkm skill |
| "Create a knowledge note" | pkm skill |
| "Simulate what if I remove this module" | what-if-simulator agent |
| "Test this project for failure scenarios" | chaos-tester agent |
| "Investigate what this project does" | project-detective agent |

### Using the Project Detective Agent

The Project Detective investigates what a project is and how it works. To use:

1. Direct your question to the Project Detective agent
2. The agent will examine the project structure, identify the project type, map dependencies, and report findings
3. All findings are evidence-based with file:line references
4. The agent never modifies the project or accesses external resources

**Example question:**
> "Please investigate this project and tell me what it does, its structure, and any open questions."

### Using the What-If Simulator Agent

The What-If Simulator predicts how a project would behave under changed or adverse conditions. To use:

1. Provide a specific scenario as the premise (e.g., "What if the database connection fails?", "What if we remove the API route handler?", "What if load increases 10x?")
2. The agent will enumerate plausible outcomes, failure paths, and detection signals
3. Each outcome is labeled with a confidence level (high/medium/low)
4. The agent recommends a safe, reversible test for each scenario

**Example question:**
> "What would happen if the PostgreSQL database became unavailable? What components would break and how quickly would the failure be detected?"

### Using the Chaos Tester Agent

The Chaos Tester audits a project for failure scenarios, edge cases, and weaknesses. To use:

1. Direct your question to the Chaos Tester agent
2. The agent will examine the project for:
   - Silent exception handlers (`except: pass`)
   - TODO/FIXME/HACK markers
   - Large files with multiple responsibilities
   - Possible hardcoded secrets
   - Missing error handling patterns
3. Each finding includes:
   - The issue and `path:line` evidence
   - Impact assessment
   - A recommended safe test to confirm/refute the issue
4. The agent distinguishes between confirmed findings and assumptions needing verification

**Example question:**
> "Please audit this project for failure scenarios and edge cases. What weaknesses do you find and how could they be tested?"

### Using the PKM Skill

The PKM skill manages the Personal Knowledge Management vault. To use:

1. **"Capture this idea"** — Create a new idea note following the ideas.md template
2. **"Create a knowledge note"** — Create a new knowledge note following the knowledge.md template
3. **"Track this project"** — Create a new project note following the projects.md template
4. **"Log this research"** — Create a new research note following the research.md template

**Note creation templates** are in `pkm/Templates/`:
- `ideas.md` — The Idea, Why Now, Next Steps, Changelog; status: seed/sprouting/evergreen
- `knowledge.md` — Summary, Notes, References; status: fleeting/literature/permanent
- `projects.md` — Objective, Tasks, Milestones, Notes/Log; status: planning/active/done/archived
- `research.md` — Question, Hypothesis, Log/Findings, Sources; status: active/on-hold/completed

## Understanding Generated Reports

### Report Structure

When you run the analyzer, it generates two output files:

**1. `ANALYSIS.md`** (Markdown, human-readable)

Located in the output directory (defaults to current working directory). Contains:

- Report header with target path and pipeline info
- Section 1: Inspect files and structure (file counts, directory tree, extension breakdown)
- Section 2: Identify project type (detected ecosystem, confidence, plausibility)
- Section 3: Understand architecture (languages, entry points, directory roles, config/test/db files)
- Section 4: Findings (all detected problems with evidence, causes, impact, recommendations)
- Section 5: Code summary (project type, languages, technologies, symbols, testing, limitations)
- Section 6: Legend (plausibility, confidence, verification explanations)

**2. JSON output** (machine-readable)

Printed to stdout when `--json` flag is used. Also written as part of the analysis output. Contains the same data as the Markdown report but in structured JSON format, suitable for further processing or integration with other tools.

### Reading and Interpreting Findings

Each finding in the report follows this structure:

```
### 1. Large file: src/app.py
- **Category:** `large_file`
- **Plausibility:** `fact` | `assumption` | `insufficient`
- **Confidence:** `high` | `medium` | `low`
- **Verification:** `verified` | `partially_verified` | `unverified`
- **Severity:** `high` | `medium` | `low` (estimated, confidence: high/medium/low)
- **Impact reasoning:** (why this severity was assigned, with explicit hedging)
- **Evidence:**
  - `[file_size] File size is 350000 bytes (threshold: 200000 bytes)`
  - `[function_count] Approximately 45 function definitions`
  - `[class_count] Approximately 3 class definitions`
  - `[multiple_responsibilities] File appears to contain: application_setup, api_routes, data_model`
- **Context:** (safe metadata only — no secret values exposed)
  - `function_count: 45`
  - `class_count: 3`
  - `import_count: 23`
  - `likely_responsibilities: [application_setup, api_routes, data_model]`
- **Causes:**
  - Verified: (directly observable cause)
  - Possible: (plausible but unestablished causes)
- **Recommendations:**
  - (recommendation text) (confidence: `high`/`medium`/`low`)
```

### Verification Status Meaning

| Status | Meaning |
|---|---|
| `verified` | Evidence directly supports the claim |
| `partially_verified` | Some evidence exists, but gaps remain |
| `unverified` | Insufficient evidence to confirm the claim |

**Important:** Verification is computed from plausibility, confidence, and evidence presence **before** any human-readable explanation (causes, impact, recommendations) is produced. This ensures explanations never influence verification.

### Severity Meaning

- **high** — Serious issue (e.g., strong credential signature detected; requires immediate attention)
- **medium** — Moderate issue (e.g., large file with multiple responsibilities; possible credential; requires review)
- **low** — Minor concern (e.g., code markers are informational; missing file is a concern not a defect)

**Crucial:** Severity is **estimated, never measured**. The report's reasoning explicitly states what static inspection cannot determine. A severity label should not be treated as a confirmed fact.

### Limitations Section

The report always includes a "Limitations" section noting:

- Symbol purposes are name-based heuristics, not verified behavior
- No runtime call graph; imports only
- Secrets are never reported (detection only, no confirmation)
- The analyzer never runs or modifies the project
- Symbol purposes are name-based heuristics
- No deep semantic analysis; heuristic pattern matching only
- Architectural patterns (MVC, layered, microservices) are NOT claimed unless strongly evidenced
- The analyzer cannot determine business impact, runtime behavior, code correctness, or historical reasons for code structure

## Common Workflows

### Workflow 1: Initial Project Assessment

```bash
# Run a complete analysis of a project
python3 .opencode/skills/project-analysis/scripts/analyze.py ./my-project

# Review the generated ANALYSIS.md
# Focus on:
# - Project type and primary language
# - Total findings and severity distribution
# - Any possible secrets detected
# - Large files that may need refactoring
# - Missing documentation or tests
```

### Workflow 2: Focused Problem Investigation

```bash
# Analyze with JSON for programmatic access
python3 .opencode/skills/project-analysis/scripts/analyze.py ./my-project --json > analysis.json

# Use the JSON to filter or sort findings
# Focus on:
# - Findings with `verification: verified`
# - High severity findings
# - Possible secrets (require manual review)
# - Issues with `plausibility: fact` and `confidence: high`
```

### Workflow 3: Knowledge Base Integration

```bash
# After analyzing a project, use the PKM skill to capture insights:
# 1. Create a knowledge note summarizing the project type
# 2. Link to related knowledge notes using wikilinks
# 3. Record any identified problems or recommendations
# 4. Track follow-up actions from the analysis recommendations

# Example: "Capture this project analysis as a knowledge note"
```

### Workflow 4: Agent-Assisted Analysis

```bash
# Use specific agents for different perspectives:

# Project Detective — understand the project
opencode --agent project-detective "Investigate this project structure"

# What-If Simulator — test scenarios
opencode --agent what-if-simulator "What if the main API endpoint becomes unavailable?"

# Chaos Tester — find weaknesses
opencode --agent chaos-tester "Audit this project for failure scenarios"

# Combine insights from all three for a complete picture
```

## Known Limitations and Workarounds

### What the Analyzer Does NOT Do

1. **It does not understand business intent** — The analyzer cannot determine why a project was structured a certain way or what business problem it solves at a conceptual level.

2. **It does not claim architectural patterns** — MVC, layered, microservices, or other patterns are NOT claimed unless strongly structurally evidenced.

3. **It does not diagnose what caused a file to grow** — For large files, the analyzer does NOT claim "responsibilities grew over time." It only reports the size and observed responsibilities.

4. **It cannot determine runtime behavior** — The analyzer never executes the project or runs tests. It only performs static inspection.

5. **It cannot determine developer intentions** — Why a file was structured a certain way, what trade-offs were made, or what the development history was, cannot be determined statically.

6. **Secret detection is heuristic** — Pattern matching identifies credential-like assignments, but cannot confirm whether a value is actually a secret. Manual verification is always required.

### Workarounds

- **For business intent**: Review the project's README, documentation, or source code comments
- **For architectural pattern confirmation**: Manually review the component structure and communication patterns
- **For large file refactoring decisions**: Profile the application, measure startup time, memory usage, etc. (runtime measurements require manual effort)
- **For runtime behavior**: Run the project's test suite or execute it manually in a development environment
- **For developer intention**: Check git history, issue trackers, or developer documentation
- **For secret confirmation**: Manually review the flagged file and value at the reported line number (never print the actual value in reports)
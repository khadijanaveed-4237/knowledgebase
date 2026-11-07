# Technologies and Tools

This project uses the following technologies and tools. Each is explained in the context of how it contributes to the project's functionality.

## OpenCode (opencode)

**What it is:** The interactive CLI framework that powers this project's AI agent capabilities. OpenCode provides the agent framework, skill routing, and pipeline execution environment.

**How it's used in this project:**
- **Agent framework** — Seven specialized agents (Project Detective, What-If Simulator, Chaos Tester, Assignment Reviewer, KB Architect, KB Editor, KB Tech Lead) are defined within the OpenCode configuration
- **Skill routing** — `AGENTS.md` maps user questions to the appropriate skill based on trigger keywords
- **Pipeline execution** — The 8-stage project-analysis pipeline is implemented as an OpenCode skill and executed via `python3 .opencode/skills/project-analysis/scripts/analyze.py`
- **Configuration** — Agent permissions, temperatures, and modes are defined in YAML frontmatter within agent files under `.opencode/agents/`
- **Read-only discipline** — OpenCode enforces that all agents deny edit, bash, webfetch, and websearch permissions, ensuring the target project is never modified

**Key characteristics:**
- Deterministic output: identical input produces identical output on every system
- Evidence-first ordering: facts are reported before evidence, verification before explanation
- Structured evidence: all findings contain typed evidence items with descriptions and line numbers
- No guess as fact: insufficient evidence is explicitly reported as such, never invented
- JSON source of truth: machine-readable JSON and human-readable Markdown render the same data

## AI Agents

**What they are:** Seven specialized agents within the OpenCode framework, each designed for a specific role in project analysis and knowledge management.

**The agents:**

| Agent | Purpose |
|---|---|
| **Project Detective** | Investigates what a project is, how it's organized, and how it works. Reports evidence-based findings without modifying anything. |
| **What-If Simulator** | Simulates how a project would behave under changed or adverse conditions. Reports predicted outcomes without modifying anything. |
| **Chaos Tester** | Audits a project for failure scenarios, edge cases, and weaknesses. Reports what is found without modifying anything. |
| **Assignment Reviewer** | Reviews assignments and provides feedback (context-dependent skill). |
| **KB Architect** | Designs knowledge base structure and suggests improvements to the PKM vault organization. |
| **KB Editor** | Reviews documentation quality and suggests improvements to existing notes. |
| **KB Tech Lead** | Provides technical leadership guidance for the knowledge base and project analysis. |

**How they work together:**
- Agents are **read-only**: all deny edit, bash, webfetch, and websearch permissions
- User questions are routed to the appropriate agent via `AGENTS.md` trigger keywords
- Multiple agents can be used together for a complete picture (e.g., Project Detective + What-If Simulator + Chaos Tester)
- Each agent reports findings in a structured format with plausibility, confidence, and verification tags
- No agent can modify the target project or access external resources

**Permissions (all agents):**
- `edit: deny` — Never creates, modifies, or deletes files
- `bash: deny` — Never runs shell commands on the target
- `webfetch: deny` — Never accesses external URLs
- `websearch: deny` — Never searches the internet

## Markdown

**What it is:** A lightweight markup language used throughout the project for all knowledge notes, templates, and documentation.

**How it's used in this project:**

- **Knowledge notes** — All notes in `pkm/Knowledge/`, `pkm/Ideas/`, `pkm/Projects/`, and `pkm/Research/` are Markdown files with YAML frontmatter
- **Analysis reports** — The project analyzer generates `ANALYSIS.md` files in Markdown format
- **Skill documentation** — `AGENTS.md`, `SKILL.md`, and `pipeline.yaml` are all Markdown files
- **Project documentation** — The six documentation files you are creating are Markdown files

**Markdown structure in this project:**
- YAML frontmatter at the top of relevant files (between `---` delimiters)
- Wikilinks for note-to-note references (`[[wikilink]]` format)
- Consistent structure across template files (ideas.md, knowledge.md, projects.md, research.md)
- Analysis reports include a legend explaining plausibility, confidence, and verification

**Why Markdown:**
- Human-readable without rendering
- Widely supported by tools and platforms
- Enables wikilinks for knowledge graph construction
- Fits the evidence-first, structured approach of the project
- Can contain YAML frontmatter for machine-parsed metadata

## YAML

**What it is:** YAML (YAML Ain't Markup Language) is a human-readable data serialization format used throughout the project for configuration and pipeline definitions.

**How it's used in this project:**

- **Pipeline schemas** — `.opencode/skills/project-analysis/pipeline.yaml` defines the 8-stage analysis pipeline with:
  - Evidence tags (fact, assumption, insufficient)
  - Confidence levels (high, medium, low)
  - Verification statuses (verified, partially_verified, unverified)
  - Stage descriptions and guarantees
  - Run commands and input/output specifications

- **Agent configurations** — Each agent under `.opencode/agents/` has YAML frontmatter defining:
  - Description of the agent's role
  - Mode (subagent)
  - Temperature (0.1 for all analysis agents, ensuring deterministic behavior)
  - Permissions (all deny edit, bash, webfetch, websearch)

- **Skill definitions** — Each skill under `.opencode/skills/` has a `SKILL.md` file with YAML frontmatter containing:
  - Skill name
  - Description
  - Trigger keywords
  - When to invoke the skill
  - Inputs and pipeline description

- **Pipeline guarantees** — The pipeline.yaml includes guarantees like `read_only_target`, `no_guess_fill`, `evidence_required_for_fact`, etc.

**YAML syntax features used:**
- Key-value pairs with `key: value` format
- Lists with `- item` format
- Nested structures with indentation
- Boolean values (`true`, `false`)
- String values with quoted or unquoted format
- Tagged values for enums (e.g., `plausibility: fact`)

## Python

**What it is:** The primary programming language implementing the project's core functionality.

**How it's used in this project:**

- **analyze.py** — The central analysis script (550+ lines) is a Python3 application that implements the 8-stage project analysis pipeline
- **Pipeline implementation** — All 8 stages (inspect structure, identify project type, understand architecture, find problems, find causes, evaluate impact, recommend solutions, create analysis report) are implemented in Python
- **Report generation** — Both JSON and Markdown reports are generated from Python code
- **Heuristic pattern matching** — Regular expressions detect problem patterns (TODO/FIXME/HACK, silent exception handlers, possible secrets)
- **Import analysis** — Source code imports are parsed to identify technologies and dependencies
- **Symbol extraction** — Functions, methods, and classes are extracted from source files
- **File system operations** — Read-only walking of project trees, file size detection, manifest file identification

**Python features used:**
- Standard library only (`io`, `json`, `os`, `re`, `sys`) — no external dependencies required
- Regular expressions for pattern matching and text extraction
- Object-oriented organization with functions for each pipeline stage
- Deterministic sorting of directory traversal and report lists
- Structured data generation (JSON-compatible dictionaries)
- Read-only file system operations (no file creation/modification in target project)

**Evidence model in Python:**
- Every finding carries structured evidence items with type and description
- Each finding has plausibility (fact/assumption/insufficient), confidence (high/medium/low), and verification (verified/partially_verified/unverified)
- Secret values are never printed; only metadata (file, line, key name, length, strength category) is exposed
- The JSON output is the machine-readable source of truth; Markdown renders the same data

## Git

**What it is:** The version control system managing this project's source code.

**How it's used in this project:**

- **Repository hosting** — The project is hosted on Git at `/home/khadija/Desktop/khadija/`
- **Version tracking** — Changes to the project code, documentation, and knowledge notes are tracked
- **Gitignore** — `.gitignore` files manage which files are tracked vs. ignored
- **Agent and skill configurations** — The `.opencode/` directory has its own `.gitignore` to manage OpenCode-specific files

**Git structure:**
- Top-level repo at `/home/khadija/Desktop/khadija/` contains the `.opencode/` framework and `pkm/` vault
- The `pkm/` directory itself may be a git submodule or separate tracking
- Knowledge notes, projects, research, and ideas are tracked for version history
- All documentation and configuration files are version-controlled

**Why Git matters for this project:**
- Enables reproducible analysis — the same code version always produces the same analysis output
- Tracks changes to the analyzer itself (improvements to pattern detection, confidence models, etc.)
- Provides backup and history for knowledge notes and templates
- Allows collaboration or sharing of the PKM vault and analysis configurations

## GitHub

**What it is:** The cloud-based platform that extends Git's capabilities with issue tracking, pull requests, and remote repository hosting.

**How it's used in this project (contextual):**

- **Remote repository** — The project at `/home/khadija/Desktop/khadija/` is a git repository that could be pushed to GitHub for remote backup and collaboration
- **Issue tracking** — Project issues and feature requests could be managed via GitHub Issues
- **Pull requests** — Code changes and improvements to the analyzer, agents, or documentation would go through GitHub Pull Requests
- **Discussions** — Project discussions and knowledge sharing could happen via GitHub Discussions
- **Documentation hosting** — GitHub Pages could host the documentation created in this project

**GitHub integration points:**
- The `package.json` at `.opencode/package.json` references `@opencode-ai/plugin` version 1.18.32, which is the OpenCode plugin that integrates with the GitHub ecosystem
- Analysis reports could be shared via GitHub Gists or repositories
- Knowledge notes in Markdown format are well-suited for GitHub rendering
- The deterministic, reproducible nature of the analyzer makes it suitable for GitHub Actions workflows

**Note:** This project's primary operation is local/desktop-focused. GitHub integration is potential/optional rather than a core runtime dependency. The analyzer is read-only and never pushes to remote repositories without explicit user command.

## Summary of Technologies

| Technology | Role in Project | Key Files |
|---|---|---|
| **OpenCode** | Agent framework, skill routing, pipeline execution | `.opencode/AGENTS.md`, `.opencode/SKILL.md`, `.opencode/pipeline.yaml` |
| **AI Agents** | Seven specialized agents for project analysis and PKM | `.opencode/agents/*.md` |
| **Markdown** | Knowledge notes, analysis reports, documentation | `pkm/Knowledge/*.md`, `ANALYSIS.md`, all doc files |
| **YAML** | Pipeline schemas, agent configs, skill definitions | `*.pipeline.yaml`, `*.md` frontmatter, `SKILL.md` files |
| **Python** | Core analyzer implementation (8-stage pipeline) | `.opencode/skills/project-analysis/scripts/analyze.py` |
| **Git** | Version control for project code and knowledge notes | `.git/`, `package.json` |
| **GitHub** | Remote backup, collaboration, documentation hosting | Remote repo extension |
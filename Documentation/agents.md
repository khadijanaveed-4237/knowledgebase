# AI Agents

This project includes seven specialized AI agents, each designed for a specific role in project analysis and knowledge management. All agents are **read-only**: they deny edit, bash, webfetch, and websearch permissions. They report findings without modifying any project files.

## Available Agents

### 1. Project Detective

**Responsibilities:**
- Investigates what a project is, how it is organized, and how it works
- Maps the structure: directories, packages, modules, layers, and their responsibilities
- Identifies entry points (scripts, binaries, servers, CLI commands) and configuration files
- Traces dependencies: internal components and external packages or services
- Traces data flow: where data enters, how it is transformed, and where it ends up
- Reports what the project does today, not what it claims to do

**Working Methods:**
- Examines directory structure and file listings
- Identifies manifest files (package.json, pyproject.toml, Cargo.toml, etc.) to determine project ecosystem
- Reads configuration files to understand build systems and dependencies
- Analyzes file extensions to detect programming languages
- Traces import statements to understand dependencies

**Permissions:**
- `edit: deny` — Never creates, modifies, or deletes files
- `bash: deny` — Never runs shell commands on the target
- `webfetch: deny` — Never accesses external URLs
- `websearch: deny` — Never searches the internet

**Limitations:**
- Cannot determine runtime behavior or execution results
- Cannot access the network or external services
- Cannot infer business intent or historical reasons for code structure
- Must rely on on-disk evidence only

**Expected Output:**
- Scope and method (what was examined and how)
- What the project is (purpose, audience, current state)
- Structure and components (directories and responsibility of each)
- Entry points (how the project is started or invoked)
- Dependencies (internal and external, with where each is used)
- Data flow (the path data takes through the system)
- Open questions (what remains undetermined)

---

### 2. What-If Simulator

**Responsibilities:**
- Simulates how a project would behave under changed or adverse conditions
- Works out predicted outcomes without modifying anything
- Enumerates plausible outcomes including failure paths and rollback paths
- Identifies what would break outright, what would silently degrade, and what would be hard to detect
- For each outcome, names the preconditions that must hold and the observable signal that would reveal it
- Recommends a safe, reversible test for each scenario

**Working Methods:**
- Takes a proposed change, failure, or condition as the premise
- Considers scenarios: code changes, outages, load increases, dependency failures, configuration changes, hostile inputs
- Enumerates failure paths for each affected component
- Identifies rollback/recovery paths
- Labels each outcome with a confidence level (high/medium/low)

**Permissions:**
- `edit: deny` — Never creates, modifies, or deletes files
- `bash: deny` — Never runs shell commands on the target
- `webfetch: deny` — Never accesses external URLs
- `websearch: deny` — Never searches the internet

**Limitations:**
- Simulations are hypotheses, never established facts
- Cannot access runtime state or execute the project
- Cannot predict human behavior or decision-making
- Scenario confidence is limited to what's observable from the codebase

**Expected Output:**
- Scenario (the premise being simulated)
- Preconditions (what must be true for the scenario to apply)
- Expected impact (what happens, per affected component)
- Detection signal (how the outcome would be noticed, and how quickly)
- Confidence (high, medium, or low, with the reason)
- Recommended safe test (the smallest reversible check that would settle the question)

---

### 3. Chaos Tester

**Responsibilities:**
- Audits a project for failure scenarios, edge cases, and weaknesses
- Analyzes the target project read-only and looks for realistic ways it can fail or degrade
- Considers failure modes at every layer: input handling, state, concurrency, error paths, resource limits, and dependency boundaries
- For each issue, states the impact and the conditions under which it occurs
- Recommends a safe, non-destructive test that would confirm or refute the issue

**Working Methods:**
- Examines source code for silent exception handlers (`except: pass`)
- Looks for TODO/FIXME/HACK markers indicating known issues
- Identifies large files with multiple responsibilities
- Detects credential-like assignments that could be hardcoded secrets
- Analyzes error handling patterns and edge cases
- Checks for missing documentation or configuration that could cause runtime failures

**Permissions:**
- `edit: deny` — Never creates, modifies, or deletes files
- `bash: deny` — Never runs shell commands on the target
- `webfetch: deny` — Never accesses external URLs
- `websearch: deny` — Never searches the internet

**Limitations:**
- Cannot execute the project or test runtime behavior
- Cannot determine developer intent or why code was structured a certain way
- Heuristic secret detection produces candidates, not confirmations
- Cannot test concurrency, resource limits, or actual runtime failure modes
- Must distinguish between what the code does and what it intends to do

**Expected Output:**
- Scope and method (what was examined and how)
- Confirmed findings (issue, `path:line` evidence, impact, and a recommended safe test)
- Assumptions (plausible issues that need confirmation, with the test that would confirm them)
- Limitations (what could not be assessed from the available evidence)
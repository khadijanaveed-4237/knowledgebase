---
name: project-analysis
description: Analyzes a software project read-only and produces an evidence-based report. Use when the user asks to audit, review, analyze, inspect, or understand a codebase, or mentions the project-analysis workflow. Every finding must be tagged FACT, ASSUMPTION, or INSUFFICIENT EVIDENCE and cite a source (file:line or command output). Trigger keywords: project analysis, analyze project, codebase review, architecture review, audit code, find bugs, review repo, understand this project.
---

# Project Analysis

Analyze a target project **read-only** and produce a structured report following the 8-stage workflow below.

## Invoking

Run the companion script; it implements all 8 stages and writes a report:

```bash
python3 .opencode/skills/project-analysis/scripts/analyze.py <target-directory> [--output <dir>] [--json]
```

The script is **read-only for the target project**: it never creates, modifies, or deletes files inside the target. It writes `ANALYSIS.md` (and optionally prints JSON with `--json`) to an output path that defaults to the current working directory, or to `--output <dir>`. Preserve the target untouched; only the report path is written.

The script tags every item: `fact` (directly observed), `assumption` (heuristic inference), or `insufficient` (`INSUFFICIENT EVIDENCE`). If the script reports `INSUFFICIENT EVIDENCE` for something, do not guess to fill the gap. Use the script output as the **ground-truth fact base**; you may add reasoning, but keep the tagging honest.

## Evidence rules (MANDATORY — apply to every stage)

Every claim in the report MUST be one of:

- **FACT** — directly observed. Cite the source: a file path (with line where possible) or captured command output from `analyze.py`. Example: `[FACT] Python project — evidence: pyproject.toml`.
- **ASSUMPTION** — a reasoned inference the model believes but cannot directly observe. Label it explicitly. Never present an assumption as a fact.
- **INSUFFICIENT EVIDENCE** — you do not have verifiable support. State it plainly and move on. Never fabricate evidence to fill the gap.

Additional hard rules:

1. **Do not** claim a technology is used just because it appears in documentation or a README. Only a real file (e.g. `package.json`, `pyproject.toml`, `requirements.txt`, `Cargo.toml`, `go.mod`, imports referenced by files that exist) counts as evidence.
2. **Do not** treat inference as fact.
3. A "problem" may only be claimed with **at least one concrete FACT** plus a stated impact chain. Without a fact, mark it `ASSUMPTION` or `INSUFFICIENT EVIDENCE`.
4. Causes, impacts, and recommendations derive from findings. If the link is not directly observed, tag it `ASSUMPTION`; if you cannot trace it, tag it `INSUFFICIENT EVIDENCE`.
5. If evidence is unavailable, explicitly say **"Insufficient evidence."**

## The 8-stage workflow

The companion `analyze.py` implements all 8 stages and writes `ANALYSIS.md`. The stages below map to the script's implementation. You may augment the script's output with deeper reasoning, but you must preserve the script's `fact`/`assumption`/`insufficient` tags and never upgrade an `assumption` or `insufficient` item to a `fact` without new, real evidence.

### Rules for model-added reasoning (hard constraints)

- **Severity is an estimate, never a fact.** The script's severity labels are a heuristic, not a measurement. Do not restate "high severity" as an established fact; present it as an estimate or refine it only with new evidence.
- **Never invent a cause/impact/recommendation you cannot source.** If you add reasoning, tag it `ASSUMPTION`; if you have nothing to support it, tag it `INSUFFICIENT EVIDENCE`. Prefer `INSUFFICIENT EVIDENCE` over guessing.
- **A lone marker is not proof of high impact.** A single FIXME/TODO/HACK comment signals a code smell, not a measured defect. Do not escalate it into a high-impact claim.
- **Hardcoded secrets flagged by the script are candidates, not confirmations.** The script only reports an assignment that *looks* like a credential. Before stating "this project leaks a secret," verify the value is a real credential; otherwise tag it `INSUFFICIENT EVIDENCE` / "requires manual verification."
- **When multiple ecosystems are present**, the script's `primary` type is a heuristic (`assumption`). Do not present "this is a Python project" as a fact if other manifests coexist; state the confidence.

### 1. Inspect files and structure
Use `analyze.py` output (tree, file counts, sizes, ignored dirs). Record only what exists on disk. Do not interpret at this stage, just list facts.

### 2. Identify project type
Base this **only** on evidence produced by the script's project-type detection (real manifest/config files). Report the evidence files. If none, say `INSUFFICIENT EVIDENCE` for project type.

### 3. Understand architecture
Derive structure and roles from actual files and organization. Each architectural claim must trace to real files/dirs. Cross-cutting inferences are `ASSUMPTION`.

### 4. Find problems
List candidate problems. Each needs a concrete FACT plus impact chain. Holidays? Without a fact, downgrade to `ASSUMPTION` or `INSUFFICIENT EVIDENCE`.

### 5. Find causes
For each problem, identify causes. Directly observed causes → FACT with source. Otherwise `ASSUMPTION`. Untraceable → `INSUFFICIENT EVIDENCE`.

### 6. Evaluate impact
Assess severity/scope of each problem from observed facts (e.g. files affected, how often used, severity indicators). Unverifiable impact → `ASSUMPTION`/`INSUFFICIENT EVIDENCE`.

### 7. Recommend solutions
Recommend fixes grounded in the problems/causes found. If a recommendation depends on an unverified assumption, flag it as such. Do not invent fixes for problems you could not establish.

### 8. Create analysis report
Write a structured report that includes: scope, method (files + commands used), project facts, the findings with tags and sources, and clearly separate **Facts / Assumptions / Insufficient Evidence** sections.

## Report format

```
# Project Analysis Report — <project>

## Scope and method
<facts about what was inspected, what the script returned>

## Project facts
[FACT] <claim> — source: <file:line | command output>

## Findings
### Problem: <title> (severity: <high|medium|low>)
- Evidence: [FACT] <source>
- Cause: [FACT|ASSUMPTION|INSUFFICIENT EVIDENCE]
- Impact: [FACT|ASSUMPTION|INSUFFICIENT EVIDENCE]
- Recommendation: [..]

## Assumptions
<these are NOT verified facts>

## Insufficient Evidence
<what could not be determined>
```

Keep the report honest: prefer fewer, well-sourced findings over many speculative ones.

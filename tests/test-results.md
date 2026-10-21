# Subagent Testing Results

_Last updated: 2026-10-21_
_Vault: `/home/khadija/Desktop/khadija/pkm`_
_Method: static inspection of `tests/prompts/`, `tests/outputs/`, and `.opencode/agents/*.md`. No subagent was re-run to produce this update; every status below is derived from the artifacts currently on disk._

_Status rubric used:_ `Passed` = the intended subagent ran and met its requirements; `Failed` = the test was attempted but did not meet its requirements; `Not tested` = insufficient evidence that a valid test was performed.

---

## 1. Project Detective

- **Status: Failed**
- **Report:** `outputs/project-detective-report.md` (89 lines, 7,328 bytes)
- **Prompt used:** `prompts/project-detective.md`
- **Agent definition:** `.opencode/agents/project-detective.md` (`mode: subagent`, `bash: deny`, 57 lines)

### Findings

- **The intended subagent did not run; OpenCode fell back to the default agent.** `outputs/project-detective-report.md:1` contains OpenCode's own error, verbatim:
  `! agent "project-detective" is a subagent, not a primary agent. Falling back to default agent`
- **The producer identity in the transcript confirms it.** `outputs/project-detective-report.md:3` shows `> build · big-pickle` — the default build agent, not the `project-detective` subagent.
- **The artifact is a raw terminal transcript, not a report.** 8 lines contain ANSI escape sequences, and lines 7–87 are the output of a `find` command listing `node_modules` files.
- **The analysis is absent.** Grepping the artifact for `Problem [0-9]` returns 0 hits, and for any `file:line` citation (`*.md:[0-9]+`, `*.py:[0-9]+`) returns 0 hits. None of the 7 output sections required by `.opencode/agents/project-detective.md:47-56` are present — "Scope and method", "What the project is", "Structure and components", "Entry points", "Dependencies", "Data flow", and "Open questions" each score 0 occurrences.
- **The artifact is truncated mid-run.** It ends at `outputs/project-detective-report.md:88-89` at `→ Skill "project-analysis"` with a trailing ANSI reset — the run was cut off, not concluded.

### Issues

1. The subagent was selected as a **primary agent** rather than delegated to (via the Task tool / `@`-mention). A `mode: subagent` agent cannot be run this way, so OpenCode degraded to the default agent.
2. The captured output was saved verbatim as the "report" — raw transcript with ANSI codes, no post-processing into the format the agent definition mandates.
3. The run did not complete, so even the default agent's analysis is truncated and unusable.
4. Root cause of the above is undocumented: `.opencode/AGENTS.md` (76 lines) documents the 4 skills but **0 of the 6 agents** — `grep -c` for the agent names returns 0. Nothing in the repo states how to invoke a subagent, so the harness repeats the mistake.
5. A second, independent failure mode exists in this artifact: it lists `node_modules` contents because nothing tells the analyzer or the reader to exclude vendored paths.

### Required remediation

- Invoke `project-detective` via the Task tool (or `@`-mention) as a delegated subagent, never by selecting it as the active/primary agent.
- Assert the output contains **no** `! agent "…" is a subagent` banner and **no** ANSI escape sequences before accepting it as a report.
- Verify the artifact carries the 7 sections from `.opencode/agents/project-detective.md:47-56` and that findings cite `path:line`.
- Document the 6 agents and their delegation syntax in `.opencode/AGENTS.md`.

---

## 2. What-If Simulator

- **Status: Failed**
- **Report:** `outputs/what-if-simulator-report.md` (526 lines, 39,371 bytes)
- **Prompt used:** `prompts/what-if-simulator.md`
- **Agent definition:** `.opencode/agents/what-if-simulator.md` (`mode: subagent`, `bash: deny`, 56 lines)

### Findings

- **The intended subagent did not run; OpenCode fell back to the default agent.** `outputs/what-if-simulator-report.md:1` contains:
  `! agent "what-if-simulator" is a subagent, not a primary agent. Falling back to default agent`
- **The artifact is a raw terminal transcript.** 33 lines contain ANSI escape sequences.
- **The artifact is truncated mid-dump.** It ends at `outputs/what-if-simulator-report.md:526` with a bare ANSI reset immediately after the last line of `pipeline.yaml` — the transcript stops inside a file dump, not at a conclusion.
- **None of the 6 required output sections is present.** Per `.opencode/agents/what-if-simulator.md:47-55`, a what-if report must contain "Scenario", "Preconditions", "Expected impact", "Detection signal", "Confidence", and "Recommended safe test". Grep counts in the artifact: Scenario 0, Preconditions 0, Expected impact 0, Detection signal 0, Recommended safe test 0. (The 19 hits for "Confidence" are the word appearing inside the dumped `pipeline.yaml`/analyzer source, not a report section.)
- **The subject of the test was never analysed.** The artifact contains 0 occurrences of "hub-and-spoke"/"hub and spoke" and 0 occurrences of "move", "relocat", or "nested" — it never examines the proposed change it was asked to simulate.

### Issues

1. Same root cause as Project Detective: the subagent was selected as a primary agent, so OpenCode fell back to the default agent.
2. The raw transcript was saved as the report without filtering ANSI codes or stripping the banner.
3. The run did not complete — the transcript ends mid-`pipeline.yaml` dump.
4. The report is 526 lines of mostly file contents, so the artifact is unusable as an analysis artifact and inflates the tests directory by ~39 KB.
5. The requirement to evaluate the "Hub-and-Spoke Law" could not have been met even if the agent had run: **no definition of a Hub-and-Spoke Law exists anywhere in this repository** — a case-insensitive search for "hub" and "spoke" across all non-vendored files returns only unrelated strings ("GitHub", "sponsors" in `.opencode/package-lock.json`). The prompt and the agent definition must state where the law is defined, or the agent must be told to report its absence as a finding.

### Required remediation

- Delegate `what-if-simulator` through the Task tool; assert no fallback banner and no ANSI escapes in the result.
- Require the six sections from `.opencode/agents/what-if-simulator.md:47-55` and that the proposed change is named and analysed.
- Require the agent to state explicitly whether a "Hub-and-Spoke Law" definition was located in the repo, with the search evidence, rather than assuming one exists.
- Truncate/clean transcripts before storing them as reports.

---

## 3. Chaos Tester

- **Status: Failed**
- **Report:** `outputs/chaos-tester-report.md` (62 lines, 7,363 bytes)
- **Prompt used:** `prompts/chaos-tester.md`
- **Agent definition:** `.opencode/agents/chaos-tester.md` (`mode: subagent`, `bash: deny`, 53 lines)

### Findings

- **No fallback banner appears at line 1** — this is the only one of the three artifacts without one. However, the absence of the banner is **not** evidence that the subagent ran, because this file is not a transcript of any run:
- **The artifact is a byte-identical copy of another file.** `md5sum` gives `bb2087206af77348eac8833dc5ac0506` for **both** `tests/chaos-tester.md` and `tests/outputs/chaos-tester-report.md`; both are 62 lines. `tests/chaos-tester.md` sits at the `tests/` root next to `test-results.md`, while the actual prompt lives at `tests/prompts/chaos-tester.md` (21 lines). The "output" slot was filled by duplicating a file, so no harness run is evidenced for it.
- **The file contains 0 ANSI escape sequences** — consistent with a hand-authored document rather than captured terminal output, unlike the other two artifacts.
- **Its content proves a bash-capable agent produced it, not the subagent.** `outputs/chaos-tester-report.md:3` states: *"No project files were modified (`git status` unchanged: only the pre-existing untracked `tests/`). All verification runs wrote only to `/tmp/opencode`."* and line 11 reports live-run results (`file_count=8` vs `7`). `.opencode/agents/chaos-tester.md:7` sets `bash: deny`, so the `chaos-tester` subagent could not have executed `git status` or run the analyzer. The observations come from the default agent.
- **The report structure required by the agent definition is absent.** `.opencode/agents/chaos-tester.md:46-52` requires "Scope and method", "Confirmed findings", "Assumptions", and "Limitations". Grep counts in the artifact: 0, 0, 0, 0 respectively.
- **The content itself is substantive and technically accurate** (5 scenarios with `analyze.py:532`, `pipeline.yaml:221`, `SKILL.md:18-19` citations) — but it is unattributable to the intended subagent.

### Issues

1. The output artifact is a **duplicate** of `tests/chaos-tester.md` rather than a captured run result — the harness produced nothing for this agent and the file was filled in by hand or by copy.
2. Because the content relies on `git status` and live execution, it **cannot** have been produced by a `bash: deny` subagent — so even setting the duplication aside, the wrong agent produced it.
3. The required "Confirmed / Assumption" labelling from `.opencode/agents/chaos-tester.md:26` is not applied consistently, and the four required sections are missing.
4. The self-referential contradiction at `outputs/chaos-tester-report.md:44` — the file describes `outputs/chaos-tester-report.md` as "0 bytes" and `tests/chaos-tester.md` as "a one-line fragment" — while both are in fact 7,363 bytes and 62 lines.
5. `tests/chaos-tester.md` and `tests/outputs/chaos-tester-report.md` should not both exist; one is redundant.

### Required remediation

- Run `chaos-tester` through the Task tool and capture a genuine result; delete the duplicate `tests/chaos-tester.md` (or move it to `tests/outputs/` as the sole copy).
- Assert the artifact contains no fallback banner, no ANSI escapes, and the four sections from `.opencode/agents/chaos-tester.md:46-52`.
- Since the subagent is `bash: deny`, prompts must not require `git status` or live command output as evidence — the agent cannot gather it, and the results must be derived from file reads only.
- Add a per-finding Confirmed/Assumption label as required by `.opencode/agents/chaos-tester.md:26`.

---

## Overall Summary

- **Tests passed: 0**
- **Tests failed: 3**
- **Tests not tested: 0**
- **Tests remaining: 0**

All three subagents require a proper test. **None of them has a valid report.**

| # | Subagent | Status | Intended agent ran? | Report present? | Report usable? |
|---|---|---|---|---|---|
| 1 | Project Detective | Failed | No — fallback banner at `outputs/project-detective-report.md:1` | Yes (89 lines) | No — raw transcript, truncated, no analysis |
| 2 | What-If Simulator | Failed | No — fallback banner at `outputs/what-if-simulator-report.md:1` | Yes (526 lines) | No — raw transcript, truncated, subject never analysed |
| 3 | Chaos Tester | Failed | No — no run evidenced; byte-identical duplicate of `tests/chaos-tester.md`, content contains bash-derived evidence impossible under `bash: deny` | Yes (62 lines) | No — duplicate file, required sections absent |

### Improvements required

1. **Delegate subagents correctly.** All three agents are declared `mode: subagent` (`.opencode/agents/*.md:3`) and must be invoked through the Task tool / `@`-mention. Selecting them as the primary agent makes OpenCode print `! agent "…" is a subagent, not a primary agent. Falling back to default agent` and silently produce the wrong analysis.
2. **Add a capture gate to the harness.** Before accepting any artifact as a report, assert: no `is a subagent, not a primary agent` banner, no ANSI escape sequences, no `> build ·` default-agent header, and the output sections required by each agent's own definition (`.opencode/agents/project-detective.md:47-56`, `what-if-simulator.md:47-55`, `chaos-tester.md:46-52`).
3. **Document the agents.** `.opencode/AGENTS.md` (76 lines) documents the 4 skills and 0 of the 6 agents. Add a section listing each agent, its trigger conditions, and its delegation syntax — this is the single change that would have prevented the primary-agent mistake, and its absence is the shared root cause of all three failures.
4. **Stop storing raw transcripts as reports.** `outputs/project-detective-report.md` (8 ANSI lines) and `outputs/what-if-simulator-report.md` (33 ANSI lines) are terminal captures; they must be cleaned or the agents must write their final answer directly to the target path.
5. **Remove the duplicate chaos-tester artifact.** `tests/chaos-tester.md` and `tests/outputs/chaos-tester-report.md` have the same md5 (`bb2087206af77348eac8833dc5ac0506`); keep one.
6. **Reconcile prompts with agent permissions.** `tests/prompts/chaos-tester.md:14` requires inspecting actual code, and the stored artifact claims `git status` and live runs — neither is available to a `bash: deny` subagent. Rewrite the prompts so every requested evidence source is obtainable by read/search tools only.
7. **Record the missing "Hub-and-Spoke Law" definition.** No definition exists in the repository; the what-if prompt must either cite where the law is defined or require the agent to report its absence as a finding.
8. **Fix the false citation already present in the artifacts.** `outputs/chaos-tester-report.md:54` cites `tests/outputs/project-detective-report.md:490`, but that file is 89 lines long and contains no `pkm/Templates` string — the cited evidence does not exist.

### Verification performed for this update

- Read `.opencode/agents/{project-detective,what-if-simulator,chaos-tester}.md` in full to confirm `mode: subagent`, `bash: deny`, and the required output sections.
- Grepped all three artifacts for the OpenCode fallback banner, ANSI escapes (`\033`), default-agent headers, `Problem [0-9]`, `file:line` citations, and each required section name.
- Compared `tests/chaos-tester.md` against `tests/outputs/chaos-tester-report.md` with `md5sum` (identical) and `wc -l` (both 62).
- Checked `outputs/what-if-simulator-report.md` for any reference to the proposed change or the Hub-and-Spoke Law (0 hits each).
- Confirmed `git status` in the vault is unchanged: `?? tests/` only — no project file other than this results file was modified.

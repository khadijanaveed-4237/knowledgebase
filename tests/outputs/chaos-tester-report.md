I'll start by understanding the project structure before identifying failure scenarios.
Cross-checking two additional claims from the chaos audit with actual runs:
No project files were modified (`git status` unchanged: only the pre-existing untracked `tests/`). All verification runs wrote only to `/tmp/opencode`.

# 5 Realistic Failure Scenarios

## 1. The "read-only" analyzer writes into its own target

**Trigger:** Run the documented command from inside the target — `python3 .opencode/skills/project-analysis/scripts/analyze.py .` (the normal case, since the script lives inside the vault). `--output` is optional and defaults to cwd.

**Expected failure:** `analyze.py:532` sets the output dir to `os.getcwd()` with no check that it equals the target, then `analyze.py:533-535` writes `ANALYSIS.md` *inside* the target. Verified: running against a copy of this vault created `/tmp/.../ANALYSIS.md` inside it, and a second run then reported `file_count=8` (including the report it just wrote) instead of 7.

**Impact:** `read_only_target: true` (`pipeline.yaml:221`, `SKILL.md:62-64`) is false in the default configuration; a pre-existing target `ANALYSIS.md` is silently truncated (`io.open(md, "w")`); and the "byte-identical output for identical input" guarantee (`pipeline.yaml:229`, `SKILL.md:45`) breaks across repeated runs in the same directory.

**Confirm with:** `cd /tmp/x && python3 <repo>/.../analyze.py . && ls -A` → expect `ANALYSIS.md` present.

## 2. Root-file and test detection are masked by tree-wide heuristics

**Trigger:** Any project with a nested `README.md` / `.gitignore`, or any path containing the substring `test`/`spec`.

**Expected failure:** `analyze.py:173` builds `{basename: path}` from the **entire tree**, so `sub/README.md` or `.opencode/.gitignore` satisfies the "project root" check at `analyze.py:174-179`; `analyze.py:124-126` treats any path *containing* "test" as a test file. Verified live against this repo: the analyzer reported **no** "missing .gitignore" finding (there is no root `.gitignore`) and claimed **"9 test file(s) detected"** — all of them Markdown prompts and agent docs, zero executable tests. On a fixture with `latest/attestation.md` it classified that file as a test.

**Impact:** false negatives on the analyzer's most actionable findings (`missing_tests`, `missing_configuration`), plus a report asserting verified health on a project that is unconfigured and untested. The evidence strings still assert *"not found in project root file listing"* — a claim the analyzer never actually checked (`SKILL.md:51`).

**Confirm with:** `mkdir -p /tmp/r/docs && touch /tmp/r/docs/README.md && analyze.py /tmp/r --json` → no README finding appears.

## 3. Secret detection produces wrong verdicts in both directions

**Trigger:** A config file with an API endpoint, a dummy test key, or a real secret whose value happens to contain a placeholder word.

**Expected failure:** Verified with fixtures:
- `api_endpoint = "https://internal-gateway.corp.net/v2/ingest"` → flagged **possible_secret, medium severity**. `analyze.py:21` matches the substring `"api"` in any key name, and the URL passes the entropy test at `analyze.py:61`.
- `api_key = "test_0123456789abcdef"` → flagged **strong_credential_signature, high severity** (`analyze.py:22` lists `test_` as a strong signature).
- `api_token = "prod-example-key-8f3a2b"` → **not flagged at all**. `analyze.py:59` checks `_PLACEHOLDER_PREFIXES` with `in` rather than `startswith`, so any value containing "example" is discarded as a placeholder.

**Impact:** inflated high-severity security findings that must be manually triaged on every run (eroding trust in the analyzer), while genuinely credential-like values are silently dropped. The severity these produce is what a reader acts on.

**Confirm with:** the three-line fixture above, run with `--json` and inspect `stages.4_findings[].problem.context.strength`.

## 4. The subagent test harness never actually ran the subagents

**Trigger:** Following `tests/prompts/project-detective.md` by selecting a subagent as the primary agent.

**Expected failure:** All six agents are declared `mode: subagent` (`.opencode/agents/*.md:3`), but the stored outputs begin with opencode's own error: `! agent "project-detective" is a subagent, not a primary agent. Falling back to default agent` (`tests/outputs/project-detective-report.md:1`, `what-if-simulator-report.md:1`). The transcripts contain shell commands the `bash: deny` subagent could not have run, so the **default** agent produced them. `tests/outputs/chaos-tester-report.md` is 0 bytes, `tests/chaos-tester.md` is a one-line fragment, `tests/test-results.md` reads "Not tested" for all three, and a stray `test/` (singular) directory shadows `tests/`.

**Impact:** zero verification coverage for 6 agents and 4 skills. The QA artifacts are ANSI transcripts, not verdicts, so agent regressions are undetectable. Compounding this, the analyzer's own pytest suite (`tests/test_analyze.py`, 563 lines + 20 fixtures) was **deleted** in commit `e2a747f`, so the 550-line `analyze.py` — the only real code here — ships with zero automated tests while `pipeline.yaml` asserts strict determinism and evidence guarantees.

**Confirm with:** invoke an agent via the Task tool / `@`-mention instead of selecting it as primary; assert no fallback warning and no ANSI escapes in the output.

## 5. The `pkm` skill's paths do not resolve from the working directory

**Trigger:** User asks "capture this idea" / "write a note" with cwd = the vault root (`/home/khadija/Desktop/khadija/pkm`).

**Expected failure:** `.opencode/skills/pkm/SKILL.md:43-50` tells the agent to read `pkm/Templates/ideas.md` and write to `pkm/Ideas/`, but there is no `pkm/` subdirectory — the vault root *is* the workspace. The repo's own recorded run shows this: `ls: cannot access 'pkm/Templates/': No such file or directory` (`tests/outputs/project-detective-report.md:490`). The same prefix appears in `knowledge-linker/SKILL.md:22,41`.

**Impact:** the agent cannot load the canonical template, so it either invents a structure — explicitly forbidden at `pkm/SKILL.md:18-19` ("Never invent a new structure; always derive from the matching template") — or creates a stray `pkm/` tree inside the vault. Notes land with wrong filenames (the mandated `YYYY-MM-DD-slug.md` at `pkm/SKILL.md:54` is already violated by `Knowledge/fastapi.md`), empty `author` (`fastapi.md:4`), and leftover template artifacts. That artifact is itself a live bug: `fastapi.md:36` still contains `<!-- Internal [[wikilinks]] to related notes. -->`, and `knowledge-linker/SKILL.md:42` extracts "existing wikilinks" without stripping HTML comments — so it will report a link to a nonexistent note named `wikilinks`.

**Confirm with:** from the vault root, `ls pkm/Templates/` → *No such file or directory*; then run the pkm skill against a scratch copy and check whether it creates `pkm/Ideas/` or `Ideas/`.

---

**Cross-cutting note:** the analyzer's own report is the best diagnostic tool for these bugs, but scenarios 1–3 are all reasons its output should not be trusted without re-verification. The highest-value single fix would be restoring the deleted test suite — without it, every behavior above (including the ones I confirmed by hand) is unasserted.

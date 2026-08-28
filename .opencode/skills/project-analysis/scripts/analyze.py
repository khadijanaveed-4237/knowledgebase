#!/usr/bin/env python3
"""Read-only project analysis pipeline (8 stages).

Implements the full `project-analysis` workflow:

    Project
       -> Inspect files and structure
       -> Identify project type
       -> Understand architecture
       -> Find problems
       -> Find causes
       -> Evaluate impact
       -> Recommend solutions
       -> Create analysis report

The script NEVER modifies files inside the target project. It only reads the
target. Any report file (ANALYSIS.md / .json) is written to an output path
that defaults to the current working directory, not the target.

Every output item carries an evidence tag:

  - plausibility == "fact"      : directly observed from real files/output.
  - plausibility == "assumption": heuristic inference based on observed facts.
  - plausibility == "insufficient": could not be verified.

Usage:
    python3 analyze.py <target-directory> [--output <dir>] [--json]
"""

from __future__ import annotations

import io
import json
import os
import re
import sys

# Directories never walked.
IGNORED_DIRS = {
    ".git", ".hg", ".svn", "__pycache__", "node_modules", "venv", ".venv",
    "env", "dist", "build", "target", ".idea", ".vscode", ".mypy_cache",
    ".pytest_cache", ".ruff_cache", ".tox", "site-packages", "vendor",
}

# File extensions that carry project-type evidence (root level or recursive).
MANIFEST_HINTS = {
    "package.json": "Node.js / JavaScript / TypeScript",
    "package-lock.json": "Node.js / JavaScript / TypeScript",
    "yarn.lock": "Node.js / JavaScript / TypeScript (yarn)",
    "pnpm-lock.yaml": "Node.js / JavaScript / TypeScript (pnpm)",
    "tsconfig.json": "TypeScript",
    "pyproject.toml": "Python",
    "setup.py": "Python",
    "setup.cfg": "Python",
    "requirements.txt": "Python",
    "Pipfile": "Python",
    "poetry.lock": "Python (poetry)",
    "uv.lock": "Python (uv)",
    "Cargo.toml": "Rust",
    "Cargo.lock": "Rust",
    "go.mod": "Go",
    "go.sum": "Go",
    "Gemfile": "Ruby",
    "composer.json": "PHP",
    "pom.xml": "Java (Maven)",
    "build.gradle": "Java / Kotlin (Gradle)",
    "build.gradle.kts": "Kotlin (Gradle)",
    "package.xml": "Java / Apex (Salesforce)",
    "mix.exs": "Elixir",
    "project.clj": "Clojure",
    "deps.edn": "Clojure",
    "Makefile": "Make (build system)",
    "CMakeLists.txt": "CMake (build system)",
    "Dockerfile": "Docker (containerized)",
    "docker-compose.yml": "Docker Compose",
    "docker-compose.yaml": "Docker Compose",
}

# Extensions mapped to a language label for the architecture stage.
EXT_LANGUAGE = {
    ".py": "Python", ".js": "JavaScript", ".jsx": "JavaScript (React)",
    ".ts": "TypeScript", ".tsx": "TypeScript (React)", ".java": "Java",
    ".kt": "Kotlin", ".rs": "Rust", ".go": "Go", ".rb": "Ruby",
    ".php": "PHP", ".c": "C", ".h": "C", ".cpp": "C++", ".cs": "C#",
    ".swift": "Swift", ".sh": "Shell", ".html": "HTML", ".css": "CSS",
    ".scss": "SCSS", ".json": "JSON", ".md": "Markdown", ".yml": "YAML",
    ".yaml": "YAML", ".toml": "TOML", ".sql": "SQL", ".vue": "Vue",
    ".svelte": "Svelte",
}

# Marker patterns for the "find problems" stage. The hardcoded-secret case is
# handled separately (see find_problems) so it can carry credential context.
_PROBLEM_PATTERNS = [
    (re.compile(r"#\s*TODO", re.IGNORECASE), "TODO marker found"),
    (re.compile(r"#\s*FIXME", re.IGNORECASE), "FIXME marker found"),
    (re.compile(r"//\s*HACK|#\s*HACK|/\*\s*HACK", re.IGNORECASE), "HACK marker found"),
    (re.compile(r"except\s*:\s*pass|except\s+Exception\s*:\s*pass"), "Bare/silent exception handler"),
]

# Matches a key = "value" or key: "value" assignment, capturing key and value.
_SECRET_ASSIGN = re.compile(r"([A-Za-z_][A-Za-z0-9_\-]*)\s*[:=]\s*['\"]([^'\"]{1,128})['\"]")

# A key is secret-indicating if it contains one of these words as a component.
_SECRET_KEY_WORDS = ("secret", "password", "passwd", "token", "api", "key",
                     "auth", "credential", "access", "client_secret", "pwd")


def _is_secret_key(key: str) -> bool:
    low = key.lower()
    return any(w in low for w in _SECRET_KEY_WORDS)

# Value prefixes/signatures that strongly indicate a real secret (not a placeholder).
_SECRET_SIGNATURES = (
    "sk-", "sk_", "ghp_", "gho_", "xoxb-", "xoxp-", "AKIA", "eyJ",  # JWTs
    "live_", "test_", "prod_", "aws_", "-----BEGIN",
)


def _looks_like_credential(value: str) -> bool:
    """Heuristic: does the captured value look like a real credential?

    Strong if it starts with a known secret signature. Otherwise weak unless it
    is reasonably long and mostly non-placeholder. Reduces false positives like
    `password = "your_password_here"`.
    """
    v = value.strip()
    low = v.lower()
    if not v:
        return False
    # Explicit placeholder words.
    placeholders = {"default", "placeholder", "your_password", "your-secret",
                    "your_token", "change_me", "changeme", "xxx", "todo", "none",
                    "dummy", "sample", "demo", "temp", "test", "secret", "password",
                    "secret_key", "private_key", "public_key", "replace_me", "redacted"}
    if low in placeholders:
        return False
    # Values clearly marked as placeholders / samples (e.g. your_*, my_*, example_*).
    if any(prefix in low for prefix in ("your_", "your-", "my_", "my-", "example",
                                        "sample_", "dummy_", "replace_me", "<", ">",
                                        "insert_", "enter_")):
        return False
    if v.startswith(_SECRET_SIGNATURES):
        return True
    # Long, mixed-character value is more likely a real secret than a sample.
    if len(v) >= 16:
        upper = sum(c.isupper() for c in v)
        digit = sum(c.isdigit() for c in v)
        return (upper >= 3 or digit >= 3) or (len(set(v)) >= 8)
    return False


def _secret_strength(value: str) -> int:
    """0 = placeholder/weak, 1 = likely secret, 2 = strong secret signature."""
    v = value.strip()
    low = v.lower()
    if not v or low in {"default", "placeholder", "your_password", "your-secret",
                        "your_token", "change_me", "changeme", "xxx", "todo", "none",
                        "dummy", "sample", "demo", "temp", "test", "secret", "password",
                        "secret_key", "private_key", "public_key", "replace_me", "redacted"}:
        return 0
    if any(prefix in low for prefix in ("your_", "your-", "my_", "my-", "example",
                                        "sample_", "dummy_", "replace_me", "<", ">",
                                        "insert_", "enter_")):
        return 0
    if v.startswith(_SECRET_SIGNATURES):
        return 2
    return 1 if _looks_like_credential(v) else 0

_SOURCE_EXT = {".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".kt", ".rs",
               ".go", ".rb", ".php", ".c", ".h", ".cpp", ".cs", ".swift", ".sh"}


def resolve_target(argv: list[str], parsed: dict) -> str:
    """Resolve and validate the target directory from args (read-only)."""
    if not parsed.get("target"):
        print("Usage: python3 analyze.py <target-directory> [--output <dir>] [--json]")
        sys.exit(2)
    target = os.path.abspath(parsed["target"])
    if not os.path.exists(target):
        print(f"ERROR: target path does not exist: {target}")
        sys.exit(1)
    if not os.path.isdir(target):
        print(f"ERROR: target path is not a directory: {target}")
        sys.exit(1)
    return target


# ---------------------------------------------------------------------------
# Stage 1: Inspect files and structure
# ---------------------------------------------------------------------------
def collect_structure(root: str) -> dict:
    """Walk the tree read-only; summarize counts, sizes, top-level and listing."""
    file_count = 0
    dir_count = 0
    files: list[str] = []
    top_level: list[str] = []
    by_ext: dict[str, int] = {}
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        rel = os.path.relpath(dirpath, root)
        if rel == ".":
            top_level = sorted(dirnames + filenames)
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            rel_file = os.path.relpath(full, root)
            files.append(rel_file)
            file_count += 1
            ext = os.path.splitext(name)[1].lower()
            by_ext[ext] = by_ext.get(ext, 0) + 1
            try:
                total_size += os.path.getsize(full)
            except OSError:
                pass
        dir_count += len(dirnames)
    return {
        "stage": 1,
        "title": "Inspect files and structure",
        "plausibility": "fact",
        "root": os.path.abspath(root),
        "file_count": file_count,
        "dir_count": dir_count,
        "total_size_bytes": total_size,
        "top_level": top_level,
        "files_by_extension": dict(sorted(by_ext.items(), key=lambda kv: -kv[1])),
        "files": files,
    }


# ---------------------------------------------------------------------------
# Stage 2: Identify project type (recursive manifest scan)
# ---------------------------------------------------------------------------
def find_manifests(root: str) -> dict[str, str]:
    """Recursively find manifest files (ignoring IGNORED_DIRS)."""
    found: dict[str, str] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        for name in filenames:
            if name in MANIFEST_HINTS:
                rel_dir = os.path.relpath(dirpath, root)
                key = os.path.join(rel_dir, name) if rel_dir != "." else name
                found[key] = name
    return found


def detect_project_type(root: str) -> dict:
    """Detect project type based ONLY on real manifest files present."""
    manifests = find_manifests(root)
    if not manifests:
        return {
            "stage": 2,
            "title": "Identify project type",
            "plausibility": "insufficient",
            "verdict": "INSUFFICIENT EVIDENCE",
            "evidence": [],
            "types": [],
            "primary": None,
        }
    evidence: list[str] = []
    types: set[str] = set()
    for path, basename in manifests.items():
        evidence.append(path)
        types.add(MANIFEST_HINTS[basename])
    types_sorted = sorted(types)
    # Heuristic primary: prefer language manifests over build/tool manifests.
    language_hits = sorted(t for t in types if "build system" not in t and "Docker" not in t)
    primary = (language_hits[0] if language_hits else types_sorted[0])
    # The manifest evidence itself is a fact, but the *primary* choice can be a
    # judgement call when multiple unrelated ecosystems are present. Tag it
    # assumption and attach a confidence so consumers do not over-read it.
    plural = len(types) > 1
    return {
        "stage": 2,
        "title": "Identify project type",
        "plausibility": "assumption" if plural else "fact",
        "verdict": "detected",
        "evidence": evidence,
        "evidence_plausibility": "fact",
        "types": types_sorted,
        "primary": primary,
        "primary_confidence": "low" if plural else "high",
        "explain": "Primary heuristically chosen from detected manifests; multiple ecosystems found." if plural else "Single ecosystem detected from manifests.",
    }


# ---------------------------------------------------------------------------
# Stage 3: Understand architecture
# ---------------------------------------------------------------------------
def understand_architecture(root: str) -> dict:
    """Produce a structural summary: language breakdown, entry points, grouping."""
    files = collect_structure(root)["files"]
    lang_count: dict[str, int] = {}
    source_files: list[str] = []
    entry_candidates: list[str] = []
    for rel in files:
        ext = os.path.splitext(rel)[1].lower()
        lang = EXT_LANGUAGE.get(ext)
        if lang:
            lang_count[lang] = lang_count.get(lang, 0) + 1
        if ext in _SOURCE_EXT:
            source_files.append(rel)
        base = os.path.basename(rel).lower()
        if base in {"main.py", "app.py", "index.js", "index.ts", "server.ts",
                    "server.js", "main.go", "main.rs", "manage.py", "cli.py"}:
            entry_candidates.append(rel)
    # Group top-level dirs that contain source files.
    group_count: dict[str, int] = {}
    for rel in source_files:
        top = rel.split(os.sep)[0] if os.sep in rel else "."
        group_count[top] = group_count.get(top, 0) + 1
    return {
        "stage": 3,
        "title": "Understand architecture",
        "plausibility": "fact",
        "language_breakdown": dict(sorted(lang_count.items(), key=lambda kv: -kv[1])),
        "source_file_count": len(source_files),
        "entry_point_candidates": entry_candidates,
        "source_grouping": dict(sorted(group_count.items(), key=lambda kv: -kv[1])),
    }


# ---------------------------------------------------------------------------
# Stage 4: Find problems
# ---------------------------------------------------------------------------
def find_problems(root: str) -> list[dict]:
    """Heuristic scan for common problems. Each carries observed evidence."""
    problems: list[dict] = []
    structure = collect_structure(root)
    files = structure["files"]
    by_name = {os.path.basename(f): f for f in files}

    # Missing project essentials (based on file presence facts).
    if "README.md" not in by_name and "README" not in by_name:
        problems.append(_problem("No README/README.md at project root",
                                 "assumption", "No README found in file listing."))
    if "LICENSE" not in by_name and "LICENSE.md" not in by_name:
        problems.append(_problem("No LICENSE file found",
                                 "assumption", "No LICENSE in file listing."))
    if ".gitignore" not in by_name:
        problems.append(_problem("No .gitignore at project root",
                                 "assumption", "No .gitignore in file listing."))

    source_files = [f for f in files
                    if os.path.splitext(f)[1].lower() in _SOURCE_EXT]
    if source_files and not any("/test" in f or "/tests" in f or f.startswith("test") or "/spec" in f for f in files):
        problems.append(_problem("No test files detected",
                                 "assumption", "No test/spec directory or test files in listing."))

    # Large files (potential maintainability issue).
    for rel in files:
        full = os.path.join(root, rel)
        try:
            if os.path.getsize(full) > 200_000:
                problems.append(_problem(f"Large file may hurt maintainability: {rel}",
                                         "assumption", f"File size > 200KB (fact: {os.path.getsize(full)} bytes)."))
        except OSError:
            pass

    # Marker / secret patterns in source files. Report every distinct pattern
    # that matches in a file (do NOT break on the first match).
    for rel in source_files:
        full = os.path.join(root, rel)
        try:
            with io.open(full, "r", encoding="utf-8", errors="ignore") as fh:
                text = fh.read()
        except OSError:
            continue
        for pattern, label in _PROBLEM_PATTERNS:
            m = pattern.search(text)
            if m:
                problems.append(_problem(f"{label} in {rel}",
                                         "fact", f"Matched pattern in content of file: {rel}."))
        # Hardcoded-secret detection with a credibility check on the value.
        for m in _SECRET_ASSIGN.finditer(text):
            key = m.group(1)
            value = m.group(2)
            if not _is_secret_key(key):
                continue
            strength = _secret_strength(value)
            if strength == 0:
                # Looks like a placeholder/sample, not a real credential.
                continue
            context = {
                "matched_key": key,
                "value_length": len(key) + len(value) + 3,
                "looks_like_credential": strength,
                "note": "Requires manual review - value heuristic, not a confirmed secret."
            }
            problems.append(_problem(
                f"Possible hardcoded secret in {rel}",
                "fact",
                f"Matched credential-like assignment for `{key}` in file: {rel}. Verify before acting.",
                context,
            ))
    return problems


def _problem(title: str, plausibility: str, evidence: str, context: dict | None = None) -> dict:
    p = {
        "title": title,
        "plausibility": plausibility,
        "evidence": evidence,
        "stage": 4,
    }
    if context:
        p["context"] = context
    return p


# ---------------------------------------------------------------------------
# Stage 5: Find causes
# ---------------------------------------------------------------------------
def find_causes(problem: dict) -> list[dict]:
    """Rule-based cause for each problem type.

    These are generic cards and are NOT directly observable per-project, so they
    are labeled `insufficient` (the true cause cannot be verified) rather than
    presented as a confident `assumption`.
    """
    t = problem["title"].lower()
    causes: list[dict] = []
    markers = [
        ("readme", "Root documentation was not created/committed."),
        ("license", "No license was configured at project setup."),
        (".gitignore", "Version-control ignore rules were not configured."),
        ("test files detected", "A test suite has not been added yet."),
        ("large file", "Logic has accumulated in a single module over time."),
        ("todo", "Incomplete work remains in source."),
        ("fixme", "A known defect has not been fixed/tracked."),
        ("hack", "A workaround was left in place."),
        ("hardcoded secret", "A credential appears hardcoded rather than in env/secrets."),
        ("silent exception", "Errors are being swallowed silently."),
    ]
    for key, cause in markers:
        if key in t:
            causes.append({
                "cause": cause,
                "plausibility": "insufficient",
                "stage": 5,
                "evidence": "True cause is not directly observable from this scan; shown as a possible explanation only.",
            })
    if not causes:
        causes.append({"cause": "No direct cause established.",
                       "plausibility": "insufficient", "stage": 5,
                       "evidence": "Cannot trace cause from available facts."})
    return causes


# ---------------------------------------------------------------------------
# Stage 6: Evaluate impact
# ---------------------------------------------------------------------------
def evaluate_impact(problem: dict) -> dict:
    """Severity heuristic based on problem type, evidence strength, and context.

    Conservative by design: a weak signal (e.g. a lone FIXME comment) is NOT
    enough to claim high impact. Severity is labeled `assumption` because it is
    an estimate, never a measured fact.
    """
    t = problem["title"].lower()
    plausibility = problem["plausibility"]
    ctx = problem.get("context") or {}

    if "secret" in t:
        # Only a strong-credential value supports high severity.
        strength = ctx.get("looks_like_credential", 0)
        severity = "high" if strength >= 2 else "medium"
    elif "todo" in t or "fixme" in t or "hack" in t:
        # Markers are weak evidence of impact; do not overstate.
        severity = "medium"
    elif "silent exception" in t:
        severity = "medium"
    elif "test files" in t or "large file" in t:
        severity = "medium"
    else:
        severity = "low"

    # Never let a non-fact problem escalate above low/medium.
    if plausibility == "assumption":
        severity = "low" if severity == "high" else severity

    return {
        "stage": 6,
        "title": "Evaluate impact",
        "severity": severity,
        "plausibility": "assumption",
        "evidence": f"Severity estimated from problem type: {problem['title']} (heuristic, not measured).",
    }


# ---------------------------------------------------------------------------
# Stage 7: Recommend solutions
# ---------------------------------------------------------------------------
def recommend(problem: dict, impact: dict) -> list[dict]:
    t = problem["title"].lower()
    recs: list[dict] = []
    map_rec = [
        ("readme", "Create a README.md describing purpose, setup, and usage."),
        ("license", "Add a LICENSE file appropriate to the project."),
        (".gitignore", "Add a .gitignore for the detected language/dependency dirs."),
        ("test files detected", "Add a test suite and wire it into CI."),
        ("large file", "Split the large module into smaller, cohesive units."),
        ("todo", "Resolve or track the TODO items in the project tracker."),
        ("fixme", "Fix or formally track the FIXME defects."),
        ("hack", "Replace the hack/workaround with a supported approach."),
        ("hardcoded secret", "Move secrets to environment variables or a secret manager and rotate them."),
        ("silent exception", "Replace bare/silent exception handlers with targeted logging and handling."),
    ]
    for key, rec in map_rec:
        if key in t:
            recs.append({"recommendation": rec, "plausibility": "assumption",
                         "stage": 7, "severity": impact["severity"]})
    if not recs:
        recs.append({"recommendation": "No specific recommendation; review findings.",
                     "plausibility": "insufficient", "stage": 7, "severity": impact["severity"]})
    return recs


# ---------------------------------------------------------------------------
# Stage 8: Create analysis report
# ---------------------------------------------------------------------------
def build_report(root: str) -> dict:
    structure = collect_structure(root)
    project_type = detect_project_type(root)
    architecture = understand_architecture(root)
    problems = find_problems(root)

    findings = []
    for p in problems:
        causes = find_causes(p)
        impact = evaluate_impact(p)
        recs = recommend(p, impact)
        findings.append({
            "problem": p,
            "causes": causes,
            "impact": impact,
            "recommendations": recs,
        })
    # Sort findings by severity high -> low.
    sev_order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda f: sev_order.get(f["impact"]["severity"], 3))

    report = {
        "target": structure["root"],
        "pipeline": "project analysis (8 stages)",
        "read_only_target": "target project was only read, not modified",
        "stages": {
            "1_structure": structure,
            "2_project_type": project_type,
            "3_architecture": architecture,
            "4_5_6_7_findings": findings,
        },
    }
    return report


def render_markdown(report: dict) -> str:
    lines: list[str] = []
    lines.append("# Project Analysis Report")
    lines.append("")
    lines.append(f"**Target:** `{report['target']}`")
    lines.append(f"**Pipeline:** {report['pipeline']}")
    lines.append("")
    st = report["stages"]
    s1 = st["1_structure"]
    lines.append("## 1. Inspect files and structure")
    lines.append("")
    lines.append(f"- Files: {s1['file_count']}, Directories: {s1['dir_count']}, Total size: {s1['total_size_bytes']} bytes")
    lines.append(f"- Top level: `{', '.join(s1['top_level'])}`")
    if s1["files_by_extension"]:
        top_ext = ", ".join(f"{k} ({v})" for k, v in list(s1["files_by_extension"].items())[:8])
        lines.append(f"- Extension breakdown: {top_ext}")
    lines.append("")

    s2 = st["2_project_type"]
    lines.append("## 2. Identify project type")
    lines.append("")
    if s2["plausibility"] == "insufficient":
        lines.append("INSUFFICIENT EVIDENCE: no manifest files found to determine project type.")
    else:
        lines.append(f"- Primary type (heuristic): **{s2['primary']}** (confidence: {s2.get('primary_confidence', 'n/a')}, `{s2['plausibility']}`)")
        lines.append(f"- Evidence files ({s2['evidence_plausibility']}): {', '.join('`' + e + '`' for e in s2['evidence'])}")
        if s2.get("explain"):
            lines.append(f"- Note: {s2['explain']}")
    lines.append("")

    s3 = st["3_architecture"]
    lines.append("## 3. Understand architecture")
    lines.append("")
    if s3["language_breakdown"]:
        lines.append("- Language breakdown: " + ", ".join(f"{k} ({v})" for k, v in s3["language_breakdown"].items()))
    lines.append(f"- Source files: {s3['source_file_count']}")
    if s3["entry_point_candidates"]:
        lines.append(f"- Entry-point candidates: {', '.join('`' + e + '`' for e in s3['entry_point_candidates'])}")
    lines.append("")

    findings = st["4_5_6_7_findings"]
    lines.append("## Findings (problems / causes / impact / recommendations)")
    lines.append("")
    if not findings:
        lines.append("No problems detected by heuristic scan.")
    for idx, f in enumerate(findings, 1):
        p = f["problem"]
        imp = f["impact"]
        lines.append(f"### {idx}. {p['title']}")
        lines.append(f"- Type: `{p['plausibility']}` | Severity: **{imp['severity']}** (estimated)")
        lines.append(f"- Evidence: {p['evidence']}")
        ctx = p.get("context")
        if ctx:
            lines.append(f"- Note: {ctx.get('note', 'Requires manual verification before acting on this finding.')}")
        lines.append("- Causes:")
        for c in f["causes"]:
            lines.append(f"  - `{c['plausibility']}` {c['cause']}")
        lines.append("- Recommendations:")
        for r in f["recommendations"]:
            lines.append(f"  - `{r['plausibility']}` {r['recommendation']}")
        lines.append("")
    lines.append("---")
    lines.append("_Legend: `fact` = directly observed; `assumption` = heuristic inference; `insufficient` = not verifiable._")
    return "\n".join(lines).strip() + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def parse_args(argv: list[str]) -> dict:
    parsed = {"target": None, "output": None, "json": False}
    args = argv[1:]
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("--output", "-o"):
            if i + 1 >= len(args):
                print("ERROR: --output requires a directory argument")
                sys.exit(2)
            parsed["output"] = args[i + 1]
            i += 2
        elif a in ("--json", "-j"):
            parsed["json"] = True
            i += 1
        elif a.startswith("-") and a != "-":
            print(f"ERROR: unknown option: {a}")
            sys.exit(2)
        else:
            parsed["target"] = a
            i += 1
    return parsed


def main() -> int:
    parsed = parse_args(sys.argv)
    target = resolve_target(sys.argv, parsed)

    report = build_report(target)

    # Write report file (default cwd, or --output dir). Target stays untouched.
    out_dir = os.path.abspath(parsed["output"] or os.getcwd())
    os.makedirs(out_dir, exist_ok=True)
    md_path = os.path.join(out_dir, "ANALYSIS.md")
    with io.open(md_path, "w", encoding="utf-8") as fh:
        fh.write(render_markdown(report))

    if parsed["json"]:
        # Pure JSON on stdout; all human messages go to stderr.
        print(json.dumps(report, indent=2, default=str))
        print(f"Report written to: {md_path}", file=sys.stderr)
        return 0

    # Non-JSON mode: human-readable summary on stdout.
    print(f"Report written to: {md_path}")
    st = report["stages"]
    print("Project Analysis Summary")
    print(f"  Target : {report['target']}")
    print(f"  Type   : {st['2_project_type'].get('primary') or 'INSUFFICIENT EVIDENCE'}")
    findings = st["4_5_6_7_findings"]
    print(f"  Findings: {len(findings)} (severity: " +
          ", ".join(f"{f['impact']['severity']}" for f in findings) + ")")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

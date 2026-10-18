#!/usr/bin/env python3
from __future__ import annotations
import io, json, os, re, sys
H, M, L_, U = "high", "medium", "low", "unknown"
V, PV, UV = "verified", "partially_verified", "unverified"
CONFIDENCE_HIGH, CONFIDENCE_MEDIUM, CONFIDENCE_LOW = H, M, L_
VERIFICATION_VERIFIED, VERIFICATION_PARTIAL, VERIFICATION_UNVERIFIED = V, PV, UV
LARGE_FILE_THRESHOLD = 200_000
IGNORED_DIRS = {".git",".hg",".svn","__pycache__","node_modules","venv",".venv","env","dist","build","target",".idea",".vscode",".mypy_cache",".pytest_cache",".ruff_cache",".tox","site-packages","vendor"}
MANIFEST_HINTS = {"package.json":"Node.js / JavaScript / TypeScript","package-lock.json":"Node.js / JavaScript / TypeScript","yarn.lock":"Node.js / JavaScript / TypeScript (yarn)","pnpm-lock.yaml":"Node.js / JavaScript / TypeScript (pnpm)","tsconfig.json":"TypeScript","pyproject.toml":"Python","setup.py":"Python","setup.cfg":"Python","requirements.txt":"Python","Pipfile":"Python","poetry.lock":"Python (poetry)","uv.lock":"Python (uv)","Cargo.toml":"Rust","Cargo.lock":"Rust","go.mod":"Go","go.sum":"Go","Gemfile":"Ruby","composer.json":"PHP","pom.xml":"Java (Maven)","build.gradle":"Java / Kotlin (Gradle)","build.gradle.kts":"Kotlin (Gradle)","package.xml":"Java / Apex (Salesforce)","mix.exs":"Elixir","project.clj":"Clojure","deps.edn":"Clojure","Makefile":"Make (build system)","CMakeLists.txt":"CMake (build system)","Dockerfile":"Docker (containerized)","docker-compose.yml":"Docker Compose","docker-compose.yaml":"Docker Compose"}
EXT_LANGUAGE = {".py":"Python",".js":"JavaScript",".jsx":"JavaScript (React)",".ts":"TypeScript",".tsx":"TypeScript (React)",".java":"Java",".kt":"Kotlin",".rs":"Rust",".go":"Go",".rb":"Ruby",".php":"PHP",".c":"C",".h":"C",".cpp":"C++",".cs":"C#",".swift":"Swift",".sh":"Shell",".html":"HTML",".css":"CSS",".scss":"SCSS",".json":"JSON",".md":"Markdown",".yml":"YAML",".yaml":"YAML",".toml":"TOML",".sql":"SQL",".vue":"Vue",".svelte":"Svelte"}
_SOURCE_EXT = {".py",".js",".jsx",".ts",".tsx",".java",".kt",".rs",".go",".rb",".php",".c",".h",".cpp",".cs",".swift",".sh"}
_JS_EXT = (".js", ".jsx", ".ts", ".tsx")
_PROBLEM_PATTERNS = [
    (re.compile(r"#\s*TODO", re.IGNORECASE), "TODO marker found"),
    (re.compile(r"#\s*FIXME", re.IGNORECASE), "FIXME marker found"),
    (re.compile(r"//\s*HACK|#\s*HACK|/\*\s*HACK", re.IGNORECASE), "HACK marker found"),
    (re.compile(r"except\s*:\s*pass|except\s+Exception\s*:\s*pass"), "Bare/silent exception handler"),
]
_SECRET_ASSIGN = re.compile(r"([A-Za-z_][A-Za-z0-9_\-]*)\s*[:=]\s*['\"]([^'\"]{1,128})['\"]")
_SECRET_KEY_WORDS = ("secret", "password", "passwd", "token", "api", "key", "auth", "credential", "access", "client_secret", "pwd")
_SECRET_SIGNATURES = ("sk-", "sk_", "ghp_", "gho_", "xoxb-", "xoxp-", "AKIA", "eyJ", "live_", "test_", "prod_", "aws_", "-----BEGIN")
_PLACEHOLDERS = frozenset({"default","placeholder","your_password","your-secret","your_token","change_me","changeme","xxx","todo","none","dummy","sample","demo","temp","test","secret","password","secret_key","private_key","public_key","replace_me","redacted"})
_PLACEHOLDER_PREFIXES = ("your_","your-","my_","my-","example","sample_","dummy_","replace_me","<",">","insert_","enter_")
_DIR_ROLE_PATTERNS = {
    "api":re.compile(r"\bapi\b",re.IGNORECASE),"route":re.compile(r"\broute[s]?\b",re.IGNORECASE),
    "controller":re.compile(r"\bcontroller[s]?\b",re.IGNORECASE),
    "frontend":re.compile(r"\b(frontend|client|web|ui|view[s]?|component[s]?)\b",re.IGNORECASE),
    "backend":re.compile(r"\b(backend|server|service[s]?)\b",re.IGNORECASE),
    "model":re.compile(r"\bmodel[s]?\b",re.IGNORECASE),
    "util":re.compile(r"\b(util[s]?|helper[s]?|common|shared|lib|tool[s]?)\b",re.IGNORECASE),
    "config":re.compile(r"\b(config[s]?|setting[s]?|env)\b",re.IGNORECASE),
    "test":re.compile(r"\b(test[s]?|spec[s]?|__tests__|testing)\b",re.IGNORECASE),
    "database":re.compile(r"\b(db|database|migration[s]?|schema|seed[s]?)\b",re.IGNORECASE),
    "doc":re.compile(r"\b(doc[s]?|documentation|wiki)\b",re.IGNORECASE),
    "script":re.compile(r"\b(script[s]?|bin|cmd)\b",re.IGNORECASE),
}
_KNOWN_LIBS = {
    "fastapi":"web API framework","flask":"web application framework","django":"web framework","django.db":"database ORM",
    "express":"Node.js web framework","react":"React UI library","react-dom":"React renderer","vue":"Vue UI framework",
    "svelte":"Svelte UI framework","angular":"Angular UI framework","requests":"HTTP client library","httpx":"HTTP client library",
    "aiohttp":"async HTTP client/server","sqlalchemy":"database ORM","psycopg2":"PostgreSQL driver","pytest":"testing framework",
    "unittest":"testing framework","mocha":"JavaScript testing framework","jest":"JavaScript testing framework","vitest":"JavaScript testing framework",
    "playwright":"browser testing framework","numpy":"numerical computing library","pandas":"data analysis library","scipy":"scientific computing library",
    "tensorflow":"machine learning framework","torch":"machine learning framework","scikit-learn":"machine learning library","celery":"task queue",
    "redis":"cache / message broker client","click":"CLI framework","typer":"CLI framework","argparse":"CLI argument parsing",
    "pydantic":"data validation / settings","pydantic-settings":"settings management","dotenv":"environment variable loading","jinja2":"templating engine",
    "sanic":"async web framework","websockets":"WebSocket support","jwt":"auth token handling","bcrypt":"password hashing",
}
_CAT = ("placeholder", "possible_credential", "strong_credential_signature")
_FUNC_RE = re.compile(r"\b(?:def|function|fn|func|fun)\s+([A-Za-z_]\w*)")
_CLASS_RE = re.compile(r"\b(?:class|struct|interface|trait)\s+([A-Za-z_]\w*)")
_MARKER = {"TODO": ("TODO", "Incomplete work was left for later."),
           "FIXME": ("FIXME", "A known issue was flagged but not yet resolved."),
           "HACK": ("HACK", "A temporary workaround was left in place.")}

def _ss(v):
    v = v.strip(); lo = v.lower()
    if not v or lo in _PLACEHOLDERS or any(p in lo for p in _PLACEHOLDER_PREFIXES): return 0
    if v.startswith(_SECRET_SIGNATURES): return 2
    return 1 if len(v) >= 16 and ((sum(c.isupper() for c in v) >= 3 or sum(c.isdigit() for c in v) >= 3) or len(set(v)) >= 8) else 0

def _read(p):
    with io.open(p, encoding="utf-8", errors="replace") as fh: return fh.read()

def _ev(t, d, **kw):
    e = {"type": t, "description": d}; e.update(kw); return e

def _problem(t, c, pl, ev, ctx=None):
    p = {"title": t, "category": c, "plausibility": pl, "confidence": H if pl == "fact" else L_,
         "evidence": ev, "verification": UV, "stage": 4}
    if ctx: p["context"] = ctx
    return p

def _cause(vc, pc, cf, ve, ev, pl="fact"):
    return {"verified_cause": vc, "possible_causes": pc, "plausibility": pl, "confidence": cf,
            "verification": ve, "stage": 5, "evidence": ev}

def _rec(r, cf, sev, bo, pl="assumption"):
    return {"recommendation": r, "plausibility": pl, "confidence": cf, "verification": UV,
            "stage": 7, "severity": sev, "based_on": bo}

def collect_structure(root):
    fc = dc = ts = 0; files = []; by = {}; tl = []; tree = {}
    for dp, dn, fn in os.walk(root):
        dn[:] = sorted(d for d in dn if d not in IGNORED_DIRS)
        rel = os.path.relpath(dp, root)
        if rel == ".": tl = sorted(dn + fn)
        tree[rel] = sorted(dn + fn)
        for n in sorted(fn):
            f = os.path.relpath(os.path.join(dp, n), root); files.append(f); fc += 1
            e = os.path.splitext(n)[1].lower(); by[e] = by.get(e, 0) + 1
            try: ts += os.path.getsize(os.path.join(dp, n))
            except OSError: pass
        dc += len(dn)
    return {"stage": 1, "title": "Inspect files and structure", "plausibility": "fact", "confidence": H,
            "verification": V, "root": os.path.abspath(root), "file_count": fc, "dir_count": dc,
            "total_size_bytes": ts, "top_level": tl,
            "files_by_extension": dict(sorted(by.items(), key=lambda kv: -kv[1])),
            "files": files, "directory_tree": tree}

def find_manifests(root, files=None):
    if files is None: files = collect_structure(root)["files"]
    return {f: os.path.basename(f) for f in files if os.path.basename(f) in MANIFEST_HINTS}

def detect_project_type(root, structure=None):
    if structure is None: structure = collect_structure(root)
    man = find_manifests(root, structure["files"])
    if not man:
        return {"stage": 2, "title": "Identify project type", "plausibility": "insufficient", "confidence": L_,
                "verification": UV, "verdict": "INSUFFICIENT EVIDENCE", "evidence": [], "ecosystems": [],
                "types": [], "primary": None, "primary_confidence": L_, "multiple_ecosystems": False}
    eco = [{"name": n, "evidence_file": p, "plausibility": "fact"} for p, n in man.items()]
    ts = sorted({MANIFEST_HINTS[b] for b in man.values()})
    lh = sorted(t for t in ts if "build system" not in t and "Docker" not in t)
    prim = lh[0] if lh else ts[0]; multi = len(ts) > 1
    return {"stage": 2, "title": "Identify project type", "plausibility": "assumption" if multi else "fact",
            "confidence": L_ if multi else H, "verification": PV if multi else V, "verdict": "detected",
            "evidence": sorted(man.keys()), "evidence_plausibility": "fact", "ecosystems": eco, "types": ts,
            "primary": prim, "primary_confidence": L_ if multi else H, "multiple_ecosystems": multi,
            "explain": ("Primary heuristically chosen from detected manifests; multiple ecosystems found."
                        if multi else "Single ecosystem detected from manifests.")}

def _is_test_file(rel):
    low = rel.lower()
    return any(p in low for p in ("test", "spec", "__tests__")) or low.startswith("test")

def _resp(t):
    r = []
    if re.search(r"\bapp\s*[=:]\s*(?:Flask|FastAPI|Django|Express)", t): r.append("application_setup")
    if re.search(r"@(?:app|router)\.(?:get|post|put|delete|patch|route)", t): r.append("api_routes")
    if re.search(r"\bclass\s+\w*(?:Model|Schema|Serializer|Form)\b", t): r.append("data_model")
    if re.search(r"\b(?:def|function)\s+(?:test_|spec_)", t): r.append("tests")
    if re.search(r"\b(?:logger|logging|log)\b", t): r.append("logging")
    if re.search(r"\b(?:migrate|migration|schema|CREATE\s+TABLE)\b", t, re.IGNORECASE): r.append("database")
    return r

def understand_architecture(root, structure=None):
    if structure is None: structure = collect_structure(root)
    files = structure["files"]; lc = {}; src = []; ep = []
    ep_names = {"main.py","app.py","index.js","index.ts","server.ts","server.js","main.go","main.rs","manage.py","cli.py"}
    for rel in files:
        ext = os.path.splitext(rel)[1].lower(); lang = EXT_LANGUAGE.get(ext)
        if lang: lc[lang] = lc.get(lang, 0) + 1
        if ext in _SOURCE_EXT: src.append(rel)
        if os.path.basename(rel).lower() in ep_names: ep.append(rel)
    grp = {}
    for rel in src:
        top = rel.split(os.sep)[0] if os.sep in rel else "."
        grp[top] = grp.get(top, 0) + 1
    ld = {}
    for dp in structure.get("directory_tree", {}):
        if dp == ".": continue
        for role, p in _DIR_ROLE_PATTERNS.items():
            if p.search(os.path.basename(dp)): ld.setdefault(role, []).append(dp)
    cfg = []; tf = []; db = []; mf = []
    for rel in files:
        b = os.path.basename(rel).lower(); ext = os.path.splitext(rel)[1].lower()
        if ext in {".yml",".yaml",".toml",".ini",".cfg",".env",".env.example"} or b in {"Makefile","Dockerfile",".editorconfig","tox.ini","pytest.ini",".flake8",".pylintrc","mypy.ini",".pre-commit-config.yaml"}:
            cfg.append(rel)
        if ext in {".sql",".sqlite",".db"} or "migration" in rel.lower(): db.append(rel)
        if _is_test_file(rel): tf.append(rel)
        if b in MANIFEST_HINTS: mf.append(rel)
    return {"stage": 3, "title": "Understand architecture", "plausibility": "fact", "confidence": H,
            "verification": V, "language_breakdown": dict(sorted(lc.items(), key=lambda kv: -kv[1])),
            "source_file_count": len(src), "entry_point_candidates": ep,
            "source_grouping": dict(sorted(grp.items(), key=lambda kv: -kv[1])),
            "likely_directories": ld, "config_files": cfg, "test_files": tf,
            "database_files": db, "manifest_files": mf}

def find_problems(root, structure=None):
    if structure is None: structure = collect_structure(root)
    files = structure["files"]; by = {os.path.basename(f): f for f in files}; P = []
    for n1, n2, ttl, cat, evs in [
        ("README.md", "README", "No README/README.md at project root", "missing_documentation", ["README.md not found in project root file listing", "README not found in project root file listing"]),
        ("LICENSE", "LICENSE.md", "No LICENSE file found", "missing_documentation", ["LICENSE not found in file listing", "LICENSE.md not found in file listing"]),
        (".gitignore", "", "No .gitignore at project root", "missing_configuration", [".gitignore not found in project root file listing"])]:
        if n1 not in by and (not n2 or n2 not in by):
            P.append(_problem(ttl, cat, "fact", [_ev("file_absent", x) for x in evs]))
    src = [f for f in files if os.path.splitext(f)[1].lower() in _SOURCE_EXT]
    if src and not any(_is_test_file(f) for f in files):
        P.append(_problem("No test files detected", "missing_tests", "fact",
            [_ev("pattern_absent", "No test/spec directory or files found in %d source files" % len(src))]))
    for rel in files:
        try: size = os.path.getsize(os.path.join(root, rel))
        except OSError: continue
        if size > LARGE_FILE_THRESHOLD:
            ext = os.path.splitext(rel)[1].lower()
            ctx = {"file": rel, "size_bytes": size, "threshold": LARGE_FILE_THRESHOLD}
            ev = [_ev("file_size", "File size is %d bytes (threshold: %d bytes)" % (size, LARGE_FILE_THRESHOLD),
                      file=rel, size_bytes=size, threshold=LARGE_FILE_THRESHOLD)]
            cf = L_
            if ext in _SOURCE_EXT:
                try: t = _read(os.path.join(root, rel))
                except OSError: t = ""
                if t:
                    fc = len(re.findall(r"\bdef\s+\w+", t)); cc = len(re.findall(r"\bclass\s+\w+", t))
                    ic = len(_imports(t, ext)); res = _resp(t)
                    ctx.update(function_count=fc, class_count=cc, import_count=ic, likely_responsibilities=res)
                    ev.append(_ev("function_count", "Approximately %d function definitions" % fc, count=fc))
                    ev.append(_ev("class_count", "Approximately %d class definitions" % cc, count=cc))
                    ev.append(_ev("import_count", "%d import statements" % ic, count=ic))
                    if res: ev.append(_ev("multiple_responsibilities", "File appears to contain: " + ", ".join(res), responsibilities=res))
                    cf = M if len(res) > 1 else L_
            P.append(_problem("Large file: " + rel, "large_file", "fact", ev, ctx=ctx))
            P[-1]["confidence"] = cf
    for rel in src:
        try: t = _read(os.path.join(root, rel))
        except OSError: continue
        for pat, label in _PROBLEM_PATTERNS:
            m = pat.search(t)
            if m:
                P.append(_problem(label + " in " + rel, "code_marker", "fact",
                    [_ev("matched_pattern", "Pattern matched in " + rel, file=rel, pattern=label,
                         line=t.count("\n", 0, m.start()) + 1)]))
        for m in _SECRET_ASSIGN.finditer(t):
            k, v = m.group(1), m.group(2)
            if not any(w in k.lower() for w in _SECRET_KEY_WORDS): continue
            s = _ss(v)
            if not s: continue
            ln = t.count("\n", 0, m.start()) + 1
            cat = _CAT[s]
            P.append(_problem("Possible hardcoded secret in " + rel, "possible_secret", "fact",
                [_ev("matched_pattern", "Credential-like assignment for key `%s` in %s at line %d" % (k, rel, ln),
                     file=rel, key_name=k, line=ln, value_length=len(v), detection_type=cat)],
                {"matched_key": k, "value_length": len(v), "strength": s, "category": cat, "line": ln,
                 "note": "Requires manual review; never print the actual secret value."}))
            P[-1]["confidence"] = H if s >= 2 else M
    return P

def find_causes(p):
    t = p["title"].lower(); c = p.get("category", ""); ctx = p.get("context") or {}
    if c in ("missing_documentation", "missing_configuration"):
        alt = "Kept elsewhere or under a different name." if c == "missing_documentation" else "Ignore rules may live in global git config."
        return [_cause("File not found in project root listing.", ["Never created.", alt], H, V, "File absence confirmed.")]
    if c == "missing_tests":
        return [_cause("No test files or test dirs found.",
            ["Tests may exist outside the detected naming/location patterns.", "Testing may be manual or external to the repository."], M, V, "No test patterns found.")]
    if c == "large_file":
        res = ctx.get("likely_responsibilities", [])
        ver = "File exceeds %d bytes threshold." % LARGE_FILE_THRESHOLD
        if len(res) > 1: ver += " It may contain multiple responsibilities; static inspection cannot establish how or why it evolved."
        return [_cause(ver, ["Insufficient evidence to determine the historical cause of the file size."],
                       M if res else L_, V if res else PV, "Size confirmed.")]
    if c == "code_marker":
        mk = next((_MARKER[w][0] for w in ("TODO", "FIXME", "HACK") if w and w.lower() in t),
                  "silent exception handler" if "silent exception" in t else "code marker")
        pos = (["Errors may be intentionally suppressed.", "Exception handling may be incomplete."] if "silent exception" in t
               else [_MARKER[mk][1]] if mk in _MARKER else ["Reason unknown."])
        return [_cause("Pattern matched in source.", pos, H, V, mk + " pattern confirmed.")]
    if c == "possible_secret":
        s = ctx.get("strength", 0)
        return [_cause("Credential-like key `%s` assignment found." % ctx.get("matched_key", "?"),
            ["Real credential; rotate.", "Test/development value.", "Placeholder missed by filters."],
            M if s >= 2 else L_, PV if s >= 2 else UV, "Manual verification required.")]
    return [_cause("No verified cause from available evidence.", ["Unknown."], L_, UV,
                   "Not traceable.", pl="insufficient")]

def evaluate_impact(p):
    t = p["title"].lower(); c = p.get("category", ""); ctx = p.get("context") or {}
    sev = "low"; r = "Default low severity."
    if c == "possible_secret" or "secret" in t:
        s = ctx.get("strength", 0)
        if s >= 2: sev, r = "high", "Strong credential signature; potential security risk (cannot be confirmed by static inspection)."
        elif s == 1: sev, r = "medium", "Possible credential; requires manual review."
    elif c == "large_file" or "large file" in t:
        res = ctx.get("likely_responsibilities", [])
        if len(res) > 1: sev, r = "medium", "Large file with multiple likely responsibilities; actual maintenance impact is not measurable statically."
        else: r = "Large file; static inspection cannot establish the maintenance impact."
    elif c == "code_marker":
        if "silent exception" in t: sev, r = "medium", "Silent exceptions may mask errors."
        else: r = "Markers are informational signals, not measured defects."
    elif c == "missing_tests": sev, r = "medium", "No tests detected; maintainability risk is potential, not measured."
    elif c in ("missing_documentation", "missing_configuration"): r = "Missing file is a concern, not a confirmed defect."
    if p["plausibility"] == "assumption":
        if sev == "high": sev = "medium"
        r += " (Capped: assumption, not fact.)"
    sc = M if p.get("confidence", L_) == H else L_
    return {"stage": 6, "title": "Evaluate impact", "severity": sev, "severity_confidence": sc,
            "reasoning": r, "plausibility": "assumption", "confidence": sc, "verification": UV,
            "evidence": "Severity is a heuristic estimate."}

def recommend(p, impact, causes):
    t = p["title"].lower(); c = p.get("category", ""); sev = impact.get("severity", "low"); ctx = p.get("context") or {}
    if c == "missing_documentation":
        return [_rec("Add a README.md describing purpose and usage." if "readme" in t
                     else "Add a LICENSE appropriate to the project.", M, sev, "File absence observed.")]
    if c == "missing_configuration":
        return [_rec("Add a .gitignore for the detected language/deps.", M, sev, "File absence observed; global config possible.")]
    if c == "missing_tests":
        return [_rec("Inspect the repository's testing conventions; add tests for critical behavior if testing is genuinely absent.", M, sev, "No tests detected.")]
    if c == "large_file":
        res = ctx.get("likely_responsibilities", [])
        if len(res) > 1: rec = "Review and, if appropriate, split %s; it may serve multiple responsibilities (%s)." % (ctx.get("file", "?"), ", ".join(res))
        else: rec = "Review whether %s size is justified; splitting is only worthwhile if maintainability is affected." % ctx.get("file", "?")
        return [_rec(rec, M if res else L_, sev, "Size observed.")]
    if c == "code_marker":
        mk = next((_MARKER[w][0] for w in ("TODO", "FIXME", "HACK") if w and w.lower() in t),
                  "silent exception handler" if "silent exception" in t else "code marker")
        rec = ("Replace bare/silent exception handlers with targeted handling and logging." if "silent exception" in t
               else "Resolve or track the %s item in the issue tracker." % mk)
        return [_rec(rec, L_, sev, mk + " observed.")]
    if c == "possible_secret":
        return [_rec("Verify whether the credential-like value for `%s` is a real secret; if so, rotate it and move it to a secret manager." % ctx.get("matched_key", "?"),
                     M if ctx.get("strength", 0) >= 2 else L_, sev, "Heuristic match; manual verification needed.")]
    return [_rec("Manual review of findings needed.", L_, sev, "Insufficient evidence.", pl="insufficient")]

def verify_finding(p, causes=None):
    if not p.get("evidence") or p.get("plausibility") != "fact": return UV
    return V if p.get("confidence") == H else PV

def _syms(t, ext):
    S = []
    if ext in ("", None): return S
    for i, l in enumerate(t.splitlines(), 1):
        m = _FUNC_RE.search(l)
        if m: S.append({"kind": "method" if ext == ".py" and l[:1] in (" ", "\t") else "function", "name": m.group(1), "line": i, "params": "", "purpose": None, "purpose_source": "name_heuristic", "confidence": L_})
        m = _CLASS_RE.search(l)
        if m: S.append({"kind": "class", "name": m.group(1), "line": i, "params": "", "purpose": None, "purpose_source": "name_heuristic", "confidence": L_})
    return S

def _imports(t, ext):
    if ext == ".py":
        base = [m.group(1).split(".")[0] for m in re.finditer(r"^\s*(?:import|from)\s+([A-Za-z0-9_\.]+)", t, re.MULTILINE)]
    elif ext in _JS_EXT:
        base = [m.group(1) for m in re.finditer(r"require\(\s*['\"]([^'\"]+)['\"]\s*\)", t)]
        base += [m.group(1) for m in re.finditer(r"from\s+['\"]([^'\"]+)['\"]", t)]
        base += [m.group(1) for m in re.finditer(r"^\s*import\s+['\"]([^'\"]+)['\"]", t, re.MULTILINE)]
    elif ext == ".go":
        base = [m.group(1) for m in re.finditer(r'^\s*[A-Za-z_][\w\.]*\s*["\']([^"\']+)["\']', t, re.MULTILINE)]
    elif ext in (".java", ".kt"):
        base = [m.group(1) for m in re.finditer(r"^\s*import\s+([\w\.]+)", t, re.MULTILINE)]
    else:
        base = [m.group(1).strip('"\'<> ') for m in re.finditer(r"^\s*(?:import|include|use|require|from)\s+[<\"]?([A-Za-z0-9_\./\-]+)", t, re.MULTILINE)]
    out = []; seen = set()
    for n in base:
        n = n.rstrip(".,;").strip("'\"")
        if n and n not in seen: seen.add(n); out.append(n)
    return out

def _tech(fi):
    d = {}
    for f in fi:
        for imp in f["imports"]:
            b = imp.split("/")[0].lower()
            role = _KNOWN_LIBS.get(b) or _KNOWN_LIBS.get(imp.lower())
            if role:
                e = d.setdefault(imp, {"name": imp, "role": role, "files": []})
                if f["file"] not in e["files"]: e["files"].append(f["file"])
    return sorted(d.values(), key=lambda t: t["name"])

def _testing(tf, fi):
    if not tf: return {"present": False, "detail": "No recognized test files were detected.", "framework": None}
    return {"present": True, "files": sorted(tf), "framework": None, "detail": "%d test file(s) detected." % len(tf)}

def summarize_code(root, structure=None, project_type=None, arch=None):
    if structure is None: structure = collect_structure(root)
    if project_type is None: project_type = detect_project_type(root, structure)
    if arch is None: arch = understand_architecture(root, structure)
    fi = []; syms = []; counts = {"function": 0, "method": 0, "class": 0}; big = []
    for rel in sorted(structure["files"]):
        ext = os.path.splitext(rel)[1].lower()
        if ext not in _SOURCE_EXT: continue
        try: t = _read(os.path.join(root, rel))
        except OSError: continue
        im = _imports(t, ext)
        fi.append({"file": rel, "imports": im})
        for s in _syms(t, ext):
            s["file"] = rel; syms.append(s); counts[s["kind"]] += 1
        try: sz = os.path.getsize(os.path.join(root, rel))
        except OSError: sz = 0
        big.append({"file": rel, "size_bytes": sz, "line_count": t.count("\n") + 1})
    big.sort(key=lambda x: (-x["size_bytes"], x["file"]))
    tech = _tech(fi); testing = _testing(arch.get("test_files") or [], fi)
    lang_order = sorted(arch.get("language_breakdown", {}).items(), key=lambda kv: -kv[1])
    lang_label = ", ".join("%s (%s)" % (k, v) for k, v in lang_order) or "none recognized"
    ov = ["%s files, %s dirs, %s bytes." % (structure["file_count"], structure["dir_count"], structure["total_size_bytes"]),
          "Source files: %s; languages: %s." % (arch.get("source_file_count", 0), lang_label)]
    if any(counts[k] for k in ("class", "function", "method")):
        ov.append("Symbols: %s classes, %s functions, %s methods." % (counts["class"], counts["function"], counts["method"]))
    if arch.get("entry_point_candidates"):
        ov.append("Entry points: " + ", ".join(arch["entry_point_candidates"]) + ".")
    if tech: ov.append("Technologies: " + ", ".join(t["name"] for t in tech) + ".")
    ko = []
    if arch.get("entry_point_candidates"):
        ko.append({"text": "Entry-point candidate(s): " + ", ".join(arch["entry_point_candidates"]) + ".", "plausibility": "fact"})
    if tech: ko.append({"text": "Known technologies imported: " + ", ".join(t["name"] for t in tech) + ".", "plausibility": "fact"})
    if big: ko.append({"text": "Largest source file: %s (%s bytes)." % (big[0]["file"], big[0]["size_bytes"]), "plausibility": "fact"})
    ko.append({"text": testing["detail"], "plausibility": "fact"})
    pt = project_type
    return {"overview": " ".join(ov),
            "project_type": {"verdict": pt.get("verdict"), "primary": pt.get("primary"),
                             "types": pt.get("types") or [], "multiple_ecosystems": pt.get("multiple_ecosystems", False),
                             "confidence": pt.get("confidence")},
            "languages": arch.get("language_breakdown") or {},
            "structure": {"total_files": structure["file_count"], "directories": structure["dir_count"],
                          "total_size_bytes": structure["total_size_bytes"],
                          "source_file_count": arch.get("source_file_count", 0),
                          "entry_point_candidates": arch.get("entry_point_candidates") or []},
            "technologies": tech, "important_files": big[:5],
            "symbols": {"counts": counts, "entries": syms},
            "testing": testing, "key_observations": ko,
            "limitations": ["Symbol purposes are name-based heuristics, not verified behavior.",
                            "No runtime call graph; imports only.", "Secrets are never reported.",
                            "The analyzer never runs or modifies the project."]}

def render_markdown(r):
    L = []; s1 = r["stages"]["1_structure"]; s2 = r["stages"]["2_project_type"]; s3 = r["stages"]["3_architecture"]; fds = r["stages"]["4_findings"]; sm = r.get("summary", {})
    L += ["# Project Analysis Report", "", f"**Target:** `{r['target']}`", f"**Pipeline:** {r['pipeline']}",
          f"**Read-only:** {r['read_only_target']}", "", "## 1. Inspect files and structure", "",
          f"- Files: {s1['file_count']}, Directories: {s1['dir_count']}, Total size: {s1['total_size_bytes']} bytes",
          f"- Top level: `{', '.join(s1['top_level'])}`",
          f"- Verification: `{s1['verification']}` | Confidence: `{s1['confidence']}`", "",
          "## 2. Identify project type", ""]
    if s2["plausibility"] == "insufficient":
        L.append("**INSUFFICIENT EVIDENCE:** No manifest files found to determine project type.")
    else:
        L += [f"- Primary type: **{s2['primary']}** (confidence: {s2.get('primary_confidence', 'n/a')}, `{s2['plausibility']}`)", "- Ecosystems detected:"]
        for e in s2.get("ecosystems", []): L.append(f"  - {e['name']} (`{e['plausibility']}`) evidence: `{e['evidence_file']}`")
        if s2.get("multiple_ecosystems"): L.append("- **Note:** Multiple ecosystems detected; primary type is heuristic.")
    L += [f"- Verification: `{s2['verification']}` | Confidence: `{s2['confidence']}`", "",
          "## 3. Understand architecture", ""]
    if s3["language_breakdown"]:
        L.append("- Language breakdown: " + ", ".join(f"{k} ({v})" for k, v in s3["language_breakdown"].items()))
    L.append(f"- Source files: {s3['source_file_count']}")
    if s3["entry_point_candidates"]:
        L.append("- Entry-point candidates: " + ", ".join("`" + e + "`" for e in s3["entry_point_candidates"]))
    if s3["config_files"]: L.append(f"- Config files: {len(s3['config_files'])}")
    if s3["test_files"]: L.append(f"- Test files: {len(s3['test_files'])}")
    L += [f"- Verification: `{s3['verification']}` | Confidence: `{s3['confidence']}`", "", "## 4. Findings", ""]
    sc = sm.get("severity_counts", {}); vc = sm.get("verification_counts", {})
    L += [f"**Total findings:** {sm.get('total_findings', len(fds))}",
          f"**Severity distribution:** high={sc.get('high', 0)}, medium={sc.get('medium', 0)}, low={sc.get('low', 0)}",
          f"**Verification distribution:** verified={vc.get('verified', 0)}, partially_verified={vc.get('partially_verified', 0)}, unverified={vc.get('unverified', 0)}", ""]
    if not fds: L.append("No problems detected by heuristic scan.")
    for i, f in enumerate(fds, 1):
        p = f["problem"]; imp = f["impact"]
        L += [f"### {i}. {p['title']}", f"- **Category:** `{p.get('category', 'unknown')}`",
              f"- **Plausibility:** `{p['plausibility']}` | **Confidence:** `{p['confidence']}` | **Verification:** `{f['verification']}`",
              f"- **Severity:** {imp['severity']} (estimated, confidence: {imp.get('severity_confidence', 'low')})"]
        if imp.get("reasoning"): L.append(f"- **Impact reasoning:** {imp['reasoning']}")
        if p.get("evidence"):
            L += ["- **Evidence:**", ] + [f"  - [{e.get('type', '')}] {e.get('description', '')}" for e in p["evidence"]]
        if p.get("context"):
            safe = {k: v for k, v in p["context"].items() if k in ("matched_key", "value_length", "strength", "category", "file", "size_bytes", "threshold", "function_count", "class_count", "import_count", "likely_responsibilities")}
            if safe: L.append(f"- **Context:** {safe}")
        L.append("- **Causes:**")
        for c in f["causes"]:
            L.append(f"  - Verified: {c.get('verified_cause', 'N/A')}")
            L += [f"  - Possible: {pc}" for pc in c.get("possible_causes", [])]
        L += ["- **Recommendations:**"]
        for rec in f["recommendations"]:
            L.append(f"  - {rec['recommendation']} (confidence: `{rec['confidence']}`)")
        L.append("")
    L += ["---", "", "### Legend", "",
          "**Plausibility:** `fact` = observed | `assumption` = inferred | `insufficient` = not verifiable", "",
          "**Confidence:** `high`/`medium`/`low` = evidence strength", "",
          "**Verification:** `verified` = evidence supports the claim | `partially_verified` = gaps | `unverified` = insufficient", "",
          "_Severity is estimated, not measured. Security findings need manual verification._"]
    return "\n".join(L).strip() + "\n"

def render_summary_markdown(s):
    L = ["# Code Summary", "", s["overview"], "", "## Project Type", ""]
    pt = s["project_type"]
    if pt.get("primary"):
        L += [f"- Primary: **{pt['primary']}** (confidence: `{pt.get('confidence')}`)",
              f"- Types: {', '.join(pt.get('types'))}"]
    else: L.append("- INSUFFICIENT EVIDENCE: no manifest files found.")
    L += ["", "## Languages", ""]
    if s.get("languages"): L += [f"- {n}: {c} file(s)" for n, c in s["languages"].items()]
    else: L.append("- None recognized.")
    tech = s.get("technologies") or []
    if tech:
        L += ["", "## Technologies (observed imports)", ""]
        L += [f"- `{t['name']}` — {t['role']}" for t in tech]
    counts = s.get("symbols", {}).get("counts") or {}; entries = s.get("symbols", {}).get("entries") or []
    L += ["", "## Functions and Classes", ""]
    if not entries: L.append("- No symbols captured from source files.")
    else:
        L.append(f"- Classes: {counts.get('class', 0)}, functions: {counts.get('function', 0)}, methods: {counts.get('method', 0)}")
        by = {}
        for e in entries: by.setdefault(e["file"], []).append(e)
        for rel in sorted(by):
            L.append(f"### {rel}")
            L += [f"- `{e['kind']}: {e['name']}`" for e in by[rel]]
        if len(entries) > 60: L.append(f"- *...and {len(entries) - 60} more symbols (see JSON).*")
    L += ["", "## Testing", "", f"- {s.get('testing', {}).get('detail', 'No test information.')}",
          "", "## Limitations", ""]
    L += [f"- {lim}" for lim in s.get("limitations", [])]
    L += ["", "_Generated by a deterministic, read-only analyzer._"]
    return "\n".join(L).strip() + "\n"

def build_report(root):
    st = collect_structure(root); pt = detect_project_type(root, st); ar = understand_architecture(root, st)
    probs = find_problems(root, st); cs = summarize_code(root, st, pt, ar)
    fds = []
    for p in probs:
        ver = verify_finding(p)
        p["verification"] = ver
        causes = find_causes(p); imp = evaluate_impact(p)
        fds.append({"problem": p, "causes": causes, "verification": ver, "impact": imp,
                    "recommendations": recommend(p, imp, causes)})
    order = {"high": 0, "medium": 1, "low": 2, "unknown": 3}
    fds.sort(key=lambda f: order.get(f["impact"]["severity"], 3))
    sev = {"high": 0, "medium": 0, "low": 0}; vc = {V: 0, PV: 0, UV: 0}
    for f in fds:
        s = f["impact"]["severity"]
        if s in sev: sev[s] += 1
        if f["verification"] in vc: vc[f["verification"]] += 1
    return {"target": st["root"], "pipeline": "facts -> evidence -> verification -> explanation -> report (8 stages)",
            "read_only_target": True,
            "stages": {"1_structure": st, "2_project_type": pt, "3_architecture": ar, "4_findings": fds},
            "summary": {"total_findings": len(fds), "severity_counts": sev, "verification_counts": vc},
            "code_summary": cs}

def main():
    p = {"target": None, "output": None, "json": False}; args = sys.argv[1:]; i = 0
    while i < len(args):
        a = args[i]
        if a in ("--output", "-o"):
            if i + 1 >= len(args): print("ERROR: --output requires a directory argument"); return 2
            p["output"] = args[i + 1]; i += 2
        elif a in ("--json", "-j"): p["json"] = True; i += 1
        elif a.startswith("-") and a != "-": print(f"ERROR: unknown option: {a}"); return 2
        else: p["target"] = a; i += 1
    if not p.get("target"):
        print("Usage: python3 analyze.py <target-directory> [--output <dir>] [--json]"); return 2
    t = os.path.abspath(p["target"])
    if not os.path.exists(t): print(f"ERROR: target path does not exist: {t}"); return 1
    if not os.path.isdir(t): print(f"ERROR: target path is not a directory: {t}"); return 1
    rep = build_report(t)
    od = os.path.abspath(p["output"] or os.getcwd()); os.makedirs(od, exist_ok=True)
    md = os.path.join(od, "ANALYSIS.md")
    with io.open(md, "w", encoding="utf-8") as fh:
        fh.write("\n\n".join(filter(None, [render_markdown(rep), render_summary_markdown(rep["code_summary"])])))
    if p["json"]:
        print(json.dumps(rep, indent=2, default=str))
        print(f"Report written to: {md}", file=sys.stderr)
    else:
        print(f"Report written to: {md}")
        print("Project Analysis Summary")
        print(f"  Target : {rep['target']}")
        print(f"  Type   : {rep['stages']['2_project_type'].get('primary') or 'INSUFFICIENT EVIDENCE'}")
        fds = rep["stages"]["4_findings"]
        print(f"  Findings: {len(fds)} (severity: " + ", ".join(f["impact"]["severity"] for f in fds) + ")")
        print("  Verification: " + ", ".join(f"{k}={v}" for k, v in rep.get("summary", {}).get("verification_counts", {}).items()))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
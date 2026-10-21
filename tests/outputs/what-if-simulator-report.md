[93m[1m! [0m agent "what-if-simulator" is a subagent, not a primary agent. Falling back to default agent
[0m
> build · big-pickle
[0m
[0m$ [0mls -la /home/khadija/Desktop/khadija/pkm/.opencode/skills/
total 24
drwxrwxr-x 6 khadija khadija 4096 Sep 18 18:01 .
drwxrwxr-x 5 khadija khadija 4096 Oct 21 18:54 ..
drwxrwxr-x 2 khadija khadija 4096 Sep 18 18:05 architecture-analysis
drwxrwxr-x 2 khadija khadija 4096 Sep 18 18:38 knowledge-linker
drwxrwxr-x 2 khadija khadija 4096 Aug 28 18:48 pkm
drwxrwxr-x 3 khadija khadija 4096 Sep 18 18:02 project-analysis
[0m
[0m$ [0mls -la /home/khadija/Desktop/khadija/pkm/.opencode/skills/project-analysis/
total 44
drwxrwxr-x 3 khadija khadija  4096 Sep 18 18:02 .
drwxrwxr-x 6 khadija khadija  4096 Sep 18 18:01 ..
-rw-rw-r-- 1 khadija khadija    18 Sep 16 15:39 .gitignore
-rw-rw-r-- 1 khadija khadija  8793 Sep 16 15:46 pipeline.yaml
drwxrwxr-x 2 khadija khadija  4096 Sep 16 15:50 scripts
-rw-rw-r-- 1 khadija khadija 13925 Sep 16 15:46 SKILL.md
[0m
[0m$ [0mls -la /home/khadija/Desktop/khadija/pkm/.opencode/skills/pkm/
total 12
drwxrwxr-x 2 khadija khadija 4096 Aug 28 18:48 .
drwxrwxr-x 6 khadija khadija 4096 Sep 18 18:01 ..
-rw-rw-r-- 1 khadija khadija 4030 Aug 28 18:48 SKILL.md
[0m
[0m$ [0mgrep -rn "project-analysis" /home/khadija/Desktop/khadija/pkm 2>&1 | head -60
grep: /home/khadija/Desktop/khadija/pkm/.git/index: binary file matches
/home/khadija/Desktop/khadija/pkm/.opencode/skills/architecture-analysis/SKILL.md:42:- Find bugs or code-quality problems → use **project-analysis**
/home/khadija/Desktop/khadija/pkm/.opencode/skills/knowledge-linker/SKILL.md:32:- Find project bugs or code quality issues → use **project-analysis**
/home/khadija/Desktop/khadija/pkm/.opencode/skills/project-analysis/SKILL.md:2:name: project-analysis
/home/khadija/Desktop/khadija/pkm/.opencode/skills/project-analysis/SKILL.md:3:description: Analyzes a software project read-only and produces an evidence-based, structured report. Use when the user asks to audit, review, analyze, inspect, or understand a codebase, or mentions the project-analysis workflow. Every finding must distinguish observed fact from inference, carry a confidence level, and pass verification before claims are made. Trigger keywords: project analysis, analyze project, codebase review, architecture review, audit code, find bugs, review repo, understand this project.
/home/khadija/Desktop/khadija/pkm/.opencode/skills/project-analysis/pipeline.yaml:4:# .opencode/skills/project-analysis/scripts/analyze.py.
/home/khadija/Desktop/khadija/pkm/.opencode/skills/project-analysis/pipeline.yaml:20:skill: project-analysis
/home/khadija/Desktop/khadija/pkm/.opencode/skills/project-analysis/pipeline.yaml:24:  python3 .opencode/skills/project-analysis/scripts/analyze.py <target-directory> \
/home/khadija/Desktop/khadija/pkm/.opencode/AGENTS.md:13:### 2. project-analysis
/home/khadija/Desktop/khadija/pkm/.opencode/AGENTS.md:14:**Location**: `.opencode/skills/project-analysis/SKILL.md`
/home/khadija/Desktop/khadija/pkm/.opencode/AGENTS.md:53:| "What problems does my project have?" | project-analysis |
/home/khadija/Desktop/khadija/pkm/.opencode/AGENTS.md:54:| "Find bugs in my code" | project-analysis |
/home/khadija/Desktop/khadija/pkm/.opencode/AGENTS.md:55:| "Review my codebase for issues" | project-analysis |
/home/khadija/Desktop/khadija/pkm/.opencode/AGENTS.md:56:| "Analyze my project" | project-analysis |
/home/khadija/Desktop/khadija/pkm/.opencode/AGENTS.md:71:**project-analysis** → General project health, problems, bugs, code quality, findings with severity
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:12:drwxrwxr-x 3 khadija khadija 4096 Sep 18 18:02 project-analysis
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:14:[0m$ [0mls -la /home/khadija/Desktop/khadija/pkm/.opencode/skills/project-analysis/
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:5:I'll start by loading the project-analysis skill since this matches its trigger.
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:6:[0m→ [0mSkill "project-analysis"
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:7:[0m→ [0mRead .opencode/skills/project-analysis/pipeline.yaml
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:8:[0m→ [0mRead .opencode/skills/project-analysis/scripts/analyze.py
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:38:./.opencode/skills/project-analysis/SKILL.md
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:39:./.opencode/skills/project-analysis/scripts/analyze.py
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:40:./.opencode/skills/project-analysis/pipeline.yaml
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:41:./.opencode/skills/project-analysis/.gitignore
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:255:./.opencode/skills/project-analysis/.gitignore
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:256:./.opencode/skills/project-analysis/pipeline.yaml
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:257:./.opencode/skills/project-analysis/scripts/analyze.py
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:258:./.opencode/skills/project-analysis/SKILL.md
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:274:[0m$ [0mpython3 .opencode/skills/project-analysis/scripts/analyze.py . --output /tmp/opencode/pkm-analysis --json > /tmp/opencode/pkm-analysis.json 2>/tmp/opencode/pkm-analysis.err; echo "exit=$?"; cat /tmp/opencode/pkm-analysis.err; ls -la /tmp/opencode/pkm-analysis
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:298:37798	./.opencode/skills/project-analysis/scripts/analyze.py
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:301:13925	./.opencode/skills/project-analysis/SKILL.md
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:302:8793	./.opencode/skills/project-analysis/pipeline.yaml
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:327:[0m→ [0mRead .opencode/skills/project-analysis/.gitignore
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:344:.opencode/skills/project-analysis/.gitignore
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:345:.opencode/skills/project-analysis/pipeline.yaml
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:346:.opencode/skills/project-analysis/scripts/analyze.py
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:347:.opencode/skills/project-analysis/SKILL.md
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:944:config_files: ['.opencode/skills/project-analysis/pipeline.yaml']
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:945:likely_dirs: {'script': ['.opencode/skills/project-analysis/scripts'], 'test': ['test', 'tests']}
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1025:[0m$ [0mecho "=== FULL STAT e2a747f ==="; git show --stat e2a747f | tail -30; echo; echo "=== all files ever under project-analysis/tests ==="; git log --all --diff-filter=D --name-only --pretty=format:"COMMIT %h %s" -- ".opencode/skills/project-analysis/tests" | head -60
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1055: .../skills/project-analysis/tests/test_analyze.py  |  563 ---
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1058:=== all files ever under project-analysis/tests ===
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1060:.opencode/skills/project-analysis/tests/fixtures/large-file-project/big_module.py
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1061:.opencode/skills/project-analysis/tests/fixtures/mixed-language/main.py
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1062:.opencode/skills/project-analysis/tests/fixtures/mixed-language/package.json
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1063:.opencode/skills/project-analysis/tests/fixtures/mixed-language/pyproject.toml
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1064:.opencode/skills/project-analysis/tests/fixtures/mixed-language/script.js
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1065:.opencode/skills/project-analysis/tests/fixtures/no-manifest/helper.py
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1066:.opencode/skills/project-analysis/tests/fixtures/placeholder-secrets/config.py
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1067:.opencode/skills/project-analysis/tests/fixtures/real-secrets/config.py
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1068:.opencode/skills/project-analysis/tests/fixtures/simple-nodejs/index.js
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1069:.opencode/skills/project-analysis/tests/fixtures/simple-nodejs/package.json
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1070:.opencode/skills/project-analysis/tests/fixtures/simple-python/app.py
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1071:.opencode/skills/project-analysis/tests/fixtures/simple-python/pyproject.toml
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1072:.opencode/skills/project-analysis/tests/fixtures/with-readme/README
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1073:.opencode/skills/project-analysis/tests/fixtures/with-readme/README.md
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1074:.opencode/skills/project-analysis/tests/fixtures/with-tests/calculator.py
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1075:.opencode/skills/project-analysis/tests/fixtures/with-tests/test_calculator.py
/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1076:.opencode/skills/project-analysis/tests/fixtures/with-todo/app.py
[0m
[0m$ [0mgrep -rn "skills.*project-analysis" /home/khadija/Desktop/khadija/pkm 2>&1 | head -40
grep: /home/khadija/Desktop/khadija/pkm/.git/index: binary file matches
/home/khadija/Desktop/khadija/pkm/.opencode/skills/project-analysis/pipeline.yaml:4:# .opencode/skills/project-analysis/scripts/analyze.py.
/home/khadija/Desktop/khadija/pkm/.opencode/skills/project-analysis/pipeline.yaml:24:  python3 .opencode/skills/project-analysis/scripts/analyze.py <target-directory> \
/home/khadija/Desktop/khadija/pkm/.opencode/AGENTS.md:14:**Location**: `.opencode/skills/project-analysis/SKILL.md`
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:14:[0m$ [0mls -la /home/khadija/Desktop/khadija/pkm/.opencode/skills/project-analysis/
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:31:/home/khadija/Desktop/khadija/pkm/.opencode/skills/architecture-analysis/SKILL.md:42:- Find bugs or code-quality problems → use **project-analysis**
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:32:/home/khadija/Desktop/khadija/pkm/.opencode/skills/knowledge-linker/SKILL.md:32:- Find project bugs or code quality issues → use **project-analysis**
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:33:/home/khadija/Desktop/khadija/pkm/.opencode/skills/project-analysis/SKILL.md:2:name: project-analysis
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:34:/home/khadija/Desktop/khadija/pkm/.opencode/skills/project-analysis/SKILL.md:3:description: Analyzes a software project read-only and produces an evidence-based, structured report. Use when the user asks to audit, review, analyze, inspect, or understand a codebase, or mentions the project-analysis workflow. Every finding must distinguish observed fact from inference, carry a confidence level, and pass verification before claims are made. Trigger keywords: project analysis, analyze project, codebase review, architecture review, audit code, find bugs, review repo, understand this project.
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:35:/home/khadija/Desktop/khadija/pkm/.opencode/skills/project-analysis/pipeline.yaml:4:# .opencode/skills/project-analysis/scripts/analyze.py.
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:36:/home/khadija/Desktop/khadija/pkm/.opencode/skills/project-analysis/pipeline.yaml:20:skill: project-analysis
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:37:/home/khadija/Desktop/khadija/pkm/.opencode/skills/project-analysis/pipeline.yaml:24:  python3 .opencode/skills/project-analysis/scripts/analyze.py <target-directory> \
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:39:/home/khadija/Desktop/khadija/pkm/.opencode/AGENTS.md:14:**Location**: `.opencode/skills/project-analysis/SKILL.md`
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:46:/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:14:[0m$ [0mls -la /home/khadija/Desktop/khadija/pkm/.opencode/skills/project-analysis/
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:49:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:7:[0m→ [0mRead .opencode/skills/project-analysis/pipeline.yaml
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:50:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:8:[0m→ [0mRead .opencode/skills/project-analysis/scripts/analyze.py
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:51:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:38:./.opencode/skills/project-analysis/SKILL.md
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:52:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:39:./.opencode/skills/project-analysis/scripts/analyze.py
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:53:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:40:./.opencode/skills/project-analysis/pipeline.yaml
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:54:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:41:./.opencode/skills/project-analysis/.gitignore
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:55:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:255:./.opencode/skills/project-analysis/.gitignore
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:56:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:256:./.opencode/skills/project-analysis/pipeline.yaml
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:57:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:257:./.opencode/skills/project-analysis/scripts/analyze.py
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:58:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:258:./.opencode/skills/project-analysis/SKILL.md
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:59:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:274:[0m$ [0mpython3 .opencode/skills/project-analysis/scripts/analyze.py . --output /tmp/opencode/pkm-analysis --json > /tmp/opencode/pkm-analysis.json 2>/tmp/opencode/pkm-analysis.err; echo "exit=$?"; cat /tmp/opencode/pkm-analysis.err; ls -la /tmp/opencode/pkm-analysis
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:60:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:298:37798	./.opencode/skills/project-analysis/scripts/analyze.py
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:61:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:301:13925	./.opencode/skills/project-analysis/SKILL.md
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:62:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:302:8793	./.opencode/skills/project-analysis/pipeline.yaml
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:63:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:327:[0m→ [0mRead .opencode/skills/project-analysis/.gitignore
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:64:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:344:.opencode/skills/project-analysis/.gitignore
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:65:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:345:.opencode/skills/project-analysis/pipeline.yaml
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:66:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:346:.opencode/skills/project-analysis/scripts/analyze.py
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:67:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:347:.opencode/skills/project-analysis/SKILL.md
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:68:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:944:config_files: ['.opencode/skills/project-analysis/pipeline.yaml']
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:69:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:945:likely_dirs: {'script': ['.opencode/skills/project-analysis/scripts'], 'test': ['test', 'tests']}
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:70:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1025:[0m$ [0mecho "=== FULL STAT e2a747f ==="; git show --stat e2a747f | tail -30; echo; echo "=== all files ever under project-analysis/tests ==="; git log --all --diff-filter=D --name-only --pretty=format:"COMMIT %h %s" -- ".opencode/skills/project-analysis/tests" | head -60
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:71:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1055: .../skills/project-analysis/tests/test_analyze.py  |  563 ---
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:73:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1060:.opencode/skills/project-analysis/tests/fixtures/large-file-project/big_module.py
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:74:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1061:.opencode/skills/project-analysis/tests/fixtures/mixed-language/main.py
/home/khadija/Desktop/khadija/pkm/tests/outputs/what-if-simulator-report.md:75:/home/khadija/Desktop/khadija/pkm/tests/outputs/project-detective-report.md:1062:.opencode/skills/project-analysis/tests/fixtures/mixed-language/package.json
[0m
[0m$ [0mcat /home/khadija/Desktop/khadija/pkm/.opencode/AGENTS.md | head -150
# AGENTS.md - Skill Routing Guide

This file documents the available skills and when to invoke each one.

## Available Skills

### 1. pkm
**Location**: `.opencode/skills/pkm/SKILL.md`
**Responsibility**: Manage the PKM knowledge base — capture ideas, create knowledge notes, track projects, log research.
**Trigger Keywords**: idea, note, knowledge, capture, save this, research, project, PKM, vault, template.
**Use When**: User wants to create, update, or organize PKM notes inside the `pkm/` folder.

### 2. project-analysis
**Location**: `.opencode/skills/project-analysis/SKILL.md`
**Responsibility**: Analyzes a software project read-only and produces an evidence-based, structured report. Finds problems, bugs, code smells, assesses project health, reviews code quality.
**Trigger Keywords**: project analysis, analyze project, codebase review, architecture review, audit code, find bugs, review repo, understand this project.
**Use When**: User asks to:
- Analyze, audit, review, or inspect a project or codebase
- Find problems, bugs, or code smells
- Assess project health or code quality
- General project review ("What problems does my project have?")

### 3. architecture-analysis
**Location**: `.opencode/skills/architecture-analysis/SKILL.md`
**Responsibility**: Analyzes and explains the architecture and structural relationships of a software project. Focuses on project structure, major components, modules, layers, component relationships, dependencies between internal components, entry points, communication between components, data flow, architectural patterns, and separation of responsibilities.
**Trigger Keywords**: software architecture, project architecture, system architecture, system structure, components, modules, layers, component relationships, internal dependencies, data flow, communication between components, architectural patterns, architecture analysis, analyze architecture.
**Use When**: User asks about:
- Software architecture or project architecture
- System structure or high-level organization
- Components, modules, or layers
- Component relationships or internal dependencies
- Data flow or communication between components
- Architectural patterns (layered, MVC, client-server, modular, monolithic)
- Separation of responsibilities between components
- How different parts of the project fit together
- Entry points and application boundaries

### 4. knowledge-linker
**Location**: `.opencode/skills/knowledge-linker/SKILL.md`
**Responsibility**: Identifies meaningful relationships between existing knowledge notes and suggests links between them. Uses observable evidence from note content, tags, and existing links.
**Trigger Keywords**: link knowledge, connect notes, find relationships, suggest links, knowledge graph, link notes.
**Use When**: User asks about:
- Find related knowledge notes
- Suggest links between notes
- What notes relate to X
- Build a knowledge graph
- Discover connections in PKM

## Skill Selection Guide

| User Question | Use Skill |
|---------------|-----------|
| "What problems does my project have?" | project-analysis |
| "Find bugs in my code" | project-analysis |
| "Review my codebase for issues" | project-analysis |
| "Analyze my project" | project-analysis |
| "What is the architecture of my project?" | architecture-analysis |
| "Explain the system structure" | architecture-analysis |
| "What are the components and how do they relate?" | architecture-analysis |
| "Show me the data flow" | architecture-analysis |
| "What architectural pattern does this follow?" | architecture-analysis |
| "How are responsibilities separated?" | architecture-analysis |
| "Find related knowledge notes" | knowledge-linker |
| "Suggest links between my notes" | knowledge-linker |
| "What notes relate to X?" | knowledge-linker |
| "Capture this idea" | pkm |
| "Create a knowledge note" | pkm |

## Key Distinctions

**project-analysis** → General project health, problems, bugs, code quality, findings with severity

**architecture-analysis** → Structural relationships, components, layers, data flow, architectural patterns (evidence-based, no quality judgment)

**knowledge-linker** → Connections between knowledge notes in PKM (evidence-based, read-only)

All skills are read-only and evidence-based. They can be used together for a complete picture.
[0m
Let us look deeper into project-analysis and how it's used, plus the skill metadata/structure.
[0m$ [0mcat /home/khadija/Desktop/khadija/pkm/.opencode/skills/project-analysis/SKILL.md | head -80
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

The analyzer is fully deterministic: directory traversal and every report list are sorted, so the same project produces byte-identical JSON and Markdown on every system. The analyzer never makes up evidence and never presents a guess as a fact.

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
[0m
[0m$ [0mcat /home/khadija/Desktop/khadija/pkm/.opencode/skills/project-analysis/pipeline.yaml
# Project Analysis — Pipeline Schema
#
# Describes the 8-stage analysis pipeline implemented by
# .opencode/skills/project-analysis/scripts/analyze.py.
#
# Every stage produces items with:
#   plausibility  : fact | assumption | insufficient
#   confidence    : high | medium | low
#   verification  : verified | partially_verified | unverified
#
# NOTE:
#   - Technology is identified ONLY from real manifest files that exist,
#     never from prose/docs.
#   - No item may be upgraded from assumption/insufficient to fact without
#     new, real evidence.
#   - The target project is always read-only; only the report file is written.
#   - The JSON output is the machine-readable source of truth.
#   - Markdown is a human-readable rendering of the same data.

skill: project-analysis
version: "2.0"
script: scripts/analyze.py
run: |
  python3 .opencode/skills/project-analysis/scripts/analyze.py <target-directory> \
    [--output <dir>] [--json]

evidence_tags:
  - fact
  - assumption
  - insufficient

confidence_levels:
  - high       # directly verified from multiple observations
  - medium     # supported by observations but not fully confirmed
  - low        # weak heuristic, single observation or inference

verification_statuses:
  - verified          # evidence directly supports the claim
  - partially_verified  # some evidence, gaps remain
  - unverified        # insufficient evidence

stages:
  - id: 1
    name: Inspect files and structure
    function: collect_structure
    produces:
      - file_count
      - dir_count
      - total_size_bytes
      - top_level
      - files_by_extension
      - files
      - directory_tree
    inputs: []
    evidence: fact
    confidence: high
    notes: >
      Walks the tree read-only, pruning ignored directories. Lists only what
      exists on disk; no interpretation. Includes directory tree for structure analysis.

  - id: 2
    name: Identify project type
    function: detect_project_type
    produces:
      - verdict          # "detected" | "INSUFFICIENT EVIDENCE"
      - evidence         # manifest file paths found
      - ecosystems       # list of detected ecosystems with evidence files
      - types            # matched technology labels
      - primary          # heuristic primary language/ecosystem
      - primary_confidence  # confidence in primary choice
      - multiple_ecosystems # whether multiple ecosystems detected
    inputs: []
    evidence: fact
    notes: >
      Recursively scans for manifest files (package.json, pyproject.toml,
      Cargo.toml, go.mod, etc.). Type is asserted ONLY from files present.
      Reports ecosystems with their evidence files. Primary is heuristic
      when multiple ecosystems exist.

  - id: 3
    name: Understand architecture
    function: understand_architecture
    produces:
      - language_breakdown
      - source_file_count
      - entry_point_candidates
      - source_grouping
      - likely_directories     # heuristic directory role detection
      - config_files
      - test_files
      - database_files
      - manifest_files
    inputs:
      - structure
    evidence: fact
    confidence: high
    notes: >
      Summarizes languages by extension, groups source by top directory, and
      flags common entry-point filenames. Identifies likely directory roles
      (api, frontend, backend, model, util, config, test, database) from
      directory names. These are heuristic and labeled as such.

  - id: 4
    name: Find problems
    function: find_problems
    produces:
      - title
      - category          # e.g. missing_documentation, large_file, code_marker, possible_secret
      - plausibility
      - confidence
      - evidence          # list of structured evidence items
      - context           # safe metadata (no secret values exposed)
    inputs:
      - structure
      - manifest_metadata
    evidence: mixed
    notes: >
      Heuristic scan for missing README/LICENSE/.gitignore/tests, oversized
      files, and source markers (TODO/FIXME/HACK, silent exception handlers).
      Large files gather additional evidence: function/class counts, import
      counts, multiple responsibilities. Hardcoded-secret detection classifies
      matches as placeholder/possible_credential/strong_credential_signature.
      Secret values are NEVER printed. Findings carry structured evidence items.

  - id: 5
    name: Find causes (conservative)
    function: find_causes
    produces:
      - verified_cause      # directly observable only
      - possible_causes     # plausible but not established by static inspection
      - plausibility        # fact | assumption | insufficient
      - confidence
      - verification
    inputs:
      - problem
    evidence: mixed
    notes: >
      Conservative cause analysis. Verified causes are limited to directly
      observable facts (e.g. "file not found in the listing"). Possible causes
      are explicitly labeled as unestablished. Historical or intentional
      explanations (e.g. "responsibilities grew over time") are NOT stated.
      If the cause cannot be determined statically, it is reported as
      insufficient or unknown.

  - id: 6
    name: Evaluate impact
    function: evaluate_impact
    produces:
      - severity           # high | medium | low
      - severity_confidence
      - reasoning          # why this severity was assigned
      - plausibility
      - confidence
      - verification
    inputs:
      - problem
      - context
    evidence: assumption
    notes: >
      Evidence-first severity heuristic based on category, evidence strength,
      and context. Severity is an ESTIMATE, never measured. Reasoning explicitly
      states what static inspection cannot determine. Large files with multiple
      responsibilities may reach medium. Strong credential signatures may
      reach high. Code markers default to low. Assumption-based findings
      are capped at medium.

  - id: 7
    name: Recommend solutions
    function: recommend
    produces:
      - recommendation
      - confidence
      - verification
      - severity
      - based_on           # explains what the recommendation depends on
    inputs:
      - problem
      - impact
      - causes
    evidence: assumption
    notes: >
      Evidence-based recommendations connected to specific findings. Each
      recommendation states what it depends on (based_on) and what the next
      human verification step should be. Recommendations for insufficient
      evidence cases suggest verification rather than assuming a solution is
      certain.

  - id: 8
    name: Create analysis report
    function: build_report + render_markdown
    produces:
      - ANALYSIS.md        # written to --output <dir> (default cwd)
      - JSON (with --json) # printed to stdout, pure JSON
      - summary            # total findings, severity counts, verification counts
    inputs:
      - all_prior_stages
    evidence: mixed
    notes: >
      Assembles the report. Per-finding order is: facts and evidence (stages 1-4),
      verification computed from evidence first, then human-readable explanation
      (causes, impact, recommendations) produced last. This ensures explanations
      never influence verification. A legend for plausibility, confidence, and
      verification is included. JSON is the machine-readable source of truth.
      Markdown is a rendering of the same data. The target project is never
      written to.

report:
  file: ANALYSIS.md
  output: --output <dir>   # defaults to current working directory
  json: --json             # stdout = pure JSON, human messages on stderr
  sections:
    - Target and pipeline
    - Inspect files and structure
    - Identify project type
    - Understand architecture
    - Findings (problem / causes / verification / impact / recommendations)
    - Code summary (project type, languages, technologies, symbols, data flow, dependencies, configuration, testing)
    - Legend (plausibility | confidence | verification)

guarantees:
  read_only_target: true
  no_guess_fill: true           # insufficient evidence is reported as such, never invented
  evidence_required_for_fact: true
  no_secret_values_exposed: true
  structured_evidence: true     # findings contain typed evidence items (including line numbers)
  verification_per_finding: true
  verification_is_evidence_first: true  # verified from evidence/plausibility/confidence, not from explanation layer
  conservative_causes: true     # causes are only "evidence-supported" when directly observable; otherwise "possible" or "unknown"
  deterministic_ordering: true  # directory traversal and all report lists are sorted; identical input -> identical output on every system
  json_source_of_truth: true    # JSON and Markdown must not conflict
[0m

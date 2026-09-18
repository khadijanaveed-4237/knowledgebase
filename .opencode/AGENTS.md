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
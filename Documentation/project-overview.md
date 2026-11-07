# Project Overview

## Introduction

This project is a **Personal Knowledge Management (PKM) vault** integrated with AI-powered analysis capabilities for software projects. It serves as a centralized knowledge base for capturing, organizing, and retrieving personal knowledge, while also providing deterministic, read-only analysis of codebases to assess project health, architecture, and quality.

## What the Project Does

The project combines two primary functionalities:

1. **Personal Knowledge Management** — A structured vault for capturing and organizing ideas, knowledge notes, projects, and research. It uses consistent templates with YAML frontmatter to ensure uniformity across all notes. The vault is located in the `pkm/` directory and contains:
   - `Ideas/` — Raw, unprocessed idea capture
   - `Knowledge/` — Distilled, permanent knowledge notes
   - `Projects/` — Project tracking with goals, tasks, and progress logs
   - `Research/` — Research questions, hypotheses, and findings
   - `Templates/` — Canonical note skeletons (ideas, knowledge, projects, research)

2. **AI Project Analysis** — A deterministic, evidence-based Python analyzer (`analyze.py`) that can inspect any software project read-only and produce structured reports covering:
   - Project type detection from manifest files
   - Architecture analysis (languages, entry points, directory roles)
   - Problem detection (missing documentation, large files, code markers, possible secrets)
   - Cause analysis with evidence classification
   - Impact assessment (heuristic severity estimates)
   - Recommendations connected to findings
   - Both JSON (machine-readable) and Markdown (human-readable) output

## Main Purpose and Objectives

The primary purpose of this project is to provide a personal knowledge management system that:

- **Organizes knowledge** consistently using structured templates and YAML frontmatter
- **Enables evidence-based project analysis** without modifying the target codebase
- **Provides deterministic, reproducible** analysis results across different systems
- **Maintains read-only behavior** — the target project is never modified
- **Supports multiple ecosystems** — detects and reports on Python, Node.js/JavaScript, Rust, Go, Ruby, PHP, Java, Kotlin, and other technology stacks
- **Emphasizes evidence-first reporting** — all claims are tagged with plausibility (fact/assumption/insufficient), confidence (high/medium/low), and verification status (verified/partially_verified/unverified)

## Problems It Aims to Solve

This project addresses several common challenges:

1. **Knowledge fragmentation** — Ideas and notes get lost across different locations; this vault provides a single, structured destination for all personal knowledge.

2. **Manual project analysis overhead** — Assessing a codebase's health, architecture, and problems typically requires manual code review and tooling; this project automates the evidence-gathering phase.

3. **Inconsistent analysis** — Human reviews of the same project can vary significantly; the deterministic analyzer produces identical output on every run.

4. **Guess-based assessments** — Many analysis tools present hypotheses as facts; this project explicitly distinguishes observed facts from inferences, supporting claims with evidence, confidence levels, and verification status.

5. **Secret exposure risk** — Many analyzers accidentally print secret values; this project explicitly never exposes actual secret values, only reporting detection metadata (file, line, key name, length, strength category).

6. **Lack of structured reporting** — Analysis results often exist only in conversation or informal notes; this project generates persistent, shareable reports in both JSON and Markdown formats.

## Key Design Principles

- **Evidence-first**: All claims must have supporting evidence from the codebase or project structure
- **Read-only**: Target projects are never modified, installed, or analyzed via runtime execution
- **Deterministic**: Same input produces identical output on every system
- **Conservative**: Insufficient evidence is reported as such; assumptions are explicitly labeled
- **Structured**: JSON is the machine-readable source of truth; Markdown renders the same data
- **Privacy-safe**: Actual secret values are never printed; only safe metadata (key name, length, detection type) is reported
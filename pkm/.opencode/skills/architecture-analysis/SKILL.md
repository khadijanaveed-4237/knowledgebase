---
name: architecture-analysis
description: Analyzes and explains how a software project is organized, including its components, layers, dependencies, entry points, and data flow. Use when the user asks about project architecture, structure, components, modules, layers, or how different parts of a project work together.
---

# Architecture Analysis

## Purpose

Explains how the different parts of a software project fit and work together.

The skill is **read-only**. It analyzes the project without changing, deleting, or creating project files.

## When to Use

Use this skill when the user asks to:

- Understand a project's architecture
- Understand the overall project structure
- Identify major components or modules
- Understand layers and their responsibilities
- Find entry points
- Understand how components communicate
- Follow data flow through the project
- Identify architectural patterns
- Understand how responsibilities are divided

## What It Analyzes

- Project folder and file structure
- Major components and modules
- Layers and their responsibilities
- Dependencies between components
- Entry points
- Data flow
- Communication between components
- Architectural patterns
- Separation of responsibilities

## What It Does Not Do

- Find bugs or code-quality problems → use **project-analysis**
- Fix or modify project files
- Delete or rename files
- Analyze security vulnerabilities
- Perform detailed dependency audits
- Organize PKM notes → use **pkm**
- Create links between knowledge notes → use **knowledge-linker**
- Guess why developers made a particular design decision

## How It Works

1. **Inspect the project**
   - Look at the folder and file structure.

2. **Identify the main components**
   - Find important modules, services, classes, and other project parts.

3. **Understand responsibilities**
   - Determine what each major component does based on its actual code.

4. **Find connections**
   - Check imports, function calls, references, APIs, and other observable connections.

5. **Find entry points**
   - Identify where the application or major workflows start.

6. **Follow the data flow**
   - Explain how data moves between important components.

7. **Identify the architecture**
   - Identify patterns such as layered, MVC, modular, or similar patterns only when there is enough evidence.

8. **Create the explanation**
   - Present the architecture in a simple and organized way.

## Evidence Rules

Every important architectural claim should be based on evidence.

Use these labels:

- **[FACT]** — Directly observed in the project.
- **[INTERPRETATION]** — A reasonable conclusion based on the evidence.
- **[INSUFFICIENT EVIDENCE]** — There is not enough information to make a reliable conclusion.

### Important Rules

- Do not assume architecture from folder names alone.
- Inspect relevant files before making architectural conclusions.
- Do not invent relationships between components.
- Do not assume a pattern just because the project resembles one.
- "Not found" does not automatically mean "does not exist."
- Clearly separate facts from interpretations.
- If there is not enough evidence, say so.

## Output Format

# Architecture Analysis

## 1. Project Overview

Brief explanation of what the project appears to do.

## 2. Project Structure

Explain the important folders and files.

## 3. Main Components

Describe the major components and their responsibilities.

## 4. Component Relationships

Explain how the components connect and communicate.

## 5. Entry Points

Identify the main places where execution begins.

## 6. Data Flow

Explain how important data moves through the system.

## 7. Architecture Pattern

Describe the architectural pattern only when supported by evidence.

## 8. Responsibility Division

Explain how responsibilities are divided between components.

## 9. Evidence and Limitations

Clearly identify uncertain areas and information that could not be determined.

## Example

Instead of saying:

> "The `api` folder handles all communication because its name suggests it."

Say:

> **[FACT]** The files inside `api/` contain functions that send HTTP requests to external services.
>
> **[INTERPRETATION]** Based on these functions, the `api/` component appears to be responsible for external API communication.
>
> **[INSUFFICIENT EVIDENCE]** The inspected files do not provide enough information to determine whether all external communication goes through this component.

## Limitations

Architecture analysis is based only on the project files that can be inspected
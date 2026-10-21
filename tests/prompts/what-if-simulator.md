# What-If Simulator Test

Ask the What-If Simulator subagent to analyze this hypothetical change:

"What if a core component used by three other components stops working?"

Check:
1. Identify the affected components and their dependencies.
2. Predict direct and indirect consequences.
3. Identify possible failure scenarios and risks.
4. Separate verified facts, assumptions, predictions, and unknowns.
5. Recommend a safe plan to prevent or handle failures.
6. Suggest verification steps.

Requirements:
- Inspect the actual project before making conclusions.
- Support findings with relevant file paths or project evidence.
- Do not invent dependencies that cannot be verified.
- Do not implement the hypothetical change.
- Do not modify, create, or delete project files.
- Clearly state any limitations.

Return a structured report with affected components, predicted impact, risks, recommendations, and unknowns.
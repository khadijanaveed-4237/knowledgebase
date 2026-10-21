# Chaos Tester Test

Ask the Chaos Tester subagent to evaluate the project against unusual conditions and potential failure scenarios.

Check:
1. Missing or invalid input.
2. Missing files or configuration.
3. Unexpected component failures.
4. Dependency failures.
5. Error handling and recovery.
6. Prioritized recommendations.

Requirements:
- Inspect the actual project structure and code before making conclusions.
- Support findings with relevant file paths or project evidence.
- Distinguish confirmed weaknesses from hypothetical risks.
- Do not run destructive commands or intentionally break working services.
- Do not modify, create, or delete project files.
- Clearly state any limitations.

Return a structured report with test scenarios, expected behavior, evidence, risk levels, and recommendations.

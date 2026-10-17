---
type: llm
---
PASS if the agent proceeds without asking the user for missing details, a mode choice, or permission to continue between stages. It should label assumptions when filling gaps.
FAIL if the agent pauses for user input or stage approval. The prompt specifies no mode, so autopilot is the default.
Research questions recorded in the workbook as future validation tasks are allowed.

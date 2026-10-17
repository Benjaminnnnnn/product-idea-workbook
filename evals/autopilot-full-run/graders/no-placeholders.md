---
type: regex
pattern: '\[(?:\.\.\.|[a-z][a-z /:–-]{2,60})\](?!\()'
match: not_contains
target: { source: file, path: workbooks/tutorloop.md }
---

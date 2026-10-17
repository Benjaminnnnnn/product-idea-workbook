---
type: regex
pattern: '\*\*Decision:\*\*\s*\**(GO|PIVOT|NO-GO)\b'
target: { source: file, path: workbooks/tutorloop.md }
---

---
name: idea-screen
description: Use when someone has several product ideas and wants to know which one to pursue, or wants a quick, cheap sanity check on an idea before a full workbook — "which of these ideas should I build?", "compare these ideas", "rank my ideas", "quick gut check on this idea".
---

# Idea Screen

A quick pass over 1–5 product ideas to find the one that deserves a full
workbook. Each idea gets a rough answer to every stage's gate question, backed
only by the few numbers the verdict depends on. It costs a small fraction of a
full run. Run `new-product-idea` only on the ideas that advance.

## Input

1–5 ideas, with the customer and geography for each if known. Fill in anything
missing yourself and label it **ASSUMPTION**. Ask only if an idea is too vague
to name a customer, and then ask once, with at most 3 questions in total.

## Procedure

1. **Sharpen each idea.** Give each one a customer (one actor you could find 10 of this week), a job (a verb plus an object, with no solution in it), and the strongest alternative, which is often doing nothing.
2. **Pick 3 numbers per idea:** (a) the loss per actor per year that the problem causes, (b) the number of actors you can reach, and (c) the price of the top competitor or the cost of the current workaround.
3. **Research on a budget.** Run every search for every idea in **one turn** (at most 3 per idea). In one more turn, open at most one page per number you'll cite, and find the number on it. If a page fails or is a PDF, don't open the saved file: mark the number **ASSUMPTION** and give a range. Never cite a source you didn't open.
4. **Score each idea from 1 to 5** on the rubric below.
5. **Give a verdict.** **ADVANCE**: no score below 3, and a total of at least 15. **DROP**: any score of 1. Otherwise **MAYBE**. Add one sentence on why, plus the riskiest assumption and the cheapest way to test it with real customers.

| Score | Problem | Market | Gap | Pay |
|---|---|---|---|---|
| 5 | Cited, recurring loss per actor | Cited count; 1% of it would sustain a small team | A buying factor where every named alternative is weak | The loss per actor is well above a price at or below competitors' |
| 3 | Plausible loss, but ASSUMPTION only | Count is borderline or assumed | A gap exists, but a strong player could close it quickly | Value is about the same as the price, or willingness to pay is unknown |
| 1 | No sign that anyone has it | Too few actors, or unreachable | Already well served, or doing nothing works fine | Customers expect it free, or the value is below any viable price |

## Output

Write `workbooks/idea-screen.md`, replacing it if it exists:

```markdown
# Idea Screen — <YYYY-MM-DD>

| Idea | Customer | Problem | Market | Gap | Pay | Total | Verdict |
|---|---|---|---|---|---|---|---|
| <name> | <actor> | 4 | 3 | 4 | 4 | 15 | ADVANCE |

## <Idea name>

- **Customer / job:** <actor> needs to <verb + object>.
- **Strongest alternative:** <competitor, or doing nothing, and why it's good enough today>.
- **Key numbers:** loss <n> per actor per year (Publisher, Year); <n> reachable actors (Publisher, Year); top alternative costs <n> (Publisher, Year).
- **Verdict:** ADVANCE — <one sentence>.
- **Riskiest assumption:** <assumption>. Test: <cheapest test with real customers>.

## Appendix — References

- Publisher (Year). *Title.* URL. Accessed YYYY-MM-DD.
```

Write money as `\$47.99`, never `$47.99`. Leave a blank line before each table and heading.

## Finish

Tell the user the ranking, and the idea to take into `new-product-idea`. The
full workbook reuses this screen's cited numbers, so that research isn't
repeated. If every idea is DROP, say so plainly. That's a good result, because
it saved the cost of a full workbook.

## Common mistakes

| Mistake | Fix |
|---|---|
| A full workbook's depth for every idea | Three numbers per idea. The full workbook comes later, for the winner. |
| Industry revenue used as the loss | Size the loss the problem causes for one actor. |
| Every idea scores 4 | Score against the rubric. If nothing separates them, the evidence is too thin, so say which number would decide it. |

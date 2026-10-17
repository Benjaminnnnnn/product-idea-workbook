---
name: market-research
description: Use when a product or market analysis needs real, cited numbers — customer counts, market size, competitor prices and positioning, industry statistics, willingness to pay — or when a figure in a product idea workbook has no source.
---

# Market Research

Return numbers someone else can check. A number without a source you can
check is an **ASSUMPTION**, never a fact.

## Input

The facts or numbers needed (e.g., "number of US independent music
teachers"), the geography, and today's date. If they aren't given, list the
facts the current workbook section needs before you search.

## Budget

Each turn re-sends the whole conversation, so the number of tool calls is what costs tokens. Research only what changes the decision.

- At most **8 questions** per workbook stage. These are the numbers the stage's decision depends on: actor counts, the loss per actor, and competitor prices. Mark every other number ASSUMPTION with a range.
- Run all the searches in **one turn**, as parallel calls. Then open all the pages in one more turn. Open one page per number, and stop once you've found it.
- If a page fails to load, is a PDF, or is saved to a file instead of shown, don't open the file. Try one other source, then mark the number ASSUMPTION.
- Never search again for a number that's already cited in the workbook or in an idea screen. Reuse that citation.

## Procedure

1. Write the list of questions first. Each one asks for a single number or fact.
2. Search the web for each one, using whatever search tool you have. Prefer sources in this order: government statistics, peer-reviewed studies, company filings and official pricing pages, industry reports, reputable press. Skip content farms, listicles, and pages that don't name their own source.
3. **Open the page and find the number on it.** A search snippet isn't a source, and snippets are often outdated or wrong.
4. Record each result in the output table. Note any mismatch: a different geography, data more than 3 years old, a small sample, or a survey rather than a census.
5. If two credible sources disagree, report both and use the range.
6. If you can't find a source, or you have no search tool, give your best estimate labeled **ASSUMPTION**. Show how you derived it and what someone should search to verify it.

## Output

| Question | Answer | Source (publisher, year) | URL | Caveat |
|---|---|---|---|---|
| [question] | [number] | [publisher, year] | [URL you opened] | [geography, age, sample] |

Then give:
- **Inline citation** for the workbook: `(Publisher, Year)`, e.g. `(BLS, 2026)`.
- **Appendix entries** for `## Appendix — References`: `Publisher (Year). *Title.* URL. Accessed YYYY-MM-DD.`
- **Assumptions**: each ASSUMPTION, with how it was derived and how to verify it.

## Quality gate

- [ ] No more than 8 questions, searched in one turn
- [ ] Every answer has a URL you actually opened, or is labeled ASSUMPTION
- [ ] Every number appears on its cited page
- [ ] Geography and age mismatches are noted
- [ ] Prices include the date you checked them

## Common mistakes

| Mistake | Fix |
|---|---|
| Citing a page you didn't open | Open it and find the number, or label it ASSUMPTION. |
| An old statistic presented as current | Look for the latest edition. Always state the year. |
| A global number used for a US market | Find the US figure, or flag the mismatch. |
| A precise-looking estimate ("1,234,567 users") with no source | Give a rounded range labeled ASSUMPTION. |

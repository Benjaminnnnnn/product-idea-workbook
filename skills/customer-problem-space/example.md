<!-- Generated from examples/shiftplate.md by scripts/build.py. Edit that file, then run: python3 scripts/build.py -->
# Worked example: ShiftPlate (fictional product)

This shows the depth and evidence standard to match. Don't copy its content or numbers; research the user's own product.

## 1. Customer Problem Space

### 1. Fertile Land
Meal planning for people with irregular work schedules. **Why now:** Mealime, a popular free meal planner with 54K App Store ratings, shuts down on 21 October 2026 (Mealime, 2026), and its users are looking for a replacement.

### 2. Customer
A US hospital staff nurse (RN) working 12-hour or rotating shifts.

### 3. Job To Be Done
Eat a proper meal during and after a 12-hour shift.

### 4. Outcomes
| Actual outcome | Desired outcome | Measurement method |
|---|---|---|
| Shift days with a skipped or snack-replaced main meal: 3 of 4 (ASSUMPTION, based on 78.2% of night-shift nurses having irregular meal timing (Samhat et al., 2020)) | 1 of 4 | Shift days logged with a skipped or snack-replaced main meal ÷ shift days logged, per user per week |
| Takeout and vending spend on shift days: \$15 per shift day (ASSUMPTION) | \$5 per shift day | Shift-day food spend logged in the app ÷ shift days, per user per week |
| Time spent planning and prepping shift meals: 3 h per week (ASSUMPTION) | 1 h per week | Weekly self-reported check-in, averaged across active users |

### 5. Problem
**a. Gap**

2 shift days per week with a skipped main meal (3 → 1 of 4), and \$10 of avoidable food spend per shift day (\$15 → \$5). This means there is a 2-day gap in eating properly at work and a \$10 gap in daily food spend.

**b. Causes**
1. Meal breaks are unpredictable, because patient care interrupts or cancels them.
2. Night shifts have few food options: cafeterias are closed, leaving vending machines.
3. After a night shift, nurses are too exhausted to cook.
4. Rotas rotate, so a fixed weekly meal plan breaks within days.
5. General meal planners assume three meals at fixed clock times.

### 6. Customer Journey Map
| Stage | Doing | Thinking / feeling | Pain point | Opportunity |
|---|---|---|---|---|
| Get the rota | Checks next month's shifts | "Three nights in a row again." | The rota arrives late and changes | Import the rota and replan automatically |
| Plan the week | Tries to plan around shifts | "I'll figure it out later." | Planners ignore shift timing | Meals timed to the shift, not the clock |
| Shop | Shops on a day off | "What do I even need?" | No list that matches the shifts | One shopping list per rota stretch |
| Prep | Cooks if there's energy | "Too tired, I'll buy something." | No energy after nights | One batch session that covers the whole stretch |
| Shift day | Grabs vending or takeout | "No break yet. Chips again." | A meal isn't ready to grab | A labeled shift box, ready in the fridge |
| Recover | Sleeps, eats whatever is there | "I'm starving and wrecked." | No plan for after nights | Recovery meals that are ready on waking |

### 7. Use Cases
- Plan meals around a rotating schedule *(for: rotating-shift nurses)*
- Grab-and-go shift box *(for: 12-hour day nurses)*
- Night-shift fueling plan *(for: night nurses)*
- Post-night recovery meal *(for: night nurses)*
- One batch-prep session per rota stretch *(for: all shift nurses)*
- Shared meal plan with a household *(for: nurses with partners or kids)*

### 8. Problem Sizing
- **Per instance:** one shift day of takeout or vending instead of a planned meal = \$15 − \$5 = \$10 of extra spend (ASSUMPTION).
- **Annualized per actor:** 2–3 such days per week × 48 working weeks × \$7–\$10 = \$672–\$1,440 per nurse per year.
- **Total impact, annually:** 1,635,669 nurses (see 2.1) × \$672–\$1,440 = **\$1.1B–\$2.4B per year** in avoidable food spend, before any health costs.
- **Assumptions:** \$15 takeout and \$5 home-meal cost per shift day (verify with a 15-nurse food diary). 2–3 affected days per week, based on a Lebanese sample (Samhat et al., 2020); US rates are unverified. 48 working weeks per year.

### 9. Problem Category
Shift-work nutrition gap

### 10. Problem Statement
Nurses are expected to eat proper meals to stay alert through 12-hour shifts. In reality, 78.2% of nurses in a night-shift study had irregular meal timing, and 56% reported gaining weight since starting work (Samhat et al., 2020). We estimate that 1,635,669 US hospital nurses on 12-hour or rotating shifts each lose \$672–\$1,440 a year to takeout and vending on shift days, or **\$1.1B–\$2.4B per year** in total. Therefore, a solution is needed to help shift-working nurses eat a proper meal during and after a 12-hour shift.

### Stage decision
**PROCEED**: the problem is documented in published research and is worth \$1.1B or more a year, even at the low end of the estimate.

**Riskiest assumption:** how many shift days US nurses actually skip a main meal. Test it with a 2-week food diary from 15 nurses at 2 hospitals.

## Appendix — References

- U.S. Bureau of Labor Statistics (BLS) (2026). *Occupational Outlook Handbook: Registered Nurses.* https://www.bls.gov/ooh/healthcare/registered-nurses.htm. Accessed 2026-10-16.
- Samhat et al. (2020). *Relationship between night shift work, eating habits and BMI among nurses in Lebanon.* BMC Nursing. https://pmc.ncbi.nlm.nih.gov/articles/PMC7158014/. Accessed 2026-10-16.
- Mealime Meal Plans Inc. (2026). *Mealime Meal Plans & Recipes*, App Store listing. https://apps.apple.com/us/app/id1079999103. Accessed 2026-10-16.
- Eat This Much Inc. (2026). *Eat This Much – Meal Planner*, App Store listing. https://apps.apple.com/us/app/eat-this-much-meal-planner/id981637806. Accessed 2026-10-16.

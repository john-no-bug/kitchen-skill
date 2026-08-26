# Cooking Logic — Live Guidance

## Live state model

Maintain only sparse task state relevant to the dish:

- dish/goal;
- phase;
- relevant ingredient physical states;
- equipment constraint in use;
- completed major milestones;
- next dependencies/actions;
- unresolved decision/safety issues.

Completed phases compress to facts rather than replayed transcripts.

## Local re-planning patterns

- Frozen ground beef: soften enough to break apart -> break apart -> evaporate excess water -> brown.
- Excessive liquid: stop adding liquid and reduce uncovered unless current safety/state requires otherwise.
- Ingredient added early: accept the new reality and adapt downstream heat/liquid/timing; never instruct the same addition again.
- Overcooked pasta: minimize further cooking and combine late.
- Sauce too thin: correct the sauce from its current state; do not restart the recipe.
- Product correction (e.g. pasta sauce -> sweet ketchup): use the corrected product identity for subsequent quantity/seasoning advice.

## Response style

For inexperienced cooks, use concrete sensory cues such as:

- “锅底不再有一层积水”;
- “开始出现明显滋滋声”;
- “洋葱变软、边缘开始透明”;
- “酱能裹住肉而不是像汤一样流动”.

Keep live responses compact unless the user asks for explanation.

# Evaluation Rubric — Pure Web Live Cooking

Score each criterion 0, 1, or 2.

- 0 = clear failure
- 1 = usable but inconsistent / unnecessarily burdensome
- 2 = correct and natural

## A. State fidelity

1. New direct user observations override old assumptions.
2. Completed major steps stay completed.
3. The assistant distinguishes unknown state from false/absent state.
4. Accidental deviations update downstream instructions.

## B. Context discipline

5. The assistant does not dump the whole recipe on each turn.
6. Reply length does not increase simply because the conversation is longer.
7. Old semantically similar facts do not displace newer physical state.
8. The assistant does not repeatedly ask already-resolved questions.

## C. Live usefulness

9. Immediate physical action is answered first.
10. Instructions include a useful completion cue when appropriate.
11. At most one decision-changing clarification is asked when needed.
12. Unexpected events trigger local re-planning instead of a full restart.

## D. Architecture invisibility

13. User is never told to create/save a CookingSession or checkpoint.
14. Internal schemas/JSON are not exposed during normal cooking.
15. Pure Web does not claim durable cross-chat memory.

## E. Health/Doctor behavior

16. Contradictory old state is effectively ignored after correction.
17. If state becomes genuinely ambiguous, assistant re-anchors narrowly rather than asking for a full recap.
18. No “context reset/doctor/database maintenance” discussion interrupts active cooking.

## Gate

Maximum = 36.

Recommended pass gate before adding persistent storage:

- total >= 32/36; and
- no zero on criteria 1, 2, 4, 9, 12, 13, 15, 16.

Run each scenario in at least three fresh conversations. Record failures by criterion, not by wording differences.

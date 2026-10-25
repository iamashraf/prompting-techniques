# Zero-Shot: what running it actually showed

Zero-shot means no examples — just a role, a constraint ("don't
fabricate"), and the task. We ran the baseline against `llama3.1:8b`,
then four experiments to see where that breaks.

## The headline: it can't add

Across five separate attempts, at two temperatures, the model never
once got "Supplier Failure + Natural Disaster" right. The real answer
is $3,300,000.

| Run | Temp | Said | Off by |
|---|---|---|---|
| First run | 0.0 | $3,410,000 | +$110,000 |
| Every later temp=0 run | 0.0 | $3,310,000 | +$10,000 |
| Worst temp=0.9 run | 0.9 | $7,110,000 | +$2,385,000 |

It wasn't sometimes right — it was *always* wrong, by varying amounts.
It isn't computing a sum; it's generating a number that sounds
plausible next to the others. Higher temperature didn't just reword
things, it blew up how wrong the arithmetic got.

## Three smaller findings

- **Temperature=0 is "mostly" deterministic, not perfectly.** Two
  back-to-back calls in the same process were identical; the very
  first call of the day (a separate process) landed on a different
  wrong number than every later one.
- **Missing data was handled well.** Given one event with every
  numeric field blank, it said "unknown" rather than inventing
  numbers — the opposite of what we expected. It did add an unrequested
  fifth section, though — format discipline slipped once the input got
  weird.
- **The system prompt encouraged the mistake.** With the persona
  removed, the model stopped attempting the combined-total math
  entirely — it stuck to per-event facts, and never got the sum wrong
  because it never tried.

## Takeaway

The risk isn't fabrication from nothing — it handled a real data gap
fine. It's quietly getting *derived* numbers wrong while sounding sure
of itself. That's the gap Chain-of-Thought is meant to close.

# Zero-Shot: what running it actually showed

Zero-shot means no worked examples — just a role, a constraint ("don't
fabricate"), and the task. We ran the baseline once against `llama3.1:8b`,
then four small experiments to see where that actually breaks. Full logs
for every run are in `runs/` if you want to check our reading of them.

## Does it repeat itself?

We sent the identical prompt twice, back to back, at `temperature=0`.
Both outputs came back word-for-word identical. Then we did the same
thing at `temperature=0.9` — the two runs diverged: different phrasing,
different structure, different numbers.

That part isn't surprising. What is: our very first run of the day (a
separate process, run earlier) landed on a different total than every
later `temperature=0` run that followed — same prompt, same setting,
different number. So `temperature=0` keeps you consistent *within a
session*, but it's not a hard guarantee across separate runs of the
program.

## Can it add?

Across five separate attempts — at both temperatures — the model never
once got "Supplier Failure + Natural Disaster" right. The real answer,
straight from the input data, is $3,300,000.

| Run | Temperature | It said | Off by |
|---|---|---|---|
| First run of the day | 0.0 | $3,410,000 | +$110,000 |
| Every later `temp=0` run | 0.0 | $3,310,000 | +$10,000 |
| Worst `temp=0.9` run | 0.9 | $7,110,000 | +$2,385,000 |

It wasn't "sometimes right, sometimes wrong" — it was *always* wrong, by
varying amounts. That's the tell: it isn't computing a sum, it's
generating a number that reads as plausible next to the others. Higher
temperature didn't just change the wording here, it also blew up how
wrong the arithmetic got.

## What happens when the data's missing?

We fed it one event with a severity rating and every numeric field left
blank. It didn't invent numbers — it wrote "revenue at risk is unknown"
and said so needs more data. Good instinct, and the opposite of what we
expected going in.

But it also added a fifth section ("Recommendations for Future
Improvement") that we never asked for. The 4-section structure held
perfectly on normal data and slipped the moment the input got weird.

## Does the system prompt matter?

Same user prompt, run with and without the "Senior Supply Chain Risk
Analyst" persona. Both kept the requested structure fine — that's coming
from the numbered list already in the user prompt, not the system
prompt. The difference showed up elsewhere: the version *with* the
persona is the one that tried to add two numbers together (and got it
wrong). The version *without* it stuck to reporting each event on its
own and never attempted that sum — so it also never got it wrong.

## Takeaway

The real risk here isn't the model making things up from nothing — it
handled a genuine data gap well. It's quietly getting *derived* numbers
wrong while sounding completely sure of itself. That's the specific gap
Chain-of-Thought is meant to close: making the model show its arithmetic
instead of jumping straight to a confident-sounding total.

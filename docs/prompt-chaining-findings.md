# Prompt Chaining: what running it actually showed

Instead of one call doing everything, this breaks the task into four
separate calls: root causes, then financial totals (in isolation),
then mitigations, then a final call that assembles everything. Each
step's output feeds the next.

## The math came out right, for a different reason than CoT

Step 2 — a narrow call asked to do nothing but add up two columns —
got both totals exactly right: $4,725,000 financial impact, $9,950,000
revenue at risk. Same correct answer Chain-of-Thought reached. But the
*reason* it's reliable here is structurally different and arguably
stronger: once Step 2 computes that number, it's handed to Step 4 as
a fixed, already-verified input. Step 4 doesn't recompute anything —
it just transcribes a number it was given. CoT computes and writes in
the same breath, so even a correct run still carries some single-pass
risk (we measured this directly with self-consistency: 2 of 5 CoT
samples failed to even state a total at higher temperature). Chaining
removes that risk for whatever gets frozen into an intermediate step,
not by being "smarter," but by never asking the final step to redo
work that's already settled.

## The root-cause step still filled in details that weren't there

Step 1 was asked for one-sentence causes and returned things like "a
severe typhoon" and "the trucking company's decision to go on strike"
— specifics invented beyond what the raw data actually said (just
"Natural Disaster" and "Transportation Disruption," no further
detail). Not a new failure mode; every technique so far has done this.
What's different is *where* it happens: isolated to one specific,
narrow call. That's a real structural advantage chaining has over
single-call techniques — it creates a natural seam where you could
insert exactly the kind of claim-by-claim check that fixed our judge
earlier, between any two steps, before a fabricated detail ever
reaches the final report.

## Takeaway

Chaining's value isn't that any one step reasons better. It's that
correct results can be frozen and passed forward instead of
re-derived, and the pipeline gives you places to check quality
mid-flight that one big prompt doesn't. The cost is real too: four
calls here, versus one for every single-shot technique so far.

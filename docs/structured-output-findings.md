# Structured Output: what running it actually showed

Instead of free prose, the model returns JSON matching a fixed schema
(one entry per event, plus two total fields), via Ollama's `format`
parameter. The payoff isn't better reasoning — it's that we can check
the model's own arithmetic in plain Python, by summing the per-event
numbers it returned and comparing them to the totals it *also*
returned, with zero ambiguity and zero LLM judge involved.

## Format was perfect. The math wasn't.

All 6 events came back, every per-event figure exactly matching the
real data — the schema did its job completely. But:

```
financial impact:  stated $4,330,000, computed $4,725,000 -> False
revenue at risk:   stated $8,350,000, computed $9,950,000 -> False
```

Both totals wrong — revenue at risk off by $1.6M, about 16%. Same
mistake Zero-Shot made on day one, now proven with `sum()` instead of
a judge's opinion or a regex guess. A schema constrains *shape*, not
*computation*. The model can return a perfectly valid, perfectly
formatted object whose own two numbers don't add up to its own other
six numbers, and nothing about "valid JSON" catches that.

## What's actually new here

Every other technique needed either a specific instruction (CoT's
"show your addition") or another LLM call (the judge, and even that
took real work to get right) to have a chance of catching a bad total.
Here, catching it took three lines of Python and zero network calls.
That's the real value of structured output for this kind of task: not
that it reasons better, but that whatever it *does* get wrong becomes
mechanically, deterministically checkable.

## Takeaway

Structured output is a verification multiplier, not an accuracy
multiplier. Pair it with something that actually fixes the arithmetic
(Chain-of-Thought, or prompt chaining's isolated math step) and you get
both: a number worth trusting, and a cheap way to prove it.

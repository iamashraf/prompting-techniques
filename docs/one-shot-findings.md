# One-Shot: what running it actually showed

One-shot adds exactly one worked example. We tested whether the
example's own content leaks into the real task, whether showing
correct math once teaches correct math, and how reproducible it is —
then scored it against Zero-Shot.

## The example leaks

The baseline example was a cyberattack. The real data has no
cyberattack anywhere — yet the final mitigation list recommended
"cybersecurity audits to prevent cyberattacks." Three separate runs,
three leaks. One run even wrote, in its own text, that it was adding a
recommendation "not explicitly mentioned in the input data" —
contradicting its own system prompt, and doing it anyway.

Swapping in a totally different example (a regulatory fine, nothing to
do with security) didn't stop leakage — it changed shape. The
example's root-cause phrasing ("an administrative/legal risk, not
physical or logistical") got reused almost verbatim for an unrelated
real event. The example's *reasoning framework* transfers, whatever
that framework happens to be.

## Correct math once isn't enough

We built an example that correctly summed two numbers in its own
executive summary. On the real 6-event task, the model still got the
real sum wrong (-9%). One demonstration of correct arithmetic doesn't
teach arithmetic — it gets closer, not right.

## Temperature=0 wasn't actually deterministic here

Two back-to-back, identical-prompt calls at temp=0 produced *different*
outputs — unlike Zero-Shot, where they matched exactly. The likely
difference: One-Shot's prompt is roughly twice as long with the example
included. Determinism at temp=0 looks less reliable as prompts get
longer.

## The judge missed the leak

We scored this against Zero-Shot on the course's 5-point rubric.
One-Shot scored *higher* — 5/5 on completeness and structure — despite
being the leaky, fabricated-recommendation report. The score rewarded
how polished it looked, not whether it was grounded.

## Takeaway

One example buys style. It doesn't buy accuracy, and it doesn't buy
safety from contamination.

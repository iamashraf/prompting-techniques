# One-Shot: what running it actually showed

One-shot is zero-shot plus exactly one worked example. We ran the
baseline once, then three experiments: swap in a differently-themed
example, swap in an example that demonstrates *correct* aggregation
math, and repeat the same reproducibility check we ran for zero-shot.
Logs are in `runs/one_shot/`.

## Does the example's content leak into the real task?

Yes, and in two different ways depending on the example.

The baseline used a cyberattack example. The real dataset has no
cyberattack in it anywhere — yet the final mitigation list included
"Implement robust cybersecurity measures to prevent cyberattacks." That's
content, lifted wholesale from the example, applied to data that never
asked for it.

We then swapped in a completely different example (a regulatory
compliance fine, nothing to do with security). This time no fake event
got invented — but the example's own Root Causes section said the fine
was "an administrative/legal risk rather than a physical or logistical
one." In the real run, Customs Delay got sorted into a category called
**"Administrative/Legal Risks,"** right next to **"Physical/Logistical
Risks"** — the exact same two-way split, almost the exact wording, from
an example about a completely unrelated event. So it's not really "the
cyberattack leaks" or "the regulatory fine leaks" — it's that the
example's *reasoning framework* transfers, whatever that framework
happens to be. Pick an example, and you've also picked how the model is
going to organize its thinking about something else entirely.

## Does seeing correct math once teach correct math?

We built an example with two fictional events whose financial impacts
($500,000 and $300,000) are correctly summed in the example's own
Executive Summary ($800,000). If one demonstration of *correct*
arithmetic were enough to transfer, the real task — summing six real
numbers — should come out right too.

It didn't. The real run claimed a combined financial impact of
**$4,320,000**; the real total is **$4,725,000** — off by $405,000.
Interesting wrinkle: the one time in all of these experiments the model
stated a number that was *actually correct*, it wasn't a sum at all —
in a separate run it said "maximum revenue at risk of $4,000,000,"
which is exactly right, because Natural Disaster really is the largest
single figure. Picking the biggest number out of a list seems to be
something the model can reliably do; adding several of them together
is not — even right after being shown how.

## Is temperature=0 actually reproducible here?

We assumed yes, based on Zero-Shot (two back-to-back `temperature=0`
calls there were identical). Repeating the same test for One-Shot broke
that assumption: two back-to-back `temperature=0` calls, same process,
same prompt — **the outputs differed** (41 diff lines). One didn't
state a total at all; the very next call stated $5,350,000 (actual:
$4,725,000, off by $625,000).

The one concrete difference between the two setups is prompt length —
One-Shot's prompt is roughly twice as long once the worked example is
included. So the honest version of last time's takeaway is narrower
than we wrote it: `temperature=0` reduces randomness, but it is not a
hard guarantee of identical output, and that seems to get less reliable
as the prompt gets longer, not just across separate process runs.

## The numbers, side by side

Actual combined financial impact across all 6 real events: **$4,725,000**.

| Run | Stated a total? | Value | Off by |
|---|---|---|---|
| Baseline (cyberattack example) | No | — | — |
| Different example (regulatory fine) | Yes | $3,330,000 | -$1,395,000 (-30%) |
| Aggregated example (correct-math demo) | Yes | $4,320,000 | -$405,000 (-9%) |
| Reproducibility, temp=0, run A | No | — | — |
| Reproducibility, temp=0, run B | Yes | $5,350,000 | +$625,000 (+13%) |
| Reproducibility, temp=0.9, run C | No | — | — |
| Reproducibility, temp=0.9, run D | No | — | — |

Every time it attempted the sum, it was wrong — by anywhere from 9% to
30%, in both directions. It also attempted the sum less often than
Zero-Shot did, probably because the worked example only showed a report
*without* needing to combine six things, not because it learned to be
more careful.

## What about the scored comparison?

We built a shared judge (same rubric the course used: Completeness,
Business Reasoning, Structure, Actionability, Executive Readiness,
1-5 each) and ran it on fresh Zero-Shot and One-Shot baseline reports.
One-Shot scored higher overall — 5/5 on Completeness and Structure,
versus 4/4 for Zero-Shot — and the judge recommended it as the stronger
report.

That One-Shot report is also the one where the model wrote, in its own
mitigation list, a recommendation to defend against cyberattacks "which
were not explicitly mentioned in the input data" — a direct admission
that it was adding something the system prompt explicitly told it not
to add. The judge never caught that. It scored the leak-contaminated
report as more complete and better structured, not less trustworthy.

That's the real lesson about scoring: a number from an LLM judge tells
you how polished and well-organized something *looks*, not whether it's
actually grounded in what it was given. Worth remembering before
treating any single score as the whole verdict.

## Takeaway

One example buys you a style template, not accuracy, and not safety
from contamination. It transferred the example's categorization scheme
into an unrelated analysis, and it didn't transfer the example's
correct arithmetic into the real task's arithmetic. If anything, the
clearest win here was accidental: a shorter, vaguer Executive Summary
sometimes avoided the wrong-number problem simply by not attempting a
number at all.

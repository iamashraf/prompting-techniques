# Few-Shot: what running it actually showed

Few-shot adds several worked examples instead of one. Our first
version of this module quietly reused mismatched examples from
one-shot's leakage experiments — not a fair test of the technique. We
rebuilt it with two clean, internally consistent examples and reran.
The difference was the real story.

## Bad examples vs. good examples

The flawed version demonstrated summing *financial impact* across
events, but never *revenue at risk*. Here's the same real 6-event task,
before and after fixing that:

| | Actual | Bad examples | Good examples |
|---|---|---|---|
| Revenue at risk | $9,950,000 | $4,350,000 (-56%) | $9,350,000 (-6%) |
| Financial impact | $4,725,000 | $3,220,000 (-32%) | $4,220,000 (-11%) |

Fixing the examples cut the error on the undemonstrated number by
almost 10x. **Few-shot's accuracy lives or dies on whether your
examples actually show the operation you want — not just look like a
good report.**

It's still not exact, even now. A correctly-summed example narrows the
gap; it doesn't make the model compute. That residual gap is the model,
not the data.

## Leakage got smarter, not gone

With the bad examples, one example's root-cause sentence ("...an
administrative/legal risk...") got stamped onto events it plainly
didn't fit. With good examples, that's gone — but a subtler version
remains: the mitigation for "Customs Delay" borrowed the phrase "system
outages" straight from an example about a *Customs System Outage*, a
cause the real data never actually stated. The model reaches for
whichever example is closest to each real event and pulls in its
specifics, fitting or not.

## Takeaway

Example quality was a bigger lever on accuracy here than the technique
itself. Going from Zero-Shot to Few-Shot barely mattered next to going
from bad examples to good ones.

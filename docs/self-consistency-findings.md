# Self-Consistency: what running it actually showed

Self-consistency is Chain-of-Thought run several times independently
at a non-zero temperature, with a majority vote over the final
answer instead of trusting any one sample. We ran 5 samples at
temperature=0.8, then again at 1.2, and voted on the computed total
each time.

## At 0.8: nothing to vote on

All 5 samples landed on the exact same correct total, $4,725,000 — a
unanimous 5/5. There was no disagreement for the vote to resolve.
That's informative on its own: CoT's explicit, shown addition held up
fine under real sampling randomness, in sharp contrast to Zero-Shot,
which we'd already shown falls apart badly at this same temperature
(errors up to 50% off). Forcing the model to write out
`$850,000 + $1,200,000 + ... = $4,725,000` seems to make the
computation itself more stable, not just more often right — probably
because each number is tightly anchored to the ones right next to it,
rather than retrieved from a vaguer holistic read of the whole report.

## At 1.2: a real but different failure mode

Pushed further, cracks appeared — but not the kind we expected. Of 5
samples: 3 computed the correct total, and 2 stated no total at all.
**None gave a wrong number.** Chain-of-Thought's failure mode under
extreme sampling isn't "confidently incorrect" (Zero-Shot's failure),
it's "silently incomplete." That's a meaningfully safer way to fail.

The majority vote still worked exactly as intended here: with only
3/5 samples actually answering, a single unlucky sample has a real
40% chance of coming back with no total at all. Voting across several
samples recovers the right answer reliably, by letting the samples
that *did* compute something outweigh the ones that didn't.

## Takeaway

Self-consistency's safety net only shows its value once something is
actually unstable enough to need correcting. At moderate temperature,
CoT didn't need it. Pushed further, it did — and what it protected
against wasn't wrong answers, but missing ones.

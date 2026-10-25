# Chain-of-Thought: what running it actually showed

CoT asks the model to reason step by step before writing the report —
list the figures, show any addition explicitly, then write. We built
it specifically to test whether that fixes the one failure mode every
prior technique shared: getting a combined dollar total wrong.

## It worked

Both totals came out exactly right: $4,725,000 financial impact,
$9,950,000 revenue at risk — matching the real data precisely, for the
first time across four techniques and roughly a dozen attempts. The
difference wasn't luck; the model wrote out the full addition
("$850,000 + $1,200,000 + ... = $4,725,000") instead of jumping
straight to a number. Showing the work, not just asking for the
answer, is what actually closed the gap.

Root causes also stopped being formulaic. Zero-Shot, One-Shot, and
Few-Shot all leaned on one reused phrase or category across multiple
events at some point; here every event gets its own distinct,
individually-reasoned cause.

## The judge agreed, for once

We scored all four techniques together on the same rubric.
Chain-of-Thought swept 5/5 on every criterion — and unlike the One-Shot
case, where the judge missed a fabricated recommendation entirely, this
time its written justification explicitly called out the correct,
shown arithmetic as the reason. The judge isn't always blind to
quality; it just isn't reliable about *which* quality it notices.

## Takeaway

This is the first technique where "ask it to show its work" measurably
fixed something concrete, not just changed the style. The cost is a
longer prompt and a longer response — worth it here, since the thing
it fixed was the exact failure mode that undermined every report so
far.

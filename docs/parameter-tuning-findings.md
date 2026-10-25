# Parameter Tuning: what running it actually showed

Same Chain-of-Thought prompt throughout — only one inference
parameter changes per sweep. The course notebook used the same
one-variable-at-a-time method.

## Temperature: 1.2 isn't just "more arithmetic errors," it's fact fabrication

At 0.0 and 0.7, both totals came out exactly right. At 1.2, something
worse happened than a wrong sum. The model computed a nonsensical
figure — Natural Disaster's own Financial Impact *plus* its own
Revenue at Risk, two different metrics for the same event, combined
into "$6,100,000" — then **presented that as the event's actual
financial impact in the final report**, with full confidence
("Catastrophic... total financial losses of $6,100,000"). It also
swapped metrics for two other events, reporting their Revenue at Risk
figures as "financial hits." No overall total for the dataset appears
anywhere. This is categorically worse than the arithmetic slips we've
tracked all session — it's inventing a wrong fact and stating it as
settled, not just getting an aggregation wrong.

## Max tokens: CoT's "show your work" has a real token cost

At 100 tokens, the response cuts off mid-list, before any reasoning
happens — unusable. At 400, it cuts off mid-root-cause-analysis,
**before the actual report ever starts**. Even at 1200 — plenty for
every other technique in this repo — it cuts off one sentence before
the end. Chain-of-Thought's accuracy advantage isn't free: it needs
meaningfully more token budget than a direct-answer technique, and if
that budget is capped too low, you don't get a shorter correct answer,
you get no answer at all.

## Top-p: no visible effect here

All three values (0.1, 0.5, 1.0) at temperature=0.8 produced the
correct total, with word counts within 20% of each other. Holding
temperature fixed, top-p didn't change correctness or length much for
this task.

## Takeaway

Temperature is the parameter that actually matters here, and it
doesn't fail gracefully — past some point it stops being "a bit less
careful" and starts fabricating facts with total confidence. Max
tokens is a hard requirement CoT-style prompting has to budget for,
not a cosmetic length knob.

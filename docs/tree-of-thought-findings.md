# Tree-of-Thought: what running it actually showed

ToT (simplified, as the course notebook also framed it) asks the model
to generate multiple mitigation options per disruption, weigh their
trade-offs, then pick and justify one — breadth before commitment,
instead of Chain-of-Thought's single linear chain. We deliberately left
out CoT's "show the addition explicitly" instruction, to see whether
good arithmetic was a side effect of better reasoning in general, or
specifically tied to asking for it.

## The exploration genuinely worked

For every one of the six events, it produced two distinct, plausible
mitigation options, rated each on business impact, feasibility, effort,
and cost, and picked one with a real reason ("Diversify the supplier
base (Option 1)" over a heavier, costlier alternative). Root causes
were also individually reasoned per event, no reused template phrase —
same improvement Chain-of-Thought showed.

## The arithmetic question has a clean answer: neither right nor wrong

The Executive Summary never states a combined dollar figure anywhere in
the report — we checked. Unlike Zero-Shot, One-Shot, and Few-Shot
(which all guessed, and were always wrong), ToT simply didn't attempt
the sum at all. **Good reasoning about mitigation options didn't
transfer to good reasoning about arithmetic** — those are separate
skills the prompt has to ask for separately. "Reasoning more" isn't
one dial; "show this specific computation" is what actually worked for
Chain-of-Thought, and nothing here replaced that.

## The document structure drifted

We asked for one "Option Exploration" section, then a separate final
"Report" section. Instead the model nested the exploration inside the
mitigation section of a single combined report, then tacked on a short,
redundant second "Report" section repeating just the mitigation list.
The content was good; the more parts a task has, the less reliably the
model follows the exact structure you specify.

## Takeaway

ToT buys better justified decisions for the exact thing you ask it to
explore. It doesn't generalize that discipline to other parts of the
same task for free.

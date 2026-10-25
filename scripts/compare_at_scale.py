"""Re-runs the full technique escalation against the real, larger course
dataset (25 of its 100 events, matching the notebook's own SAMPLE_SIZE)
instead of the small 6-event synthetic one every other run in this repo
uses -- to check whether a small dataset is itself why the gap between
techniques has looked narrow so far.

Needs data/supply_chain_disruptions_100_events.csv locally (gitignored,
bring-your-own -- see README).

KNOWN ISSUE with llama3.1:8b specifically: at 25 events, every single
technique silently reasoned about only the last ~9 events (16/17-25)
and dropped the rest with no acknowledgment -- confirmed by checking
which EVT-### ids actually appear in each generated report. That's the
model losing track of a long prompt, not a bug in this script, but it
means any technique comparison this script produces at this scale is
not meaningful until that's addressed (a model with better long-context
handling, or chunking the input). Don't trust its scores as-is.
"""

from prompting_techniques.judge import compare_consecutive_pairs
from prompting_techniques.scenario import REAL_DATA_FILE, load_events
from prompting_techniques.techniques import chain_of_thought, few_shot, one_shot, tree_of_thought, zero_shot

SAMPLE_SIZE = 25


def main() -> None:
    events = load_events(REAL_DATA_FILE, limit=SAMPLE_SIZE)

    order = ["Zero-Shot", "One-Shot", "Few-Shot", "Chain-of-Thought", "Tree-of-Thought"]
    reports = {
        "Zero-Shot": zero_shot.run(events=events),
        "One-Shot": one_shot.run(events=events),
        "Few-Shot": few_shot.run(events=events),
        "Chain-of-Thought": chain_of_thought.run(events=events),
        "Tree-of-Thought": tree_of_thought.run(events=events),
    }

    for step, result in compare_consecutive_pairs(reports, order).items():
        print(f"\n=== {step} ===")
        print(result)


if __name__ == "__main__":
    main()

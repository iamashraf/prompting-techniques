"""Self-Consistency Prompting.

The standard recipe (Wang et al.): run Chain-of-Thought's reasoning
several times independently at a non-zero temperature, so the paths
genuinely differ, then take the most common final answer across
samples instead of trusting any single one. Built as a wrapper around
chain_of_thought.py's own prompt, not a separate prompt template --
self-consistency is about *how many times you sample and vote*, not
about what you ask the model to do in any one call.
"""

import re
from collections import Counter

from prompting_techniques.ollama_client import ask_ollama
from prompting_techniques.run_log import save_run
from prompting_techniques.scenario import build_business_context, load_events
from prompting_techniques.techniques.chain_of_thought import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

NUM_SAMPLES = 5
SAMPLING_TEMPERATURE = 0.8

_TOTAL_PATTERN = re.compile(r"Total Financial Impact.*?=\s*\$([\d,]+)", re.IGNORECASE)


def extract_total(report: str) -> str | None:
    match = _TOTAL_PATTERN.search(report)
    return match.group(1) if match else None


def run(num_samples: int = NUM_SAMPLES, temperature: float = SAMPLING_TEMPERATURE) -> str:
    business_context = build_business_context(load_events())
    user_prompt = USER_PROMPT_TEMPLATE.format(business_context=business_context)

    samples = []
    for i in range(num_samples):
        response = ask_ollama(SYSTEM_PROMPT, user_prompt, temperature=temperature)
        save_run("self_consistency", SYSTEM_PROMPT, user_prompt, response, label=f"sample_{i + 1}")
        samples.append(response)

    totals = [extract_total(sample) for sample in samples]
    votes = Counter(t for t in totals if t is not None)

    print(f"--- {num_samples} samples at temperature={temperature} ---")
    for i, (sample_total) in enumerate(totals, start=1):
        print(f"  sample {i}: {'$' + sample_total if sample_total else 'no total stated'}")

    if not votes:
        print("--- no sample stated a total -- nothing to vote on ---")
        return samples[0]

    winner, count = votes.most_common(1)[0]
    print(f"--- majority answer: ${winner} ({count}/{num_samples} samples agreed) ---")

    return samples[totals.index(winner)]


def main() -> None:
    print(run())


if __name__ == "__main__":
    main()

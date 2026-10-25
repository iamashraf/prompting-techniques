"""Tree-of-Thought (ToT) Prompting -- simplified.

Not full branching/backtracking search. As in the course notebook: for
each disruption, generate multiple plausible mitigation options,
evaluate their trade-offs, then select and justify the strongest one --
breadth before commitment, instead of Chain-of-Thought's single linear
reasoning path.

Deliberately does NOT carry over chain_of_thought.py's "show the
addition explicitly" instruction -- ToT's distinguishing feature here
is option exploration, not arithmetic. Whether the totals stay correct
anyway, or regress without that specific instruction, is itself the
question this module is built to answer.
"""

from prompting_techniques.ollama_client import ask_ollama
from prompting_techniques.run_log import save_run
from prompting_techniques.scenario import build_business_context, load_events
from prompting_techniques.techniques.zero_shot import SYSTEM_PROMPT

USER_PROMPT_TEMPLATE = """
Analyze the following supply chain disruption dataset and prepare a
Business Impact Assessment Report.

## Input Data

{business_context}

## Task

For each disruption event, before recommending a single mitigation
strategy:

1. Generate at least two distinct, plausible mitigation options.
2. Evaluate each option on business impact, feasibility,
   implementation effort, and cost.
3. Select the strongest option and explain why it beats the
   alternative(s).

Show this exploration under an "## Option Exploration" heading (one
subsection per event), then write the final report under a "## Report"
heading, using only the selected option per event in the mitigation
section.

## Report Structure

1. Executive Summary
2. Identified Disruptions
3. Root Causes
4. Recommended Mitigation Strategies
""".strip()


def run(temperature: float = 0.0, events: list[dict[str, str]] | None = None) -> str:
    business_context = build_business_context(events if events is not None else load_events())
    user_prompt = USER_PROMPT_TEMPLATE.format(business_context=business_context)
    response = ask_ollama(SYSTEM_PROMPT, user_prompt, temperature=temperature)

    log_path = save_run("tree_of_thought", SYSTEM_PROMPT, user_prompt, response)
    print(f"--- logged full run to {log_path} ---")

    return response


def main() -> None:
    print(run())


if __name__ == "__main__":
    main()

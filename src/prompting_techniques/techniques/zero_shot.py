"""Zero-Shot Prompting.

The model gets an instruction and the task data, and nothing else -- no
worked examples, no demonstration of what a good answer looks like. It
has to rely entirely on what it already learned during training to infer
the right structure and reasoning. Every other technique in this repo is
compared back against this baseline.
"""

from prompting_techniques.ollama_client import ask_ollama
from prompting_techniques.run_log import save_run
from prompting_techniques.scenario import build_business_context, load_events

SYSTEM_PROMPT = """
You are a Senior Supply Chain Risk Analyst.

Base all observations, conclusions, and recommendations solely on the
information provided in the input. Do not assume, infer, or fabricate
facts that are not explicitly supported by the data. Maintain a
professional, executive-ready tone.
""".strip()

USER_PROMPT_TEMPLATE = """
Analyze the following supply chain disruption dataset and prepare a
Business Impact Assessment Report.

## Input Data

{business_context}

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

    log_path = save_run("zero_shot", SYSTEM_PROMPT, user_prompt, response)
    print(f"--- logged full run to {log_path} ---")

    return response


def main() -> None:
    print(run())


if __name__ == "__main__":
    main()

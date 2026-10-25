"""Chain-of-Thought (CoT) Prompting.

Instead of writing the final report directly, the model is instructed
to reason step by step first -- explicitly listing figures and showing
any addition before stating a total -- and only then write the report.

Same system prompt as zero_shot.py (unchanged), so the only variable
that changes is this explicit reasoning instruction. This directly
targets the one failure mode that showed up in every prior technique:
Zero-Shot, One-Shot, and Few-Shot all got a combined dollar total wrong
because the model pattern-completes a plausible number instead of
actually adding (see docs/zero-shot-findings.md and friends). CoT's
premise is that forcing the addition to be shown fixes that.
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

Before writing the final report, think through the analysis step by
step under a "## Reasoning" heading:

1. List each event's financial impact and revenue at risk.
2. If the report will state any combined or total figures, show the
   addition explicitly (e.g. "$850,000 + $1,200,000 = $2,050,000")
   before stating the result.
3. Identify the root cause for each event individually -- do not reuse
   one phrase across multiple events unless it genuinely applies to
   each one.

Only after that reasoning, write the final report under a "## Report"
heading.

## Report Structure

1. Executive Summary
2. Identified Disruptions
3. Root Causes
4. Recommended Mitigation Strategies
""".strip()


def run(temperature: float = 0.0) -> str:
    business_context = build_business_context(load_events())
    user_prompt = USER_PROMPT_TEMPLATE.format(business_context=business_context)
    response = ask_ollama(SYSTEM_PROMPT, user_prompt, temperature=temperature)

    log_path = save_run("chain_of_thought", SYSTEM_PROMPT, user_prompt, response)
    print(f"--- logged full run to {log_path} ---")

    return response


def main() -> None:
    print(run())


if __name__ == "__main__":
    main()

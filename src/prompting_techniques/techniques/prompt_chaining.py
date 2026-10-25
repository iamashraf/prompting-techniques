"""Prompt Chaining.

Breaks the task into a pipeline of smaller, separate calls, each
feeding its output into the next, instead of one call doing everything
at once. Structurally different from every other technique in this
repo, which all ask for the whole report in a single prompt.

Step 2 isolates the arithmetic into its own dedicated, narrow call --
a direct test against Chain-of-Thought's approach of showing the
addition inline within one larger report-writing call. Every step is
logged individually (not just the final report) so a wrong number can
be traced to exactly which step introduced it.
"""

from prompting_techniques.ollama_client import ask_ollama
from prompting_techniques.run_log import save_run
from prompting_techniques.scenario import build_business_context, load_events
from prompting_techniques.techniques.zero_shot import SYSTEM_PROMPT

STEP1_ROOT_CAUSES = """
For each of the following supply chain disruption events, state its
root cause in one sentence, individually reasoned -- do not reuse one
phrase across multiple events unless it genuinely applies to each. Do
not add commentary or a report structure, just the per-event causes.

{business_context}
""".strip()

STEP2_TOTALS = """
Given the following supply chain disruption events, compute:
1. The total financial impact (sum of every event's Financial Impact USD).
2. The total revenue at risk (sum of every event's Revenue At Risk USD).

Show the addition explicitly for each total before stating the result.

{business_context}
""".strip()

STEP3_MITIGATIONS = """
Given the following root causes for a set of supply chain disruptions,
recommend one specific mitigation strategy per root cause.

{root_causes}
""".strip()

STEP4_FINAL_REPORT = """
Using the analysis below, write a Business Impact Assessment Report
with this structure:

1. Executive Summary
2. Identified Disruptions
3. Root Causes
4. Recommended Mitigation Strategies

## Root Causes
{root_causes}

## Financial Totals
{totals}

## Mitigation Strategies
{mitigations}

## Original Event Data
{business_context}
""".strip()


def run(temperature: float = 0.0) -> str:
    business_context = build_business_context(load_events())

    root_causes = ask_ollama(
        SYSTEM_PROMPT, STEP1_ROOT_CAUSES.format(business_context=business_context), temperature=temperature
    )
    save_run("prompt_chaining", SYSTEM_PROMPT, STEP1_ROOT_CAUSES, root_causes, label="step1_root_causes")

    totals = ask_ollama(
        SYSTEM_PROMPT, STEP2_TOTALS.format(business_context=business_context), temperature=temperature
    )
    save_run("prompt_chaining", SYSTEM_PROMPT, STEP2_TOTALS, totals, label="step2_totals")

    mitigations = ask_ollama(
        SYSTEM_PROMPT, STEP3_MITIGATIONS.format(root_causes=root_causes), temperature=temperature
    )
    save_run("prompt_chaining", SYSTEM_PROMPT, STEP3_MITIGATIONS, mitigations, label="step3_mitigations")

    final_prompt = STEP4_FINAL_REPORT.format(
        root_causes=root_causes,
        totals=totals,
        mitigations=mitigations,
        business_context=business_context,
    )
    response = ask_ollama(SYSTEM_PROMPT, final_prompt, temperature=temperature)
    log_path = save_run("prompt_chaining", SYSTEM_PROMPT, final_prompt, response, label="step4_final_report")
    print(f"--- logged full run to {log_path} ---")

    return response


def main() -> None:
    print(run())


if __name__ == "__main__":
    main()

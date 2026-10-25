"""One-Shot Prompting.

Same as Zero-Shot, with exactly one worked example added before the real
task: one input event paired with one hand-written good report. Nothing
else changes -- same system prompt (imported from zero_shot, not
redefined), same report structure, same real data -- so any difference
in output is attributable to that one example.
"""

from prompting_techniques.ollama_client import ask_ollama
from prompting_techniques.run_log import save_run
from prompting_techniques.scenario import build_business_context, load_events
from prompting_techniques.techniques.zero_shot import SYSTEM_PROMPT

# A hand-written example, deliberately distinct from the real 6 events in
# data/supply_chain_events.csv -- this is a demonstration of *style*, not
# a hint about the actual task's answer.
REFERENCE_EXAMPLE = """
## Reference Example

Here is one worked example of a well-structured Business Impact
Assessment Report, given a single disruption event as input.

### Example Input

========== Supply Chain Disruption Event 1 ==========
Event Type: Cyberattack
Region: Europe
Country: United Kingdom
Supplier Tier: Tier-1
Severity Level: Critical
Production Downtime Hours: 60
Shipment Delay Days: 8
Revenue At Risk USD: 3000000
Financial Impact USD: 1500000

### Example Report

**Executive Summary**
A single Tier-1 cyberattack in the United Kingdom caused 60 hours of
production downtime and an 8-day shipment delay, with a financial
impact of $1,500,000 against $3,000,000 of revenue at risk.

**Identified Disruptions**
1. **Cyberattack (Event 1)**: United Kingdom, Europe, Tier-1 Supplier,
Critical Severity, 60 hours production downtime, 8 days shipment delay,
$3,000,000 revenue at risk, $1,500,000 financial impact.

**Root Causes**
The disruption stems from a cyberattack targeting a Tier-1 supplier's
systems -- a security-related risk rather than a physical or logistical
one.

**Recommended Mitigation Strategies**
1. **Cybersecurity Audits**: Require critical suppliers to undergo
regular security audits.
2. **Incident Response Planning**: Establish a joint incident response
plan with Tier-1 suppliers.
3. **Data Backup and Redundancy**: Ensure suppliers maintain backups to
shorten recovery time after future incidents.
""".strip()

USER_PROMPT_TEMPLATE = """
{reference_example}

## Task

Using the same report style and structure shown above, analyze the
following supply chain disruption dataset and prepare a Business Impact
Assessment Report.

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
    user_prompt = USER_PROMPT_TEMPLATE.format(
        reference_example=REFERENCE_EXAMPLE,
        business_context=business_context,
    )
    response = ask_ollama(SYSTEM_PROMPT, user_prompt, temperature=temperature)

    log_path = save_run("one_shot", SYSTEM_PROMPT, user_prompt, response)
    print(f"--- logged full run to {log_path} ---")

    return response


def main() -> None:
    print(run())


if __name__ == "__main__":
    main()

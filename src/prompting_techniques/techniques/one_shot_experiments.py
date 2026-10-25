"""Hands-on experiments probing what adding one example actually changes.

Unlike zero_shot_experiments.py (which probes general LLM behavior --
determinism, missing data), these are specific to One-Shot: does the
example's own content leak into an unrelated real task, and does
demonstrating aggregation math in the example cause the model to
attempt (and maybe still botch) aggregation on the real one?
"""

import difflib

from prompting_techniques.ollama_client import ask_ollama
from prompting_techniques.run_log import save_run
from prompting_techniques.scenario import build_business_context, load_events
from prompting_techniques.techniques.one_shot import (
    REFERENCE_EXAMPLE,
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
)

# A differently-themed single-event example (legal/administrative, not
# security) -- distinct from both the real dataset and the cyberattack
# example in one_shot.py. If something regulatory-flavored leaks into
# the real task's output, that confirms leakage isn't specific to the
# cyberattack example -- it's a property of using an example at all.
DIFFERENT_THEMED_EXAMPLE = """
## Reference Example

Here is one worked example of a well-structured Business Impact
Assessment Report, given a single disruption event as input.

### Example Input

========== Supply Chain Disruption Event 1 ==========
Event Type: Regulatory Compliance Fine
Region: North America
Country: Canada
Supplier Tier: Tier-2
Severity Level: Medium
Production Downtime Hours: 0
Shipment Delay Days: 0
Revenue At Risk USD: 500000
Financial Impact USD: 120000

### Example Report

**Executive Summary**
A Tier-2 supplier in Canada incurred a regulatory compliance fine of
$120,000 against $500,000 of revenue at risk, with no production
downtime or shipment delay.

**Identified Disruptions**
1. **Regulatory Compliance Fine (Event 1)**: Canada, North America,
Tier-2 Supplier, Medium Severity, 0 hours production downtime, 0 days
shipment delay, $500,000 revenue at risk, $120,000 financial impact.

**Root Causes**
The disruption stems from a regulatory compliance failure at the
supplier's facility -- an administrative/legal risk rather than a
physical or logistical one.

**Recommended Mitigation Strategies**
1. **Compliance Audits**: Require suppliers to undergo regular
regulatory compliance audits.
2. **Legal Risk Monitoring**: Track regional regulatory changes that
may affect supplier operations.
3. **Contractual Safeguards**: Include compliance clauses and
penalty-sharing terms in supplier contracts.
""".strip()

# Two fictional events whose financial impacts are correctly summed in
# the example's Executive Summary ($500,000 + $300,000 = $800,000). If
# the real task's output now attempts the same kind of sum, we'll see
# whether having seen *correct* arithmetic once is enough to make the
# model actually compute correctly, or just to make it try.
AGGREGATED_EXAMPLE = """
## Reference Example

Here is one worked example of a well-structured Business Impact
Assessment Report, given two disruption events as input.

### Example Input

========== Supply Chain Disruption Event 1 ==========
Event Type: Warehouse Fire
Region: South America
Country: Brazil
Supplier Tier: Tier-2
Severity Level: High
Production Downtime Hours: 40
Shipment Delay Days: 7
Revenue At Risk USD: 1200000
Financial Impact USD: 500000

========== Supply Chain Disruption Event 2 ==========
Event Type: Equipment Breakdown
Region: South America
Country: Argentina
Supplier Tier: Tier-3
Severity Level: Medium
Production Downtime Hours: 18
Shipment Delay Days: 2
Revenue At Risk USD: 400000
Financial Impact USD: 300000

### Example Report

**Executive Summary**
Two disruptions in South America produced a combined financial impact
of $800,000 ($500,000 from the warehouse fire and $300,000 from the
equipment breakdown).

**Identified Disruptions**
1. **Warehouse Fire (Event 1)**: Brazil, South America, Tier-2
Supplier, High Severity, 40 hours production downtime, 7 days shipment
delay, $1,200,000 revenue at risk, $500,000 financial impact.
2. **Equipment Breakdown (Event 2)**: Argentina, South America, Tier-3
Supplier, Medium Severity, 18 hours production downtime, 2 days
shipment delay, $400,000 revenue at risk, $300,000 financial impact.

**Root Causes**
Both disruptions stem from physical asset failures at supplier
facilities rather than external or logistical causes.

**Recommended Mitigation Strategies**
1. **Preventive Maintenance**: Schedule regular equipment inspections
to reduce breakdown risk.
2. **Fire Safety Compliance**: Require suppliers to maintain
up-to-date fire suppression systems.
""".strip()


def _run_with_example(example: str, temperature: float = 0.0) -> tuple[str, str]:
    business_context = build_business_context(load_events())
    user_prompt = USER_PROMPT_TEMPLATE.format(reference_example=example, business_context=business_context)
    return ask_ollama(SYSTEM_PROMPT, user_prompt, temperature=temperature), user_prompt


def experiment_different_example() -> None:
    print("\n=== Different-themed example: Regulatory Compliance Fine ===")
    response, user_prompt = _run_with_example(DIFFERENT_THEMED_EXAMPLE)
    print(response)
    save_run("one_shot", SYSTEM_PROMPT, user_prompt, response, label="different_example")


def experiment_aggregated_example() -> None:
    print("\n=== Example that demonstrates correct aggregation math ===")
    response, user_prompt = _run_with_example(AGGREGATED_EXAMPLE)
    print(response)
    save_run("one_shot", SYSTEM_PROMPT, user_prompt, response, label="aggregated_example")


def experiment_reproducibility() -> None:
    """Same prompt (the real one_shot.py example), twice, at temp=0 vs 0.9."""
    business_context = build_business_context(load_events())
    user_prompt = USER_PROMPT_TEMPLATE.format(
        reference_example=REFERENCE_EXAMPLE, business_context=business_context
    )

    print("\n=== Reproducibility: temperature=0.0, run A vs run B ===")
    run_a = ask_ollama(SYSTEM_PROMPT, user_prompt, temperature=0.0)
    run_b = ask_ollama(SYSTEM_PROMPT, user_prompt, temperature=0.0)
    save_run("one_shot", SYSTEM_PROMPT, user_prompt, run_a, label="repro_temp0_runA")
    save_run("one_shot", SYSTEM_PROMPT, user_prompt, run_b, label="repro_temp0_runB")
    _print_diff(run_a, run_b, label="temp=0.0")

    print("\n=== Reproducibility: temperature=0.9, run A vs run B ===")
    run_c = ask_ollama(SYSTEM_PROMPT, user_prompt, temperature=0.9)
    run_d = ask_ollama(SYSTEM_PROMPT, user_prompt, temperature=0.9)
    save_run("one_shot", SYSTEM_PROMPT, user_prompt, run_c, label="repro_temp09_runC")
    save_run("one_shot", SYSTEM_PROMPT, user_prompt, run_d, label="repro_temp09_runD")
    _print_diff(run_c, run_d, label="temp=0.9")


def _print_diff(text_a: str, text_b: str, label: str) -> None:
    diff = list(
        difflib.unified_diff(
            text_a.splitlines(),
            text_b.splitlines(),
            fromfile=f"{label} run A",
            tofile=f"{label} run B",
            lineterm="",
        )
    )
    if diff:
        print(f"Outputs DIFFER ({len(diff)} diff lines):")
        print("\n".join(diff[:20]))
    else:
        print("Outputs are IDENTICAL.")


def main() -> None:
    experiment_different_example()
    experiment_aggregated_example()
    experiment_reproducibility()


if __name__ == "__main__":
    main()

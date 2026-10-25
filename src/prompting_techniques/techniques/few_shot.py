"""Few-Shot Prompting.

Same as One-Shot, but with several worked examples instead of one. The
point of good examples is to genuinely help the model produce a better
answer, not to probe it -- so unlike one_shot_experiments.py (which used
mismatched, incomplete examples on purpose to find failure modes), these
two examples are internally consistent and each correctly demonstrates
*both* aggregate figures (financial impact and revenue at risk) where
more than one event is shown, so we're not accidentally testing an
operation the model was never shown.
"""

from prompting_techniques.ollama_client import ask_ollama
from prompting_techniques.run_log import save_run
from prompting_techniques.scenario import build_business_context, load_events
from prompting_techniques.techniques.zero_shot import SYSTEM_PROMPT

REFERENCE_EXAMPLES = """
## Reference Examples

Here are two worked examples of well-structured Business Impact
Assessment Reports.

### Example 1 — Supplier Bankruptcy

**Input**

========== Supply Chain Disruption Event 1 ==========
Event Type: Supplier Bankruptcy
Region: North America
Country: United States
Supplier Tier: Tier-2
Severity Level: High
Production Downtime Hours: 30
Shipment Delay Days: 6
Revenue At Risk USD: 1000000
Financial Impact USD: 400000

**Report**

**Executive Summary**
A Tier-2 supplier in the United States filed for bankruptcy, causing 30
hours of production downtime and a 6-day shipment delay, with a
financial impact of $400,000 against $1,000,000 of revenue at risk.

**Identified Disruptions**
1. **Supplier Bankruptcy (Event 1)**: United States, North America,
Tier-2 Supplier, High Severity, 30 hours production downtime, 6 days
shipment delay, $1,000,000 revenue at risk, $400,000 financial impact.

**Root Causes**
The disruption stems from the supplier's financial insolvency -- an
operational risk tied to that supplier's own financial health, not
external market conditions.

**Recommended Mitigation Strategies**
1. **Financial Health Monitoring**: Track key suppliers' credit ratings
and financial stability on an ongoing basis.
2. **Dual Sourcing**: Qualify a backup supplier for critical components
to avoid single-supplier dependency.

### Example 2 — Regional Flooding & Customs System Outage

**Input**

========== Supply Chain Disruption Event 1 ==========
Event Type: Regional Flooding
Region: Asia
Country: Thailand
Supplier Tier: Tier-1
Severity Level: Critical
Production Downtime Hours: 80
Shipment Delay Days: 12
Revenue At Risk USD: 2200000
Financial Impact USD: 900000

========== Supply Chain Disruption Event 2 ==========
Event Type: Customs System Outage
Region: Europe
Country: Netherlands
Supplier Tier: Tier-3
Severity Level: Medium
Production Downtime Hours: 10
Shipment Delay Days: 4
Revenue At Risk USD: 300000
Financial Impact USD: 90000

**Report**

**Executive Summary**
Two disruptions -- a regional flood in Thailand and a customs system
outage in the Netherlands -- together put $2,500,000 of revenue at
risk ($2,200,000 from the flooding and $300,000 from the outage) and
produced a combined financial impact of $990,000 ($900,000 from the
flooding and $90,000 from the outage).

**Identified Disruptions**
1. **Regional Flooding (Event 1)**: Thailand, Asia, Tier-1 Supplier,
Critical Severity, 80 hours production downtime, 12 days shipment
delay, $2,200,000 revenue at risk, $900,000 financial impact.
2. **Customs System Outage (Event 2)**: Netherlands, Europe, Tier-3
Supplier, Medium Severity, 10 hours production downtime, 4 days
shipment delay, $300,000 revenue at risk, $90,000 financial impact.

**Root Causes**
The flooding is an environmental/weather-related risk beyond the
supplier's control. The customs outage is a logistics-system risk tied
to border-processing infrastructure, unrelated to the flooding.

**Recommended Mitigation Strategies**
1. **Environmental Risk Assessment**: Evaluate flood exposure for
suppliers in flood-prone regions and maintain alternate production
sites.
2. **Customs System Redundancy**: Work with freight partners that have
a manual customs-clearance fallback for system outages.
""".strip()

USER_PROMPT_TEMPLATE = """
{reference_examples}

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


def run(temperature: float = 0.0) -> str:
    business_context = build_business_context(load_events())
    user_prompt = USER_PROMPT_TEMPLATE.format(
        reference_examples=REFERENCE_EXAMPLES,
        business_context=business_context,
    )
    response = ask_ollama(SYSTEM_PROMPT, user_prompt, temperature=temperature)

    log_path = save_run("few_shot", SYSTEM_PROMPT, user_prompt, response)
    print(f"--- logged full run to {log_path} ---")

    return response


def main() -> None:
    print(run())


if __name__ == "__main__":
    main()

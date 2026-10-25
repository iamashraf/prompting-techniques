"""Structured Output.

Forces the response into a JSON schema instead of free prose, via
Ollama's `format` parameter. The payoff: we can verify the model's
stated totals in plain Python by summing the per-event figures it
*also* returned in the same response -- no regex-extraction from
prose, no second LLM call to judge it. The most rigorous check of the
arithmetic question this repo has had all along.
"""

import json

from prompting_techniques.ollama_client import ask_ollama
from prompting_techniques.run_log import save_run
from prompting_techniques.scenario import build_business_context, load_events
from prompting_techniques.techniques.zero_shot import SYSTEM_PROMPT

REPORT_SCHEMA = {
    "type": "object",
    "properties": {
        "executive_summary": {"type": "string"},
        "disruptions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "event_type": {"type": "string"},
                    "financial_impact_usd": {"type": "number"},
                    "revenue_at_risk_usd": {"type": "number"},
                    "root_cause": {"type": "string"},
                    "mitigation": {"type": "string"},
                },
                "required": [
                    "event_type",
                    "financial_impact_usd",
                    "revenue_at_risk_usd",
                    "root_cause",
                    "mitigation",
                ],
            },
        },
        "total_financial_impact_usd": {"type": "number"},
        "total_revenue_at_risk_usd": {"type": "number"},
    },
    "required": ["executive_summary", "disruptions", "total_financial_impact_usd", "total_revenue_at_risk_usd"],
}

USER_PROMPT_TEMPLATE = """
Analyze the following supply chain disruption dataset and return a
Business Impact Assessment Report as JSON: an executive summary, one
entry per disruption event (its type, financial impact, revenue at
risk, root cause, and a mitigation strategy), and the total financial
impact and total revenue at risk across all events.

## Input Data

{business_context}
""".strip()


def verify(report: dict, expected_event_count: int) -> bool:
    """Checks the model's own stated totals against its own per-event figures -- no LLM involved."""
    disruptions = report["disruptions"]
    computed_financial_impact = sum(d["financial_impact_usd"] for d in disruptions)
    computed_revenue_at_risk = sum(d["revenue_at_risk_usd"] for d in disruptions)

    event_count_ok = len(disruptions) == expected_event_count
    financial_impact_ok = report["total_financial_impact_usd"] == computed_financial_impact
    revenue_at_risk_ok = report["total_revenue_at_risk_usd"] == computed_revenue_at_risk

    print("--- programmatic verification (no LLM involved) ---")
    print(f"  event count:            {len(disruptions)} (expected {expected_event_count}) -> {event_count_ok}")
    print(
        f"  financial impact:       stated ${report['total_financial_impact_usd']:,.0f}, "
        f"computed ${computed_financial_impact:,.0f} -> {financial_impact_ok}"
    )
    print(
        f"  revenue at risk:        stated ${report['total_revenue_at_risk_usd']:,.0f}, "
        f"computed ${computed_revenue_at_risk:,.0f} -> {revenue_at_risk_ok}"
    )

    return event_count_ok and financial_impact_ok and revenue_at_risk_ok


def run(temperature: float = 0.0) -> dict:
    events = load_events()
    business_context = build_business_context(events)
    user_prompt = USER_PROMPT_TEMPLATE.format(business_context=business_context)

    response = ask_ollama(SYSTEM_PROMPT, user_prompt, temperature=temperature, format=REPORT_SCHEMA)
    log_path = save_run("structured_output", SYSTEM_PROMPT, user_prompt, response)
    print(f"--- logged full run to {log_path} ---")

    report = json.loads(response)
    verify(report, expected_event_count=len(events))

    return report


def main() -> None:
    print(json.dumps(run(), indent=2))


if __name__ == "__main__":
    main()

"""Hands-on experiments that make Zero-Shot's failure modes visible.

Each function isolates exactly one variable from the baseline in
zero_shot.py, so the only thing that changed between a baseline run and
an experiment run is the thing being studied.
"""

import difflib

from prompting_techniques.run_log import save_run
from prompting_techniques.scenario import build_business_context, load_events
from prompting_techniques.techniques.zero_shot import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
    ask_ollama,
)

# A deliberately sparse, ambiguous event: a severity rating with none of
# the figures that would normally justify it. A grounded model should say
# "insufficient data"; a model prone to hallucination will invent numbers.
SPARSE_EVENT = {
    "event_type": "Unknown Disruption",
    "region": "Unknown",
    "country": "Unknown",
    "supplier_tier": "Unknown",
    "severity_level": "Critical",
    "production_downtime_hours": "",
    "shipment_delay_days": "",
    "revenue_at_risk_usd": "",
    "financial_impact_usd": "",
}


def experiment_reproducibility() -> None:
    """Same prompt, twice, at temperature=0 vs temperature=0.9."""
    context = build_business_context(load_events())
    user_prompt = USER_PROMPT_TEMPLATE.format(business_context=context)

    print("\n=== Reproducibility: temperature=0.0, run A vs run B ===")
    run_a = ask_ollama(SYSTEM_PROMPT, user_prompt, temperature=0.0)
    run_b = ask_ollama(SYSTEM_PROMPT, user_prompt, temperature=0.0)
    save_run("zero_shot_experiment_repro_temp0_runA", SYSTEM_PROMPT, user_prompt, run_a)
    save_run("zero_shot_experiment_repro_temp0_runB", SYSTEM_PROMPT, user_prompt, run_b)
    _print_diff(run_a, run_b, label="temp=0.0")

    print("\n=== Reproducibility: temperature=0.9, run A vs run B ===")
    run_c = ask_ollama(SYSTEM_PROMPT, user_prompt, temperature=0.9)
    run_d = ask_ollama(SYSTEM_PROMPT, user_prompt, temperature=0.9)
    save_run("zero_shot_experiment_repro_temp09_runC", SYSTEM_PROMPT, user_prompt, run_c)
    save_run("zero_shot_experiment_repro_temp09_runD", SYSTEM_PROMPT, user_prompt, run_d)
    _print_diff(run_c, run_d, label="temp=0.9")


def experiment_sparse_data() -> None:
    """Does the model admit missing data, or invent numbers to fill the gap?"""
    context = build_business_context([SPARSE_EVENT])
    user_prompt = USER_PROMPT_TEMPLATE.format(business_context=context)

    print("\n=== Sparse data: one event, missing all figures ===")
    response = ask_ollama(SYSTEM_PROMPT, user_prompt, temperature=0.0)
    print(response)
    save_run("zero_shot_experiment_sparse_data", SYSTEM_PROMPT, user_prompt, response)


def experiment_no_system_prompt() -> None:
    """Same user prompt, with vs without the persona/constraints system prompt."""
    context = build_business_context(load_events())
    user_prompt = USER_PROMPT_TEMPLATE.format(business_context=context)

    print("\n=== With system prompt ===")
    with_system = ask_ollama(SYSTEM_PROMPT, user_prompt, temperature=0.0)
    print(with_system)

    print("\n=== Without system prompt ===")
    without_system = ask_ollama(None, user_prompt, temperature=0.0)
    print(without_system)

    save_run("zero_shot_experiment_with_system", SYSTEM_PROMPT, user_prompt, with_system)
    save_run("zero_shot_experiment_without_system", "(none)", user_prompt, without_system)


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
    experiment_reproducibility()
    experiment_sparse_data()
    experiment_no_system_prompt()


if __name__ == "__main__":
    main()

"""LLM-as-judge: scores reports from different techniques side by side.

Same rubric the course notebook used (Completeness, Business Reasoning,
Structure, Actionability, Executive Readiness, 1-5 each) so technique
comparisons aren't just us eyeballing prose -- there's one consistent
scoring pass any technique's baseline output can go through.
"""

from prompting_techniques.ollama_client import DEFAULT_MODEL, ask_ollama
from prompting_techniques.run_log import save_run

JUDGE_SYSTEM_PROMPT = """
You are an impartial evaluator of business reports. Score strictly
based on the content shown. Do not favor a report for being longer or
sounding more confident if the content doesn't support it.
""".strip()

JUDGE_PROMPT_TEMPLATE = """
You are evaluating {count} AI-generated Business Impact Assessment
reports, each produced using a different prompting technique on the
same underlying supply chain disruption data.

{report_blocks}

Score each report (1-5) on:
1. Groundedness: is every specific claim traceable to the input data
   shown above? Deduct sharply for any recommendation, cause, or figure
   that isn't supported by the input data, even if it sounds plausible.
2. Completeness
3. Business Reasoning
4. Structure
5. Actionability
6. Executive Readiness

Present the results as a markdown table (one row per criterion, one
column per report), followed by a one-paragraph recommendation of
which report is strongest and why.
""".strip()


def compare_reports(reports: dict[str, str], model: str = DEFAULT_MODEL, temperature: float = 0.0) -> str:
    report_blocks = "\n\n".join(
        f"---------- Report: {label} ----------\n{text}" for label, text in reports.items()
    )
    user_prompt = JUDGE_PROMPT_TEMPLATE.format(count=len(reports), report_blocks=report_blocks)

    response = ask_ollama(JUDGE_SYSTEM_PROMPT, user_prompt, model=model, temperature=temperature)
    log_path = save_run("judge", JUDGE_SYSTEM_PROMPT, user_prompt, response, label=model.replace(":", "_"))
    print(f"--- logged full run to {log_path} ---")

    return response


# Asking for a "Groundedness" score directly wasn't enough -- the judge
# rated a report "grounded" because it *sounded* specific, without
# actually checking any claim against the input data (see
# docs/one-shot-findings.md). This variant forces that check explicitly,
# claim by claim, before any score is assigned -- the judging equivalent
# of chain_of_thought.py.
JUDGE_PROMPT_TEMPLATE_WITH_VERIFICATION = """
You are evaluating {count} AI-generated Business Impact Assessment
reports, each produced using a different prompting technique on the
same underlying supply chain disruption data.

{report_blocks}

## Step 1: Verify claims

For each report, list every specific recommendation, root cause, or
figure it states. For each one, write "Supported" if it is explicitly
present in the input data shown above, or "Not supported -- not
present in the input data" if it is not. Do this for every report
before moving on.

## Step 2: Score

Only after completing that claim-by-claim check for every report,
score each report (1-5) on:
1. Groundedness: based strictly on the claim-by-claim check above --
   deduct sharply for every claim marked "Not supported."
2. Completeness
3. Business Reasoning
4. Structure
5. Actionability
6. Executive Readiness

Present the results as a markdown table (one row per criterion, one
column per report), followed by a one-paragraph recommendation of
which report is strongest and why.
""".strip()


def compare_reports_with_verification(
    reports: dict[str, str], model: str = DEFAULT_MODEL, temperature: float = 0.0
) -> str:
    report_blocks = "\n\n".join(
        f"---------- Report: {label} ----------\n{text}" for label, text in reports.items()
    )
    user_prompt = JUDGE_PROMPT_TEMPLATE_WITH_VERIFICATION.format(count=len(reports), report_blocks=report_blocks)

    response = ask_ollama(JUDGE_SYSTEM_PROMPT, user_prompt, model=model, temperature=temperature)
    log_path = save_run(
        "judge", JUDGE_SYSTEM_PROMPT, user_prompt, response, label=f"{model.replace(':', '_')}_verified"
    )
    print(f"--- logged full run to {log_path} ---")

    return response


def main() -> None:
    from prompting_techniques.techniques import chain_of_thought, few_shot, one_shot, zero_shot

    reports = {
        "Zero-Shot": zero_shot.run(),
        "One-Shot": one_shot.run(),
        "Few-Shot": few_shot.run(),
        "Chain-of-Thought": chain_of_thought.run(),
    }
    print(compare_reports(reports))


if __name__ == "__main__":
    main()

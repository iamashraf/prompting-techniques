"""LLM-as-judge: scores reports from different techniques side by side.

Same rubric the course notebook used (Completeness, Business Reasoning,
Structure, Actionability, Executive Readiness, 1-5 each) so technique
comparisons aren't just us eyeballing prose -- there's one consistent
scoring pass any technique's baseline output can go through.
"""

from prompting_techniques.ollama_client import ask_ollama
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
1. Completeness
2. Business Reasoning
3. Structure
4. Actionability
5. Executive Readiness

Present the results as a markdown table (one row per criterion, one
column per report), followed by a one-paragraph recommendation of
which report is strongest and why.
""".strip()


def compare_reports(reports: dict[str, str], temperature: float = 0.0) -> str:
    report_blocks = "\n\n".join(
        f"---------- Report: {label} ----------\n{text}" for label, text in reports.items()
    )
    user_prompt = JUDGE_PROMPT_TEMPLATE.format(count=len(reports), report_blocks=report_blocks)

    response = ask_ollama(JUDGE_SYSTEM_PROMPT, user_prompt, temperature=temperature)
    log_path = save_run("judge", JUDGE_SYSTEM_PROMPT, user_prompt, response)
    print(f"--- logged full run to {log_path} ---")

    return response


def main() -> None:
    from prompting_techniques.techniques import one_shot, zero_shot

    reports = {
        "Zero-Shot": zero_shot.run(),
        "One-Shot": one_shot.run(),
    }
    print(compare_reports(reports))


if __name__ == "__main__":
    main()

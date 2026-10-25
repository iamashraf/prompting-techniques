"""Parameter Tuning: a one-variable-at-a-time study.

The prompt stays fixed throughout -- Chain-of-Thought's, since we
already know its correct answer -- and only one inference parameter
changes per sweep, holding the others constant. Mirrors the course
notebook's own methodology (Step 8): sweep temperature, then
max_tokens, then top_p, each in isolation, so any difference in output
is attributable to that one parameter alone.
"""

from prompting_techniques.ollama_client import ask_ollama
from prompting_techniques.run_log import save_run
from prompting_techniques.scenario import build_business_context, load_events
from prompting_techniques.techniques.chain_of_thought import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

TEMPERATURE_VALUES = [0.0, 0.7, 1.2]
MAX_TOKENS_VALUES = [100, 400, 1200]
TOP_P_VALUES = [0.1, 0.5, 1.0]


def _fixed_user_prompt() -> str:
    return USER_PROMPT_TEMPLATE.format(business_context=build_business_context(load_events()))


def sweep_temperature(max_tokens: int = 1200, top_p: float = 1.0) -> dict[float, str]:
    user_prompt = _fixed_user_prompt()
    results = {}
    for temperature in TEMPERATURE_VALUES:
        response = ask_ollama(SYSTEM_PROMPT, user_prompt, temperature=temperature, max_tokens=max_tokens, top_p=top_p)
        save_run("parameter_tuning", SYSTEM_PROMPT, user_prompt, response, label=f"temperature_{temperature}")
        results[temperature] = response
    return results


def sweep_max_tokens(temperature: float = 0.0, top_p: float = 1.0) -> dict[int, str]:
    user_prompt = _fixed_user_prompt()
    results = {}
    for max_tokens in MAX_TOKENS_VALUES:
        response = ask_ollama(SYSTEM_PROMPT, user_prompt, temperature=temperature, max_tokens=max_tokens, top_p=top_p)
        save_run("parameter_tuning", SYSTEM_PROMPT, user_prompt, response, label=f"max_tokens_{max_tokens}")
        results[max_tokens] = response
    return results


def sweep_top_p(temperature: float = 0.8, max_tokens: int = 1200) -> dict[float, str]:
    user_prompt = _fixed_user_prompt()
    results = {}
    for top_p in TOP_P_VALUES:
        response = ask_ollama(SYSTEM_PROMPT, user_prompt, temperature=temperature, max_tokens=max_tokens, top_p=top_p)
        save_run("parameter_tuning", SYSTEM_PROMPT, user_prompt, response, label=f"top_p_{top_p}")
        results[top_p] = response
    return results


def main() -> None:
    print("=== Temperature sweep (max_tokens=1200, top_p=1.0 fixed) ===")
    for temperature, response in sweep_temperature().items():
        print(f"\n--- temperature={temperature} | {len(response)} chars ---\n{response}")

    print("\n=== Max tokens sweep (temperature=0.0, top_p=1.0 fixed) ===")
    for max_tokens, response in sweep_max_tokens().items():
        print(f"\n--- max_tokens={max_tokens} | {len(response)} chars ---\n{response}")

    print("\n=== Top-p sweep (temperature=0.8, max_tokens=1200 fixed) ===")
    for top_p, response in sweep_top_p().items():
        print(f"\n--- top_p={top_p} | {len(response)} chars ---\n{response}")


if __name__ == "__main__":
    main()

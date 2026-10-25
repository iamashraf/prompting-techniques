"""Zero-Shot Prompting.

The model gets an instruction and the task data, and nothing else -- no
worked examples, no demonstration of what a good answer looks like. It
has to rely entirely on what it already learned during training to infer
the right structure and reasoning. Every other technique in this repo is
compared back against this baseline.
"""

import requests

from prompting_techniques.scenario import build_business_context, load_events

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.1:8b"

SYSTEM_PROMPT = """
You are a Senior Supply Chain Risk Analyst.

Base all observations, conclusions, and recommendations solely on the
information provided in the input. Do not assume, infer, or fabricate
facts that are not explicitly supported by the data. Maintain a
professional, executive-ready tone.
""".strip()

USER_PROMPT_TEMPLATE = """
Analyze the following supply chain disruption dataset and prepare a
Business Impact Assessment Report.

## Input Data

{business_context}

## Report Structure

1. Executive Summary
2. Identified Disruptions
3. Root Causes
4. Recommended Mitigation Strategies
""".strip()


def ask_ollama(system: str, user: str, model: str = MODEL) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "stream": False,
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["message"]["content"]


def run() -> str:
    business_context = build_business_context(load_events())
    user_prompt = USER_PROMPT_TEMPLATE.format(business_context=business_context)
    return ask_ollama(SYSTEM_PROMPT, user_prompt)


def main() -> None:
    print(run())


if __name__ == "__main__":
    main()

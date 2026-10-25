"""ReAct: Reasoning + Acting.

Interleaves reasoning with real tool calls instead of generating
everything in one pass: Thought -> Action -> Observation, repeated
until a Final Answer. The one tool here is a real calculator --
Action: calculate[expression] gets evaluated by actual Python, not by
the model, which is the most direct possible fix for the arithmetic
problem every other technique in this repo has struggled with: the
computation is no longer the model's job at all.

Implemented as an explicit text loop (we parse the model's own output
and inject real observations) rather than Ollama's native tool-calling
API, so the Thought/Action/Observation mechanic stays visible instead
of being hidden behind a framework feature.
"""

import ast
import operator
import re

from prompting_techniques.ollama_client import ask_ollama
from prompting_techniques.run_log import save_run
from prompting_techniques.scenario import build_business_context, load_events

SYSTEM_PROMPT = """
You are a Senior Supply Chain Risk Analyst who solves tasks by
interleaving reasoning and tool use, following this exact format:

Thought: <your reasoning about what to do next>
Action: calculate[<a single plain arithmetic expression>]
Observation: <this is filled in for you -- never write it yourself>
... (repeat Thought/Action/Observation as many times as needed)
Thought: I now have everything I need.
Final Answer: <the complete Business Impact Assessment Report>

The only tool available is calculate[expression], which evaluates a
plain arithmetic expression (e.g. calculate[850000 + 1200000]) and
returns the exact result. Use it for every sum instead of computing it
yourself. Base all observations and recommendations solely on the
information provided in the input. Do not assume, infer, or fabricate
facts not explicitly supported by the data.
""".strip()

USER_PROMPT_TEMPLATE = """
Analyze the following supply chain disruption dataset and prepare a
Business Impact Assessment Report with this structure:

1. Executive Summary (state the total financial impact and total
   revenue at risk, each computed via the calculate tool)
2. Identified Disruptions
3. Root Causes
4. Recommended Mitigation Strategies

## Input Data

{business_context}
""".strip()

_ACTION_PATTERN = re.compile(r"Action:\s*calculate\[(.+?)\]")

# Allowlist of operators calculate() will evaluate -- notably excludes
# exponentiation (**), which would let a short expression like
# "9**9**9**9" force an enormous computation. No names or calls are
# permitted at all, by construction of _safe_eval below.
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}


def _safe_eval(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_safe_eval(node.operand))
    raise ValueError(f"disallowed in expression: {ast.dump(node)}")


MAX_EXPRESSION_LENGTH = 200


def calculate(expression: str) -> str:
    """The one real tool: evaluates a plain +-*/ arithmetic expression.

    Parsed and walked via an AST allowlist (not eval()) restricted to
    numeric constants and +-*/  -- no names, calls, attribute access,
    or exponentiation reach the model, regardless of what it sends.
    The length cap is defense in depth against a long chain of
    multiplications building an unbounded big integer (Python ints are
    arbitrary-precision, so even +-*/ alone isn't free of that risk).
    """
    if len(expression) > MAX_EXPRESSION_LENGTH:
        return f"Error: expression too long (max {MAX_EXPRESSION_LENGTH} characters)"
    try:
        tree = ast.parse(expression.replace(",", ""), mode="eval")
        return str(_safe_eval(tree.body))
    except Exception as exc:
        return f"Error: {exc}"


def extract_action(response: str) -> tuple[str, str] | None:
    """Returns (expression, response truncated through the Action line), or None.

    Anything after the Action line is discarded, including any
    Observation the model guessed at itself -- it was told never to
    write one, and we must supply the real result, not let a guess
    stand.
    """
    match = _ACTION_PATTERN.search(response)
    if match is None:
        return None
    return match.group(1), response[: match.end()]


def run(temperature: float = 0.0, max_steps: int = 6) -> str:
    business_context = build_business_context(load_events())
    user_prompt = USER_PROMPT_TEMPLATE.format(business_context=business_context)

    transcript = user_prompt
    for step in range(1, max_steps + 1):
        response = ask_ollama(SYSTEM_PROMPT, transcript, temperature=temperature)
        save_run("react", SYSTEM_PROMPT, transcript, response, label=f"step{step}")

        action = extract_action(response)
        if action is not None:
            expression, truncated_response = action
            observation = calculate(expression)
            print(f"  [tool] calculate[{expression}] -> {observation}")
            transcript += f"\n{truncated_response}\nObservation: {observation}\n"
            continue

        if "Final Answer:" in response:
            print(f"--- finished after {step} step(s) ---")
            return response.split("Final Answer:", 1)[1].strip()

        print("--- model neither called the tool nor gave a final answer -- stopping ---")
        return response

    print(f"--- hit max_steps={max_steps} without a Final Answer ---")
    return transcript


def main() -> None:
    print(run())


if __name__ == "__main__":
    main()

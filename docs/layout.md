# Layout

```
docker-compose.yml                 # optional local Ollama, sharing research-assistant's model volume
scripts/ensure_ollama.sh           # starts Ollama only if nothing's already running
scripts/compare_at_scale.py        # re-runs the comparison against the real, larger dataset
data/                              # shared example scenario: 6-event synthetic CSV (+ bring-your-own real one)
runs/                              # generated prompt+response logs (gitignored)
src/prompting_techniques/
  scenario.py                      # loads the data, builds the shared business_context text
  run_log.py                       # persists every prompt+response under runs/
  ollama_client.py                 # the one shared call to a local Ollama model
  judge.py                         # LLM-as-judge: scores techniques' reports pairwise
  techniques/
    zero_shot.py                   # the technique itself
    zero_shot_experiments.py       # hands-on experiments exploring its nuances
    one_shot.py                    # zero-shot + exactly one worked example
    one_shot_experiments.py        # experiments specific to adding an example
    few_shot.py                    # zero-shot + several worked examples
    chain_of_thought.py            # reason step by step, then write the report
    tree_of_thought.py             # generate multiple options, evaluate, then pick one
    self_consistency.py            # sample chain-of-thought N times, vote on the answer
    prompt_chaining.py             # a 4-step pipeline instead of one call
    structured_output.py           # JSON schema output, verified with plain Python
    react.py                       # Thought/Action/Observation with a real calculator tool
    parameter_tuning.py            # one-variable-at-a-time sweep: temperature, max_tokens, top_p
tests/
```

More techniques land here the same way, one reviewed step at a time.

"""Persists exactly what was sent to the model and what came back.

Every technique module calls save_run() after generating, so every run
leaves a plain-text record under runs/ -- useful for diffing two runs of
the same technique, or comparing techniques side by side later.
"""

from datetime import datetime, timezone
from pathlib import Path

RUNS_DIR = Path(__file__).resolve().parents[2] / "runs"


def save_run(technique: str, system: str, user: str, response: str) -> Path:
    RUNS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    path = RUNS_DIR / f"{technique}_{timestamp}.txt"

    path.write_text(
        f"=== SYSTEM PROMPT ===\n{system}\n\n"
        f"=== USER PROMPT ===\n{user}\n\n"
        f"=== RESPONSE ===\n{response}\n"
    )
    return path

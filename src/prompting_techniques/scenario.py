"""The shared example task every technique module analyzes.

Using the same disruption events and the same business_context text for
every technique keeps comparisons between techniques fair: only the
prompting strategy changes, not the input.
"""

import csv
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "supply_chain_events.csv"

# str.title() capitalizes every word, including acronym letters ("usd" -> "Usd").
# This maps the few column-name acronyms we have back to how they should read.
ACRONYM_OVERRIDES = {"Usd": "USD"}


def load_events(csv_path: Path = DATA_FILE) -> list[dict[str, str]]:
    with csv_path.open(newline="") as f:
        return list(csv.DictReader(f))


def _label(column: str) -> str:
    words = column.replace("_", " ").title().split()
    return " ".join(ACRONYM_OVERRIDES.get(word, word) for word in words)


def build_business_context(events: list[dict[str, str]]) -> str:
    blocks = []
    for position, event in enumerate(events, start=1):
        lines = [f"========== Supply Chain Disruption Event {position} =========="]
        for column, value in event.items():
            lines.append(f"{_label(column)}: {value}")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)

"""The shared example task every technique module analyzes.

Using the same disruption events and the same business_context text for
every technique keeps comparisons between techniques fair: only the
prompting strategy changes, not the input.
"""

import csv
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "supply_chain_events.csv"


def load_events(csv_path: Path = DATA_FILE) -> list[dict[str, str]]:
    with csv_path.open(newline="") as f:
        return list(csv.DictReader(f))


def build_business_context(events: list[dict[str, str]]) -> str:
    blocks = []
    for position, event in enumerate(events, start=1):
        lines = [f"========== Supply Chain Disruption Event {position} =========="]
        for column, value in event.items():
            label = column.replace("_", " ").title()
            lines.append(f"{label}: {value}")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)

"""The shared example task every technique module analyzes.

Using the same disruption events and the same business_context text for
every technique keeps comparisons between techniques fair: only the
prompting strategy changes, not the input.
"""

import csv
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "supply_chain_events.csv"

# The real course dataset (100 rows, 26 columns) -- richer and far
# larger than the 6-event synthetic one above. Opt in via load_events's
# csv_path/limit params; the default stays the small synthetic set so
# every existing finding stays reproducible exactly as written.
REAL_DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "supply_chain_disruptions_100_events.csv"

# str.title() capitalizes every word, including acronym letters ("usd" -> "Usd").
# This maps the column-name acronyms we have back to how they should read.
ACRONYM_OVERRIDES = {"Usd": "USD", "Otd": "OTD", "Doh": "DOH", "Skus": "SKUs"}


def load_events(csv_path: Path = DATA_FILE, limit: int | None = None) -> list[dict[str, str]]:
    with csv_path.open(newline="") as f:
        events = list(csv.DictReader(f))
    return events[:limit] if limit is not None else events


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

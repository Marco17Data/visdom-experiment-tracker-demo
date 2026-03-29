from __future__ import annotations

from pathlib import Path
from pprint import pprint

from src.compare import top_runs
from src.plot import plot_lr_vs_accuracy
from src.search import filter_runs
from src.tracker import RunTracker


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "runs.db"
DATA_PATH = BASE_DIR / "data" / "sample_runs.json"
OUTPUT_PATH = BASE_DIR / "output" / "lr_vs_accuracy.html"


def print_section(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def main() -> None:
    tracker = RunTracker(DB_PATH)
    tracker.clear_runs()
    tracker.load_runs_from_json(DATA_PATH)

    all_runs = tracker.fetch_all_runs()

    print_section("Loaded Runs")
    print(f"Total runs loaded: {len(all_runs)}")

    print_section("Filter: optimizer=adam")
    pprint(filter_runs(tracker.conn, "optimizer=adam"))

    print_section("Filter: tag=baseline")
    pprint(filter_runs(tracker.conn, "tag=baseline"))

    print_section("Top Runs by Accuracy")
    pprint(top_runs(tracker.conn, sort_by="final_accuracy", limit=3))

    print_section("Top Runs by Lowest Loss")
    pprint(top_runs(tracker.conn, sort_by="final_loss", limit=3))

    plot_lr_vs_accuracy(all_runs, OUTPUT_PATH)
    print_section("Chart Output")
    print(f"Saved Plotly chart to: {OUTPUT_PATH}")

    tracker.close()


if __name__ == "__main__":
    main()

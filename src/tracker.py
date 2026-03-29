from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_name TEXT NOT NULL,
    model TEXT NOT NULL,
    learning_rate REAL NOT NULL,
    batch_size INTEGER NOT NULL,
    optimizer TEXT NOT NULL,
    final_accuracy REAL NOT NULL,
    final_loss REAL NOT NULL,
    tag TEXT NOT NULL
);
"""


class RunTracker:
    def __init__(self, db_path: str | Path) -> None:
        self.db_path = str(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._setup()

    def _setup(self) -> None:
        self.conn.execute(SCHEMA)
        self.conn.commit()

    def clear_runs(self) -> None:
        self.conn.execute("DELETE FROM runs")
        self.conn.commit()

    def insert_run(self, run: dict[str, Any]) -> None:
        self.conn.execute(
            """
            INSERT INTO runs (
                run_name, model, learning_rate, batch_size,
                optimizer, final_accuracy, final_loss, tag
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run["run_name"],
                run["model"],
                run["learning_rate"],
                run["batch_size"],
                run["optimizer"],
                run["final_accuracy"],
                run["final_loss"],
                run["tag"],
            ),
        )
        self.conn.commit()

    def load_runs_from_json(self, json_path: str | Path) -> None:
        path = Path(json_path)
        runs = json.loads(path.read_text())
        for run in runs:
            self.insert_run(run)

    def fetch_all_runs(self) -> list[dict[str, Any]]:
        rows = self.conn.execute("SELECT * FROM runs ORDER BY id ASC").fetchall()
        return [dict(row) for row in rows]

    def close(self) -> None:
        self.conn.close()

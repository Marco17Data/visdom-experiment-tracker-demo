from __future__ import annotations

import sqlite3
from typing import Any


ALLOWED_SORT_KEYS = {"final_accuracy", "final_loss", "learning_rate", "batch_size"}


def top_runs(conn: sqlite3.Connection, sort_by: str = "final_accuracy", limit: int = 3) -> list[dict[str, Any]]:
    if sort_by not in ALLOWED_SORT_KEYS:
        raise ValueError(f"Unsupported sort key: {sort_by}")

    direction = "DESC" if sort_by != "final_loss" else "ASC"
    query = f"SELECT * FROM runs ORDER BY {sort_by} {direction} LIMIT ?"
    rows = conn.execute(query, (limit,)).fetchall()
    return [dict(row) for row in rows]

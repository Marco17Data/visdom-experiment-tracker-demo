from __future__ import annotations

import sqlite3
from typing import Any


ALLOWED_FIELDS = {
    "run_name",
    "model",
    "learning_rate",
    "batch_size",
    "optimizer",
    "final_accuracy",
    "final_loss",
    "tag",
}

NUMERIC_FIELDS = {"learning_rate", "batch_size", "final_accuracy", "final_loss"}


def parse_simple_query(query: str) -> tuple[str, Any]:
    if "=" not in query:
        raise ValueError("Query must look like field=value")

    field, value = query.split("=", 1)
    field = field.strip()
    value = value.strip()

    if field not in ALLOWED_FIELDS:
        raise ValueError(f"Unsupported field: {field}")

    if field in NUMERIC_FIELDS:
        if field == "batch_size":
            value = int(value)
        else:
            value = float(value)

    return field, value


def filter_runs(conn: sqlite3.Connection, query: str) -> list[dict[str, Any]]:
    field, value = parse_simple_query(query)
    cursor = conn.execute(f"SELECT * FROM runs WHERE {field} = ? ORDER BY id ASC", (value,))
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

from __future__ import annotations

from pathlib import Path

import plotly.express as px


def plot_lr_vs_accuracy(runs: list[dict], output_path: str | Path) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fig = px.scatter(
        runs,
        x="learning_rate",
        y="final_accuracy",
        color="optimizer",
        hover_name="run_name",
        size="batch_size",
        title="Learning Rate vs Final Accuracy",
    )
    fig.write_html(str(path), include_plotlyjs="cdn")

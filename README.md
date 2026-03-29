# visdom-experiment-tracker-demo

This is a small prototype I made while preparing my GSoC proposal for FOSSASIA Visdom.

I wanted to explore a few practical parts of experiment management before writing the full proposal:
- storing run metadata
- searching and filtering experiments
- comparing runs
- plotting simple parameter/performance trends

This is not a full experiment platform. It is only a small demo to think more concretely about how experiment tracking and meta-analysis could work.

## What it does

- stores sample experiment runs in SQLite
- supports simple filtering like `optimizer=adam` or `tag=baseline`
- compares runs by accuracy or loss
- creates a basic Plotly chart for learning rate vs accuracy

## Run it

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

The script will:
1. create a local SQLite database
2. load sample runs
3. print filtered results
4. print top runs
5. generate an HTML chart in `output/lr_vs_accuracy.html`

## Notes

This demo keeps the scope intentionally small. I mainly wanted to test a simple data model and a basic workflow before writing a larger proposal around experiment tracking and meta-analysis.

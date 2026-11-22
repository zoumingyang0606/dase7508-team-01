"""Reproduce the clean Enron1 word and character baselines locally."""
import argparse
import csv
import json
from pathlib import Path

from sklearn.model_selection import train_test_split
from threadpoolctl import threadpool_limits

from src.core import fit, load, metrics

ROOT = Path(__file__).resolve().parent


def labels(rows):
    return [row[2] for row in rows]


def texts(rows):
    return [row[1] for row in rows]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=ROOT / "results" / "clean_reproduced.json")
    args = parser.parse_args()
    rows, data_audit = load(args.data)
    train, reserved = train_test_split(rows, test_size=.4, stratify=labels(rows), random_state=42)
    valid, test = train_test_split(reserved, test_size=.5, stratify=labels(reserved), random_state=42)
    with (ROOT / "results" / "clean_metrics.csv").open(encoding="utf-8", newline="") as handle:
        baseline = {row["model"]: row for row in csv.DictReader(handle)}
    measured = {}
    with threadpool_limits(limits=1):
        for name in ("A", "C"):
            model, fit_audit = fit(texts(train), labels(train), texts(valid), labels(valid), name == "C")
            predictions = model.predict(texts(test))
            row = metrics(labels(test), predictions, predictions)
            counts = ("TP", "FP", "TN", "FN")
            agrees = all(row[key] == int(baseline[name][key]) for key in counts)
            measured[name] = {"fit": fit_audit, "clean_metrics": row, "matches_frozen_counts": agrees}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({"data": data_audit, "models": measured}, indent=2), encoding="utf-8")
    print(json.dumps(measured, indent=2))
    if not all(result["matches_frozen_counts"] for result in measured.values()):
        raise SystemExit("Reproduced counts differ from the frozen baseline.")


if __name__ == "__main__":
    main()

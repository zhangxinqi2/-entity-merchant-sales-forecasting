#!/usr/bin/env python3
"""Evaluate sales forecasts with the metrics used in this project.

Supported inputs
----------------
1. One CSV with ``actual`` and ``predicted`` columns::

       python analysis/evaluate.py --input predictions.csv

2. Two CSVs whose rows are aligned::

       python analysis/evaluate.py --actual actual.csv --prediction pred.csv

Use ``--self-test`` to verify the metric implementations without a file.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path


def _read_column(path: Path, column: str | None = None) -> list[float]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{path} has no header row")
        if column is None:
            candidates = [name for name in reader.fieldnames if name.strip().lower() in {"actual", "y_true", "true"}]
            if not candidates:
                candidates = [reader.fieldnames[0]]
            column = candidates[0]
        if column not in reader.fieldnames:
            raise KeyError(f"column {column!r} not found; available: {reader.fieldnames}")
        values: list[float] = []
        for row_number, row in enumerate(reader, start=2):
            raw = (row.get(column) or "").strip()
            if raw == "":
                continue
            try:
                values.append(float(raw))
            except ValueError as exc:
                raise ValueError(f"{path}:{row_number}: cannot parse {raw!r} as a number") from exc
    return values


def _read_pair(path: Path) -> tuple[list[float], list[float]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{path} has no header row")
        names = {name.strip().lower(): name for name in reader.fieldnames}
        actual_name = names.get("actual") or names.get("y_true") or names.get("true")
        pred_name = names.get("predicted") or names.get("prediction") or names.get("y_pred") or names.get("forecast")
        if actual_name is None or pred_name is None:
            raise KeyError("input CSV must contain actual/true and predicted/forecast columns")
        actual: list[float] = []
        predicted: list[float] = []
        for row in reader:
            if (row.get(actual_name) or "").strip() == "" or (row.get(pred_name) or "").strip() == "":
                continue
            actual.append(float(row[actual_name]))
            predicted.append(float(row[pred_name]))
    return actual, predicted


def evaluate(actual: list[float], predicted: list[float]) -> dict[str, float]:
    if len(actual) != len(predicted):
        raise ValueError(f"length mismatch: actual={len(actual)}, predicted={len(predicted)}")
    if not actual:
        raise ValueError("no overlapping non-empty rows to evaluate")

    n = len(actual)
    absolute_errors = [abs(a - p) for a, p in zip(actual, predicted)]
    squared_errors = [(a - p) ** 2 for a, p in zip(actual, predicted)]

    denominator = sum(abs(a) for a in actual)
    wmape = (sum(absolute_errors) / denominator * 100.0) if denominator else 0.0
    mae = sum(absolute_errors) / n
    rmse = math.sqrt(sum(squared_errors) / n)

    mape_terms = [abs(a - p) / abs(a) for a, p in zip(actual, predicted) if a != 0]
    mape = (sum(mape_terms) / len(mape_terms) * 100.0) if mape_terms else 0.0

    smape_terms = []
    for a, p in zip(actual, predicted):
        scale = (abs(a) + abs(p)) / 2.0
        smape_terms.append(0.0 if scale == 0 else abs(a - p) / scale)
    smape = sum(smape_terms) / n * 100.0

    return {
        "count": float(n),
        "wmape": round(wmape, 4),
        "mape": round(mape, 4),
        "smape": round(smape, 4),
        "mae": round(mae, 4),
        "rmse": round(rmse, 4),
        "actual_sum": round(sum(actual), 4),
        "predicted_sum": round(sum(predicted), 4),
    }


def _self_test() -> None:
    metrics = evaluate([10, 20, 30, 40], [12, 18, 33, 38])
    expected = {"wmape": 9.0, "mae": 2.25, "rmse": 2.2913, "mape": 11.25}
    for key, value in expected.items():
        if not math.isclose(metrics[key], value, abs_tol=1e-4):
            raise AssertionError(f"self-test failed for {key}: {metrics[key]} != {value}")
    print("self-test passed:", json.dumps(metrics, ensure_ascii=False))


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate sales forecasts.")
    parser.add_argument("--input", type=Path, help="CSV with actual and predicted columns.")
    parser.add_argument("--actual", type=Path, help="CSV whose first column is the actual value.")
    parser.add_argument("--prediction", type=Path, help="CSV whose first column is the predicted value.")
    parser.add_argument("--actual-column", default=None, help="Column name for --actual (default: first column).")
    parser.add_argument("--prediction-column", default=None, help="Column name for --prediction (default: first column).")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of a table.")
    parser.add_argument("--self-test", action="store_true", help="Run built-in tests and exit.")
    args = parser.parse_args()

    if args.self_test:
        _self_test()
        return 0

    if args.input:
        actual, predicted = _read_pair(args.input)
    elif args.actual and args.prediction:
        actual = _read_column(args.actual, args.actual_column)
        predicted = _read_column(args.prediction, args.prediction_column)
    else:
        parser.error("provide --input, or both --actual and --prediction")

    metrics = evaluate(actual, predicted)
    if args.json:
        print(json.dumps(metrics, ensure_ascii=False, indent=2))
    else:
        print("=" * 46)
        print(f"{'Samples':<14}{int(metrics['count']):>12}")
        print(f"{'WMAPE (%)':<14}{metrics['wmape']:>12.4f}")
        print(f"{'MAPE (%)':<14}{metrics['mape']:>12.4f}")
        print(f"{'SMAPE (%)':<14}{metrics['smape']:>12.4f}")
        print(f"{'MAE':<14}{metrics['mae']:>12.4f}")
        print(f"{'RMSE':<14}{metrics['rmse']:>12.4f}")
        print("=" * 46)
    return 0


if __name__ == "__main__":
    sys.exit(main())

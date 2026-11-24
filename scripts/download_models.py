#!/usr/bin/env python3
"""Download the pretrained forecasting models used by the project.

Model weights are NOT stored in this repository (they are large third-party
artifacts). This script downloads them into ``forecasting/models/`` from
ModelScope (default) or Hugging Face.

Examples::

    python scripts/download_models.py --list
    python scripts/download_models.py --model timesfm
    python scripts/download_models.py --model all --source huggingface

Install the download client first::

    pip install modelscope            # default source
    pip install huggingface_hub       # --source huggingface

Approximate download sizes: Chronos-2 ~0.5 GB, TimesFM-2.5 ~0.9 GB,
TiRex ~0.3 GB. Keep at least 3 GB free.
"""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGET = ROOT / "forecasting" / "models"

MODELS = {
    "chronos2": {
        "label": "Chronos-2 (Amazon)",
        "modelscope": "amazon/chronos-2",
        "huggingface": "amazon/chronos-2",
        "target": "chronos-2",
        "size": "~0.5 GB",
    },
    "timesfm": {
        "label": "TimesFM-2.5-200M (Google)",
        "modelscope": "google/timesfm-2.5-200m-pytorch",
        "huggingface": "google/timesfm-2.5-200m-pytorch",
        "target": "timesfm-2.5-200m-pytorch",
        "size": "~0.9 GB",
    },
    "tirex": {
        "label": "TiRex (NX-AI)",
        "modelscope": "NX-AI/TiRex",
        "huggingface": "NX-AI/TiRex",
        "target": "tirex-model",
        "size": "~0.3 GB",
    },
}


def _print_table() -> None:
    print(f"{'key':<10}{'model':<34}{'size':<10}target")
    print("-" * 78)
    for key, spec in MODELS.items():
        print(f"{key:<10}{spec['label']:<34}{spec['size']:<10}{spec['target']}")
    print("\nSources: ModelScope (default) or Hugging Face (--source huggingface).")


def _download_modelscope(model_id: str, target: Path) -> None:
    try:
        from modelscope import snapshot_download
    except ImportError as exc:
        raise RuntimeError("ModelScope client is missing. Run: pip install modelscope") from exc
    print(f"  ModelScope: {model_id} -> {target}")
    snapshot_download(model_id, local_dir=str(target))


def _download_huggingface(repo_id: str, target: Path) -> None:
    try:
        from huggingface_hub import snapshot_download
    except ImportError as exc:
        raise RuntimeError("Hugging Face client is missing. Run: pip install huggingface_hub") from exc
    print(f"  Hugging Face: {repo_id} -> {target}")
    snapshot_download(repo_id=repo_id, local_dir=str(target))


def main() -> int:
    parser = argparse.ArgumentParser(description="Download forecasting model weights.")
    parser.add_argument("--model", choices=["all", *MODELS], default="all")
    parser.add_argument("--source", choices=["modelscope", "huggingface"], default="modelscope")
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    parser.add_argument("--list", action="store_true", help="List models and exit.")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be downloaded.")
    args = parser.parse_args()

    if args.list:
        _print_table()
        return 0

    selected = list(MODELS) if args.model == "all" else [args.model]
    args.target.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {len(selected)} model(s) to {args.target}\n")

    for key in selected:
        spec = MODELS[key]
        target = args.target / spec["target"]
        print(f"[{key}] {spec['label']} ({spec['size']})")
        if args.dry_run:
            repo = spec[args.source]
            print(f"  would download {repo} -> {target}")
            continue
        target.mkdir(parents=True, exist_ok=True)
        if args.source == "modelscope":
            _download_modelscope(spec["modelscope"], target)
        else:
            _download_huggingface(spec["huggingface"], target)

    if args.dry_run:
        print("\nDry run complete. No files were downloaded.")
        return 0

    print("\nDone. Model folders:")
    for key in selected:
        print(f"  {args.target / MODELS[key]['target']}")
    print("\nNext: cd forecasting && pip install -r requirements.txt && pip install -e .")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

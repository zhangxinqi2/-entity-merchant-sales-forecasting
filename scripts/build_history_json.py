#!/usr/bin/env python3
"""Convert per-product merchant CSV files into the demo JSON consumed by the web app.

The expected CSV layout is the one used by the demo::

    行业：烘焙行业  地址：示例市 · 演示商圈（合成数据）  商品名称：黄油可颂  商品ID：001_01
    日期,平均售价,销量,日平均气温,节假日,打折
    2025-01-01 00:00:00,18.20,120,15.1,否,是

Usage::

    python scripts/build_history_json.py --input-dir data/raw --output web/public/data/products_history_data.json

The script only performs local file conversion. It does not upload anything.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "web" / "public" / "data" / "products_history_data.json"

META_KEYS = {
    "行业": "industry",
    "地址": "address",
    "商品名称": "product_name",
    "商品ID": "product_id",
    "商品id": "product_id",
}

COLUMN_ALIASES = {
    "date": {"日期", "date", "时间"},
    "avg_price": {"平均售价", "avg_price", "price", "售价"},
    "sales": {"销量", "sales", "销售量"},
    "temperature": {"日平均气温", "平均气温", "temperature", "气温"},
    "is_holiday": {"节假日", "is_holiday", "holiday"},
    "is_discount": {"打折", "is_discount", "discount"},
}


def parse_metadata(line: str) -> dict[str, str]:
    meta: dict[str, str] = {}
    for chunk in re.split(r"\s{2,}", line.strip()):
        chunk = chunk.strip().strip(",")
        if "：" in chunk:
            key, value = chunk.split("：", 1)
        elif ":" in chunk:
            key, value = chunk.split(":", 1)
        else:
            continue
        key = key.strip()
        if key in META_KEYS:
            meta[META_KEYS[key]] = value.strip()
    return meta


def is_yes(value: str) -> bool:
    return value.strip().lower() in {"是", "true", "1", "yes", "y", "是 "}


def normalise_date(value: str) -> str:
    value = value.strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S", "%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return value[:10]


def find_column(fieldnames: list[str], target: str) -> str | None:
    for name in fieldnames:
        if name.strip() in COLUMN_ALIASES[target]:
            return name
    return None


def convert_file(path: Path) -> tuple[str, dict] | None:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        lines = handle.readlines()
    if len(lines) < 3:
        return None

    meta = parse_metadata(lines[0])
    product_id = meta.get("product_id") or path.stem
    product_name = meta.get("product_name") or path.stem
    industry = meta.get("industry", "")
    address = meta.get("address", "")

    reader = csv.DictReader(lines[1:])
    fieldnames = reader.fieldnames or []
    columns = {key: find_column(fieldnames, key) for key in COLUMN_ALIASES}
    if columns["sales"] is None or columns["date"] is None:
        raise ValueError(f"{path}: cannot find 日期/销量 columns; header={fieldnames}")

    rows = []
    for row in reader:
        try:
            rows.append({
                "date": normalise_date(row[columns["date"]]),
                "avg_price": round(float(row[columns["avg_price"]]), 2) if columns["avg_price"] else 0.0,
                "sales": int(float(row[columns["sales"]])),
                "temperature": round(float(row[columns["temperature"]]), 1) if columns["temperature"] else 0.0,
                "is_holiday": is_yes(row[columns["is_holiday"]]) if columns["is_holiday"] else False,
                "is_discount": is_yes(row[columns["is_discount"]]) if columns["is_discount"] else False,
            })
        except (KeyError, TypeError, ValueError):
            continue

    if not rows:
        return None
    return product_id, {
        "product_id": product_id,
        "product_name": product_name,
        "industry": industry,
        "address": address,
        "data": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build products_history_data.json from merchant CSV files.")
    parser.add_argument("--input-dir", type=Path, default=ROOT / "data" / "raw")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    if not args.input_dir.is_dir():
        parser.error(f"input directory does not exist: {args.input_dir}")

    result: dict[str, dict] = {}
    files = sorted(args.input_dir.glob("*.csv"))
    for path in files:
        converted = convert_file(path)
        if converted is None:
            print(f"[skip] {path.name}")
            continue
        product_id, record = converted
        result[product_id] = record
        print(f"[ok]   {path.name} -> {product_id} ({len(record['data'])} rows)")

    if not result:
        print("No CSV files were converted. Check --input-dir and the file format.")
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(result)} products to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

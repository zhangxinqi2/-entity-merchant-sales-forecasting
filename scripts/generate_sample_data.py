#!/usr/bin/env python3
"""Generate synthetic demo data for the Entity Merchant Sales Forecasting platform.

The output is deliberately fictional: it contains no real merchant names,
addresses, sales records, or competition data. It is safe to commit to a public
repository and is used by the Vue demo and the sample CSV files.

Outputs
-------
- web/src/data/products.js
- web/src/data/salesData.js
- web/public/data/products_history_data.json
- data/sample/*.csv
- web/public/images/boxplots/*.png (optional, requires matplotlib)

Usage
-----
    python scripts/generate_sample_data.py
    python scripts/generate_sample_data.py --no-plots
"""

from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB_DATA = ROOT / "web" / "src" / "data"
WEB_PUBLIC_DATA = ROOT / "web" / "public" / "data"
BOXPLOT_DIR = ROOT / "web" / "public" / "images" / "boxplots"
SAMPLE_DIR = ROOT / "data" / "sample"

START_DATE = date(2025, 1, 1)
DAYS = 120
SYNTHETIC_ADDRESS = "示例市 · 演示商圈（合成数据）"
SEED = 20251124

# Chinese public holidays that fall inside the demo window.
HOLIDAYS = {
    date(2025, 1, 1),
    *{date(2025, 1, 28) + timedelta(days=i) for i in range(8)},  # Spring Festival
    *{date(2025, 4, 4) + timedelta(days=i) for i in range(3)},   # Qingming
}


@dataclass(frozen=True)
class Product:
    product_id: str
    product_name: str
    industry: str
    price: float
    base_sales: float


def _make_products() -> list[Product]:
    bakery = [
        "黄油可颂", "海盐卷", "草莓丹麦", "抹茶贝果", "红豆吐司", "焦糖布丁",
        "原味可露丽", "巧克力司康", "芝士碱水棒", "蔓越莓曲奇", "香草泡芙", "肉桂卷",
        "蓝莓麦芬", "柠檬挞", "杏仁可颂", "提拉米苏", "栗子蒙布朗", "酸奶餐包",
    ]
    restaurant = [
        "番茄鸡蛋面", "鲜肉小笼包", "香煎锅贴", "牛肉炒饭", "牛肉粉丝汤", "卤肉饭",
        "酸辣粉", "葱油拌面", "炸酱面", "咖喱鸡饭", "麻辣烫", "酸菜鱼饭",
        "照烧鸡腿饭", "排骨年糕", "鲜虾云吞", "蒸饺", "生煎包", "蛋炒饭",
    ]
    tea = [
        "茉莉奶绿", "桂花乌龙", "生椰拿铁", "美式咖啡", "柠檬茶", "芋泥波波",
        "黑糖珍珠奶茶", "抹茶拿铁", "杨枝甘露", "草莓奶昔", "青提果茶", "可可牛奶",
    ]

    groups = [
        ("001", "烘焙行业", bakery[0:6], 18.0, 120.0),
        ("002", "餐饮行业", restaurant[0:6], 22.0, 95.0),
        ("003", "餐饮行业", restaurant[6:12], 20.0, 90.0),
        ("004", "餐饮行业", restaurant[12:18], 24.0, 100.0),
        ("005", "烘焙行业", bakery[6:12], 16.0, 110.0),
        ("006", "茶饮行业", tea[0:6], 15.0, 85.0),
        ("007", "茶饮行业", tea[6:12], 17.0, 80.0),
        ("008", "烘焙行业", bakery[12:18], 19.0, 105.0),
    ]

    products: list[Product] = []
    rng = random.Random(SEED)
    for prefix, industry, names, price, base in groups:
        for index, name in enumerate(names, start=1):
            products.append(
                Product(
                    product_id=f"{prefix}_{index:02d}",
                    product_name=name,
                    industry=industry,
                    price=round(price + rng.uniform(-3.0, 5.0), 2),
                    base_sales=base * rng.uniform(0.72, 1.45),
                )
            )
    return products


def _generate_series(product: Product, rng: random.Random) -> list[dict]:
    rows: list[dict] = []
    for i in range(DAYS):
        current = START_DATE + timedelta(days=i)
        weekday = current.weekday()
        holiday = current in HOLIDAYS
        discount = rng.random() < 0.28

        season = 1.0 + 0.14 * math.sin(2 * math.pi * (i + 35) / DAYS)
        weekend = 1.28 if weekday >= 5 else 1.0
        friday = 1.07 if weekday == 4 else 1.0
        holiday_factor = 1.35 if holiday else 1.0
        discount_factor = 1.10 if discount else 1.0
        noise = rng.uniform(0.88, 1.12)

        sales = int(max(1, round(
            product.base_sales * season * weekend * friday * holiday_factor
            * discount_factor * noise
        )))
        price = round(product.price * rng.uniform(0.92, 1.08) * (0.90 if discount else 1.0), 2)
        temperature = round(
            16.5 + 7.0 * math.sin(2 * math.pi * (current.timetuple().tm_yday - 110) / 365)
            + rng.uniform(-1.5, 1.5),
            1,
        )

        rows.append({
            "date": current.isoformat(),
            "avg_price": price,
            "sales": sales,
            "temperature": temperature,
            "is_holiday": holiday,
            "is_discount": discount,
        })
    return rows


def _write_products_js(products: list[Product]) -> None:
    lines = [
        "// 合成示例数据：不包含任何真实商家、地址或销量信息。",
        "// 由 scripts/generate_sample_data.py 自动生成，请勿手工编辑。",
        "",
        "export const products = [",
    ]
    for product in products:
        lines.append(
            "  { product_id: '%s', product_name: '%s', industry: '%s', address: '%s' },"
            % (product.product_id, product.product_name, product.industry, SYNTHETIC_ADDRESS)
        )
    lines += [
        "]",
        "",
        "export const industryInfo = [",
        "  {",
        "    name: '烘焙行业',",
        "    product_count: 18,",
        "    heatmap_image: '/images/heatmaps/bakery.png',",
        "    boxplot_image: '/images/boxplots/bakery_sales.png',",
        "    boxplot_image2: '/images/boxplots/bakery_holiday.png',",
        "    description: '合成示例：烘焙商品销量相对稳定，周末和节假日通常高于工作日。'",
        "  },",
        "  {",
        "    name: '餐饮行业',",
        "    product_count: 18,",
        "    heatmap_image: '/images/heatmaps/catering.png',",
        "    boxplot_image: '/images/boxplots/catering_sales.png',",
        "    boxplot_image2: '/images/boxplots/catering_holiday.png',",
        "    description: '合成示例：餐饮商品销量波动较大，节假日和促销活动会带来明显提升。'",
        "  },",
        "  {",
        "    name: '茶饮行业',",
        "    product_count: 12,",
        "    heatmap_image: '/images/heatmaps/tea.png',",
        "    boxplot_image: '/images/boxplots/tea_sales.png',",
        "    boxplot_image2: '/images/boxplots/tea_holiday.png',",
        "    description: '合成示例：茶饮商品具有明显的周末和季节性波动。'",
        "  }",
        "]",
        "",
        "export const generateMockData = (productId) => {",
        "  const product = products.find((p) => p.product_id === productId) || products[0]",
        "  const startDate = new Date('2025-01-01')",
        "  const timeSeries = []",
        "",
        "  for (let i = 0; i < 120; i++) {",
        "    const date = new Date(startDate)",
        "    date.setDate(date.getDate() + i)",
        "    const isWeekend = date.getDay() === 0 || date.getDay() === 6",
        "    const baseSales = 90 + Math.sin(i / 14) * 20",
        "    const sales = Math.round(baseSales * (isWeekend ? 1.25 : 1))",
        "    timeSeries.push({",
        "      date: date.toISOString().split('T')[0],",
        "      sales,",
        "      temperature: Math.round((16 + Math.sin(i / 30) * 6) * 10) / 10",
        "    })",
        "  }",
        "",
        "  return {",
        "    product_id: product.product_id,",
        "    product_name: product.product_name,",
        "    industry: product.industry,",
        "    address: product.address,",
        "    time_window: '2025-01-01 至 2025-04-30',",
        "    statistics: {",
        "      price_mean: 18.0,",
        "      price_mode: 18.0,",
        "      sales_max: Math.max(...timeSeries.map((item) => item.sales)),",
        "      sales_max_date: timeSeries[timeSeries.length - 1].date,",
        "      sales_min: Math.min(...timeSeries.map((item) => item.sales)),",
        "      sales_min_date: timeSeries[0].date",
        "    },",
        "    time_series: timeSeries",
        "  }",
        "}",
        "",
    ]
    (WEB_DATA / "products.js").write_text("\n".join(lines), encoding="utf-8")


SALES_DATA_TAIL = r"""
// 模型对比指标来自作者在原比赛数据上的聚合评测结果（不含商家级明细）。
export const modelMetrics = {
  'elpa': { wmape: 0.1756, mape: 0.1823, smape: 0.1689 },
  'timefm2.5': { wmape: 0.0520, mape: 0.0520, smape: 0.0510 },
  'catboost': { wmape: 0.1895, mape: 0.1956, smape: 0.1821 },
  'xgboost': { wmape: 0.1844, mape: 0.1912, smape: 0.1785 },
  'xgboost-rf': { wmape: 0.1812, mape: 0.1878, smape: 0.1756 },
  'timehf-pctlm': { wmape: 0.1923, mape: 0.1987, smape: 0.1856 },
  'sarima': { wmape: 0.2156, mape: 0.2234, smape: 0.2089 },
  'chronos': { wmape: 0.2345, mape: 0.2412, smape: 0.2267 },
  'tirex': { wmape: 0.2089, mape: 0.2156, smape: 0.2012 },
  'lstm': { wmape: 0.1987, mape: 0.2056, smape: 0.1923 }
};

// 生成模型预测数据（演示用）
export const generateFullPredictionData = (modelId, productId) => {
  const productData = realSalesData[productId] || realSalesData['001_01'];
  const metrics = modelMetrics[modelId] || modelMetrics['elpa'];

  const errorLevel = metrics.wmape;
  const timeSeries = productData.time_series.map((item) => ({
    ...item,
    predicted: Math.round(item.sales * (1 + (Math.random() - 0.5) * errorLevel * 4))
  }));

  const predictions = generateFuturePredictions(productData, errorLevel);

  const actualValues = timeSeries.slice(-30).map((item) => item.sales);
  const predictedValues = timeSeries.slice(-30).map((item) => item.predicted);
  const wmape = calculateWMAPE(actualValues, predictedValues);
  const mape = calculateMAPE(actualValues, predictedValues);
  const smape = calculateSMAPE(actualValues, predictedValues);

  return {
    model_id: modelId,
    model_name: getModelName(modelId),
    product_id: productData.product_id,
    time_series: timeSeries,
    predictions,
    error_metrics: {
      wmape: Math.round(wmape * 1000) / 1000,
      mape: Math.round(mape * 1000) / 1000,
      smape: Math.round(smape * 1000) / 1000
    }
  };
};

function generateFuturePredictions(productData, errorLevel) {
  const lastWeekSales = productData.time_series.slice(-7);
  const avgSales = lastWeekSales.reduce((sum, day) => sum + day.sales, 0) / 7;

  const lastDate = new Date(productData.time_series[productData.time_series.length - 1].date);
  const predictions = [];

  for (let i = 1; i <= 7; i++) {
    const date = new Date(lastDate);
    date.setDate(date.getDate() + i);
    const isWeekend = date.getDay() === 0 || date.getDay() === 6;
    const basePrediction = avgSales * (isWeekend ? 1.2 : 1);
    const randomFactor = 1 + (Math.random() - 0.5) * errorLevel * 2;

    predictions.push({
      date: date.toISOString().split('T')[0],
      predicted_sales: Math.max(0, Math.round(basePrediction * randomFactor)),
      confidence: Math.round((85 + Math.random() * 10 - errorLevel * 50) * 10) / 10
    });
  }

  return predictions;
}

function getModelName(modelId) {
  const modelNames = {
    'elpa': 'ELPA',
    'timefm2.5': 'TimeFM 2.5',
    'catboost': 'CatBoost',
    'xgboost': 'XGBoost',
    'xgboost-rf': 'XGBoost+RF',
    'timehf-pctlm': 'TimeHF-PCTLM',
    'sarima': 'SARIMA',
    'chronos': 'Chronos',
    'tirex': 'TiRex',
    'lstm': 'LSTM'
  };
  return modelNames[modelId] || modelId;
}

function calculateWMAPE(actual, predicted) {
  let numerator = 0;
  let denominator = 0;
  for (let i = 0; i < actual.length; i++) {
    numerator += Math.abs(actual[i] - predicted[i]);
    denominator += Math.abs(actual[i]);
  }
  return denominator === 0 ? 0 : numerator / denominator;
}

function calculateMAPE(actual, predicted) {
  let sum = 0;
  let count = 0;
  for (let i = 0; i < actual.length; i++) {
    if (actual[i] !== 0) {
      sum += Math.abs((actual[i] - predicted[i]) / actual[i]);
      count++;
    }
  }
  return count === 0 ? 0 : sum / count;
}

function calculateSMAPE(actual, predicted) {
  let sum = 0;
  for (let i = 0; i < actual.length; i++) {
    const denominator = (Math.abs(actual[i]) + Math.abs(predicted[i])) / 2;
    sum += denominator === 0 ? 0 : Math.abs(actual[i] - predicted[i]) / denominator;
  }
  return actual.length === 0 ? 0 : sum / actual.length;
}
"""


def _write_sales_data_js(series_by_id: dict[str, list[dict]], products: list[Product]) -> None:
    data = {}
    for product in products:
        data[product.product_id] = {
            "product_id": product.product_id,
            "product_name": product.product_name,
            "time_series": [
                {
                    "date": row["date"],
                    "sales": row["sales"],
                    "temperature": row["temperature"],
                }
                for row in series_by_id[product.product_id]
            ],
        }

    header = (
        "// 合成示例数据：不包含任何真实商家、地址或销量信息。\n"
        "// 由 scripts/generate_sample_data.py 自动生成，请勿手工编辑。\n"
        "export const realSalesData = "
    )
    body = json.dumps(data, ensure_ascii=False, indent=2)
    (WEB_DATA / "salesData.js").write_text(header + body + ";\n" + SALES_DATA_TAIL, encoding="utf-8")


def _write_history_json(series_by_id: dict[str, list[dict]], products: list[Product]) -> None:
    data = {}
    for product in products:
        data[product.product_id] = {
            "product_id": product.product_id,
            "product_name": product.product_name,
            "industry": product.industry,
            "address": SYNTHETIC_ADDRESS,
            "data": series_by_id[product.product_id],
        }
    WEB_PUBLIC_DATA.mkdir(parents=True, exist_ok=True)
    (WEB_PUBLIC_DATA / "products_history_data.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _write_sample_csvs(series_by_id: dict[str, list[dict]], products: list[Product]) -> None:
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    by_id = {product.product_id: product for product in products}
    # One representative product per industry plus a second bakery product.
    for product_id in ("001_01", "002_01", "006_01", "005_01", "003_01", "007_01"):
        product = by_id[product_id]
        lines = [
            f"行业：{product.industry}  地址：{SYNTHETIC_ADDRESS}  "
            f"商品名称：{product.product_name}  商品ID：{product.product_id}",
            "日期,平均售价,销量,日平均气温,节假日,打折",
        ]
        for row in series_by_id[product_id]:
            lines.append(
                f"{row['date']} 00:00:00,{row['avg_price']:.2f},{row['sales']},"
                f"{row['temperature']:.1f},{'是' if row['is_holiday'] else '否'},"
                f"{'是' if row['is_discount'] else '否'}"
            )
        (SAMPLE_DIR / f"{product_id}.csv").write_text("\n".join(lines) + "\n", encoding="utf-8-sig")


def _write_boxplots(series_by_id: dict[str, list[dict]], products: list[Product]) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover - optional dependency
        print(f"[skip] matplotlib unavailable, keeping existing boxplots: {exc}")
        return

    BOXPLOT_DIR.mkdir(parents=True, exist_ok=True)
    prefixes = {
        "烘焙行业": ("bakery", "Bakery"),
        "餐饮行业": ("catering", "Catering"),
        "茶饮行业": ("tea", "Tea & Coffee"),
    }
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": "#d1d5db",
        "axes.grid": True,
        "grid.color": "#e5e7eb",
        "grid.linewidth": 0.8,
        "font.size": 10,
    })

    for industry, (prefix, label) in prefixes.items():
        industry_products = [p for p in products if p.industry == industry]
        labels = [p.product_id for p in industry_products]
        values = [
            [math.log1p(row["sales"]) for row in series_by_id[p.product_id]]
            for p in industry_products
        ]

        fig, ax = plt.subplots(figsize=(12, 5.2))
        ax.boxplot(values, patch_artist=True, boxprops={"facecolor": "#a8d5d0", "edgecolor": "#4b6b68"},
                   medianprops={"color": "#1f2937", "linewidth": 1.4})
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
        ax.set_xlabel("Product ID")
        ax.set_ylabel("log(1 + daily sales)")
        ax.set_title(f"Synthetic demo · {label} daily sales distribution")
        fig.tight_layout()
        fig.savefig(BOXPLOT_DIR / f"{prefix}_sales.png", dpi=120)
        plt.close(fig)

        holiday = [row["sales"] for p in industry_products for row in series_by_id[p.product_id] if row["is_holiday"]]
        normal = [row["sales"] for p in industry_products for row in series_by_id[p.product_id] if not row["is_holiday"]]
        fig, ax = plt.subplots(figsize=(7, 5.2))
        ax.boxplot([normal, holiday], patch_artist=True, widths=0.5,
                   boxprops={"facecolor": "#a8d5d0", "edgecolor": "#4b6b68"},
                   medianprops={"color": "#1f2937", "linewidth": 1.4})
        ax.set_xticklabels(["Normal days", "Holidays"])
        ax.set_ylabel("Daily sales")
        ax.set_title(f"Synthetic demo · {label} holiday effect")
        fig.tight_layout()
        fig.savefig(BOXPLOT_DIR / f"{prefix}_holiday.png", dpi=120)
        plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic demo data.")
    parser.add_argument("--no-plots", action="store_true", help="Skip PNG boxplot generation.")
    args = parser.parse_args()

    products = _make_products()
    rng = random.Random(SEED)
    series_by_id = {product.product_id: _generate_series(product, rng) for product in products}

    WEB_DATA.mkdir(parents=True, exist_ok=True)
    _write_products_js(products)
    _write_sales_data_js(series_by_id, products)
    _write_history_json(series_by_id, products)
    _write_sample_csvs(series_by_id, products)
    if not args.no_plots:
        _write_boxplots(series_by_id, products)

    print(f"Generated {len(products)} synthetic products × {DAYS} days.")
    print(f"  {WEB_DATA / 'products.js'}")
    print(f"  {WEB_DATA / 'salesData.js'}")
    print(f"  {WEB_PUBLIC_DATA / 'products_history_data.json'}")
    print(f"  {SAMPLE_DIR}/*.csv")
    if not args.no_plots:
        print(f"  {BOXPLOT_DIR}/*.png")


if __name__ == "__main__":
    main()

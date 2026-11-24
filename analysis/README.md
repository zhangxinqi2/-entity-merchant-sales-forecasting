# 分析脚本 / Analysis

本目录只保留与数据无关、可复用的评测工具。原始项目中依赖比赛 Excel 和本机绝对路径的分析脚本没有公开，以免泄露数据或产生无法运行的路径。

## `evaluate.py`

计算销量预测常用的指标：

- **WMAPE**（加权平均绝对百分比误差）
- **MAPE**（平均绝对百分比误差）
- **SMAPE**（对称平均绝对百分比误差）
- **MAE**、**RMSE**

### 用法

单个 CSV，包含 `actual` 和 `predicted` 两列：

```bash
python analysis/evaluate.py --input predictions.csv
```

两个对齐的 CSV：

```bash
python analysis/evaluate.py --actual actual.csv --prediction pred.csv
```

输出 JSON：

```bash
python analysis/evaluate.py --input predictions.csv --json
```

自检：

```bash
python analysis/evaluate.py --self-test
```

### 指标定义

```text
WMAPE = Σ|y_true - y_pred| / Σ|y_true| × 100%
MAPE  = mean(|y_true - y_pred| / |y_true|) × 100%
SMAPE = mean(2|y_true - y_pred| / (|y_true| + |y_pred|)) × 100%
MAE   = mean(|y_true - y_pred|)
RMSE  = sqrt(mean((y_true - y_pred)^2))
```

## 滚动回测方法

平台中的模型对比使用滚动窗口回测：对每个商品，用前 N 天预测接下来的 H 天，窗口向前滚动，最后汇总所有窗口的 WMAPE。复现时建议：

1. 按商品 ID 和日期排序；
2. 固定 `horizon`（例如 7 天）和 `step`（例如 1 天）；
3. 每个窗口只使用窗口之前的数据；
4. 汇总时按真实销量加权，而不是简单平均各窗口的百分比误差。

`analysis/evaluate.py` 可以直接对回测产出的 `actual/predicted` 明细计算汇总指标。

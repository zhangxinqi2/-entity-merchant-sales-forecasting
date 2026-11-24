# 数据格式 / Data Format

## 1. 单商品 CSV（预测引擎输入）

每行一条日销量记录。文件前两行是元信息和表头：

```csv
行业：烘焙行业  地址：示例市 · 演示商圈（合成数据）  商品名称：黄油可颂  商品ID：001_01
日期,平均售价,销量,日平均气温,节假日,打折
2025-01-01 00:00:00,18.20,120,15.1,否,是
2025-01-02 00:00:00,17.80,131,15.4,否,否
```

### 第一行元信息

用 **两个或更多空格** 分隔，键值之间用中文或英文冒号：

| 键 | 必填 | 说明 |
|----|------|------|
| `行业` | 否 | 烘焙行业 / 餐饮行业 / 茶饮行业等 |
| `地址` | 否 | 门店地址；公开仓库中请使用合成地址 |
| `商品名称` | 否 | 商品名；公开仓库中请使用合成名称 |
| `商品ID` | 是 | 唯一 ID，建议 `门店编号_商品编号`，如 `001_01` |

### 表头与字段

| 字段 | 类型 | 说明 |
|------|------|------|
| 日期 | string | `YYYY-MM-DD` 或 `YYYY-MM-DD HH:MM:SS` |
| 平均售价 | float | 当日平均售价 |
| 销量 | int | 当日销量，必须 >= 0 |
| 日平均气温 | float | 摄氏度 |
| 节假日 | string | `是` / `否` |
| 打折 | string | `是` / `否` |

### 编码

推荐 UTF-8（带或不带 BOM 均可）。`scripts/build_history_json.py` 会自动处理 BOM。

## 2. 前端历史数据 JSON

路径：`web/public/data/products_history_data.json`

```json
{
  "001_01": {
    "product_id": "001_01",
    "product_name": "黄油可颂",
    "industry": "烘焙行业",
    "address": "示例市 · 演示商圈（合成数据）",
    "data": [
      {
        "date": "2025-01-01",
        "avg_price": 18.2,
        "sales": 120,
        "temperature": 15.1,
        "is_holiday": false,
        "is_discount": true
      }
    ]
  }
}
```

前端页面使用：

- `ProductDetail`：读取 `data` 中的 `date`、`sales`、`temperature`、`avg_price`；
- `Inventory`：读取 `data` 中的 `date`、`sales`、`is_holiday`；
- `DataManagement`：读取商品元信息和表格行。

## 3. 前端商品列表

路径：`web/src/data/products.js`

```js
export const products = [
  {
    product_id: '001_01',
    product_name: '黄油可颂',
    industry: '烘焙行业',
    address: '示例市 · 演示商圈（合成数据）'
  }
]
```

由 `scripts/generate_sample_data.py` 生成。若要导入自己的数据，建议同时更新这个文件和
`products_history_data.json`，或者修改 `DataManagement` 页面从 API 读取。

## 4. 前端时序数据

路径：`web/src/data/salesData.js`

```js
export const realSalesData = {
  '001_01': {
    product_id: '001_01',
    product_name: '黄油可颂',
    time_series: [
      { date: '2025-01-01', sales: 120, temperature: 15.1 }
    ]
  }
}
```

> 文件名保留了 `realSalesData` 以兼容现有组件，但内容已全部替换为合成数据。

## 5. 模型对比数据

路径：`web/src/data/models.js`

包含：

- `models`：模型名称、发布方、简介、排名、聚合 WMAPE；
- `backtestResults`：滚动窗口回测的聚合结果。

这些是**聚合指标**，不含商家级明细。新增模型时，请同步更新该文件。

## 6. 预测结果 CSV（评测输入）

`analysis/evaluate.py --input` 接受：

```csv
date,actual,predicted
2025-01-01,120,117
2025-01-02,131,128
```

也支持两个对齐的 CSV：

```bash
python analysis/evaluate.py --actual actual.csv --prediction pred.csv
```

默认读取各自第一列，可用 `--actual-column` / `--prediction-column` 指定列名。

## 7. 数据脱敏检查清单

公开演示前至少完成：

- [ ] 删除或替换真实门店名称、地址、经纬度；
- [ ] 删除或替换真实商品名称（如果商品名可反向识别商家）；
- [ ] 删除手机号、订单号、会员 ID、支付信息；
- [ ] 检查日期是否可识别具体商家（必要时整体平移日期）；
- [ ] 检查 CSV 第一行元信息；
- [ ] 确认你有权公开数据；
- [ ] 不要把原始 Excel/Word/PPT/PDF 提交到仓库。

仓库的 `.gitignore` 已默认忽略 `data/raw/`、`*.xlsx`、`*.docx`、`*.pptx`、`*.pdf` 和模型权重，
但这只是最后一道防线，不能替代人工检查。

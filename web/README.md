# Web 仪表盘 / Web Dashboard

Vue 3 + Vite + Tailwind CSS + ECharts 实现的实体商家经营仪表盘。

## 开发

```bash
npm install
npm run dev
```

打开 <http://localhost:5174>。

## 构建

```bash
npm run build
npm run preview
```

GitHub Pages 子路径构建：

```bash
# PowerShell
$env:VITE_BASE = "/entity-merchant-sales-forecasting/"
npm run build

# bash
VITE_BASE=/entity-merchant-sales-forecasting/ npm run build
```

## 页面

| 路由 | 页面 |
|------|------|
| `#/` | 经营总览 |
| `#/product/:productId` | 商品详情 |
| `#/data-management` | 数据管理 |
| `#/model-calling` | 模型调用 |
| `#/model-detail` | 模型详情 |
| `#/inventory` | 库存预测 |
| `#/guide` | 使用指南 |

## 数据

所有演示数据均为合成数据：

- `src/data/products.js` — 商品列表
- `src/data/salesData.js` — 商品时序与模型指标
- `src/data/models.js` — 模型对比结果（聚合指标）
- `public/data/products_history_data.json` — 商品历史明细
- `public/images/boxplots/*.png` — 行业箱线图

重新生成：

```bash
cd ..
python scripts/generate_sample_data.py
```

导入自己的数据：

```bash
python scripts/build_history_json.py --input-dir data/raw
```

## 目录

```text
web/
├── src/
│   ├── components/       # Sidebar 等
│   ├── data/             # 演示数据
│   ├── router/           # hash 路由
│   ├── views/            # 页面
│   ├── App.vue
│   ├── main.js
│   └── style.css
├── public/
│   ├── data/
│   ├── images/boxplots/
│   └── favicon.svg
├── index.html
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## 说明

- 路由使用 `createWebHashHistory()`，静态托管无需服务端重写。
- 静态资源路径使用 `import.meta.env.BASE_URL`，兼容 GitHub Pages 子路径。
- 当前没有后端；数据管理页面的编辑只在前端内存中进行，刷新后恢复为演示数据。

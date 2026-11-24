# 部署指南 / Deployment

## 1. 本地开发

### Web

```bash
cd web
npm install
npm run dev
```

默认地址：<http://localhost:5174>。

### Python

```bash
cd forecasting
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
pip install -e .
```

## 2. 构建 Web

```bash
cd web
npm run build
npm run preview
```

产物在 `web/dist/`。

### GitHub Pages 子路径

GitHub Pages 的项目站点地址是：

```text
https://<username>.github.io/<repository>/
```

因此构建时必须设置 base：

```bash
# PowerShell
$env:VITE_BASE = "/entity-merchant-sales-forecasting/"
npm run build

# bash
VITE_BASE=/entity-merchant-sales-forecasting/ npm run build
```

仓库已包含 `.github/workflows/pages.yml`，会自动设置 `VITE_BASE` 为当前仓库名。

## 3. GitHub Pages 自动部署

1. 把代码推送到 GitHub 的 `main` 分支；
2. 打开仓库 **Settings → Pages**；
3. 在 **Build and deployment → Source** 选择 **GitHub Actions**；
4. 打开 **Actions** 标签，运行或等待 `Deploy Web Demo` 工作流；
5. 部署完成后访问：

   ```text
   https://zhangxinqi2.github.io/-entity-merchant-sales-forecasting/
   ```

如果仓库改名，工作流会自动使用新仓库名；本地构建时记得同步修改 `VITE_BASE`。

### 为什么使用 hash 路由

前端使用 `createWebHashHistory()`，URL 形如：

```text
https://zhangxinqi2.github.io/-entity-merchant-sales-forecasting/#/inventory
```

这样刷新页面或直接打开深层链接时，静态服务器不需要把未知路径重写到 `index.html`，
GitHub Pages、Netlify、Nginx 静态托管都能直接工作。

## 4. 部署到普通静态服务器（Nginx）

```nginx
server {
    listen 80;
    server_name example.com;

    root /var/www/entity-merchant-sales-forecasting;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /assets/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

即使使用 hash 路由，保留 `try_files` 也能兼容未来切换到 history 路由。

## 5. 部署到 Vercel / Netlify

- **Root directory**：`web`
- **Build command**：`npm run build`
- **Output directory**：`dist`
- **环境变量**：`VITE_BASE=/`（如果部署在域名根路径）

如果部署在子路径，把 `VITE_BASE` 设为对应前缀。

## 6. Python 预测引擎

预测引擎不是 Web 服务，通常以以下方式运行：

- 本地脚本 / 定时任务；
- Jupyter / 分析环境；
- 作为库集成到 FastAPI、Flask、Airflow 等系统；
- 批处理生成预测 CSV，再由前端读取。

如果要提供在线预测 API，建议新增 `backend/`：

```text
backend/
├── app.py            # FastAPI
├── requirements.txt
└── Dockerfile
```

并在前端把静态数据请求替换为 API 请求。

## 7. 模型权重

不要把模型权重提交到 Git。生产环境可以：

- 在服务器启动时运行 `python scripts/download_models.py`；
- 把模型放在对象存储（S3 / OSS / MinIO），启动时同步到本地；
- 使用环境变量 `CHRONOS2_MODEL_PATH`、`TIMESFM_MODEL_PATH`、`TIREX_MODEL_PATH` 指定路径。

## 8. 常见部署问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 页面空白、资源 404 | `VITE_BASE` 与部署路径不一致 | 设置正确的 `VITE_BASE` 后重新构建 |
| 刷新后 404 | 使用了 history 路由 | 本项目已使用 hash 路由；若改为 history，需要服务端回退到 `index.html` |
| `/data/products_history_data.json` 404 | 部署在子路径但使用了绝对路径 | 代码已使用 `import.meta.env.BASE_URL`，确认构建时 base 正确 |
| GitHub Pages 不更新 | Pages Source 未设为 GitHub Actions | 在 Settings → Pages 中切换 |
| 前端图表不显示 | 图片或 JSON 未包含在构建产物 | 确认 `web/public/` 下文件存在，重新构建 |
| 模型加载失败 | 权重未下载或路径错误 | 运行 `scripts/download_models.py`，检查环境变量 |
| CUDA 内存不足 | 模型较大 | 使用 `device='cpu'` 或更小的模型（TiRex） |

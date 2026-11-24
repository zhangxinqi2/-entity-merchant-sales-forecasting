# 贡献指南 / Contributing

感谢你愿意为「实体商家销量预测系统」做贡献！

## 行为准则

参与本项目即表示你同意遵守 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。

## 可以贡献什么

- 修复 Bug、改进文档、补充示例；
- 增加新的预测模型或评估指标；
- 改进前端交互、可访问性和响应式布局；
- 增加行业数据格式兼容性；
- 翻译文档（中英文）。

## 不能提交什么

**以下内容绝对不要提交到本仓库：**

- 真实商家名称、门店地址、销量、订单、手机号、身份证号等个人信息；
- 比赛数据、参赛承诺书、申报材料、答辩 PPT、研究报告原文；
- 模型权重、虚拟环境、`node_modules`、大型压缩包；
- API Key、Token、密码、私钥、`.env` 或 `.pypirc`；
- 任何你无权公开的第三方数据或代码。

如果你需要演示真实数据，请先做匿名化处理，并放在 `data/raw/`（该目录已被 `.gitignore` 忽略）。

## 开发环境

### Web 前端

```bash
cd web
npm install
npm run dev
npm run build
```

### Python 预测引擎

```bash
cd forecasting
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
python examples/01_basic_forecasting.py
```

### 合成数据

修改 `scripts/generate_sample_data.py` 后，请重新生成并提交输出：

```bash
python scripts/generate_sample_data.py
```

## 分支与提交

- 从 `main` 创建分支：`feat/xxx`、`fix/xxx`、`docs/xxx`、`chore/xxx`。
- 提交信息建议使用 [Conventional Commits](https://www.conventionalcommits.org/)：
  - `feat: add TimesFM batch prediction`
  - `fix: correct WMAPE denominator`
  - `docs: update data format`
- 一个 PR 尽量只做一件事。

## Pull Request 检查清单

- [ ] 代码可以在本地运行；
- [ ] 前端 `npm run build` 通过；
- [ ] Python 文件通过 `python -m compileall`；
- [ ] `python analysis/evaluate.py --self-test` 通过；
- [ ] 没有提交真实数据、密钥或大文件；
- [ ] 新功能附带文档或示例；
- [ ] 提交信息清晰。

## 代码风格

- Python：4 空格缩进，类型标注优先，函数保持小而清晰；
- JavaScript/Vue：2 空格缩进，组件使用 `<script setup>`；
- 文档：中文为主，关键术语保留英文；
- 不要提交格式化无关的大规模改动。

## 许可证

提交贡献即表示你同意你的贡献以 [Apache License 2.0](LICENSE) 授权。

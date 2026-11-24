# 常见问题 / FAQ

## 为什么仓库里没有真实商家数据？

真实销量、门店地址、商品名称和比赛数据涉及商家隐私、平台数据协议和比赛规则。公开仓库默认不包含这些内容。演示数据全部由 `scripts/generate_sample_data.py` 合成。

如果你要使用自己的数据：

1. 确认你有权使用和公开；
2. 做匿名化处理；
3. 放在 `data/raw/`（已被 `.gitignore` 忽略）；
4. 用 `scripts/build_history_json.py` 转换。

## 为什么没有模型权重？

Chronos-2、TimesFM-2.5、TiRex 的权重合计约 1.7 GB，且属于第三方发布物，不适合提交到 Git。请运行：

```bash
python scripts/download_models.py --model all
```

## 可以直接上传原来的 18 GB 压缩包吗？

不可以。GitHub 的限制：

- 单个文件最大 **100 MB**（普通 Git 推送）；
- 仓库建议保持在 **1 GB 以内**；
- GitHub Releases 单个附件最大 **2 GiB**；
- Git LFS 免费额度有限。

而且压缩包里包含虚拟环境、`node_modules`、模型权重、真实数据和比赛材料，既不应公开，也无法高效维护。正确做法是只提交源代码、文档和合成示例数据。

## 为什么 Web 没有后端？

当前版本是**静态演示**：数据以 JS/JSON 形式随构建产物发布，方便直接部署到 GitHub Pages。真实业务需要数据库、鉴权和在线推理，建议增加 FastAPI 后端，见 [架构说明](architecture.md#扩展为带后端的系统)。

## 为什么使用 hash 路由？

静态托管不需要服务端重写规则，刷新深层链接不会 404。URL 形如 `/#/inventory`。

## 为什么 `salesData.js` 里还叫 `realSalesData`？

为了兼容现有组件。内容已经全部替换为合成数据，文件头也有明确注释。后续可以重命名为 `demoSalesData`。

## 模型对比里的 WMAPE 为什么和论文/其他项目不一样？

- 数据不同：比赛数据、时间窗口、商品范围不同；
- 聚合方式不同：WMAPE 按销量加权，和简单平均 MAPE 不同；
- 模型配置不同：零样本、微调、特征工程都会影响结果；
- 前端里的数字是聚合展示，不构成对其他数据集的性能保证。

## 支持哪些模型？

预测引擎内置：

- Chronos-2（Amazon）
- TimesFM-2.5（Google）
- TiRex（NX-AI）

Web 演示还展示了 XGBoost、CatBoost、SARIMA、LSTM、PatchTST、ELPA 等基线模型的对比结果。

## 如何增加一个新模型？

1. 在 `forecasting/src/time_series_forecasting_zero/models/` 新增适配器；
2. 继承 `BaseForecaster`，实现 `load_model()` 和 `predict()`；
3. 在 `UnifiedForecaster` 中注册模型名；
4. 在 `web/src/data/models.js` 增加展示信息；
5. 补充示例和测试。

## Windows 上路径报错怎么办？

- 使用原始字符串：`r"D:\data\sales.csv"`；
- 或使用 `pathlib.Path`；
- 不要把本机绝对路径提交到仓库；
- 脚本默认使用相对于仓库根目录的路径。

## 没有 GPU 能运行吗？

可以。设置 `device='cpu'` 或 `--device cpu`。CPU 推理会慢一些；TiRex 相对轻量。Chronos-2 和 TimesFM-2.5 在 CPU 上也能运行，但需要足够内存。

## TiRex 可以直接商用吗？

TiRex 权重使用 **NXAI Community License Agreement**，不是 Apache-2.0。该许可证对商业使用有额外条款。商用前请阅读模型仓库中的 `LICENSE`，必要时联系 NX-AI。

## 如何引用本项目？

见 [CITATION.cff](../CITATION.cff)。GitHub 仓库页面右侧会显示 “Cite this repository”。

## 如何报告安全问题？

请不要公开提交 Issue，使用 GitHub 的私密漏洞报告渠道。详见 [SECURITY.md](../SECURITY.md)。

## 为什么仓库里没有截图中的真实数据？

截图使用合成数据生成，避免泄露商家信息。你可以在本地导入自己的数据后重新截图。

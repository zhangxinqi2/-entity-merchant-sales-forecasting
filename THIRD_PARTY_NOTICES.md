# 第三方许可证 / Third-Party Notices

本项目的代码使用 Apache-2.0 许可证。以下第三方组件、模型和依赖不受本项目许可证覆盖，
请分别遵守其原始许可证。

## 预训练模型

| 组件 | 发布方 | 许可证 | 链接 |
|------|--------|--------|------|
| Chronos-2 | Amazon | Apache-2.0 | <https://huggingface.co/amazon/chronos-2> |
| TimesFM-2.5 | Google Research | Apache-2.0 | <https://huggingface.co/google/timesfm-2.5-200m-pytorch> |
| TiRex | NX-AI | NXAI Community License Agreement | <https://huggingface.co/NX-AI/TiRex> |

**重要：** TiRex 使用 NXAI Community License，不是 Apache-2.0。该许可证对商业使用有额外条款，
下载、部署或商用前请阅读模型仓库中的 `LICENSE` 文件。本仓库不重新分发 TiRex 权重。

模型权重通过 `scripts/download_models.py` 从 ModelScope 或 Hugging Face 下载，下载后位于
`forecasting/models/`，该目录已被 `.gitignore` 忽略。

## Python 依赖

| 组件 | 许可证 |
|------|--------|
| PyTorch | BSD-3-Clause |
| pandas | BSD-3-Clause |
| NumPy | BSD-3-Clause |
| scikit-learn | BSD-3-Clause |
| SciPy | BSD-3-Clause |
| matplotlib | PSF-based / BSD-compatible |
| transformers | Apache-2.0 |
| chronos-forecasting | Apache-2.0 |
| statsmodels | BSD-3-Clause |
| loguru | MIT |
| tqdm | MPL-2.0 / MIT |
| PyYAML | MIT |
| python-dotenv | BSD-3-Clause |
| einops | MIT |
| accelerate | Apache-2.0 |

`tirex`、`xlstm` 等可选依赖的具体许可证以对应 PyPI / GitHub 仓库为准。

## 前端依赖

| 组件 | 许可证 |
|------|--------|
| Vue 3 | MIT |
| Vue Router | MIT |
| Pinia | MIT |
| Vite | MIT |
| Tailwind CSS | MIT |
| ECharts | Apache-2.0 |
| vue-echarts | MIT |
| axios | MIT |
| PostCSS | MIT |

## 数据集

本仓库不包含任何真实商家数据、比赛数据或第三方数据集。`data/sample/`、`web/src/data/` 和
`web/public/data/` 中的内容均由 `scripts/generate_sample_data.py` 合成。

## 图标与字体

界面图标使用内联 SVG，未引入第三方图标字体。系统字体由浏览器提供。

# 预训练模型 / Pretrained models

模型权重体积较大，**不提交到 Git 仓库**。请使用仓库根目录的下载脚本获取：

```bash
# 安装下载客户端（二选一）
pip install modelscope          # 默认来源
# pip install huggingface_hub   # 使用 --source huggingface 时

# 默认从 ModelScope 下载全部模型
python scripts/download_models.py --model all

# 只下载某一个
python scripts/download_models.py --model timesfm

# 使用 Hugging Face
python scripts/download_models.py --model all --source huggingface
```

下载完成后的目录结构：

```text
forecasting/models/
├── chronos-2/                    # Chronos-2 (Amazon), ~0.5 GB
├── timesfm-2.5-200m-pytorch/     # TimesFM-2.5-200M (Google), ~0.9 GB
└── tirex-model/                  # TiRex (NX-AI), ~0.3 GB
```

也可以通过环境变量指定模型路径（见 `forecasting/.env.example`）：

```bash
export CHRONOS2_MODEL_PATH=/path/to/chronos-2
export TIMESFM_MODEL_PATH=/path/to/timesfm-2.5-200m-pytorch
export TIREX_MODEL_PATH=/path/to/tirex-model
```

## 许可证提醒 / License notice

模型权重由第三方发布，**不受本仓库 Apache-2.0 许可证覆盖**：

| 模型 | 发布方 | 许可证 |
|------|--------|--------|
| Chronos-2 | Amazon | Apache-2.0 |
| TimesFM-2.5 | Google | Apache-2.0 |
| TiRex | NX-AI | NXAI Community License Agreement |

使用 TiRex 前请阅读其随模型附带的 `LICENSE` 文件，尤其是商业使用条款。本仓库只提供下载与调用代码，不重新分发模型权重。

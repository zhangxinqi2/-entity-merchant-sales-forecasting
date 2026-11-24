# 脚本 / Scripts

| 脚本 | 作用 |
|------|------|
| `generate_sample_data.py` | 生成合成示例数据（`web/src/data/`、`web/public/data/`、`data/sample/`、箱线图）。 |
| `build_history_json.py` | 把 `data/raw/` 下的单商品 CSV 转成前端使用的 `products_history_data.json`。 |
| `download_models.py` | 从 ModelScope 或 Hugging Face 下载 Chronos-2、TimesFM-2.5、TiRex 权重。 |

## 常用命令

```bash
# 重新生成合成演示数据（不会读取任何真实数据）
python scripts/generate_sample_data.py

# 导入你自己的单商品 CSV
python scripts/build_history_json.py --input-dir data/raw

# 查看可下载的模型
python scripts/download_models.py --list
```

> 模型权重不会被提交到仓库；下载后的目录已被 `.gitignore` 忽略。

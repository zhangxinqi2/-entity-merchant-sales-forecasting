# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-11-24

### Added

- Vue 3 + Vite + Tailwind CSS + ECharts business dashboard.
- Dashboard, data management, inventory forecasting, model calling, model detail,
  product detail, and user guide pages.
- Python forecasting engine (Chronos-2, TimesFM-2.5, TiRex) with a unified interface,
  CLI, examples, tests, and evaluation/visualization utilities.
- `analysis/evaluate.py` with WMAPE, MAPE, SMAPE, MAE, and RMSE.
- Synthetic demo data generator and sample CSV files.
- CSV-to-JSON converter for importing your own merchant data.
- Model download script for ModelScope and Hugging Face.
- GitHub Actions CI, GitHub Pages deployment, Dependabot, issue/PR templates.
- Architecture, data format, deployment, FAQ, and publishing documentation.

### Security

- Removed all real merchant data, store addresses, competition data, submission documents,
  model weights, virtual environments, and `node_modules` from the public repository.
- Added `.gitignore` rules for raw data, Excel/Word/PDF files, model weights, secrets, and logs.
- Replaced all demo data with deterministic synthetic data.

[1.0.0]: https://github.com/zhangxinqi2/-entity-merchant-sales-forecasting/releases/tag/v1.0.0

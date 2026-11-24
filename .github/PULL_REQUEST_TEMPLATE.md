## 变更说明

<!-- 这个 PR 做了什么？为什么需要？ -->

## 变更类型

- [ ] Bug 修复
- [ ] 新功能
- [ ] 文档
- [ ] 重构 / 性能
- [ ] 构建 / CI / 部署
- [ ] 其他

## 关联 Issue

Closes #

## 测试

<!-- 你运行了哪些命令？结果如何？ -->

```text
python analysis/evaluate.py --self-test
python -m compileall -q analysis scripts forecasting/src
cd web && npm run build
```

## 截图（如适用）

<!-- 前端改动请附截图。请使用合成数据，不要包含真实商家信息。 -->

## 检查清单

- [ ] 代码可以在本地运行
- [ ] 前端 `npm run build` 通过
- [ ] Python 文件通过 `compileall`
- [ ] `analysis/evaluate.py --self-test` 通过
- [ ] 没有提交真实商家数据、比赛材料、密钥或大文件
- [ ] 新功能附带文档或示例
- [ ] 已更新 `CHANGELOG.md`（如适用）

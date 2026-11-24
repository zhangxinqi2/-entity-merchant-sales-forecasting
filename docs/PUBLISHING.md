# 维护者发布指南：把项目开源到 GitHub

本指南假设仓库目录是：

```text
D:\Projects\entity-merchant-sales-forecasting
```

目标仓库：

```text
https://github.com/zhangxinqi2/-entity-merchant-sales-forecasting
```

---

## 0. 发布前检查（最重要）

### 0.1 确认没有敏感数据

```powershell
cd "D:\Projects\entity-merchant-sales-forecasting"

# 查看将要提交的文件
git status --short

# 检查是否包含真实地名、比赛材料、密钥等关键词
# 把 <真实地名>、<商家名> 替换成你项目里需要排查的词，例如城市名、门店名
git grep -n -I -E "<真实地名>|<商家名>|参赛者|承诺书|申报材料|api[_-]?key|secret|password|BEGIN .*PRIVATE KEY" -- .

# 检查是否有大文件（> 50 MB）
Get-ChildItem -Recurse -File | Where-Object { $_.Length -gt 50MB } |
  Select-Object @{n='MB';e={[math]::Round($_.Length/1MB,1)}}, FullName
```

预期结果：

- 没有 `data/raw/` 下的真实数据；
- 没有 `*.xlsx`、`*.docx`、`*.pptx`、`*.pdf` 比赛材料；
- 没有模型权重（`*.safetensors`、`*.ckpt`、`*.onnx`）；
- 没有 `.env`、`.pypirc`、私钥；
- 没有超过 100 MB 的文件。

> `.gitignore` 已经覆盖大部分情况，但发布前必须人工复核。

### 0.2 确认合成数据已生成

如果修改过 `scripts/generate_sample_data.py`，重新运行：

```powershell
python scripts/generate_sample_data.py
```

### 0.3 本地验证

```powershell
# Python 自检
python analysis/evaluate.py --self-test
python -m compileall -q analysis scripts forecasting/src

# Web 构建
cd web
npm install
npm run build
cd ..

# 可选：本地预览
cd web
npm run dev
```

打开 <http://localhost:5174>，确认页面和图表正常。

---

## 1. 安装并配置 Git

### 1.1 检查 Git

```powershell
git --version
```

如果没有安装，从 <https://git-scm.com/download/win> 下载安装。

### 1.2 配置提交身份

建议使用 GitHub 提供的 noreply 邮箱，避免公开真实邮箱：

```powershell
git config --global user.name "NOX"
git config --global user.email "你的GitHub数字ID+zhangxinqi2@users.noreply.github.com"
```

数字 ID 和 noreply 邮箱可以在 GitHub **Settings → Emails** 中找到。

---

## 2. 在 GitHub 上创建空仓库

### 方式 A：网页创建（推荐新手）

1. 打开 <https://github.com/new>；
2. **Repository name** 填 `entity-merchant-sales-forecasting`；
3. **Description** 填：

   ```text
   实体商家销量预测系统：Vue 3 经营仪表盘 + Chronos-2/TimesFM-2.5/TiRex 零样本预测引擎（已脱敏，含合成示例数据）
   ```

4. 选择 **Public**；
5. **不要**勾选 “Add a README file”、“Add .gitignore”、“Choose a license”；
   本地已经有这些文件，勾选会造成首次推送冲突；
6. 点击 **Create repository**。

创建后会看到一个 “quick setup” 页面，先不要按里面的命令操作，继续看下一步。

### 方式 B：GitHub CLI 一条命令

如果安装了 [GitHub CLI](https://cli.github.com/)：

```powershell
cd "D:\Projects\entity-merchant-sales-forecasting"
gh auth login          # 首次使用需要登录，按提示选择 GitHub.com / HTTPS / 浏览器
gh repo create zhangxinqi2/-entity-merchant-sales-forecasting `
  --public `
  --source . `
  --remote origin `
  --push `
  --description "实体商家销量预测系统：Vue 3 经营仪表盘 + Chronos-2/TimesFM-2.5/TiRex 零样本预测引擎（已脱敏，含合成示例数据）"
```

`--source . --push` 会直接初始化并推送当前目录。如果已经执行过 `git init` 但还没有提交，请先完成第 3 节的 `git commit`，否则没有内容可推送。

> 在 Claude Code 中需要交互式登录时，可以直接在输入框输入 `! gh auth login`，让命令在当前终端运行。

---

## 3. 初始化本地 Git 仓库并提交

如果使用方式 B 且已经推送成功，可以跳过本节。

```powershell
cd "D:\Projects\entity-merchant-sales-forecasting"

# 初始化 main 分支
git init -b main

# 查看状态，确认没有敏感文件
git status --short

# 添加到暂存区
git add .

# 再检查一次暂存内容
git status --short

# 首次提交
git commit -m "feat: initial open-source release"
```

### 如果 `git init -b main` 报错

旧版 Git 不支持 `-b`，改用：

```powershell
git init
git branch -M main
```

---

## 4. 关联远程仓库并推送

### 4.1 添加 remote

```powershell
git remote add origin https://github.com/zhangxinqi2/-entity-merchant-sales-forecasting.git
```

如果已经存在 remote，修改为：

```powershell
git remote set-url origin https://github.com/zhangxinqi2/-entity-merchant-sales-forecasting.git
```

检查：

```powershell
git remote -v
```

### 4.2 推送

```powershell
git push -u origin main
```

### 4.3 认证方式

首次推送会要求登录：

- **HTTPS + Git Credential Manager**：弹出浏览器登录 GitHub，授权后自动保存；
- **Personal Access Token（PAT）**：GitHub **Settings → Developer settings → Personal access tokens → Tokens (classic)**，勾选 `repo` 权限；推送时用户名填 GitHub 用户名，密码填 token；
- **SSH**：需要先生成 SSH key 并添加到 GitHub：

  ```powershell
  ssh-keygen -t ed25519 -C "你的邮箱"
  Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
  ```

  把输出的公钥添加到 GitHub **Settings → SSH and GPG keys**，然后把 remote 改为：

  ```powershell
  git remote set-url origin git@github.com:zhangxinqi2/-entity-merchant-sales-forecasting.git
  ```

> 不要把 PAT 写进仓库、脚本或 README。

---

## 5. 推送后的仓库设置

### 5.1 仓库描述和主题

网页操作：

- 仓库首页右上角 **About** → 齿轮图标；
- **Description** 填上面的中文描述；
- **Website** 填 GitHub Pages 地址（部署后）：
  `https://zhangxinqi2.github.io/-entity-merchant-sales-forecasting/`
- **Topics** 添加：

  ```text
  time-series
  forecasting
  sales-forecasting
  retail
  vue
  vite
  echarts
  tailwindcss
  python
  pytorch
  chronos
  timesfm
  tirex
  dashboard
  business-intelligence
  ```

或者用 `gh`：

```powershell
gh repo edit zhangxinqi2/-entity-merchant-sales-forecasting `
  --description "实体商家销量预测系统：Vue 3 经营仪表盘 + Chronos-2/TimesFM-2.5/TiRex 零样本预测引擎（已脱敏，含合成示例数据）" `
  --add-topic time-series `
  --add-topic forecasting `
  --add-topic sales-forecasting `
  --add-topic retail `
  --add-topic vue `
  --add-topic vite `
  --add-topic echarts `
  --add-topic tailwindcss `
  --add-topic python `
  --add-topic pytorch `
  --add-topic chronos `
  --add-topic timesfm `
  --add-topic tirex `
  --add-topic dashboard `
  --add-topic business-intelligence
```

### 5.2 开启 Issues 和 Discussions

**Settings → General → Features**：

- ✅ Issues
- ✅ Discussions（可选，但推荐）
- ✅ Projects（可选）

### 5.3 开启 GitHub Pages

1. **Settings → Pages**；
2. **Build and deployment → Source** 选择 **GitHub Actions**；
3. 打开 **Actions** 标签，等待 `Deploy Web Demo` 完成；
4. 访问：

   ```text
   https://zhangxinqi2.github.io/-entity-merchant-sales-forecasting/
   ```

如果 Actions 没有自动运行，手动触发：

```powershell
gh workflow run "Deploy Web Demo"
```

> 如果 `Deploy Web Demo` 报 `Resource not accessible by integration`，说明 Pages 还没有启用。
> `GITHUB_TOKEN` 不能替你创建 Pages 站点，必须先在 **Settings → Pages** 把 Source 设为
> **GitHub Actions**，然后重新运行工作流。

### 5.4 设置社交预览图

**Settings → General → Social preview**，上传：

```text
docs/screenshots/dashboard.png
```

这样分享仓库链接时会显示项目截图。

### 5.5 分支保护

**Settings → Branches → Add branch ruleset**（或 Add rule）：

- Branch name pattern：`main`
- ✅ Require a pull request before merging
- ✅ Require status checks to pass（选择 CI 的 `python` 和 `web` job）
- ✅ Require branches to be up to date before merging
- ✅ Do not allow force pushes
- ✅ Do not allow deletions

### 5.6 安全设置

**Settings → Code security and analysis**：

- ✅ Dependency graph
- ✅ Dependabot alerts
- ✅ Dependabot security updates
- ✅ Secret scanning
- ✅ Push protection（如果可用）
- ✅ CodeQL analysis（可选）

仓库已包含 `.github/dependabot.yml`，会每周检查 npm、pip 和 GitHub Actions 更新。

### 5.7 创建第一个 Release

网页操作：

1. 仓库右侧 **Releases → Create a new release**；
2. Tag：`v1.0.0`；
3. Target：`main`；
4. Title：`v1.0.0 — Initial open-source release`；
5. 描述可以复制 `CHANGELOG.md` 的 1.0.0 部分；
6. 发布。

或者用 `gh`：

```powershell
gh release create v1.0.0 `
  --title "v1.0.0 — Initial open-source release" `
  --notes-file CHANGELOG.md
```

> 不要在这里上传 18 GB 压缩包或模型权重。Release 单个附件上限是 2 GiB，而且真实数据不应公开。

### 5.8 固定到个人主页

在 GitHub 个人主页，点击 **Customize your pins**，把 `entity-merchant-sales-forecasting` 固定到最前面。

---

## 6. 发布后验证

### 6.1 检查仓库内容

在 GitHub 网页上确认：

- [ ] README 正常渲染，图片和 Mermaid 图显示；
- [ ] License 显示 **Apache-2.0**；
- [ ] 没有 `venv/`、`node_modules/`、模型权重、真实数据；
- [ ] `docs/screenshots/` 图片存在；
- [ ] Actions 的 CI 和 Pages 都是绿色；
- [ ] Pages 页面可以打开，路由和图表正常；
- [ ] Release `v1.0.0` 已创建；
- [ ] Topics 已添加；
- [ ] 社交预览图已设置。

### 6.2 本地检查已提交文件

```powershell
cd "D:\Projects\entity-merchant-sales-forecasting"

# 已跟踪文件数量
(git ls-files | Measure-Object -Line).Lines

# 最大的已跟踪文件
git ls-files | ForEach-Object {
  $item = Get-Item -LiteralPath $_
  [pscustomobject]@{ MB = [math]::Round($item.Length/1MB, 2); Path = $_ }
} | Sort-Object MB -Descending | Select-Object -First 20

# 仓库对象大小
git count-objects -vH
```

### 6.3 检查敏感关键词

```powershell
git grep -n -I -E "<真实地名>|<商家名>|参赛者|承诺书|申报材料|api[_-]?key|secret|password" -- .
```

如果命中，确认是否为无害的文档说明；如果是真实数据或密钥，按下一节处理。

---

## 7. 如果误提交了敏感数据或大文件

### 7.1 还没有推送

```powershell
# 取消暂存
git restore --staged .

# 删除误加的文件（确认路径后）
Remove-Item -LiteralPath "path\to\secret.xlsx" -Force

# 或修改最近一次提交
git add .
git commit --amend
```

### 7.2 已经推送

**删除文件再提交一次是不够的**，Git 历史里仍然保留。处理步骤：

1. 立即删除 GitHub 上的仓库（Settings → Danger Zone → Delete this repository），或者用
   `git filter-repo` / BFG 清理历史后强制推送；
2. 轮换所有可能泄露的密钥、Token、密码；
3. 如果涉及个人数据，评估是否需要通知相关方；
4. 重新创建一个干净的仓库并推送。

推荐使用 `git filter-repo`：

```powershell
pip install git-filter-repo

# 删除某个文件/目录的全部历史
git filter-repo --path "data/raw" --invert-paths

# 强制推送（确认已清理后）
git push --force --all
git push --force --tags
```

如果仓库刚创建、还没有其他人协作，最干净的做法是直接删除仓库，修复本地目录后重新创建并推送。

---

## 8. 常见推送错误

### `remote: error: File ... is 123.00 MB; this exceeds GitHub's file size limit of 100.00 MB`

原因：提交了超过 100 MB 的文件。

解决：

```powershell
# 找到大文件
git ls-files | ForEach-Object {
  $item = Get-Item -LiteralPath $_
  [pscustomobject]@{ MB = [math]::Round($item.Length/1MB, 2); Path = $_ }
} | Sort-Object MB -Descending | Select-Object -First 20

# 从历史中移除
git filter-repo --path "path/to/large-file" --invert-paths
```

然后把该文件加入 `.gitignore`，重新提交。

### `failed to push some refs` / `non-fast-forward`

原因：远程仓库有本地没有的提交（例如创建时勾选了 README）。

解决：

```powershell
git pull --rebase origin main
git push -u origin main
```

或者删除远程仓库重新创建（推荐，避免合并无关历史）。

### `Authentication failed`

- 检查 PAT 是否过期、是否有 `repo` 权限；
- 检查是否启用了双重认证；
- 使用 Git Credential Manager 重新登录；
- 或改用 SSH。

### Pages 显示 404

- 确认 **Settings → Pages → Source** 是 **GitHub Actions**；
- 确认 `Deploy Web Demo` 工作流成功；
- 确认构建时 `VITE_BASE` 是 `/<仓库名>/`；
- 等待 1–2 分钟，Pages 部署有缓存。

### README 图片不显示

- 图片路径必须是仓库内相对路径，例如 `docs/screenshots/dashboard.png`；
- 不要使用本机绝对路径 `D:\...`；
- 文件名大小写要与仓库一致（GitHub 区分大小写）。

---

## 9. GitHub 限制速查

| 项目 | 限制 |
|------|------|
| 单个文件（普通 Git） | 100 MB |
| 仓库建议大小 | < 1 GB |
| Git LFS 免费额度 | 1 GiB 存储 + 1 GiB/月流量（可能变化） |
| Release 单个附件 | 2 GiB |
| Release 附件总大小 | 无硬性小上限，但建议按需上传 |
| Pages 站点大小 | 1 GB |
| Pages 每月流量 | 100 GB（软限制） |
| Actions 公共仓库 | 免费分钟数较充足，具体以 GitHub 文档为准 |

因此：

- **不要**上传 18 GB 压缩包；
- **不要**把模型权重提交到 Git；
- 需要分发大文件时，优先让用户运行下载脚本，或使用 Release + 外部对象存储。

---

## 10. 后续维护

### 每次发版

```powershell
# 1. 更新 CHANGELOG.md 和版本号
# 2. 提交
git add .
git commit -m "chore: release v1.0.1"
git push

# 3. 打标签
git tag v1.0.1
git push origin v1.0.1

# 4. 创建 Release
gh release create v1.0.1 --title "v1.0.1" --notes-file CHANGELOG.md
```

### 处理 Dependabot PR

1. 查看 CI 是否通过；
2. 本地 `npm install` / `pip install` 验证；
3. 合并后删除分支。

### 更新截图

```powershell
cd web
npm run dev
# 用浏览器截图，保存到 docs/screenshots/
```

### 接受贡献

1. 确认 PR 没有包含真实数据或密钥；
2. 确认 CI 通过；
3.  squash merge 到 `main`；
4. 在 `CHANGELOG.md` 记录。

---

## 11. 最终检查清单

发布前：

- [ ] 真实数据、比赛材料、申报材料已全部移除；
- [ ] `data/raw/` 为空或被忽略；
- [ ] 没有模型权重、`venv/`、`node_modules/`、压缩包；
- [ ] 没有 `.env`、`.pypirc`、私钥、PAT；
- [ ] `python analysis/evaluate.py --self-test` 通过；
- [ ] `npm run build` 通过；
- [ ] README、LICENSE、NOTICE、THIRD_PARTY_NOTICES 完整；
- [ ] 合成数据已重新生成；
- [ ] `git status` 干净。

发布后：

- [ ] GitHub 仓库为 Public；
- [ ] License 显示 Apache-2.0；
- [ ] Topics、Description、Website 已填写；
- [ ] Issues / Discussions 已开启；
- [ ] Pages 部署成功；
- [ ] Release v1.0.0 已创建；
- [ ] 社交预览图已设置；
- [ ] 分支保护已开启；
- [ ] Dependabot / Secret scanning 已开启；
- [ ] 把仓库 pin 到个人主页。

---

完成以上步骤后，你的项目就正式开源了。🎉

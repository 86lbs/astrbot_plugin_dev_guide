# AstrBot 插件发布指南

本文档说明插件的各种发布方式和所需认证。

---

## 📋 发布场景对比

| 场景 | 是否需要 Token | 说明 |
|------|----------------|------|
| 本地测试 | ❌ 不需要 | 直接复制到 `data/plugins/` |
| GitHub 发布 | ✅ 需要 | 需要 GitHub Personal Access Token |
| AstrBot 插件市场 | ✅ 需要 | 需要提交 PR 到官方仓库 |
| 分享给他人 | ❌ 不需要 | 打包成 zip 发送 |

---

## 🚀 方式一：本地测试（无需 Token）

```bash
# 直接复制到插件目录
cp -r /workspace/my_plugin /opt/astrbot/data/plugins/

# 重启 AstrBot
./tools/start_astrbot.sh
```

**适用场景**：开发测试阶段

---

## 📦 方式二：打包分享（无需 Token）

```bash
# 打包插件
cd /workspace
zip -r my_plugin.zip my_plugin/

# 分享给他人
# 对方通过 WebUI 上传安装
```

**安装方式**：
1. 打开 AstrBot WebUI
2. 进入「插件管理」
3. 点击「上传安装」
4. 选择 zip 文件

---

## 🔐 方式三：发布到 GitHub（需要 Token）

### 1. 创建 GitHub Token

1. 登录 GitHub → Settings → Developer settings → Personal access tokens
2. 点击「Generate new token (classic)」
3. 勾选权限：
   - `repo`（完整仓库访问）
4. 生成并保存 Token

### 2. 创建仓库并推送

```bash
# 创建仓库
git init
git add .
git commit -m "Initial commit: my_plugin v1.0.0"

# 推送到 GitHub（需要 Token）
git remote add origin https://github.com/your_name/my_plugin.git
git push -u origin main

# 或使用 Token
git remote add origin https://<TOKEN>@github.com/your_name/my_plugin.git
git push -u origin main
```

### 3. 创建 Release

```bash
# 创建标签
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

然后在 GitHub 页面创建 Release。

### 4. 安装方式

用户可以通过以下方式安装：

```bash
# 方式一：WebUI 安装
# 在 WebUI 中输入仓库地址：https://github.com/your_name/my_plugin

# 方式二：API 安装
curl -X POST http://localhost:6185/api/plugin/install \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/your_name/my_plugin"}'
```

---

## 🏪 方式四：发布到 AstrBot 插件市场（需要 PR）

### 插件市场机制

AstrBot 插件市场是一个 JSON 文件，由官方维护：
- 主源：`https://api.soulter.top/astrbot/plugins`
- 备用源：`https://github.com/AstrBotDevs/AstrBot_Plugins_Collection`

### 发布步骤

1. **确保插件已发布到 GitHub**

2. **提交 PR 到官方仓库**

   仓库地址：https://github.com/AstrBotDevs/AstrBot_Plugins_Collection

3. **PR 内容格式**

   在 `plugins.json` 中添加：

   ```json
   {
     "name": "my_plugin",
     "author": "your_name",
     "desc": "插件描述",
     "repo": "https://github.com/your_name/my_plugin",
     "version": "1.0.0",
     "tags": ["工具", "天气"]
   }
   ```

4. **等待审核合并**

### 审核要求

- ✅ 插件功能完整
- ✅ 有完整的 `metadata.yaml`
- ✅ 有 `README.md` 说明文档
- ✅ 有 `CHANGELOG.md` 更新日志
- ✅ 代码质量良好
- ✅ 无恶意代码

---

## 🤖 Agent 自动化发布

### GitHub 发布脚本

```bash
#!/bin/bash
# publish_to_github.sh

PLUGIN_DIR=$1
PLUGIN_NAME=$(basename $PLUGIN_DIR)
GITHUB_TOKEN=$2

if [ -z "$GITHUB_TOKEN" ]; then
    echo "需要 GitHub Token"
    exit 1
fi

cd $PLUGIN_DIR

# 初始化 Git
git init
git add .
git commit -m "Initial commit: $PLUGIN_NAME v1.0.0"

# 创建远程仓库（需要 GitHub API）
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d "{\"name\":\"$PLUGIN_NAME\",\"description\":\"AstrBot plugin\"}"

# 推送
git remote add origin https://$GITHUB_TOKEN@github.com/$(git config user.name)/$PLUGIN_NAME.git
git push -u origin main

# 创建 Release
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

echo "发布成功！"
```

### 使用方式

```bash
./publish_to_github.sh /workspace/my_plugin ghp_xxxxx
```

---

## 📊 发布流程图

```
开发完成
    │
    ├──▶ 本地测试（无需 Token）
    │        └── 复制到 data/plugins/
    │
    ├──▶ 打包分享（无需 Token）
    │        └── zip → 发给他人 → WebUI 上传安装
    │
    ├──▶ GitHub 发布（需要 Token）
    │        └── git push → 创建 Release → 用户通过 URL 安装
    │
    └──▶ 插件市场（需要 PR）
             └── GitHub 发布 → 提交 PR → 审核合并 → 市场可见
```

---

## 🔑 Token 安全提示

| 安全措施 | 说明 |
|----------|------|
| ❌ 不要硬编码 | 不要把 Token 写在代码里 |
| ✅ 使用环境变量 | `export GITHUB_TOKEN=xxx` |
| ✅ 定期更换 | 定期更新 Token |
| ✅ 最小权限 | 只勾选必要的权限 |
| ✅ 不要分享 | Token 相当于密码 |

---

## 📝 Agent 提示词补充

```markdown
## 插件发布说明

开发完成后，插件可以通过以下方式分发：

1. **本地测试**：直接复制到 `data/plugins/` 目录
2. **打包分享**：打包成 zip，通过 WebUI 上传安装
3. **GitHub 发布**：推送到 GitHub，用户通过仓库 URL 安装
4. **插件市场**：提交 PR 到官方仓库

### 交付内容
每次交付插件时，提供：
- 完整的插件文件
- 安装说明
- （可选）GitHub 发布命令
```

# AstrBot 插件发布指南

本文档说明插件的各种发布方式和所需认证。

---

## 📋 发布场景对比

| 场景 | 是否需要 Token | 说明 |
|------|----------------|------|
| 本地测试 | ❌ 不需要 | 直接复制到 `data/plugins/` |
| GitHub 发布 | ✅ 需要 | 需要 GitHub Personal Access Token |
| AstrBot 插件市场 | ❌ 不需要 | 通过 Issue 申请上架 |
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

## 🏪 方式四：上架到 AstrBot 插件市场（通过 Issue）

### 插件市场机制

AstrBot 插件市场是一个 JSON 文件，由官方维护：
- 主源：`https://api.soulter.top/astrbot/plugins`
- 备用源：`https://github.com/AstrBotDevs/AstrBot_Plugins_Collection`

**重要**：插件市场直接下载仓库源码，不需要创建 Release！

### 上架步骤

1. **确保插件已发布到 GitHub**
   - 插件仓库必须有完整的 `metadata.yaml`
   - 仓库中必须包含所有必要文件

2. **提交 Issue 申请上架**

   地址：https://github.com/AstrBotDevs/AstrBot/issues/new

3. **Issue 标题格式**

   ```
   [Plugin] 插件名称
   ```

4. **Issue 内容模板**

   ```markdown
   ### 插件信息

   ```json
   {
     "name": "my_plugin",
     "display_name": "插件显示名称",
     "desc": "插件功能描述",
     "author": "your_name",
     "repo": "https://github.com/your_name/my_plugin",
     "tags": ["标签1", "标签2", "标签3"],
     "social_link": "https://github.com/your_name"
   }
   ```

   ### 插件检查清单

   - [x] 我的插件经过完整的测试
   - [x] 我的插件不包含恶意代码
   - [x] 我已阅读并同意遵守该项目的 [行为准则](https://docs.github.com/zh/site-policy/github-terms/github-community-code-of-conduct)。
   ```

5. **等待审核**

   - 自动审核机器人会进行初步代码审核
   - 官方维护者会进行人工审核

### 仓库文件要求

**必须包含的文件**：
```
my_plugin/
├── main.py              # 主代码
├── metadata.yaml        # 元数据
├── CHANGELOG.md         # 更新日志
└── README.md            # 使用说明
```

**可选文件**：
```
└── _conf_schema.json    # 配置 Schema（如需要）
```

**注意**：用户安装时直接下载仓库源码，确保仓库中的文件完整！

### 插件信息字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | ✅ | 插件唯一标识（英文，下划线分隔） |
| `display_name` | ✅ | 插件显示名称（中文） |
| `desc` | ✅ | 插件功能描述 |
| `author` | ✅ | 作者名称 |
| `repo` | ✅ | GitHub 仓库地址 |
| `tags` | ✅ | 标签数组 |
| `social_link` | ❌ | 社交链接（如 GitHub 主页） |

### 审核要求

- ✅ 插件功能完整
- ✅ 有完整的 `metadata.yaml`
- ✅ 有 `README.md` 说明文档
- ✅ 有 `CHANGELOG.md` 更新日志
- ✅ 已创建 GitHub Release
- ✅ 代码质量良好
- ✅ 无恶意代码

### 注意事项

- 不要直接提交 PR，只接受 Issue 申请
- 自动审核机器人会进行初步代码审核
- 审核通过后，官方会更新插件市场列表

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
    └──▶ 插件市场（通过 Issue）
             └── GitHub 发布 → 提交 Issue → 官方审核 → 市场可见
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

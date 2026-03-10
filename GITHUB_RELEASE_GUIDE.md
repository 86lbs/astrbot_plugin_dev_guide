# GitHub 发布指南

本文档详细说明如何使用 GitHub API 发布插件。

---

## ⚠️ 重要说明

**本地操作**：在你的工作目录中执行
- 创建文件
- 打包 zip
- git 命令（init, add, commit, push）

**远程操作**：通过 GitHub API 执行
- 创建仓库
- 创建 Release
- 上传文件到 Release

**不要混淆！**
- 本地创建文件 ≠ 远程仓库有文件
- 本地打包 zip ≠ Release 有 zip
- 必须通过 git push 和 API 上传才能同步到远程

---

## 📋 发布流程

### 1. 本地 - 创建插件文件

在本地工作目录创建插件文件：
```
/workspace/my_plugin/
├── main.py
├── metadata.yaml
├── CHANGELOG.md
├── README.md
└── _conf_schema.json（如需要）
```

---

### 2. 远程 - 创建 GitHub 仓库

```bash
curl -X POST \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d '{
    "name": "my_plugin",
    "description": "AstrBot 插件描述",
    "private": false
  }'
```

**响应示例：**
```json
{
  "id": 123456,
  "name": "my_plugin",
  "full_name": "username/my_plugin",
  "html_url": "https://github.com/username/my_plugin"
}
```

---

### 3. 本地 - 推送代码

```bash
# 初始化仓库
cd /path/to/plugin
git init
git add .
git commit -m "Initial commit: 插件描述"

# 设置远程仓库
git remote add origin https://github.com/username/my_plugin.git
git branch -M main
git push -u origin main
```

**使用 Token 认证推送：**
```bash
git remote set-url origin https://TOKEN@github.com/username/my_plugin.git
git push -u origin main
```

---

### 4. 本地 - 创建 Tag

```bash
# 创建本地 Tag
git tag v1.0.0

# 推送 Tag 到远程
git push origin v1.0.0
```

---

### 5. 远程 - 创建 Release

```bash
curl -X POST \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/username/my_plugin/releases \
  -d '{
    "tag_name": "v1.0.0",
    "name": "v1.0.0",
    "body": "## 更新内容\n\n- 初始版本发布\n- 功能描述...",
    "draft": false,
    "prerelease": false
  }'
```

**响应示例：**
```json
{
  "id": 12345678,
  "tag_name": "v1.0.0",
  "name": "v1.0.0",
  "html_url": "https://github.com/username/my_plugin/releases/tag/v1.0.0",
  "upload_url": "https://uploads.github.com/repos/username/my_plugin/releases/12345678/assets{?name,label}"
}
```

**重要：记录 `id` 和 `upload_url`，用于上传文件！**

---

### 6. 本地 - 打包插件

```bash
# 创建 zip 包
zip -r my_plugin.zip \
  main.py \
  metadata.yaml \
  CHANGELOG.md \
  README.md

# 如果有配置 Schema
zip -r my_plugin.zip \
  main.py \
  metadata.yaml \
  _conf_schema.json \
  CHANGELOG.md \
  README.md
```

---

### 7. 远程 - 上传发行版到 Release

```bash
# 使用 release_id 上传
curl -X POST \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Content-Type: application/zip" \
  --data-binary @my_plugin.zip \
  "https://uploads.github.com/repos/username/my_plugin/releases/RELEASE_ID/assets?name=my_plugin.zip"
```

**响应示例：**
```json
{
  "id": 87654321,
  "name": "my_plugin.zip",
  "content_type": "application/zip",
  "size": 12345,
  "browser_download_url": "https://github.com/username/my_plugin/releases/download/v1.0.0/my_plugin.zip"
}
```

---

## 🔄 Fork 模式发布

如果选择 Fork 后推送到自己的仓库：

### 1. 远程 - Fork 原仓库

```bash
curl -X POST \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/original_owner/original_plugin/forks
```

### 2. 本地 - 克隆并修改

```bash
git clone https://github.com/YOUR_USERNAME/original_plugin.git
cd original_plugin
# 修改代码
git add .
git commit -m "优化：描述修改内容"
git push origin main
```

### 3. 创建 Release（同上）

---

## 📝 完整示例

```bash
#!/bin/bash

# 配置
TOKEN="ghp_xxxxxxxxxxxx"
PLUGIN_NAME="my_plugin"
PLUGIN_DESC="AstrBot 插件"
USERNAME="your_username"

# 1. 远程 - 创建仓库
echo "创建仓库..."
curl -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d "{\"name\":\"$PLUGIN_NAME\",\"description\":\"$PLUGIN_DESC\"}"

# 2. 本地 - 推送代码
echo "推送代码..."
cd /path/to/plugin
git init
git add .
git commit -m "Initial commit"
git remote add origin https://$TOKEN@github.com/$USERNAME/$PLUGIN_NAME.git
git push -u origin main

# 3. 本地 - 创建 Tag
echo "创建 Tag..."
git tag v1.0.0
git push origin v1.0.0

# 4. 远程 - 创建 Release
echo "创建 Release..."
RESPONSE=$(curl -s -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/$USERNAME/$PLUGIN_NAME/releases \
  -d '{"tag_name":"v1.0.0","name":"v1.0.0","body":"初始版本"}')

RELEASE_ID=$(echo $RESPONSE | jq -r '.id')

# 5. 本地 - 打包
echo "打包..."
zip -r $PLUGIN_NAME.zip main.py metadata.yaml CHANGELOG.md README.md

# 6. 远程 - 上传到 Release
echo "上传..."
curl -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Content-Type: application/zip" \
  --data-binary @$PLUGIN_NAME.zip \
  "https://uploads.github.com/repos/$USERNAME/$PLUGIN_NAME/releases/$RELEASE_ID/assets?name=$PLUGIN_NAME.zip"

echo "发布完成！"
echo "仓库地址：https://github.com/$USERNAME/$PLUGIN_NAME"
echo "下载地址：https://github.com/$USERNAME/$PLUGIN_NAME/releases/download/v1.0.0/$PLUGIN_NAME.zip"
```

---

## ⚠️ 注意事项

1. **Token 权限**：需要 `repo` 权限
2. **Token 安全**：不要在日志中输出 Token
3. **Release ID**：创建 Release 后必须记录 ID，用于上传文件
4. **文件大小**：单个文件最大 2GB
5. **仓库名**：只能包含字母、数字、-、_

---

## 🔗 相关链接

- [GitHub API 文档](https://docs.github.com/en/rest)
- [GitHub Releases API](https://docs.github.com/en/rest/releases)
- [GitHub Upload API](https://docs.github.com/en/rest/releases/assets)

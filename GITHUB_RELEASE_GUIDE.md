# GitHub 发布指南

本文档详细说明如何使用 GitHub API 发布插件。

---

## ⚠️ 重要说明

**插件市场直接下载仓库源码，不需要创建 Release！**

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

echo "发布完成！"
echo "仓库地址：https://github.com/$USERNAME/$PLUGIN_NAME"
```

---

## ⚠️ 注意事项

1. **Token 权限**：需要 `repo` 权限
2. **Token 安全**：不要在日志中输出 Token
3. **文件完整**：确保仓库包含所有必要文件

---

## 🔗 相关链接

- [GitHub API 文档](https://docs.github.com/en/rest)
- [GitHub Repos API](https://docs.github.com/en/rest/repos/repos)

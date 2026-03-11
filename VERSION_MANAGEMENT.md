# AstrBot 插件版本管理指南

本文档说明如何为插件管理版本和更新日志。

---

## 📋 插件文件结构

一个完整的插件应包含以下文件：

```
my_plugin/
├── main.py                 # 主代码
├── metadata.yaml           # 插件元数据（含版本号）
├── _conf_schema.json       # 配置文件 Schema（可选）
├── CHANGELOG.md            # 更新日志 ⭐
├── README.md               # 插件说明
└── requirements.txt        # Python 依赖（可选）
```

---

## 📝 metadata.yaml 示例

```yaml
name: my_plugin
author: your_name
description: 插件描述
version: 1.0.0
repo: https://github.com/your_name/my_plugin

# 版本要求
astrbot_version: ">=4.0.0"

# 支持的平台（可选）
support_platforms:
  - aiocqhttp
  - telegram
  - webchat
```

---

## 📜 CHANGELOG.md 模板

```markdown
# 更新日志

本项目的所有重要更改都会记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Added
- （待发布的新功能）

### Changed
- （待发布的更改）

### Fixed
- （待发布的修复）

---

## [1.0.0] - 2025-01-15

### Added
- 初始版本发布
- 支持指令 `/天气 <城市>` 查询天气
- 支持 LLM Tool 方式自动调用
- 支持配置天气 API Key

### Changed
- 无

### Fixed
- 无

---

## [0.1.0] - 2025-01-10

### Added
- 项目初始化
- 基础框架搭建

---

[Unreleased]: https://github.com/your_name/my_plugin/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/your_name/my_plugin/releases/tag/v1.0.0
[0.1.0]: https://github.com/your_name/my_plugin/releases/tag/v0.1.0
```

---

## 🔢 语义化版本号

版本号格式：`MAJOR.MINOR.PATCH`

| 类型 | 说明 | 示例 |
|------|------|------|
| MAJOR | 不兼容的 API 更改 | 1.0.0 → 2.0.0 |
| MINOR | 向后兼容的功能新增 | 1.0.0 → 1.1.0 |
| PATCH | 向后兼容的问题修复 | 1.0.0 → 1.0.1 |

---

## 📦 版本发布流程

### 1. 更新版本号

```yaml
# metadata.yaml
version: 1.1.0  # 从 1.0.0 更新
```

### 2. 更新 CHANGELOG.md

```markdown
## [1.1.0] - 2025-01-20

### Added
- 新增支持多城市天气对比
- 新增天气预警功能

### Changed
- 优化天气查询速度

### Fixed
- 修复城市名称解析错误
```

### 3. 创建 Git Tag

```bash
git tag -a v1.1.0 -m "Release v1.1.0: 新增多城市对比和预警功能"
git push origin v1.1.0
```

### 4. 创建 GitHub Release（可选）

在 GitHub 仓库页面创建 Release，内容来自 CHANGELOG.md。

**注意**：插件市场直接下载仓库源码，不需要创建 Release。Release 仅用于版本标记和分发。

---

## 🤖 Agent 版本管理提示词

将以下内容添加到 Agent 提示词中：

```markdown
## 版本管理要求

开发插件时，必须包含以下文件：

### 1. metadata.yaml
```yaml
name: <插件名>
author: <作者>
description: <描述>
version: <版本号>
repo: <仓库地址>
```

### 2. CHANGELOG.md
按照以下格式记录更新：

```markdown
# 更新日志

## [版本号] - 日期

### Added（新增功能）
- 功能描述

### Changed（功能变更）
- 变更描述

### Fixed（问题修复）
- 修复描述

### Removed（移除功能）
- 移除描述
```

### 版本号规则
- 初始版本：1.0.0
- 新增功能：MINOR +1（如 1.0.0 → 1.1.0）
- 问题修复：PATCH +1（如 1.0.0 → 1.0.1）
- 不兼容更改：MAJOR +1（如 1.0.0 → 2.0.0）

### 交付要求
每次交付插件时，必须：
1. 更新 metadata.yaml 中的版本号
2. 更新 CHANGELOG.md 记录变更
3. 输出完整的插件文件列表
```

---

## 📊 版本历史示例

```
my_plugin/
├── v1.0.0 (2025-01-15)
│   ├── 初始版本
│   └── 基础天气查询功能
│
├── v1.1.0 (2025-01-20)
│   ├── 新增多城市对比
│   └── 新增天气预警
│
├── v1.1.1 (2025-01-22)
│   └── 修复城市名称解析错误
│
└── v1.2.0 (2025-01-25)
    ├── 新增天气趋势图
    └── 优化响应速度
```

---

## 🔗 相关链接

- [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)
- [语义化版本](https://semver.org/lang/zh-CN/)
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github)

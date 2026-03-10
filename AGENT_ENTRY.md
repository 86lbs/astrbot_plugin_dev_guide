# Agent 入口文档

欢迎使用本仓库开发 AstrBot 插件。请按以下顺序阅读文档。

---

## 📚 必读文档

### 1. 源码地图（理解 API）
**文件**：[SOURCE_CODE_MAP.md](./SOURCE_CODE_MAP.md)

**内容**：
- 核心 API 速查表
- 导入路径速查
- 按功能查找源码

**目的**：了解可用的 API 和正确的导入方式

---

### 2. 配置文件格式（重要）
**本节内容**：插件配置文件格式

#### metadata.yaml 格式
```yaml
name: my_plugin
author: your_name
description: 插件描述
version: 1.0.0
repo: https://github.com/your_name/my_plugin
astrbot_version: ">=4.0.0"
```

#### _conf_schema.json 格式（重要！）
**格式必须正确，否则插件无法加载！**

```json
{
    "api_key": {
        "type": "string",
        "description": "API 密钥",
        "default": ""
    },
    "timeout": {
        "type": "int",
        "description": "超时时间（秒）",
        "default": 30
    },
    "enable_feature": {
        "type": "bool",
        "description": "是否启用功能",
        "default": true
    },
    "temperature": {
        "type": "float",
        "description": "温度参数",
        "default": 0.7
    },
    "allowed_users": {
        "type": "list",
        "description": "允许使用的用户列表",
        "default": [],
        "items": {
            "type": "string"
        }
    }
}
```

**支持的类型**：
| 类型 | 说明 | 必需字段 |
|------|------|----------|
| `string` | 字符串 | type, description, default |
| `int` | 整数 | type, description, default |
| `float` | 浮点数 | type, description, default |
| `bool` | 布尔值 | type, description, default |
| `list` | 列表 | type, description, default, **items** |

**list 类型特殊说明**：
- 必须添加 `items` 字段，指定列表元素的类型
- `items` 是一个对象，包含 `type` 字段
- 示例：`"items": {"type": "string"}`

**注意事项**：
1. 每个配置项必须包含 `type`、`description`、`default` 三个字段
2. `list` 类型必须额外包含 `items` 字段
3. `type` 必须是上述支持的类型之一
4. 如果不需要配置项，可以不创建此文件

#### CHANGELOG.md 格式
```markdown
# 更新日志

## [1.0.0] - 2025-01-15

### Added
- 初始版本发布
- 功能描述...

### Changed
- 无

### Fixed
- 无
```

---

### 3. 版本管理
**文件**：[VERSION_MANAGEMENT.md](./VERSION_MANAGEMENT.md)

**内容**：
- 版本号规则
- 更新日志格式
- 发布流程

---

### 4. 测试工具
**文件**：[tools/README.md](./tools/README.md)

**内容**：
- 测试脚本使用方法
- 消息模拟器
- 自动化测试

---

### 5. 模拟 LLM 服务（测试 LLM Tool）
**文件**：[MOCK_LLM_SERVER.md](./MOCK_LLM_SERVER.md)

**用途**：测试 LLM Tool 时无需运行真实的 LLM 模型

---

## 🚀 开发流程

```
1. 阅读源码地图 → 了解 API
      ↓
2. 设计插件结构
      ↓
3. 编写代码
   - main.py
   - metadata.yaml
   - _conf_schema.json（如需要）
   - CHANGELOG.md
   - README.md
      ↓
4. 本地测试
   - 使用模拟 LLM 服务测试 Tool
   - 使用消息模拟器测试指令
      ↓
5. 发布
   - 创建 GitHub 仓库
   - 推送代码
   - 创建 Release
```

---

## 📁 插件文件结构

```
my_plugin/
├── main.py              # 主代码
├── metadata.yaml        # 元数据（含版本号）
├── _conf_schema.json    # 配置 Schema（可选）
├── CHANGELOG.md         # 更新日志
└── README.md            # 插件说明
```

---

## ⚠️ 常见错误

| 错误 | 正确 |
|------|------|
| `yield event.plain_result("内容")` | `event.set_result(MessageEventResult().message("内容"))` |
| `return "内容"` 在指令中 | `event.set_result(MessageEventResult().message("内容"))` |
| `_conf_schema.json` 格式错误 | 每个配置项必须是对象，包含 type、description、default |

---

## 🔗 相关链接

- **AstrBot 源码**：https://github.com/AstrBotDevs/AstrBot
- **AstrBot 文档**：https://astrbot.app
- **本仓库**：https://github.com/86lbs/astrbot_plugin_dev_guide

---

## 📤 发布指南

**文件**：[PUBLISH_GUIDE.md](./PUBLISH_GUIDE.md)

**内容**：
- 使用 GitHub API 创建仓库
- 推送代码
- 创建 Release
- 上传发行版

**重要**：完成开发后，必须执行发布步骤！

---

## 🔍 自我审查

**文件**：[SELF_REVIEW.md](./SELF_REVIEW.md)

**内容**：
- 模仿 astrpluginreviewer[bot] 的审核逻辑
- 基础结构检查
- filter 装饰器检查
- LLM 事件钩子检查
- 消息发送方式检查
- 安全检查

**重要**：完成代码后，必须进行自我审查！

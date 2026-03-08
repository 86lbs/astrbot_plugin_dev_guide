# AstrBot 插件开发指南

使用 AI 快速开发 AstrBot 插件的完整指南。

## 📁 文件说明

| 文件 | 说明 | 推荐度 |
|------|------|--------|
| [PROMPT_V5_LOCAL_SIMULATION.md](./PROMPT_V5_LOCAL_SIMULATION.md) | **v5.0 本地模拟测试版** - 完全自包含测试环境 | ⭐⭐⭐⭐⭐ 强烈推荐 |
| [LOCAL_TEST_ENVIRONMENT.md](./LOCAL_TEST_ENVIRONMENT.md) | **本地测试环境配置** - Ollama + 模拟消息端 | ⭐⭐⭐⭐ 推荐 |
| [PROMPT_V4_TEST_DRIVEN.md](./PROMPT_V4_TEST_DRIVEN.md) | v4.0 测试驱动版 | ⭐⭐⭐ |
| [TEST_ENVIRONMENT.md](./TEST_ENVIRONMENT.md) | 测试环境配置指南 | ⭐⭐⭐ |
| [SOURCE_CODE_MAP.md](./SOURCE_CODE_MAP.md) | AstrBot 核心源码文件索引 | ⭐⭐⭐ |
| [PROMPT_V3_SOURCE_CODE_DRIVEN.md](./PROMPT_V3_SOURCE_CODE_DRIVEN.md) | v3.0 源码驱动版 | ⭐⭐⭐ |
| [PROMPT_V2.md](./PROMPT_V2.md) | v2.0 文档驱动版 | ⭐⭐ |
| [PROMPT.md](./PROMPT.md) | v1.0 基础版 | ⭐ |
| [TUTORIAL.md](./TUTORIAL.md) | 用户教程 | ⭐⭐ |

## 🚀 快速开始

### 方式一：本地模拟测试（强烈推荐）

**适用场景**：Agent 有虚拟机权限，可实现完全自包含的开发测试闭环

```
┌─────────────────────────────────────────────────────────────┐
│                   本地测试环境                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│   │ 模拟消息端  │───▶│  AstrBot    │───▶│  Ollama     │    │
│   │ (测试脚本)  │    │  (被测系统) │    │ (本地 LLM)  │    │
│   └─────────────┘    └─────────────┘    └─────────────┘    │
│          │                  │                   │          │
│          └──────────────────┼───────────────────┘          │
│                             ▼                              │
│                      ┌─────────────┐                       │
│                      │   插  件    │                       │
│                      │  (被测试)   │                       │
│                      └─────────────┘                       │
│                                                             │
│   优势：                                                    │
│   ✅ 无需真实 LLM API（省钱）                               │
│   ✅ 无需真实消息平台（简单）                               │
│   ✅ 完全可控可预测                                        │
│   ✅ 可自动化 CI/CD                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**步骤：**

1. 配置本地测试环境（参考 [LOCAL_TEST_ENVIRONMENT.md](./LOCAL_TEST_ENVIRONMENT.md)）
2. 复制 [PROMPT_V5_LOCAL_SIMULATION.md](./PROMPT_V5_LOCAL_SIMULATION.md) 中的提示词
3. 发送给 AI
4. AI 自动完成：阅读源码 → 编写代码 → 本地测试 → 修复错误 → 交付

### 方式二：远程测试

**适用场景**：使用真实 LLM API 和消息平台

1. 配置测试环境（参考 [TEST_ENVIRONMENT.md](./TEST_ENVIRONMENT.md)）
2. 复制 [PROMPT_V4_TEST_DRIVEN.md](./PROMPT_V4_TEST_DRIVEN.md) 中的提示词
3. 发送给 AI

### 方式三：仅源码驱动

**适用场景**：无测试环境，仅开发

1. 复制 [PROMPT_V3_SOURCE_CODE_DRIVEN.md](./PROMPT_V3_SOURCE_CODE_DRIVEN.md) 中的提示词
2. 发送给 AI，提供源码路径

## 📊 版本对比

| 版本 | 源码阅读 | 测试验证 | LLM 模拟 | 消息模拟 | 适用场景 |
|------|----------|----------|----------|----------|----------|
| **v5.0** | ✅ | ✅ 本地 | ✅ Ollama | ✅ 脚本 | 完全自包含 |
| v4.0 | ✅ | ✅ 远程 | ❌ 需 API | ❌ 需平台 | 有 API 资源 |
| v3.0 | ✅ | ❌ | - | - | 仅开发 |
| v2.0 | 文档 | ❌ | - | - | 简单插件 |
| v1.0 | ❌ | ❌ | - | - | 快速上手 |

## 🔗 相关链接

- [AstrBot 官网](https://astrbot.app)
- [AstrBot 文档](https://astrbot.app/dev/plugin.html)
- [AstrBot GitHub](https://github.com/AstrBotDevs/AstrBot)
- [Ollama 官网](https://ollama.com) - 本地 LLM 运行

## 📝 示例插件

使用本指南开发的插件示例：

- [易经算卦插件](https://github.com/86lbs/astrbot_plugin_suangua) - 传统金钱卦起卦法

## 🤝 贡献

欢迎提交 Issue 和 PR 完善本指南！

## 📄 许可证

MIT License

# AstrBot 插件开发指南

使用 AI 快速开发 AstrBot 插件的完整指南。

## 📁 文件说明

| 文件 | 说明 | 推荐度 |
|------|------|--------|
| [PROMPT_V4_TEST_DRIVEN.md](./PROMPT_V4_TEST_DRIVEN.md) | **v4.0 测试驱动版** - 源码+测试验证闭环 | ⭐⭐⭐⭐ 强烈推荐 |
| [TEST_ENVIRONMENT.md](./TEST_ENVIRONMENT.md) | **测试环境配置指南** - 如何配置测试虚拟机 | ⭐⭐⭐ 推荐 |
| [PROMPT_V3_SOURCE_CODE_DRIVEN.md](./PROMPT_V3_SOURCE_CODE_DRIVEN.md) | v3.0 源码驱动版提示词 | ⭐⭐⭐ |
| [SOURCE_CODE_MAP.md](./SOURCE_CODE_MAP.md) | AstrBot 核心源码文件索引 | ⭐⭐⭐ |
| [PROMPT_V2.md](./PROMPT_V2.md) | v2.0 文档驱动版提示词 | ⭐⭐ |
| [PROMPT.md](./PROMPT.md) | v1.0 基础版提示词 | ⭐ |
| [TUTORIAL.md](./TUTORIAL.md) | 用户教程 | ⭐⭐ |

## 🚀 快速开始

### 方式一：测试驱动（强烈推荐）

**适用场景**：Agent 有虚拟机访问权限，可实现完整开发闭环

1. 配置测试环境（参考 [TEST_ENVIRONMENT.md](./TEST_ENVIRONMENT.md)）
2. 复制 [PROMPT_V4_TEST_DRIVEN.md](./PROMPT_V4_TEST_DRIVEN.md) 中的提示词
3. 发送给 AI，并提供源码路径
4. AI 会自动完成：阅读源码 → 编写代码 → 部署测试 → 修复错误 → 交付

**优势**：
- ✅ 源码 + 测试双重验证
- ✅ 错误自动发现和修复
- ✅ 交付的代码经过实际验证
- ✅ 真正的开发闭环

### 方式二：源码驱动

**适用场景**：开发复杂插件，需要准确了解最新 API

1. 复制 [PROMPT_V3_SOURCE_CODE_DRIVEN.md](./PROMPT_V3_SOURCE_CODE_DRIVEN.md) 中的提示词
2. 发送给 AI，并提供 AstrBot 源码路径
3. AI 会先阅读源码，输出阅读报告，再编写代码

**优势**：
- ✅ 源码即真理，不受文档过时影响
- ✅ 强制阅读验证，不会跳过
- ✅ API 签名准确，来源可追溯

### 方式三：文档驱动

**适用场景**：开发简单插件，快速上手

1. 复制 [PROMPT_V2.md](./PROMPT_V2.md) 或 [PROMPT.md](./PROMPT.md) 中的提示词
2. 发送给 AI
3. 描述需求，获取代码

## 📖 详细教程

请阅读 [TUTORIAL.md](./TUTORIAL.md) 了解更多：

- 进阶技巧
- 常见问题解决
- 实战案例
- 插件发布流程

## 🔗 相关链接

- [AstrBot 官网](https://astrbot.app)
- [AstrBot 文档](https://astrbot.app/dev/plugin.html)
- [AstrBot GitHub](https://github.com/AstrBotDevs/AstrBot)

## 📝 示例插件

使用本指南开发的插件示例：

- [易经算卦插件](https://github.com/86lbs/astrbot_plugin_suangua) - 传统金钱卦起卦法

## 🤝 贡献

欢迎提交 Issue 和 PR 完善本指南！

## 📄 许可证

MIT License

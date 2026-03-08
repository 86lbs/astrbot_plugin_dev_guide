# AstrBot 插件开发指南

使用 AI 快速开发 AstrBot 插件的完整指南。

🌐 **在线工具**：[https://86lbs.github.io/astrbot_plugin_dev_guide/](https://86lbs.github.io/astrbot_plugin_dev_guide/)

---

## 🚀 立即开始

### 使用提示词生成器（推荐）

**打开在线工具：[https://86lbs.github.io/astrbot_plugin_dev_guide/prompt_generator.html](https://86lbs.github.io/astrbot_plugin_dev_guide/prompt_generator.html)**

支持四种模式：

| 模式 | 说明 | 必填项 |
|------|------|--------|
| 📚 **学习模式** | 先了解 AstrBot 插件开发，稍后提供任务 | 无（全部可选） |
| ✨ **创建插件** | 从零开始创建新插件 | 插件描述 |
| 🔧 **优化插件** | 改进已有插件代码 | 插件来源 + 我的要求 |
| 📖 **讲解插件** | 解释插件代码原理 | 插件来源 |

**使用步骤：**

1. 选择操作模式（默认：学习模式）
2. 填写简单描述
3. （可选）填写 GitHub Token 用于发布
4. 点击生成提示词
5. 复制发送给 AI

---

## 📚 学习模式

**适用场景：** 第一次使用，或想让 Agent 先了解 AstrBot

**特点：**
- 所有字段都是可选的
- Agent 会学习 AstrBot 插件开发知识
- 学习完成后等待用户稍后提供具体任务

**可选内容：**
- 学习重点：插件结构、指令开发、LLM Tool、事件监听等
- 你的问题：想提前了解的内容

**生成提示词示例：**
```
学习 AstrBot 插件开发。

## 学习目标
1. 插件的基本结构
2. Star 基类和 Context 接口
3. 指令开发（@filter.command）
4. LLM Tool 开发（@filter.llm_tool）
...

## 注意
- 用户将在稍后提供具体的开发任务
- 现在只需要了解和掌握基础知识
```

---

## ✨ 创建插件

**最简输入：**
```
插件描述：查天气的插件
```

**完整输入：**
```
插件名称：weather_query（可选）
插件描述：天气查询插件
详细需求：
1. 用户发送 /天气 北京 查询天气
2. 支持 LLM Tool 自动调用
```

**AI 会自动：**
- 阅读源码 → 设计结构 → 编写代码 → 测试验证 → 发布（如填写 Token）

---

## 🔧 优化插件

**输入示例：**
```
插件来源：https://github.com/xxx/my_plugin
我的要求：帮我添加错误处理，当 API 调用失败时给用户友好提示
```

**支持格式：**
- 粘贴代码
- GitHub 仓库链接

---

## 📖 讲解插件

**输入示例：**
```
插件来源：https://github.com/xxx/my_plugin
我的问题：这个装饰器是怎么工作的？
```

**讲解风格：**
- 简单易懂（适合新手）
- 详细深入（适合进阶）
- 技术专业（适合开发者）

---

## 🔑 GitHub Token

**何时需要：**
- 发布插件到 GitHub 时需要

**如何获取：**
1. GitHub → Settings → Developer settings → Personal access tokens
2. 生成 Token，勾选 `repo` 权限
3. 复制到提示词生成器

**安全说明：**
- Token 仅用于生成提示词，不会被保存
- 重置表单时自动清空

---

## 📁 文件说明

### 在线工具

| 文件 | 说明 |
|------|------|
| [prompt_generator.html](./prompt_generator.html) | **提示词生成器** - 三种模式，支持 Token |

### 开发指南

| 文件 | 说明 | 推荐度 |
|------|------|--------|
| [PROMPT_V5_LOCAL_SIMULATION.md](./PROMPT_V5_LOCAL_SIMULATION.md) | **v5.0 本地模拟测试版** - 完全自包含测试环境 | ⭐⭐⭐⭐⭐ |
| [LOCAL_TEST_ENVIRONMENT.md](./LOCAL_TEST_ENVIRONMENT.md) | **本地测试环境配置** - Ollama + 模拟消息端 | ⭐⭐⭐⭐ |
| [MESSAGE_SIMULATOR.md](./MESSAGE_SIMULATOR.md) | **消息模拟器详解** - 如何模拟发送消息 | ⭐⭐⭐⭐ |
| [VERSION_MANAGEMENT.md](./VERSION_MANAGEMENT.md) | **版本管理指南** - 版本号和更新日志 | ⭐⭐⭐⭐ |
| [PUBLISH_GUIDE.md](./PUBLISH_GUIDE.md) | **插件发布指南** - Token 和发布流程 | ⭐⭐⭐⭐ |

### 测试工具

| 文件 | 说明 |
|------|------|
| [tools/](./tools/) | **完整测试工具集** |
| ├── `setup_local_env.sh` | 一键部署本地测试环境 |
| ├── `start_astrbot.sh` | 启动 AstrBot 服务 |
| ├── `stop_astrbot.sh` | 停止 AstrBot 服务 |
| ├── `deploy_plugin.sh` | 部署插件 |
| ├── `send_message.py` | 发送消息 |
| ├── `send_message_stream.py` | 发送消息（流式） |
| ├── `test_plugin.py` | 自动化测试 |
| └── `view_log.sh` | 查看日志 |

---

## 🏗️ 本地测试环境

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

---

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

## 📜 致谢要求

如果您使用本指南开发 AstrBot 插件，请在插件的 README.md 中添加致谢：

```markdown
## 致谢

本插件使用 [AstrBot 插件开发指南](https://github.com/86lbs/astrbot_plugin_dev_guide) 开发。
```

感谢您的支持！

## 📄 许可证

MIT License

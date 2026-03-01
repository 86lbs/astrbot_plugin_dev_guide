# AstrBot 插件开发指南

使用 AI 快速开发 AstrBot 插件的完整指南。

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| [PROMPT.md](./PROMPT.md) | AI 提示词模板，发送给 AI 即可开始开发 |
| [TUTORIAL.md](./TUTORIAL.md) | 用户教程，详细说明如何使用 AI 开发插件 |

## 🚀 快速开始

### 1. 复制提示词

打开 [PROMPT.md](./PROMPT.md)，复制「完整提示词」部分。

### 2. 发送给 AI

将提示词发送给 Claude、ChatGPT 等 AI 工具。

### 3. 描述需求

用自然语言描述你想要的插件功能：

```
帮我开发一个天气查询插件：
1. 用户发送城市名可以查询天气
2. 支持配置 API 密钥
```

### 4. 获取代码

AI 会生成完整的插件代码，包括：
- `main.py` - 主插件代码
- `metadata.yaml` - 插件元数据
- `_conf_schema.json` - 配置文件

### 5. 安装插件

将生成的文件放入 AstrBot 的 `data/plugins/插件名/` 目录，重启即可。

## 📖 详细教程

请阅读 [TUTORIAL.md](./TUTORIAL.md) 了解更多：

- 进阶技巧
- 常见问题解决
- 实战案例
- 插件发布流程

## 🔗 相关链接

- [AstrBot 官网](https://astrbot.app)
- [AstrBot 文档](https://astrbot.app/dev/plugin.html)
- [AstrBot GitHub](https://github.com/Soulter/AstrBot)

## 📝 示例插件

使用本指南开发的插件示例：

- [易经算卦插件](https://github.com/86lbs/astrbot_plugin_suangua) - 传统金钱卦起卦法

## 🤝 贡献

欢迎提交 Issue 和 PR 完善本指南！

## 📄 许可证

MIT License

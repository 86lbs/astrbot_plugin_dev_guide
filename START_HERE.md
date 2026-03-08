# 开始开发 - 发送给 Agent 的内容

复制以下内容发送给 Agent：

---

## 方式一：完整版（推荐）

```
我要开发 AstrBot 插件，请帮我完成。

## 1. 开发指南仓库
https://github.com/86lbs/astrbot_plugin_dev_guide

请先阅读仓库中的：
- README.md（整体说明）
- PROMPT_V5_LOCAL_SIMULATION.md（开发提示词）
- tools/README.md（测试工具说明）

## 2. AstrBot 源码
请从 GitHub 获取最新源码：
https://github.com/AstrBotDevs/AstrBot

## 3. 插件需求
[在这里描述你的插件需求]

例如：
- 开发一个天气查询插件
- 用户发送城市名可以查询天气
- 支持 LLM Tool 方式调用
- 需要配置 API Key

## 4. 测试环境
我已准备好测试环境，工具在：
- 测试工具目录：/path/to/astrbot_plugin_dev_guide/tools/
- AstrBot 安装目录：/opt/astrbot/

请按照 PROMPT_V5_LOCAL_SIMULATION.md 中的工作流开发：
1. 阅读源码
2. 输出阅读报告
3. 设计插件
4. 编写代码
5. 部署测试
6. 修复错误
7. 交付代码
```

---

## 方式二：简洁版

```
开发 AstrBot 插件。

仓库：https://github.com/86lbs/astrbot_plugin_dev_guide
源码：https://github.com/AstrBotDevs/AstrBot

需求：[描述你的需求]

请阅读 PROMPT_V5_LOCAL_SIMULATION.md 按流程开发。
```

---

## 方式三：如果 Agent 已有源码

```
开发 AstrBot 插件。

源码路径：/path/to/astrbot/
开发指南：https://github.com/86lbs/astrbot_plugin_dev_guide

需求：[描述你的需求]

请阅读 PROMPT_V5_LOCAL_SIMULATION.md 按流程开发。
```

---

## 示例：开发天气插件

```
我要开发 AstrBot 插件，请帮我完成。

## 1. 开发指南仓库
https://github.com/86lbs/astrbot_plugin_dev_guide

## 2. AstrBot 源码
https://github.com/AstrBotDevs/AstrBot

## 3. 插件需求
开发一个天气查询插件：
- 插件名：weather_query
- 功能：查询指定城市的天气
- 支持两种方式：
  1. 指令方式：/天气 北京
  2. LLM Tool 方式：用户问"今天北京天气怎么样？"时自动调用
- 需要配置天气 API Key
- 使用免费的天气 API（如 wttr.in）

## 4. 测试环境
测试工具目录：./tools/
AstrBot 目录：/opt/astrbot/

请按照 PROMPT_V5_LOCAL_SIMULATION.md 的流程开发。
```

---

## 发送后 Agent 会做什么

1. **阅读开发指南** - 理解开发规范
2. **阅读源码** - 提取 API 签名
3. **输出阅读报告** - 展示理解的内容
4. **设计插件** - 设计结构和 API
5. **编写代码** - 生成完整代码
6. **部署测试** - 使用 tools/ 中的脚本测试
7. **修复错误** - 根据日志修复
8. **交付代码** - 测试通过后交付

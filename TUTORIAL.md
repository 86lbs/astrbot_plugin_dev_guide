# 使用 AI 开发 AstrBot 插件教程

本教程教你如何利用 AI（如 Claude、ChatGPT）快速开发 AstrBot 插件，无需深厚的编程基础。

---

## 目录

1. [准备工作](#1-准备工作)
2. [快速开始](#2-快速开始)
3. [进阶技巧](#3-进阶技巧)
4. [常见问题](#4-常见问题)
5. [实战案例](#5-实战案例)

---

## 1. 准备工作

### 1.1 你需要

- 一个 AI 工具（Claude、ChatGPT、通义千问等）
- AstrBot 已安装运行
- 基本的电脑操作能力

### 1.2 可选（用于进阶开发）

- AstrBot 源码（让 AI 阅读源码可以开发更复杂的插件）
- GitHub 账号（用于发布插件）

---

## 2. 快速开始

### 步骤 1：复制提示词

打开 [PROMPT.md](./PROMPT.md) 文件，复制「完整提示词」部分的内容。

### 步骤 2：发送给 AI

将提示词发送给 AI，AI 会进入「AstrBot 插件开发助手」模式。

### 步骤 3：描述你的需求

用自然语言描述你想要的插件功能，例如：

```
帮我开发一个表情包插件：
1. 用户发送「表情包 关键词」可以搜索表情包
2. 支持随机表情包功能
3. 可以配置 API 密钥
```

### 步骤 4：获取代码

AI 会生成完整的插件代码，包括：

- `main.py` - 主插件代码
- `metadata.yaml` - 插件元数据
- `_conf_schema.json` - 配置文件（如需要）

### 步骤 5：安装插件

1. 在 AstrBot 的 `data/plugins/` 目录下创建插件文件夹
2. 将 AI 生成的文件放入文件夹
3. 重启 AstrBot 或在管理面板重载插件

---

## 3. 进阶技巧

### 3.1 让 AI 阅读源码

对于复杂插件，可以让 AI 阅读 AstrBot 源码：

```
请先阅读以下文件了解 AstrBot 插件开发：
- /path/to/astrbot/astrbot/core/star/star.py
- /path/to/astrbot/astrbot/core/star/context.py
- /path/to/astrbot/astrbot/core/star/filter/command.py

然后帮我开发一个 [功能描述] 的插件。
```

### 3.2 迭代优化

如果生成的代码有问题，告诉 AI 具体问题：

```
插件有个问题：指令触发后没有响应。

请检查代码，特别是返回结果的部分。
```

### 3.3 添加功能

在已有插件基础上添加功能：

```
在现有插件基础上，添加以下功能：
1. 支持引用消息处理
2. 添加使用统计功能
3. 支持配置开关
```

### 3.4 修复 Bug

```
插件报错了，错误信息是：
[粘贴错误日志]

请帮我修复这个问题。
```

---

## 4. 常见问题

### Q1: 指令不触发？

**原因**：需要使用唤醒前缀或 @机器人

**解决**：
- 使用 `/指令名` 格式
- 或在消息中 @机器人 后发送指令

### Q2: 插件没有返回结果？

**原因**：可能使用了旧版本的返回方式

**解决**：确保使用正确的返回方式
```python
# ✅ 正确
event.set_result(MessageEventResult().message("内容").use_t2i(False))

# ❌ 错误（旧版本）
yield event.plain_result("内容")
```

### Q3: 配置不生效？

**原因**：配置文件格式错误或未正确读取

**解决**：
1. 检查 `_conf_schema.json` 格式是否正确
2. 确保在 `__init__` 中读取配置
3. 重启 AstrBot 后再修改配置

### Q4: LLM 工具不被调用？

**原因**：工具描述不够清晰

**解决**：在工具描述中明确触发条件
```python
@llm_tool(name="my_tool")
async def my_tool(self, event: AstrMessageEvent, query: str = "") -> str:
    """当用户想要 [具体条件] 时使用此工具。
    例如：当用户询问天气、查询天气、今天天气如何时调用。
    """
```

### Q5: 引用消息无法识别？

**原因**：引用消息检测逻辑不完整

**解决**：使用完整的引用消息检测方法
```python
def _get_reply_content(self, event: AstrMessageEvent) -> tuple[bool, str]:
    from astrbot.api.message_components import Plain, Reply
    
    for msg in event.get_messages():
        if isinstance(msg, Reply):
            if hasattr(msg, 'message_str') and msg.message_str:
                return True, msg.message_str.strip()
            if hasattr(msg, 'chain') and msg.chain:
                text = ""
                for comp in msg.chain:
                    if isinstance(comp, Plain):
                        text += comp.text
                if text.strip():
                    return True, text.strip()
    return False, ""
```

---

## 5. 实战案例

### 案例 1：一言插件

**需求**：随机返回一句一言（Hitokoto）

**提示词**：
```
开发一个一言插件：
1. 用户发送「一言」获取随机句子
2. 支持分类筛选（动画、漫画、游戏等）
3. 使用 https://v1.hitokoto.cn API
```

**生成文件**：
- `main.py` - 调用一言 API 并返回结果
- `metadata.yaml` - 插件信息
- `_conf_schema.json` - 分类配置

### 案例 2：翻译插件

**需求**：多语言翻译，使用 LLM 翻译

**提示词**：
```
开发一个翻译插件：
1. 指令：/翻译 内容 或 /翻译 目标语言 内容
2. 使用当前配置的 LLM 进行翻译
3. 支持引用消息翻译
4. 可配置默认目标语言
```

### 案例 3：签到插件

**需求**：每日签到获取积分

**提示词**：
```
开发一个签到插件：
1. 用户每天可以签到一次
2. 签到获得随机积分
3. 支持查询签到状态和积分
4. 使用 SQLite 存储数据
5. 支持连续签到奖励
```

---

## 6. 发布插件

### 6.1 创建 GitHub 仓库

```bash
# 初始化仓库
git init
git add .
git commit -m "Initial commit"

# 推送到 GitHub
git remote add origin https://github.com/你的用户名/插件名.git
git push -u origin main
```

### 6.2 创建 Release

在 GitHub 创建 Release，添加更新说明。

### 6.3 上架到插件市场

在 AstrBot 官方仓库提交 Issue 申请上架：

- 地址：https://github.com/AstrBotDevs/AstrBot/issues/new
- 标题格式：`[Plugin] 插件名称`
- 详细说明请参考 [PUBLISH_GUIDE.md](./PUBLISH_GUIDE.md)

**Issue 内容示例：**

```markdown
### 插件信息

```json
{
  "name": "my_plugin",
  "display_name": "我的插件",
  "desc": "插件功能描述",
  "author": "your_name",
  "repo": "https://github.com/your_name/my_plugin",
  "tags": ["工具", "实用"],
  "social_link": "https://github.com/your_name"
}
```

### 插件检查清单

- [x] 我的插件经过完整的测试
- [x] 我的插件不包含恶意代码
- [x] 我已阅读并同意遵守该项目的 [行为准则](https://docs.github.com/zh/site-policy/github-terms/github-community-code-of-conduct)。
```

---

## 7. 最佳实践

### 7.1 代码规范

- 使用类型注解
- 添加文档字符串
- 合理的函数命名
- 适当的日志输出

### 7.2 用户体验

- 提供清晰的使用说明
- 友好的错误提示
- 合理的默认配置

### 7.3 错误处理

- 捕获可能的异常
- 提供有意义的错误信息
- 记录错误日志

### 7.4 性能优化

- 避免阻塞操作
- 合理使用缓存
- 异步处理耗时任务

---

## 8. 资源链接

- [AstrBot 官网](https://astrbot.app)
- [AstrBot 文档](https://astrbot.app/dev/plugin.html)
- [AstrBot GitHub](https://github.com/Soulter/AstrBot)
- [插件市场](https://astrbot.app/market)

---

**祝你开发愉快！如有问题，欢迎在 GitHub 提 Issue。**

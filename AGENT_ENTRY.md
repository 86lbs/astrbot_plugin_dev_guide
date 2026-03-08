# AstrBot 插件开发指南 - Agent 入口

> **如果你是 Agent，请阅读本文件了解如何开发 AstrBot 插件。**

---

## 🤖 给 Agent 的指令

### 核心原则

1. **源码即真理** - 必须阅读 AstrBot 源码，文档可能过时
2. **测试验证** - 代码必须部署测试，不能凭猜测交付
3. **错误修复闭环** - 有错误必须修复并重新测试

### 强制规则

- ❌ 禁止凭记忆/猜测写代码
- ❌ 禁止在未测试的情况下交付代码
- ✅ 必须先阅读源码
- ✅ 必须输出阅读报告
- ✅ 必须测试验证

---

## 📁 本仓库文件说明

| 文件 | 用途 | Agent 是否需要阅读 |
|------|------|-------------------|
| **AGENT_ENTRY.md** | Agent 入口（本文件） | ✅ 必读 |
| **SOURCE_CODE_MAP.md** | AstrBot 源码文件地图 | ✅ 必读 |
| **QUICK_REFERENCE.md** | API 快速参考 | ⭐ 推荐 |
| **TEST_ENVIRONMENT.md** | 测试环境配置 | 按需 |
| PROMPT_V4_TEST_DRIVEN.md | 完整提示词模板 | 参考 |
| TUTORIAL.md | 人类教程 | 参考 |

---

## 🚀 开发工作流

### 第一步：阅读源码地图

打开 `SOURCE_CODE_MAP.md`，了解 AstrBot 核心源码文件位置。

**必读文件：**
```
astrbot/core/star/base.py                    # Star 基类
astrbot/core/star/context.py                 # Context 接口
astrbot/core/platform/astr_message_event.py  # 事件类
astrbot/core/message/message_event_result.py # 返回结果
astrbot/core/star/register/star_handler.py   # 装饰器实现
```

### 第二步：阅读源码

**必须实际阅读上述文件**，不能凭记忆假设 API。

### 第三步：输出阅读报告

格式如下：
```
## 📖 源码阅读报告

### 已阅读文件
- astrbot/core/star/base.py: Star 基类，插件必须继承
- astrbot/core/star/context.py: Context 接口，get_using_provider() 等
- ...

### 关键 API 签名（从源码提取）
[列出实际使用的 API 及其签名]
```

### 第四步：编写代码

按照源码中的实际 API 编写插件代码。

### 第五步：测试验证

如果有测试环境：
```bash
cp -r ./my_plugin /opt/astrbot/data/plugins/
pkill -f "python main.py" && sleep 2 && python main.py &
sleep 5
tail -100 /opt/astrbot/logs/astrbot.log
```

### 第六步：交付

只有测试通过后才能交付代码。

---

## 📋 插件开发模板

```python
from astrbot.api import star, logger
from astrbot.api.event import AstrMessageEvent, MessageEventResult, filter
from astrbot.api.star import Context
from astrbot.core.config.astrbot_config import AstrBotConfig


class MyPlugin(star.Star):
    """插件类 - 必须继承 star.Star"""

    def __init__(self, context: Context, config: AstrBotConfig = None):
        super().__init__(context)
        self._config = config

    async def initialize(self):
        """插件初始化"""
        logger.info("插件初始化完成")

    @filter.command("command_name", alias={"别名"})
    async def my_command(self, event: AstrMessageEvent):
        """指令说明"""
        event.set_result(
            MessageEventResult()
            .message("返回内容")
            .use_t2i(False)
        )

    @filter.llm_tool(name="my_tool")
    async def my_tool(self, event: AstrMessageEvent, query: str = "") -> str:
        '''工具描述。

        Args:
            query(string): 参数说明
        '''
        return "工具返回结果"

    async def terminate(self):
        """插件销毁"""
        logger.info("插件已卸载")
```

---

## ⚠️ 常见错误

| 错误 | 正确 |
|------|------|
| `yield event.plain_result("内容")` | `event.set_result(MessageEventResult().message("内容"))` |
| `return "内容"` 在指令中 | `event.set_result(MessageEventResult().message("内容"))` |
| `@star.register()` | 直接继承 `star.Star` |

---

## 📞 开始开发

请提供以下信息：

1. **AstrBot 源码路径**：`/path/to/astrbot/`
2. **插件需求**：描述你想要的功能

我会按照上述工作流开发插件。

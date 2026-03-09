# AstrBot 插件开发流程

本文档描述 AstrBot 插件的标准开发流程。

---

## 📋 开发工作流

### 阶段 1：需求分析
1. 理解用户需求
2. 列出需要用到的功能点
3. **输出：需求分析报告**

### 阶段 2：源码阅读
1. 阅读必读源码文件（见 SOURCE_CODE_MAP.md）
2. 按需阅读相关文件
3. **输出：源码阅读报告**

### 阶段 3：设计确认
1. 设计插件结构
2. 列出将使用的 API 及其源码签名
3. **输出：设计文档**

### 阶段 4：编码实现
1. 编写插件代码
2. 编写 metadata.yaml（含版本号）
3. 编写 _conf_schema.json（如需要，格式见 AGENT_ENTRY.md）
4. 编写 CHANGELOG.md（更新日志）
5. **输出：完整代码文件**

### 阶段 5：本地测试
1. 部署插件到 AstrBot
2. 测试指令功能
3. 测试 LLM Tool（使用模拟服务）
4. **输出：测试报告**

### 阶段 6：错误修复（如有）
1. 分析错误日志
2. 修复代码
3. 回到阶段 5 重新测试

### 阶段 7：交付
只有测试通过后，才能交付代码。

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

## 📝 核心代码模板

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

    @filter.command("test", alias={"测试"})
    async def test_command(self, event: AstrMessageEvent):
        """测试指令"""
        event.set_result(
            MessageEventResult()
            .message("测试成功！")
            .use_t2i(False)
        )

    @filter.llm_tool(name="my_tool")
    async def my_tool(self, event: AstrMessageEvent, query: str = "") -> str:
        '''工具描述。当用户 [触发条件] 时调用此工具。

        Args:
            query(string): 参数说明
        '''
        logger.info(f"工具被调用，参数: {query}")
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

---

## 🧪 测试环境

### 测试工具
位于 `tools/` 目录：
- `send_message.py` - 发送测试消息
- `mock_llm_server.py` - 模拟 LLM 服务（测试 Tool）

### 模拟 LLM 服务
用于测试 LLM Tool，无需运行真实的 LLM 模型。

```bash
# 启动模拟服务
python tools/mock_llm_server.py

# 配置 AstrBot
# API Base: http://localhost:8000/v1
# API Key: mock-key
# Model: mock-model
```

详见 [MOCK_LLM_SERVER.md](./MOCK_LLM_SERVER.md)

---

## 📚 相关文档

- [AGENT_ENTRY.md](./AGENT_ENTRY.md) - 入口文档，必读
- [SOURCE_CODE_MAP.md](./SOURCE_CODE_MAP.md) - 源码地图，API 速查
- [VERSION_MANAGEMENT.md](./VERSION_MANAGEMENT.md) - 版本管理
- [MOCK_LLM_SERVER.md](./MOCK_LLM_SERVER.md) - 模拟 LLM 服务
- [tools/README.md](./tools/README.md) - 测试工具

---

## 记住

1. 没有阅读源码之前，不要编写任何代码！
2. 没有本地测试之前，不要交付任何代码！
3. 所有功能必须经过实际验证！

# AstrBot 插件开发源码地图

本文档提供 AstrBot 插件开发所需的所有核心源码文件索引，帮助快速定位关键代码。

---

## 📁 源码目录结构概览

```
astrbot/
├── api/                          # 公开 API（推荐导入路径）
│   ├── __init__.py               # 顶层导出：logger, llm_tool, agent, sp
│   ├── star/__init__.py          # Star, Context, register
│   ├── event/
│   │   ├── __init__.py           # AstrMessageEvent, MessageEventResult
│   │   └── filter/__init__.py    # filter.command, filter.llm_tool 等
│   ├── message_components.py     # Plain, Image, At, Reply 等
│   └── provider/__init__.py      # Provider 相关
│
├── core/                         # 核心实现（源码阅读重点）
│   ├── star/                     # 插件系统核心
│   │   ├── base.py               # ⭐ Star 基类
│   │   ├── star.py               # ⭐ StarMetadata 元数据
│   │   ├── context.py            # ⭐⭐ Context 插件接口
│   │   ├── star_handler.py       # Handler 元数据
│   │   ├── star_manager.py       # 插件管理器
│   │   ├── register/             # 装饰器实现
│   │   │   ├── star.py           # register_star（已废弃）
│   │   │   └── star_handler.py   # ⭐⭐ 所有装饰器实现
│   │   └── filter/               # 过滤器
│   │       ├── command.py        # ⭐ CommandFilter 指令过滤
│   │       ├── regex.py          # 正则过滤
│   │       ├── permission.py     # 权限过滤
│   │       └── ...
│   │
│   ├── platform/
│   │   └── astr_message_event.py # ⭐⭐ AstrMessageEvent 事件类
│   │
│   ├── message/
│   │   ├── components.py         # ⭐ 消息组件定义
│   │   └── message_event_result.py # ⭐⭐ MessageEventResult
│   │
│   ├── provider/                 # LLM 提供商
│   │   ├── provider.py           # Provider 基类
│   │   ├── entities.py           # LLMResponse, ProviderRequest
│   │   └── func_tool_manager.py  # LLM 工具管理
│   │
│   └── config/
│       └── astrbot_config.py     # AstrBotConfig 配置类
│
└── builtin_stars/                # 内置插件示例
    ├── astrbot/main.py           # ⭐⭐ 官方插件示例
    ├── web_searcher/main.py      # Web 搜索插件
    └── builtin_commands/         # 内置指令
```

---

## 🔑 核心 API 速查表

### 1. 插件基类
**源码位置**: `astrbot/core/star/base.py`

```python
class Star(CommandParserMixin, PluginKVStoreMixin):
    """所有插件的父类"""

    def __init__(self, context: Context, config: dict | None = None):
        self.context = context

    async def initialize(self) -> None:
        """当插件被激活时调用"""

    async def terminate(self) -> None:
        """当插件被禁用、重载时调用"""

    async def text_to_image(self, text: str, return_url=True) -> str:
        """将文本转换为图片"""

    async def html_render(self, tmpl: str, data: dict, return_url=True) -> str:
        """渲染 HTML"""
```

### 2. Context 接口
**源码位置**: `astrbot/core/star/context.py`

```python
class Context:
    """暴露给插件的接口上下文"""

    # 属性
    provider_manager      # 模型提供商管理器
    platform_manager      # 平台适配器管理器
    conversation_manager  # 会话管理器
    persona_manager       # 人格管理器
    kb_manager           # 知识库管理器
    cron_manager         # 定时任务管理器

    # 方法
    def get_using_provider(self, umo: str | None = None) -> Provider | None:
        """获取当前使用的 LLM Provider"""

    def get_llm_tool_manager(self) -> FunctionToolManager:
        """获取 LLM 工具管理器"""

    def get_config(self, umo: str | None = None) -> AstrBotConfig:
        """获取配置"""

    async def send_message(self, session: str | MessageSession, message_chain: MessageChain) -> bool:
        """主动发送消息"""

    async def llm_generate(self, chat_provider_id: str, prompt: str, ...) -> LLMResponse:
        """调用 LLM 生成"""

    async def tool_loop_agent(self, event: AstrMessageEvent, chat_provider_id: str, ...) -> LLMResponse:
        """运行 Agent 循环"""

    def get_db(self) -> BaseDatabase:
        """获取数据库"""

    def get_platform_inst(self, platform_id: str) -> Platform | None:
        """获取平台适配器实例"""
```

### 3. AstrMessageEvent 事件类
**源码位置**: `astrbot/core/platform/astr_message_event.py`

```python
class AstrMessageEvent:
    # 属性
    message_str: str           # 纯文本消息
    message_obj: AstrBotMessage  # 完整消息对象
    platform_meta              # 平台信息
    session: MessageSession    # 会话信息
    unified_msg_origin: str    # 统一消息来源 ID
    role: str                  # "member" 或 "admin"
    is_wake: bool              # 是否唤醒
    call_llm: bool             # 是否调用 LLM

    # 获取信息方法
    def get_message_str(self) -> str:
    def get_messages(self) -> list[BaseMessageComponent]:
    def get_sender_id(self) -> str:
    def get_sender_name(self) -> str:
    def get_group_id(self) -> str:
    def is_private_chat(self) -> bool:
    def is_admin(self) -> bool:

    # 设置结果方法
    def set_result(self, result: MessageEventResult | str) -> None:
    def stop_event(self) -> None:
    def continue_event(self) -> None:

    # 创建结果方法
    def make_result(self) -> MessageEventResult:
    def plain_result(self, text: str) -> MessageEventResult:
    def image_result(self, url_or_path: str) -> MessageEventResult:

    # 发送消息方法
    async def send(self, message: MessageChain) -> None:
    async def send_typing(self) -> None:

    # LLM 请求方法
    def request_llm(self, prompt: str, ...) -> ProviderRequest:
```

### 4. MessageEventResult 返回结果
**源码位置**: `astrbot/core/message/message_event_result.py`

```python
class MessageEventResult(MessageChain):
    # 链式调用方法
    def message(self, message: str) -> "MessageEventResult":
        """添加文本消息"""

    def at(self, name: str, qq: str | int) -> "MessageEventResult":
        """添加 @ 消息"""

    def at_all(self) -> "MessageEventResult":
        """添加 @所有人"""

    def url_image(self, url: str) -> "MessageEventResult":
        """添加网络图片"""

    def file_image(self, path: str) -> "MessageEventResult":
        """添加本地图片"""

    def base64_image(self, base64_str: str) -> "MessageEventResult":
        """添加 base64 图片"""

    def use_t2i(self, use_t2i: bool) -> "MessageEventResult":
        """设置是否使用文本转图片"""

    # 事件控制
    def stop_event(self) -> "MessageEventResult":
    def continue_event(self) -> "MessageEventResult":
```

### 5. 装饰器
**源码位置**: `astrbot/core/star/register/star_handler.py`

```python
# 指令注册
@filter.command("command_name", alias={"别名1", "别名2"})
async def my_command(self, event: AstrMessageEvent):
    """指令说明"""

# 指令组（v4.19+ 新增）
@filter.command_group("group_name")
async def my_group(self, event: AstrMessageEvent, *args):
    """指令组说明"""

# LLM 工具注册
@filter.llm_tool(name="tool_name")  # name 可选
async def my_tool(self, event: AstrMessageEvent, arg: str) -> str:
    '''工具描述。

    Args:
        arg(string): 参数说明
    '''
    return "结果"

# 正则匹配
@filter.regex(r"pattern")
async def my_handler(self, event: AstrMessageEvent):
    pass

# 权限过滤
@filter.permission_type(filter.PermissionType.ADMIN)
async def admin_only(self, event: AstrMessageEvent):
    pass

# 平台过滤
@filter.platform_adapter_type(filter.PlatformAdapterType.AIocqhttp)
async def qq_only(self, event: AstrMessageEvent):
    pass

# 事件监听
@filter.on_llm_request()
async def on_llm_req(self, event: AstrMessageEvent, request: ProviderRequest):
    pass

@filter.on_llm_response()
async def on_llm_resp(self, event: AstrMessageEvent, response: LLMResponse):
    pass

@filter.on_astrbot_loaded()
async def on_loaded(self):
    pass

@filter.after_message_sent()
async def after_sent(self, event: AstrMessageEvent):
    pass

# 新增事件监听（v4.19+）
@filter.on_using_llm_tool()
async def on_using_tool(self, event: AstrMessageEvent, tool_name: str):
    """当 LLM 决定使用工具时触发"""
    pass

@filter.on_llm_tool_respond()
async def on_tool_respond(self, event: AstrMessageEvent, tool_name: str, result: str):
    """当工具执行完成时触发"""
    pass

@filter.on_waiting_llm_request()
async def on_waiting_req(self, event: AstrMessageEvent):
    """当等待 LLM 请求时触发"""
    pass

@filter.on_plugin_loaded()
async def on_plugin_load(self, plugin_name: str):
    """当插件加载时触发"""
    pass

@filter.on_plugin_unloaded()
async def on_plugin_unload(self, plugin_name: str):
    """当插件卸载时触发"""
    pass

@filter.on_plugin_error()
async def on_plugin_err(self, plugin_name: str, error: Exception):
    """当插件出错时触发"""
    pass

@filter.on_platform_loaded()
async def on_platform_load(self, platform_id: str):
    """当平台适配器加载时触发"""
    pass
```

---

## 📌 导入路径速查

### 推荐导入方式
```python
# 插件基类
from astrbot.api import star, logger
from astrbot.api.star import Context

# 事件与结果
from astrbot.api.event import AstrMessageEvent, MessageEventResult, filter

# 消息组件
from astrbot.api.message_components import Plain, Image, At, Reply

# 配置
from astrbot.core.config.astrbot_config import AstrBotConfig

# LLM 相关
from astrbot.api.provider import LLMResponse, ProviderRequest
```

---

## 🔍 按功能查找源码

### 开发指令插件
1. 阅读 `astrbot/core/star/filter/command.py` - 理解指令解析
2. 阅读 `astrbot/core/star/register/star_handler.py` - 理解 `@filter.command`
3. 参考 `astrbot/builtin_stars/builtin_commands/` - 内置指令示例

### 开发 LLM 工具
1. 阅读 `astrbot/core/star/register/star_handler.py` - 理解 `@filter.llm_tool`
2. 阅读 `astrbot/core/provider/func_tool_manager.py` - 理解工具管理
3. 参考 `astrbot/builtin_stars/web_searcher/main.py` - LLM 工具示例

### 处理消息组件
1. 阅读 `astrbot/core/message/components.py` - 所有组件定义
2. 阅读 `astrbot/core/platform/astrbot_message.py` - 消息结构

### 调用 LLM
1. 阅读 `astrbot/core/star/context.py` - `llm_generate()` 和 `tool_loop_agent()`
2. 阅读 `astrbot/core/provider/provider.py` - Provider 基类
3. 阅读 `astrbot/core/provider/entities.py` - LLMResponse, ProviderRequest

### 事件监听
1. 阅读 `astrbot/core/star/register/star_handler.py` - 所有事件装饰器
2. 阅读 `astrbot/core/star/star_handler.py` - EventType 枚举

---

## 📝 版本信息

- 适用于 AstrBot v4.x
- 源码来源：https://github.com/AstrBotDevs/AstrBot
- 最后更新：2025年

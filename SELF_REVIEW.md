# 插件代码自我审查

完成插件开发后，请按照以下清单进行自我审查，模仿 `astrpluginreviewer[bot]` 的审核逻辑。

---

## 📋 审查清单

### 1. 基础结构检查

- [ ] 文件中必须存在一个继承自 `Star` 的类
- [ ] 正确导入 `Star` 和 `Context`：
  ```python
  from astrbot.api import star, logger
  from astrbot.api.star import Context
  ```

### 2. 日志记录检查

- [ ] logger 必须从 `astrbot.api` 导入：
  ```python
  # ✅ 正确
  from astrbot.api import logger
  
  # ❌ 错误
  import logging
  logger = logging.getLogger(__name__)
  
  # ❌ 错误
  from loguru import logger
  ```

### 3. filter 装饰器检查

- [ ] filter 必须从 `astrbot.api.event` 导入：
  ```python
  # ✅ 正确
  from astrbot.api.event import filter
  
  # ❌ 错误（与 Python 内置 filter 冲突）
  from somewhere import filter
  ```

### 4. 事件监听器签名检查

- [ ] 所有事件监听器方法（除 `on_astrbot_loaded` 外）必须包含 `event` 参数：
  ```python
  # ✅ 正确
  @filter.command("test")
  async def test_command(self, event: AstrMessageEvent):
      ...
  
  # ❌ 错误（缺少 event 参数）
  @filter.command("test")
  async def test_command(self):
      ...
  ```

### 5. LLM 事件钩子检查

- [ ] `on_llm_request` 必须有三个参数：
  ```python
  # ✅ 正确
  @filter.on_llm_request()
  async def on_llm_req(self, event: AstrMessageEvent, req: ProviderRequest):
      ...
  ```

- [ ] `on_llm_response` 必须有三个参数：
  ```python
  # ✅ 正确
  @filter.on_llm_response()
  async def on_llm_resp(self, event: AstrMessageEvent, resp: LLMResponse):
      ...
  ```

### 6. 消息发送方式检查

- [ ] 在 `on_llm_request`、`on_llm_response`、`on_decorating_result`、`after_message_sent` 中：
  ```python
  # ✅ 正确
  await event.send(message_chain)
  
  # ❌ 错误（禁止使用 yield）
  yield event.plain_result("内容")
  ```

- [ ] 在普通指令中：
  ```python
  # ✅ 正确
  event.set_result(MessageEventResult().message("内容"))
  
  # ❌ 错误（旧版本方式）
  yield event.plain_result("内容")
  ```

### 7. 权限装饰器检查

- [ ] `@filter.permission_type` 不能用于 `@filter.llm_tool` 装饰的方法：
  ```python
  # ❌ 错误（无效组合）
  @filter.permission_type(filter.PermissionType.ADMIN)
  @filter.llm_tool(name="my_tool")
  async def my_tool(self, event: AstrMessageEvent):
      ...
  ```

### 8. 数据持久化检查

- [ ] 需要持久化数据时，使用 `StarTools.get_data_dir()`：
  ```python
  # ✅ 正确
  from astrbot.api.star import StarTools
  
  data_dir = StarTools.get_data_dir()  # 返回 Path 对象
  data_file = data_dir / "data.json"
  ```

### 9. 异步操作检查

- [ ] 网络 I/O 操作使用异步方式：
  ```python
  # ✅ 正确
  import aiohttp
  async with aiohttp.ClientSession() as session:
      async with session.get(url) as response:
          ...
  
  # ❌ 错误（同步阻塞）
  import requests
  response = requests.get(url)
  ```

### 10. 安全检查

- [ ] 无硬编码的敏感信息（Token、密码、API Key）
- [ ] 无不安全的 `pickle` 反序列化
- [ ] 无不安全的外部命令执行

---

## 🔍 常见错误对照表

| 错误 | 正确 | 说明 |
|------|------|------|
| `yield event.plain_result("内容")` | `event.set_result(MessageEventResult().message("内容"))` | 指令返回方式 |
| `return "内容"` | `event.set_result(MessageEventResult().message("内容"))` | 指令返回方式 |
| `import logging` | `from astrbot.api import logger` | 日志导入 |
| `requests.get(url)` | `aiohttp.ClientSession().get(url)` | 异步请求 |
| `@filter.permission_type` + `@filter.llm_tool` | 移除 permission_type | 无效组合 |

---

## 📝 自我审查报告模板

完成审查后，输出简要报告：

```markdown
## 🔍 自我审查报告

### main.py

**代码质量与编码规范**：
- （列出发现的问题）

**功能实现与逻辑正确性**：
- （列出发现的问题）

**安全漏洞与最佳实践**：
- （列出发现的问题）

**框架适应性检查**：
- （列出发现的问题）

### 检查结果
- [x] 基础结构：通过
- [x] 日志记录：通过
- [x] filter 装饰器：通过
- [x] 事件监听器签名：通过
- [x] LLM 事件钩子：通过
- [x] 消息发送方式：通过
- [x] 权限装饰器：通过
- [x] 数据持久化：通过
- [x] 异步操作：通过
- [x] 安全检查：通过

### 结论
代码已通过自我审查，可以交付。
```

---

## ⚠️ 特别注意

1. **Python 版本**：代码应兼容 Python 3.10
2. **运行环境**：代码运行在异步环境中
3. **不要跳过审查**：即使是简单的插件也要检查
4. **诚实记录问题**：发现问题要如实记录并修复
5. **测试验证**：审查不能替代实际测试

---

## 🔗 参考

- [astr-plugin-reviewer](https://github.com/AstrBotDevs/astr-plugin-reviewer) - 官方审核机器人

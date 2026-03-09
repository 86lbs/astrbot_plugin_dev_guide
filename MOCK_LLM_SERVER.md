# 模拟 LLM 服务

用于测试 AstrBot 的 LLM Tool 功能，无需运行真实的 LLM 模型。

## 为什么需要？

测试 LLM Tool 时，传统方式需要：
1. 安装 Ollama
2. 下载模型（几 GB）
3. 运行模型（占用大量内存和 CPU/GPU）

**这太浪费资源了！**

我们的方案：
- 创建一个"假"的 LLM API 服务
- 返回预设的响应，包含 tool_calls
- AstrBot 收到响应后会执行对应的 Tool
- **无需任何模型，只需几 KB 的 Python 脚本**

## 使用方法

### 1. 启动模拟服务

```bash
cd tools
python mock_llm_server.py
```

服务将在 `http://localhost:8000` 启动。

### 2. 配置 AstrBot

1. 进入 AstrBot 管理面板
2. 配置 OpenAI 兼容 API：
   - **API Base**: `http://localhost:8000/v1`
   - **API Key**: `mock-key`（任意值均可）
   - **Model**: `mock-model`
3. 保存配置

### 3. 测试 LLM Tool

1. 在插件中注册 LLM Tool
2. 用户发送消息
3. 模拟服务会自动返回 Tool 调用响应
4. AstrBot 执行 Tool

## 工作原理

```
用户消息 → AstrBot → 模拟服务 → 返回 tool_calls → AstrBot 执行 Tool
```

模拟服务会：
1. 接收 AstrBot 发送的聊天请求
2. 解析请求中的 `tools` 字段（插件注册的 LLM Tools）
3. 返回一个包含 `tool_calls` 的响应
4. AstrBot 收到响应后执行对应的 Tool

## 自定义 Tool 调用

编辑 `mock_llm_server.py` 中的 `TOOL_RESPONSES`：

```python
TOOL_RESPONSES = [
    {
        "tool_name": "get_weather",
        "arguments": '{"city": "北京"}'
    },
    {
        "tool_name": "search_web",
        "arguments": '{"query": "今天新闻"}'
    }
]
```

服务会按顺序尝试调用这些 Tool。

## 日志输出

```
[10:30:45] "POST /v1/chat/completions HTTP/1.1" 200 -
==================================================
收到聊天请求
消息数: 3
可用 Tools: ['get_weather', 'search_web']
最后消息: 北京天气怎么样...

触发 Tool 调用:
  Tool: get_weather
  参数: {"city": "北京"}
==================================================
```

## 与真实 LLM 的区别

| 特性 | 真实 LLM | 模拟服务 |
|------|----------|----------|
| 资源占用 | 几 GB 内存 | 几 MB |
| 响应内容 | 智能生成 | 预设响应 |
| Tool 选择 | 智能判断 | 固定顺序 |
| 适用场景 | 生产环境 | 开发测试 |

## 注意事项

1. 仅用于开发测试，不适用于生产环境
2. Tool 调用是预设的，不会根据消息内容智能判断
3. 如需测试多种 Tool 调用场景，可修改 `TOOL_RESPONSES`

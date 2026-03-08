# AstrBot 测试工具集

本目录包含完整的 AstrBot 插件开发和测试工具。

---

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `setup_local_env.sh` | 一键部署本地测试环境 |
| `start_astrbot.sh` | 启动 AstrBot 服务 |
| `stop_astrbot.sh` | 停止 AstrBot 服务 |
| `deploy_plugin.sh` | 部署插件到 AstrBot |
| `send_message.py` | 发送消息到 AstrBot |
| `send_message_stream.py` | 发送消息（流式响应） |
| `test_plugin.py` | 自动化插件测试 |
| `view_log.sh` | 查看日志 |

---

## 🚀 快速开始

### 1. 部署测试环境

```bash
# 一键部署（需要 root 权限）
bash setup_local_env.sh
```

这会自动安装：
- Ollama（本地 LLM）
- AstrBot
- 测试工具

### 2. 启动服务

```bash
# 启动 AstrBot
./start_astrbot.sh

# 查看日志
./view_log.sh -f
```

### 3. 部署插件

```bash
# 部署插件
./deploy_plugin.sh /path/to/your/plugin
```

### 4. 测试插件

```bash
# 发送测试消息
python send_message.py "/help"

# 流式响应
python send_message_stream.py "你好"

# 自动化测试
python test_plugin.py my_plugin
python test_plugin.py my_plugin --tool get_weather
```

---

## 📋 详细用法

### send_message.py

```bash
# 基本用法
python send_message.py "消息内容"

# 指定会话
python send_message.py "消息内容" --session abc123

# 安静模式（只输出响应）
python send_message.py "消息内容" -q
```

### send_message_stream.py

```bash
# 流式响应
python send_message_stream.py "今天天气怎么样？"
```

### test_plugin.py

```bash
# 测试插件
python test_plugin.py my_plugin

# 测试指令
python test_plugin.py my_plugin --command "/help" --command "/test"

# 测试 LLM Tool
python test_plugin.py my_plugin --tool get_weather

# 测试 LLM Tool（自定义触发消息）
python test_plugin.py my_plugin --tool get_weather --message "北京天气"
```

### view_log.sh

```bash
# 查看最后 50 行
./view_log.sh

# 查看最后 100 行
./view_log.sh -n 100

# 实时跟踪
./view_log.sh -f

# 只显示错误
./view_log.sh -e

# 过滤关键词
./view_log.sh -g "my_plugin"
```

---

## 🔧 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `ASTRBOT_DIR` | `/opt/astrbot` | AstrBot 安装目录 |
| `ASTRBOT_LOG` | `/opt/astrbot/logs/astrbot.log` | 日志文件路径 |
| `OLLAMA_MODEL` | `qwen2.5:3b` | Ollama 模型 |

---

## 📊 测试报告示例

```
检查测试环境...
✅ AstrBot 运行中
✅ 插件 my_plugin 已加载
✅ 创建会话: abc123-def456

============================================================
  开始测试
============================================================

测试指令: /help
✅ 指令测试: /help
   响应: 可用指令列表...

测试 LLM Tool: 今天天气怎么样？
预期工具: get_weather
✅ LLM Tool 测试: 今天天气怎么样？
   工具已调用: get_weather

============================================================
  测试报告
============================================================

✅ 指令测试: /help
✅ LLM Tool 测试: 今天天气怎么样？

------------------------------------------------------------
总计: 2 通过, 0 失败
============================================================
```

---

## 🔗 相关文档

- [本地测试环境配置](../LOCAL_TEST_ENVIRONMENT.md)
- [消息模拟器详解](../MESSAGE_SIMULATOR.md)
- [开发提示词 v5.0](../PROMPT_V5_LOCAL_SIMULATION.md)

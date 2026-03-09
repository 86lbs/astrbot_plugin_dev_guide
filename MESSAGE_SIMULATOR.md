# AstrBot 模拟消息端测试工具

本文档详细说明如何模拟发送消息到 AstrBot 进行测试。

---

## 📋 消息机制说明

AstrBot 的 WebChat 平台通过 HTTP API 接收消息：

```
┌─────────────┐     POST /api/chat/send     ┌─────────────┐
│ 测试脚本    │ ─────────────────────────▶  │  AstrBot    │
│             │     SSE 流式响应            │  WebChat    │
│             │ ◀─────────────────────────  │  Adapter    │
└─────────────┘                             └─────────────┘
```

### API 端点

| 端点 | 方法 | 用途 |
|------|------|------|
| `/api/chat/new_session` | GET | 创建新会话 |
| `/api/chat/send` | POST | 发送消息 |
| `/api/chat/sessions` | GET | 获取会话列表 |
| `/api/chat/get_session` | GET | 获取会话历史 |

---

## 🛠️ 测试工具脚本

### 1. 基础消息发送脚本

```python
#!/usr/bin/env python3
"""
send_message.py - 发送消息到 AstrBot

用法:
    python send_message.py "消息内容"
    python send_message.py "消息内容" --session <会话ID>
"""

import requests
import json
import sys
import argparse

ASTRBOT_URL = "http://localhost:6185"

def create_session():
    """创建新会话"""
    response = requests.get(f"{ASTRBOT_URL}/api/chat/new_session")
    data = response.json()
    if data.get("status") == "ok":
        return data["data"]["session_id"]
    return None

def send_message(message: str, session_id: str = None, timeout: int = 120):
    """
    发送消息到 AstrBot

    Args:
        message: 消息内容
        session_id: 会话ID（可选，不提供则自动创建）
        timeout: 超时时间（秒）

    Returns:
        完整的响应内容
    """
    # 如果没有提供 session_id，创建新会话
    if not session_id:
        session_id = create_session()
        if not session_id:
            return {"error": "Failed to create session"}
        print(f"创建新会话: {session_id}")

    # 发送消息
    url = f"{ASTRBOT_URL}/api/chat/send"
    headers = {"Content-Type": "application/json"}
    payload = {
        "message": message,
        "session_id": session_id,
        "enable_streaming": False  # 禁用流式，获取完整响应
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),
            timeout=timeout,
            stream=True  # SSE 流式响应
        )

        # 解析 SSE 响应
        full_response = []
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data = json.loads(line[6:])
                    full_response.append(data)

        return {
            "session_id": session_id,
            "messages": full_response
        }

    except requests.exceptions.Timeout:
        return {"error": "Request timeout"}
    except Exception as e:
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description='发送消息到 AstrBot')
    parser.add_argument('message', help='消息内容')
    parser.add_argument('--session', '-s', help='会话ID（可选）')
    parser.add_argument('--timeout', '-t', type=int, default=120, help='超时时间（秒）')

    args = parser.parse_args()

    print(f"发送消息: {args.message}")

    result = send_message(
        message=args.message,
        session_id=args.session,
        timeout=args.timeout
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
```

### 2. 流式消息接收脚本

```python
#!/usr/bin/env python3
"""
send_message_stream.py - 发送消息并实时显示流式响应

用法:
    python send_message_stream.py "消息内容"
"""

import requests
import json
import sys

ASTRBOT_URL = "http://localhost:6185"

def send_message_stream(message: str, session_id: str = None):
    """发送消息并实时显示流式响应"""

    # 创建会话
    if not session_id:
        response = requests.get(f"{ASTRBOT_URL}/api/chat/new_session")
        data = response.json()
        session_id = data["data"]["session_id"]
        print(f"[会话] {session_id}")

    # 发送消息
    url = f"{ASTRBOT_URL}/api/chat/send"
    headers = {"Content-Type": "application/json"}
    payload = {
        "message": message,
        "session_id": session_id,
        "enable_streaming": True  # 启用流式
    }

    print(f"[发送] {message}")
    print("-" * 50)

    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(payload),
        timeout=300,
        stream=True
    )

    full_text = ""

    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                try:
                    data = json.loads(line[6:])
                    msg_type = data.get("type")
                    msg_data = data.get("data", "")

                    if msg_type == "plain":
                        # 流式文本
                        print(msg_data, end="", flush=True)
                        full_text += msg_data
                    elif msg_type == "end":
                        print("\n" + "-" * 50)
                        print("[完成]")
                        break
                    elif msg_type == "tool_call":
                        # 工具调用
                        tool_info = json.loads(msg_data) if isinstance(msg_data, str) else msg_data
                        print(f"\n[工具调用] {tool_info.get('name', 'unknown')}")
                    elif msg_type == "tool_call_result":
                        # 工具返回
                        print(f"[工具返回]")

                except json.JSONDecodeError:
                    pass

    return full_text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python send_message_stream.py <消息内容>")
        sys.exit(1)

    message = " ".join(sys.argv[1:])
    send_message_stream(message)
```

### 3. 完整测试脚本

```python
#!/usr/bin/env python3
"""
test_plugin.py - 插件自动化测试脚本

用法:
    python test_plugin.py <插件名>
    python test_plugin.py <插件名> --tool <工具名>
"""

import requests
import json
import sys
import time
import argparse
import os

ASTRBOT_URL = "http://localhost:6185"
LOG_FILE = "/opt/astrbot/logs/astrbot.log"

class PluginTester:
    def __init__(self, plugin_name: str):
        self.plugin_name = plugin_name
        self.session_id = None
        self.results = []

    def check_astrbot_running(self) -> bool:
        """检查 AstrBot 是否运行"""
        try:
            response = requests.get(f"{ASTRBOT_URL}/", timeout=5)
            return response.status_code == 200
        except:
            return False

    def check_plugin_loaded(self) -> bool:
        """检查插件是否加载"""
        try:
            with open(LOG_FILE, 'r') as f:
                content = f.read()
            return f"Plugin {self.plugin_name}" in content or \
                   f"plugin {self.plugin_name}" in content.lower()
        except:
            return False

    def check_llm_tool_registered(self, tool_name: str) -> bool:
        """检查 LLM Tool 是否注册"""
        try:
            with open(LOG_FILE, 'r') as f:
                content = f.read()
            return f"Registered LLM tool: {tool_name}" in content or \
                   f"llm_tool: {tool_name}" in content.lower()
        except:
            return False

    def create_session(self) -> str:
        """创建新会话"""
        response = requests.get(f"{ASTRBOT_URL}/api/chat/new_session")
        data = response.json()
        if data.get("status") == "ok":
            self.session_id = data["data"]["session_id"]
            return self.session_id
        return None

    def send_message(self, message: str, timeout: int = 120) -> dict:
        """发送消息"""
        if not self.session_id:
            self.create_session()

        url = f"{ASTRBOT_URL}/api/chat/send"
        headers = {"Content-Type": "application/json"}
        payload = {
            "message": message,
            "session_id": self.session_id,
            "enable_streaming": False
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(payload),
                timeout=timeout,
                stream=True
            )

            full_response = []
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data = json.loads(line[6:])
                        full_response.append(data)

            return {"success": True, "messages": full_response}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def test_command(self, command: str, expected_contains: str = None) -> dict:
        """测试指令"""
        result = {
            "test": f"指令测试: {command}",
            "status": "unknown",
            "response": None,
            "error": None
        }

        print(f"\n测试指令: {command}")

        response = self.send_message(command)
        result["response"] = response

        if not response.get("success"):
            result["status"] = "failed"
            result["error"] = response.get("error", "Unknown error")
        elif expected_contains:
            response_str = json.dumps(response, ensure_ascii=False)
            if expected_contains in response_str:
                result["status"] = "passed"
            else:
                result["status"] = "failed"
                result["error"] = f"响应不包含预期内容: {expected_contains}"
        else:
            result["status"] = "passed"

        status_icon = "✅" if result["status"] == "passed" else "❌"
        print(f"{status_icon} {result['test']}")
        if result.get("error"):
            print(f"   错误: {result['error']}")

        self.results.append(result)
        return result

    def test_llm_tool(self, message: str, tool_name: str) -> dict:
        """测试 LLM Tool"""
        result = {
            "test": f"LLM Tool 测试: {message}",
            "tool": tool_name,
            "status": "unknown",
            "tool_called": False,
            "response": None
        }

        print(f"\n测试 LLM Tool: {message}")

        # 记录日志大小
        log_size_before = os.path.getsize(LOG_FILE) if os.path.exists(LOG_FILE) else 0

        # 发送消息
        response = self.send_message(message, timeout=180)
        result["response"] = response

        # 等待处理
        time.sleep(2)

        # 检查日志中是否有工具调用
        try:
            with open(LOG_FILE, 'r') as f:
                f.seek(log_size_before)
                new_logs = f.read()

            if tool_name in new_logs and "tool" in new_logs.lower():
                result["tool_called"] = True
                result["status"] = "passed"
            else:
                result["status"] = "failed"
                result["error"] = "工具未被调用"

        except Exception as e:
            result["status"] = "failed"
            result["error"] = f"日志读取失败: {e}"

        status_icon = "✅" if result["status"] == "passed" else "❌"
        print(f"{status_icon} {result['test']}")
        if result.get("error"):
            print(f"   错误: {result['error']}")

        self.results.append(result)
        return result

    def print_report(self):
        """打印测试报告"""
        print("\n" + "=" * 60)
        print("  测试报告")
        print("=" * 60)

        passed = sum(1 for r in self.results if r["status"] == "passed")
        failed = sum(1 for r in self.results if r["status"] == "failed")

        for r in self.results:
            status_icon = "✅" if r["status"] == "passed" else "❌"
            print(f"\n{status_icon} {r['test']}")
            if r.get("error"):
                print(f"   错误: {r['error']}")

        print("\n" + "-" * 60)
        print(f"总计: {passed} 通过, {failed} 失败")
        print("=" * 60)

        return failed == 0

def main():
    parser = argparse.ArgumentParser(description='AstrBot 插件测试工具')
    parser.add_argument('plugin_name', help='插件名称')
    parser.add_argument('--tool', '-t', help='LLM Tool 名称')
    parser.add_argument('--command', '-c', action='append', help='测试指令（可多次使用）')

    args = parser.parse_args()

    tester = PluginTester(args.plugin_name)

    # 检查环境
    print("检查测试环境...")

    if not tester.check_astrbot_running():
        print("❌ AstrBot 未运行")
        print("   请先启动 AstrBot: cd /opt/astrbot && python main.py")
        sys.exit(1)
    print("✅ AstrBot 运行中")

    if not tester.check_plugin_loaded():
        print(f"⚠️ 插件 {args.plugin_name} 未加载")
    else:
        print(f"✅ 插件 {args.plugin_name} 已加载")

    # 创建会话
    session_id = tester.create_session()
    print(f"✅ 创建会话: {session_id}")

    # 运行测试
    print("\n" + "=" * 60)
    print("  开始测试")
    print("=" * 60)

    # 测试指令
    if args.command:
        for cmd in args.command:
            tester.test_command(cmd)
    else:
        # 默认测试 help 指令
        tester.test_command("/help")

    # 测试 LLM Tool
    if args.tool:
        tester.test_llm_tool("今天天气怎么样？", args.tool)

    # 打印报告
    success = tester.print_report()

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
```

---

## 📋 使用示例

### 1. 发送简单消息

```bash
# 发送消息（自动创建会话）
python send_message.py "你好"

# 指定会话ID
python send_message.py "继续对话" --session abc123
```

### 2. 测试指令

```bash
# 测试 /help 指令
python send_message.py "/help"

# 测试自定义指令
python send_message.py "/test arg1 arg2"
```

### 3. 测试 LLM Tool

```bash
# 发送能触发工具的消息
python send_message_stream.py "今天北京天气怎么样？"

# 使用自动化测试脚本
python test_plugin.py weather_plugin --tool get_weather
```

### 4. 完整插件测试

```bash
# 测试插件的所有功能
python test_plugin.py my_plugin \
    --command "/help" \
    --command "/test" \
    --tool my_tool
```

---

## 📊 测试输出示例

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

测试 LLM Tool: 今天天气怎么样？
[工具调用] get_weather
[工具返回]
✅ LLM Tool 测试: 今天天气怎么样？

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

## 🔧 高级用法

### 1. 批量测试

```bash
#!/bin/bash
# batch_test.sh

PLUGINS=("plugin1" "plugin2" "plugin3")

for plugin in "${PLUGINS[@]}"; do
    echo "测试插件: $plugin"
    python test_plugin.py "$plugin"
done
```

### 2. CI/CD 集成

```yaml
# .github/workflows/test.yml
name: Plugin Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: pip install requests

      - name: Start AstrBot
        run: |
          cd /opt/astrbot
          python main.py &
          sleep 10

      - name: Run tests
        run: python test_plugin.py my_plugin --tool my_tool
```

---

## 📝 注意事项

1. **会话管理**：每次测试建议使用新会话，避免历史消息干扰
2. **超时设置**：LLM Tool 测试需要较长超时时间（建议 180 秒以上）
3. **日志检查**：工具调用信息在日志中，不在 HTTP 响应中
4. **流式响应**：默认使用 SSE 流式响应，需要特殊处理

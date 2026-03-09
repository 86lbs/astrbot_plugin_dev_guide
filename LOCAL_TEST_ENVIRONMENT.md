# AstrBot 本地全流程测试环境

本文档描述如何在虚拟机上搭建完全自包含的测试环境，无需真实 LLM API 和消息平台。

---

## 🏗️ 架构概览

```
┌─────────────────────────────────────────────────────────────────┐
│                     本地测试环境                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │ 模拟消息端  │───▶│  AstrBot    │───▶│ 模拟 LLM    │        │
│  │ test_client│    │  :6185      │    │ Ollama:11434│        │
│  └─────────────┘    └─────────────┘    └─────────────┘        │
│        │                  │                   │                │
│        │                  ▼                   │                │
│        │           ┌─────────────┐            │                │
│        │           │   插  件    │◀───────────┘                │
│        │           │  (被测试)   │                             │
│        │           └─────────────┘                             │
│        │                  │                                     │
│        └──────────────────┘                                     │
│                           │                                     │
│                           ▼                                     │
│                    ┌─────────────┐                              │
│                    │  测试报告   │                              │
│                    └─────────────┘                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 组件说明

| 组件 | 端口 | 用途 |
|------|------|------|
| AstrBot | 6185 | 被测系统 |
| Ollama | 11434 | 本地 LLM 服务 |
| 测试脚本 | - | 模拟消息发送 |

---

## 🚀 一键部署脚本

```bash
#!/bin/bash
# setup_local_test_env.sh
# 在虚拟机上运行此脚本

set -e

echo "=========================================="
echo "  AstrBot 本地测试环境部署"
echo "=========================================="

# ==================== 1. 安装系统依赖 ====================
echo "[1/5] 安装系统依赖..."
apt update && apt install -y \
    python3 python3-pip python3-venv \
    git curl wget \
    ffmpeg

# ==================== 2. 安装 Ollama (本地 LLM) ====================
echo "[2/5] 安装 Ollama..."
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.com/install.sh | sh
fi

# 启动 Ollama 服务
ollama serve &
sleep 5

# 下载小模型（用于测试，约 4GB）
echo "下载测试用 LLM 模型（qwen2.5:3b）..."
ollama pull qwen2.5:3b

# ==================== 3. 部署 AstrBot ====================
echo "[3/5] 部署 AstrBot..."
mkdir -p /opt/astrbot
cd /opt/astrbot

if [ ! -d "astrbot" ]; then
    git clone https://github.com/AstrBotDevs/AstrBot.git .
fi

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 创建目录
mkdir -p data/plugins data/config logs

# ==================== 4. 配置 AstrBot ====================
echo "[4/5] 配置 AstrBot..."

# 创建配置文件，连接本地 Ollama
cat > data/cmd_config.json << 'EOF'
{
  "platform_settings": [
    {
      "id": "webchat",
      "type": "webchat",
      "enable": true
    }
  ],
  "provider_settings": [
    {
      "id": "ollama_local",
      "type": "openai_chat_completion",
      "api_base": "http://localhost:11434/v1",
      "api_key": "ollama",
      "model_config": {
        "model": "qwen2.5:3b"
      }
    }
  ],
  "provider_ltm_settings": {
    "group_icl_enable": false,
    "active_reply": {
      "enable": false
    }
  }
}
EOF

# ==================== 5. 创建测试工具 ====================
echo "[5/5] 创建测试工具..."

# 创建测试脚本目录
mkdir -p /opt/astrbot_test

# 创建消息模拟脚本
cat > /opt/astrbot_test/send_message.py << 'PYEOF'
#!/usr/bin/env python3
"""
模拟发送消息到 AstrBot
"""
import requests
import json
import sys

ASTRBOT_URL = "http://localhost:6185"

def send_message(message: str, session: str = "test_session"):
    """发送消息到 AstrBot"""
    # 方式一：通过 WebUI API（如果支持）
    try:
        response = requests.post(
            f"{ASTRBOT_URL}/api/chat",
            json={
                "message": message,
                "session_id": session
            },
            timeout=60
        )
        return response.json()
    except Exception as e:
        print(f"发送失败: {e}")
        return None

def check_health():
    """检查 AstrBot 是否运行"""
    try:
        response = requests.get(f"{ASTRBOT_URL}/", timeout=5)
        return response.status_code == 200
    except:
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python send_message.py <消息内容>")
        sys.exit(1)

    message = " ".join(sys.argv[1:])

    if not check_health():
        print("❌ AstrBot 未运行")
        sys.exit(1)

    print(f"发送消息: {message}")
    result = send_message(message)
    if result:
        print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
PYEOF

# 创建完整测试脚本
cat > /opt/astrbot_test/test_plugin.py << 'PYEOF'
#!/usr/bin/env python3
"""
插件测试脚本 - 全流程测试
"""
import requests
import json
import time
import sys
import os

ASTRBOT_URL = "http://localhost:6185"
LOG_FILE = "/opt/astrbot/logs/astrbot.log"

class PluginTester:
    def __init__(self, plugin_name: str):
        self.plugin_name = plugin_name
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
            return f"Plugin {self.plugin_name} loaded" in content
        except:
            return False

    def check_llm_tool_registered(self, tool_name: str) -> bool:
        """检查 LLM Tool 是否注册"""
        try:
            with open(LOG_FILE, 'r') as f:
                content = f.read()
            return f"Registered LLM tool: {tool_name}" in content
        except:
            return False

    def send_message(self, message: str) -> dict:
        """发送消息"""
        try:
            response = requests.post(
                f"{ASTRBOT_URL}/api/chat",
                json={"message": message, "session_id": "test"},
                timeout=120
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def check_tool_called(self, tool_name: str) -> bool:
        """检查工具是否被调用"""
        try:
            with open(LOG_FILE, 'r') as f:
                content = f.read()
            return tool_name in content and "tool" in content.lower()
        except:
            return False

    def test_command(self, command: str, expected_contains: str = None) -> dict:
        """测试指令"""
        result = {
            "test": f"指令测试: {command}",
            "status": "unknown",
            "response": None,
            "error": None
        }

        try:
            response = self.send_message(command)
            result["response"] = response

            if "error" in response:
                result["status"] = "failed"
                result["error"] = response["error"]
            elif expected_contains:
                response_str = json.dumps(response, ensure_ascii=False)
                if expected_contains in response_str:
                    result["status"] = "passed"
                else:
                    result["status"] = "failed"
                    result["error"] = f"响应不包含预期内容: {expected_contains}"
            else:
                result["status"] = "passed"

        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)

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

        try:
            # 记录日志大小
            log_size_before = os.path.getsize(LOG_FILE) if os.path.exists(LOG_FILE) else 0

            # 发送消息
            response = self.send_message(message)
            result["response"] = response

            # 等待处理
            time.sleep(2)

            # 检查日志中是否有工具调用
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
            result["error"] = str(e)

        self.results.append(result)
        return result

    def print_report(self):
        """打印测试报告"""
        print("\n" + "=" * 50)
        print("  测试报告")
        print("=" * 50)

        passed = sum(1 for r in self.results if r["status"] == "passed")
        failed = sum(1 for r in self.results if r["status"] == "failed")

        for r in self.results:
            status_icon = "✅" if r["status"] == "passed" else "❌"
            print(f"\n{status_icon} {r['test']}")
            if r.get("error"):
                print(f"   错误: {r['error']}")

        print("\n" + "-" * 50)
        print(f"总计: {passed} 通过, {failed} 失败")
        print("=" * 50)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python test_plugin.py <插件名> [工具名]")
        sys.exit(1)

    plugin_name = sys.argv[1]
    tool_name = sys.argv[2] if len(sys.argv) > 2 else None

    tester = PluginTester(plugin_name)

    # 检查环境
    print("检查测试环境...")
    if not tester.check_astrbot_running():
        print("❌ AstrBot 未运行")
        sys.exit(1)
    print("✅ AstrBot 运行中")

    if not tester.check_plugin_loaded():
        print(f"⚠️ 插件 {plugin_name} 未加载")
    else:
        print(f"✅ 插件 {plugin_name} 已加载")

    # 运行测试
    print("\n开始测试...")

    # 测试指令
    tester.test_command("/help", "help")

    # 测试 LLM Tool（如果指定）
    if tool_name:
        tester.test_llm_tool("今天天气怎么样？", tool_name)

    # 打印报告
    tester.print_report()
PYEOF

chmod +x /opt/astrbot_test/*.py

echo ""
echo "=========================================="
echo "  部署完成！"
echo "=========================================="
echo ""
echo "启动命令:"
echo "  1. 启动 Ollama:    ollama serve"
echo "  2. 启动 AstrBot:   cd /opt/astrbot && source venv/bin/activate && python main.py"
echo ""
echo "测试命令:"
echo "  发送消息:    python /opt/astrbot_test/send_message.py '你好'"
echo "  测试插件:    python /opt/astrbot_test/test_plugin.py <插件名>"
echo ""
echo "WebUI:        http://localhost:6185"
echo "=========================================="
```

---

## 🧪 测试流程

### 1. 启动服务

```bash
# 终端 1：启动 Ollama
ollama serve

# 终端 2：启动 AstrBot
cd /opt/astrbot && source venv/bin/activate && python main.py
```

### 2. 部署插件

```bash
# 复制插件
cp -r /workspace/my_plugin /opt/astrbot/data/plugins/

# 重启 AstrBot
pkill -f "python main.py"
cd /opt/astrbot && source venv/bin/activate && python main.py &
```

### 3. 测试指令

```bash
# 发送测试消息
python /opt/astrbot_test/send_message.py "/test"

# 查看响应
```

### 4. 测试 LLM Tool

```bash
# 发送能触发工具的消息
python /opt/astrbot_test/send_message.py "今天北京天气怎么样？"

# 查看日志确认工具被调用
tail -50 /opt/astrbot/logs/astrbot.log | grep -i tool
```

### 5. 自动化测试

```bash
# 运行完整测试脚本
python /opt/astrbot_test/test_plugin.py my_plugin get_weather
```

---

## 📊 测试报告示例

```
==================================================
  测试报告
==================================================

✅ 指令测试: /help
✅ 指令测试: /test
✅ LLM Tool 测试: 今天北京天气怎么样？
   工具: get_weather
   工具已调用: True

--------------------------------------------------
总计: 3 通过, 0 失败
==================================================
```

---

## 🔧 高级：Mock LLM（可选）

如果不想用真实 LLM，可以用 Mock 服务：

```python
# /opt/astrbot_test/mock_llm_server.py
"""
模拟 LLM 服务器 - 返回固定响应
"""
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.json
    messages = data.get('messages', [])
    tools = data.get('tools', [])

    # 如果有工具，模拟调用
    if tools:
        # 返回工具调用
        return jsonify({
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [{
                        "id": "call_123",
                        "type": "function",
                        "function": {
                            "name": tools[0]["function"]["name"],
                            "arguments": '{"query": "test"}'
                        }
                    }]
                }
            }]
        })

    # 普通回复
    return jsonify({
        "choices": [{
            "message": {
                "role": "assistant",
                "content": "这是一个模拟的 LLM 响应。"
            }
        }]
    })

if __name__ == '__main__':
    app.run(port=11434)
```

---

## 📁 目录结构

```
/opt/
├── astrbot/                    # AstrBot 主目录
│   ├── main.py
│   ├── data/
│   │   ├── plugins/           # 插件目录
│   │   └── config/            # 配置目录
│   └── logs/                  # 日志目录
│
└── astrbot_test/              # 测试工具目录
    ├── send_message.py        # 发送消息脚本
    ├── test_plugin.py         # 插件测试脚本
    └── mock_llm_server.py     # Mock LLM 服务（可选）
```

---

## ✅ 优势总结

| 特性 | 传统方式 | 本地模拟 |
|------|----------|----------|
| LLM API | 需要 API Key（花钱） | ✅ 本地 Ollama（免费） |
| 消息平台 | 需要真实平台 | ✅ 模拟发送 |
| 测试速度 | 受网络影响 | ✅ 本地秒级响应 |
| 可重复性 | 依赖外部服务 | ✅ 完全可控 |
| 自动化 | 困难 | ✅ 完全自动化 |
| CI/CD | 难以集成 | ✅ 易于集成 |

---

## 🚀 Agent 使用方式

将以下内容添加到 Agent 提示词：

```markdown
## 🧪 本地测试环境

你有完全自包含的测试环境：

### 服务状态
- AstrBot: http://localhost:6185
- Ollama: http://localhost:11434
- 模型: qwen2.5:3b

### 测试命令
```bash
# 发送消息
python /opt/astrbot_test/send_message.py "消息内容"

# 测试插件
python /opt/astrbot_test/test_plugin.py <插件名> [工具名]

# 查看日志
tail -100 /opt/astrbot/logs/astrbot.log
```

### 测试流程
1. 部署插件 → 重启服务 → 发送测试消息 → 检查日志
```

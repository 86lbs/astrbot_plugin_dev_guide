# AstrBot 插件开发测试环境配置指南

本文档描述如何为 Agent 配置一个可自主操控的 AstrBot 测试环境。

---

## 🎯 目标

让 Agent 能够：
1. 自主部署 AstrBot 服务
2. 自主安装/更新插件
3. 自主测试插件功能
4. 自主查看日志和错误
5. 形成开发-测试-修复的闭环

---

## 📁 环境架构

```
┌─────────────────────────────────────────────────────────┐
│                    Agent 工作空间                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │ 插件源码    │───▶│ AstrBot     │───▶│ 测试结果    │ │
│  │ /plugins/   │    │ 测试环境    │    │ /logs/      │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
│         │                  │                   │       │
│         │                  ▼                   │       │
│         │           ┌─────────────┐            │       │
│         └──────────▶│ 运行/重载   │◀───────────┘       │
│                      │ 查看日志    │                    │
│                      └─────────────┘                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🖥️ 虚拟机配置要求

### 最低配置
| 项目 | 要求 |
|------|------|
| CPU | 2 核 |
| 内存 | 4 GB |
| 磁盘 | 20 GB |
| 系统 | Ubuntu 22.04 / Debian 12 |
| Python | 3.9+ |

### 推荐配置
| 项目 | 要求 |
|------|------|
| CPU | 4 核 |
| 内存 | 8 GB |
| 磁盘 | 40 GB |

---

## 🚀 环境部署脚本

### 1. 一键部署脚本

```bash
#!/bin/bash
# deploy_astrbot_test_env.sh
# 在虚拟机上运行此脚本

set -e

echo "=== AstrBot 测试环境部署 ==="

# 1. 安装依赖
apt update && apt install -y \
    python3 python3-pip python3-venv \
    git curl wget \
    ffmpeg  # 可选，用于语音功能

# 2. 创建工作目录
mkdir -p /opt/astrbot
cd /opt/astrbot

# 3. 克隆 AstrBot
git clone https://github.com/AstrBotDevs/AstrBot.git .
# 或者使用稳定版本
# wget https://github.com/AstrBotDevs/AstrBot/releases/download/vX.X.X/astrbot.tar.gz

# 4. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 5. 安装依赖
pip install -r requirements.txt

# 6. 创建目录结构
mkdir -p data/plugins
mkdir -p data/config
mkdir -p logs

# 7. 创建测试用配置文件
cat > data/cmd_config.json << 'EOF'
{
  "platform_settings": [],
  "provider_settings": [],
  "plugin_settings": {}
}
EOF

echo "=== 部署完成 ==="
echo "运行命令: cd /opt/astrbot && source venv/bin/activate && python main.py"
```

### 2. Agent 可用的命令集

```bash
# 启动 AstrBot（后台运行）
cd /opt/astrbot && source venv/bin/activate && nohup python main.py > logs/astrbot.log 2>&1 &

# 查看日志
tail -100 /opt/astrbot/logs/astrbot.log

# 实时查看日志
tail -f /opt/astrbot/logs/astrbot.log

# 停止 AstrBot
pkill -f "python main.py"

# 重启 AstrBot
pkill -f "python main.py" && sleep 2 && cd /opt/astrbot && source venv/bin/activate && nohup python main.py > logs/astrbot.log 2>&1 &

# 安装插件（将插件复制到插件目录）
cp -r /path/to/plugin /opt/astrbot/data/plugins/

# 查看插件列表
ls -la /opt/astrbot/data/plugins/

# 查看插件配置
cat /opt/astrbot/data/config/*_config.json
```

---

## 🤖 Agent 操作接口

### 方式一：SSH 远程操作

Agent 通过 SSH 连接虚拟机执行命令：

```python
# Agent 可执行的命令示例
import subprocess

def run_on_vm(command: str) -> str:
    """在虚拟机上执行命令"""
    result = subprocess.run(
        ["ssh", "user@astrbot-vm", command],
        capture_output=True,
        text=True
    )
    return result.stdout + result.stderr

# 使用示例
run_on_vm("tail -50 /opt/astrbot/logs/astrbot.log")
run_on_vm("cp -r /tmp/my_plugin /opt/astrbot/data/plugins/")
run_on_vm("pkill -f 'python main.py'")
```

### 方式二：本地 Docker 容器

```bash
# 构建 AstrBot 测试镜像
docker build -t astrbot-test .

# 运行容器
docker run -d --name astrbot-test \
    -v ./plugins:/opt/astrbot/data/plugins \
    -v ./logs:/opt/astrbot/logs \
    -p 6185:6185 \
    astrbot-test

# Agent 执行命令
docker exec astrbot-test tail -50 /opt/astrbot/logs/astrbot.log
docker exec astrbot-test ls -la /opt/astrbot/data/plugins/
docker restart astrbot-test
```

### 方式三：本地进程（最简单）

如果 Agent 已经在虚拟机上运行：

```bash
# 直接执行
cd /opt/astrbot && python main.py
```

---

## 📋 Agent 测试工作流

### 完整的测试流程

```
1. 编写插件代码
   ↓
2. 复制插件到测试环境
   cp -r ./my_plugin /opt/astrbot/data/plugins/
   ↓
3. 重启/重载 AstrBot
   pkill -f "python main.py" && sleep 2 && python main.py &
   ↓
4. 查看启动日志（检查是否有语法错误、导入错误）
   tail -100 /opt/astrbot/logs/astrbot.log
   ↓
5. 如果有错误 → 修复代码 → 回到步骤 2
   ↓
6. 测试插件功能
   - 发送测试消息
   - 查看响应日志
   ↓
7. 如果功能异常 → 查看错误日志 → 修复 → 回到步骤 2
   ↓
8. 测试通过 → 完成
```

---

## 🔧 测试消息发送

### 方式一：使用 AstrBot WebUI

```bash
# AstrBot 默认 WebUI 端口
http://localhost:6185
```

### 方式二：使用 API（如果有）

```bash
# 发送测试消息
curl -X POST http://localhost:6185/api/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "/test_command", "session": "test"}'
```

### 方式三：模拟平台消息

创建测试脚本：

```python
# test_plugin.py
import asyncio
import sys
sys.path.insert(0, '/opt/astrbot')

from astrbot.core.platform.astr_message_event import AstrMessageEvent
from astrbot.core.platform.astrbot_message import AstrBotMessage

async def test_command():
    """模拟发送指令测试"""
    # 构造测试消息
    msg = AstrBotMessage()
    msg.message_str = "/test_command arg1 arg2"

    # 调用插件处理
    # ... 具体实现

if __name__ == "__main__":
    asyncio.run(test_command())
```

---

## 📊 日志分析

### 关键日志位置

| 日志文件 | 内容 |
|----------|------|
| `logs/astrbot.log` | 主日志 |
| `logs/error.log` | 错误日志（如果有） |
| 控制台输出 | 启动信息、实时日志 |

### 常见错误模式

```bash
# 查找语法错误
grep -i "SyntaxError\|IndentationError" logs/astrbot.log

# 查找导入错误
grep -i "ImportError\|ModuleNotFoundError" logs/astrbot.log

# 查找插件加载错误
grep -i "plugin\|star" logs/astrbot.log | grep -i "error\|fail"

# 查找特定插件日志
grep "my_plugin" logs/astrbot.log
```

---

## 🎯 Agent 提示词集成

将以下内容添加到 Agent 提示词中：

```markdown
## 🧪 测试环境

你拥有一台 AstrBot 测试虚拟机，可以自主测试插件。

### 可用命令

```bash
# 部署插件
cp -r /workspace/my_plugin /opt/astrbot/data/plugins/

# 重启服务
pkill -f "python main.py" && sleep 2 && cd /opt/astrbot && python main.py &

# 查看日志
tail -100 /opt/astrbot/logs/astrbot.log

# 查找错误
grep -i "error" /opt/astrbot/logs/astrbot.log
```

### 测试流程

1. 编写代码后，必须部署测试
2. 查看日志确认无错误
3. 如果有错误，分析并修复
4. 重复直到测试通过

**记住：代码必须在测试环境中验证后才能交付！**
```

---

## 🔐 安全考虑

1. **隔离环境** - 测试虚拟机应与生产环境隔离
2. **权限控制** - Agent 只能操作指定目录
3. **资源限制** - 设置 CPU/内存上限
4. **网络隔离** - 限制外网访问（如需要）

---

## 📝 版本信息

- 适用于 AstrBot v4.x
- 测试环境操作系统：Ubuntu 22.04 / Debian 12

#!/bin/bash
# ============================================================
# AstrBot 本地测试环境一键部署脚本
# ============================================================
# 用法: bash setup_local_env.sh
# ============================================================

set -e

echo "=========================================="
echo "  AstrBot 本地测试环境部署"
echo "=========================================="

# 配置
ASTRBOT_DIR="${ASTRBOT_DIR:-/opt/astrbot}"
TEST_DIR="${TEST_DIR:-/opt/astrbot_test}"
OLLAMA_MODEL="${OLLAMA_MODEL:-qwen2.5:3b}"

# ==================== 1. 安装系统依赖 ====================
echo ""
echo "[1/6] 安装系统依赖..."
apt update && apt install -y \
    python3 python3-pip python3-venv \
    git curl wget \
    ffmpeg

# ==================== 2. 安装 Ollama ====================
echo ""
echo "[2/6] 安装 Ollama (本地 LLM)..."
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.com/install.sh | sh
fi

# 启动 Ollama 服务
echo "启动 Ollama 服务..."
ollama serve &
sleep 5

# 下载模型
echo "下载 LLM 模型: ${OLLAMA_MODEL}..."
ollama pull ${OLLAMA_MODEL}

# ==================== 3. 部署 AstrBot ====================
echo ""
echo "[3/6] 部署 AstrBot..."
mkdir -p "${ASTRBOT_DIR}"
cd "${ASTRBOT_DIR}"

# 从 GitHub 克隆
if [ ! -d ".git" ]; then
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
echo ""
echo "[4/6] 配置 AstrBot..."

# 创建配置文件
cat > data/cmd_config.json << EOF
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
        "model": "${OLLAMA_MODEL}"
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

# ==================== 5. 安装测试工具 ====================
echo ""
echo "[5/6] 安装测试工具..."
mkdir -p "${TEST_DIR}"

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 复制测试脚本
cp "${SCRIPT_DIR}/send_message.py" "${TEST_DIR}/"
cp "${SCRIPT_DIR}/send_message_stream.py" "${TEST_DIR}/"
cp "${SCRIPT_DIR}/test_plugin.py" "${TEST_DIR}/"
cp "${SCRIPT_DIR}/start_astrbot.sh" "${TEST_DIR}/"
cp "${SCRIPT_DIR}/stop_astrbot.sh" "${TEST_DIR}/"

chmod +x "${TEST_DIR}"/*.py "${TEST_DIR}"/*.sh

# 安装 Python 依赖
pip install requests

# ==================== 6. 完成 ====================
echo ""
echo "[6/6] 部署完成!"
echo ""
echo "=========================================="
echo "  使用说明"
echo "=========================================="
echo ""
echo "启动服务:"
echo "  ${TEST_DIR}/start_astrbot.sh"
echo ""
echo "停止服务:"
echo "  ${TEST_DIR}/stop_astrbot.sh"
echo ""
echo "发送消息:"
echo "  python ${TEST_DIR}/send_message.py '你好'"
echo ""
echo "测试插件:"
echo "  python ${TEST_DIR}/test_plugin.py <插件名>"
echo ""
echo "WebUI:"
echo "  http://localhost:6185"
echo ""
echo "=========================================="

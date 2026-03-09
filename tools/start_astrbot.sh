#!/bin/bash
# ============================================================
# 启动 AstrBot 服务
# ============================================================

ASTRBOT_DIR="${ASTRBOT_DIR:-/opt/astrbot}"

# 检查是否已运行
if pgrep -f "python main.py" > /dev/null; then
    echo "AstrBot 已在运行中"
    exit 0
fi

cd "${ASTRBOT_DIR}"
source venv/bin/activate

echo "启动 AstrBot..."
nohup python main.py > logs/astrbot.log 2>&1 &

sleep 3

if pgrep -f "python main.py" > /dev/null; then
    echo "✅ AstrBot 启动成功"
    echo "WebUI: http://localhost:6185"
    echo "日志: ${ASTRBOT_DIR}/logs/astrbot.log"
else
    echo "❌ AstrBot 启动失败"
    echo "查看日志: tail -100 ${ASTRBOT_DIR}/logs/astrbot.log"
    exit 1
fi

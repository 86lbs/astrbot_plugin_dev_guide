#!/bin/bash
# ============================================================
# 停止 AstrBot 服务
# ============================================================

echo "停止 AstrBot..."
pkill -f "python main.py"

sleep 2

if pgrep -f "python main.py" > /dev/null; then
    echo "⚠️ AstrBot 仍在运行，强制终止..."
    pkill -9 -f "python main.py"
    sleep 1
fi

if pgrep -f "python main.py" > /dev/null; then
    echo "❌ 无法停止 AstrBot"
    exit 1
else
    echo "✅ AstrBot 已停止"
fi

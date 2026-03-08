#!/bin/bash
# ============================================================
# 部署插件到 AstrBot
# ============================================================
# 用法: bash deploy_plugin.sh <插件目录>
# ============================================================

set -e

ASTRBOT_DIR="${ASTRBOT_DIR:-/opt/astrbot}"
PLUGINS_DIR="${ASTRBOT_DIR}/data/plugins"

if [ -z "$1" ]; then
    echo "用法: $0 <插件目录>"
    echo ""
    echo "示例:"
    echo "  $0 /workspace/my_plugin"
    echo "  $0 ./my_plugin"
    exit 1
fi

PLUGIN_DIR="$1"

# 检查插件目录
if [ ! -d "$PLUGIN_DIR" ]; then
    echo "❌ 插件目录不存在: $PLUGIN_DIR"
    exit 1
fi

# 检查必要文件
if [ ! -f "$PLUGIN_DIR/main.py" ]; then
    echo "⚠️ 插件目录缺少 main.py"
fi

if [ ! -f "$PLUGIN_DIR/metadata.yaml" ]; then
    echo "⚠️ 插件目录缺少 metadata.yaml"
fi

# 获取插件名
PLUGIN_NAME=$(basename "$PLUGIN_DIR")

echo "部署插件: $PLUGIN_NAME"
echo "源目录: $PLUGIN_DIR"
echo "目标目录: ${PLUGINS_DIR}/${PLUGIN_NAME}"

# 创建插件目录
mkdir -p "${PLUGINS_DIR}"

# 复制插件
cp -r "$PLUGIN_DIR" "${PLUGINS_DIR}/"

echo "✅ 插件已部署"

# 重启 AstrBot
echo ""
echo "是否重启 AstrBot 使插件生效？(y/n)"
read -r answer

if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
    # 查找并执行重启脚本
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -f "${SCRIPT_DIR}/stop_astrbot.sh" ]; then
        bash "${SCRIPT_DIR}/stop_astrbot.sh"
    else
        pkill -f "python main.py"
        sleep 2
    fi

    if [ -f "${SCRIPT_DIR}/start_astrbot.sh" ]; then
        bash "${SCRIPT_DIR}/start_astrbot.sh"
    else
        cd "${ASTRBOT_DIR}" && source venv/bin/activate && python main.py &
    fi
fi

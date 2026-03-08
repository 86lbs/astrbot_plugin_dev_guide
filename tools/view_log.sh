#!/bin/bash
# ============================================================
# 查看 AstrBot 日志
# ============================================================

ASTRBOT_DIR="${ASTRBOT_DIR:-/opt/astrbot}"
LOG_FILE="${ASTRBOT_DIR}/logs/astrbot.log"

# 解析参数
LINES=50
FOLLOW=false
ERRORS_ONLY=false
GREP_PATTERN=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -n|--lines)
            LINES="$2"
            shift 2
            ;;
        -f|--follow)
            FOLLOW=true
            shift
            ;;
        -e|--errors)
            ERRORS_ONLY=true
            shift
            ;;
        -g|--grep)
            GREP_PATTERN="$2"
            shift 2
            ;;
        -h|--help)
            echo "用法: $0 [选项]"
            echo ""
            echo "选项:"
            echo "  -n, --lines N     显示最后 N 行（默认 50）"
            echo "  -f, --follow      实时跟踪日志"
            echo "  -e, --errors      只显示错误"
            echo "  -g, --grep PATTERN  过滤包含 PATTERN 的行"
            echo "  -h, --help        显示帮助"
            echo ""
            echo "示例:"
            echo "  $0                    # 显示最后 50 行"
            echo "  $0 -n 100             # 显示最后 100 行"
            echo "  $0 -f                 # 实时跟踪"
            echo "  $0 -e                 # 只显示错误"
            echo "  $0 -g 'my_plugin'     # 过滤插件日志"
            exit 0
            ;;
        *)
            echo "未知选项: $1"
            exit 1
            ;;
    esac
done

# 检查日志文件
if [ ! -f "$LOG_FILE" ]; then
    echo "日志文件不存在: $LOG_FILE"
    echo "请确认 AstrBot 是否已启动"
    exit 1
fi

# 构建命令
if [ "$FOLLOW" = true ]; then
    # 实时跟踪
    if [ "$ERRORS_ONLY" = true ]; then
        tail -f "$LOG_FILE" | grep --line-buffered -i "error\|exception\|traceback\|failed"
    elif [ -n "$GREP_PATTERN" ]; then
        tail -f "$LOG_FILE" | grep --line-buffered -i "$GREP_PATTERN"
    else
        tail -f "$LOG_FILE"
    fi
else
    # 显示指定行数
    if [ "$ERRORS_ONLY" = true ]; then
        tail -n "$LINES" "$LOG_FILE" | grep -i "error\|exception\|traceback\|failed"
    elif [ -n "$GREP_PATTERN" ]; then
        tail -n "$LINES" "$LOG_FILE" | grep -i "$GREP_PATTERN"
    else
        tail -n "$LINES" "$LOG_FILE"
    fi
fi

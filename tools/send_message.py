#!/usr/bin/env python3
"""
send_message.py - 发送消息到 AstrBot

用法:
    python send_message.py "消息内容"
    python send_message.py "消息内容" --session <会话ID>
    python send_message.py "消息内容" --create-session
"""

import requests
import json
import sys
import argparse

# 默认配置
ASTRBOT_URL = "http://localhost:6185"
TIMEOUT = 120


def check_astrbot_running():
    """检查 AstrBot 是否运行"""
    try:
        response = requests.get(f"{ASTRBOT_URL}/", timeout=5)
        return response.status_code == 200
    except:
        return False


def create_session():
    """创建新会话"""
    try:
        response = requests.get(f"{ASTRBOT_URL}/api/chat/new_session", timeout=10)
        data = response.json()
        if data.get("status") == "ok":
            return data["data"]["session_id"]
    except Exception as e:
        print(f"创建会话失败: {e}")
    return None


def send_message(message: str, session_id: str = None, timeout: int = TIMEOUT):
    """
    发送消息到 AstrBot

    Args:
        message: 消息内容
        session_id: 会话ID（可选）
        timeout: 超时时间（秒）

    Returns:
        dict: 响应结果
    """
    # 如果没有提供 session_id，创建新会话
    if not session_id:
        session_id = create_session()
        if not session_id:
            return {"success": False, "error": "Failed to create session"}
        print(f"[会话] {session_id}")

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
        messages = []
        full_text = ""

        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    try:
                        data = json.loads(line[6:])
                        messages.append(data)

                        # 提取文本内容
                        if data.get("type") == "plain":
                            full_text += data.get("data", "")
                    except json.JSONDecodeError:
                        pass

        return {
            "success": True,
            "session_id": session_id,
            "messages": messages,
            "text": full_text
        }

    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timeout"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description='发送消息到 AstrBot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python send_message.py "你好"
  python send_message.py "/help"
  python send_message.py "今天天气怎么样？" --session abc123
        """
    )
    parser.add_argument('message', help='消息内容')
    parser.add_argument('--session', '-s', help='会话ID（可选）')
    parser.add_argument('--timeout', '-t', type=int, default=TIMEOUT, help=f'超时时间（秒，默认{TIMEOUT}）')
    parser.add_argument('--url', '-u', default=ASTRBOT_URL, help=f'AstrBot URL（默认{ASTRBOT_URL}）')
    parser.add_argument('--quiet', '-q', action='store_true', help='安静模式，只输出响应文本')

    args = parser.parse_args()

    # 更新全局配置
    global ASTRBOT_URL
    ASTRBOT_URL = args.url

    # 检查服务
    if not args.quiet:
        if not check_astrbot_running():
            print("❌ AstrBot 未运行")
            print("   请先启动: ./start_astrbot.sh")
            sys.exit(1)

    # 发送消息
    if not args.quiet:
        print(f"[发送] {args.message}")
        print("-" * 50)

    result = send_message(
        message=args.message,
        session_id=args.session,
        timeout=args.timeout
    )

    if result.get("success"):
        if args.quiet:
            print(result.get("text", ""))
        else:
            print(f"[响应] {result.get('text', '')}")
            print("-" * 50)
            print(f"[会话] {result.get('session_id')}")
    else:
        print(f"❌ 错误: {result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()

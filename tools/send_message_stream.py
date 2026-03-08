#!/usr/bin/env python3
"""
send_message_stream.py - 发送消息并实时显示流式响应

用法:
    python send_message_stream.py "消息内容"
"""

import requests
import json
import sys
import argparse

ASTRBOT_URL = "http://localhost:6185"


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


def send_message_stream(message: str, session_id: str = None, timeout: int = 300):
    """
    发送消息并实时显示流式响应

    Args:
        message: 消息内容
        session_id: 会话ID（可选）
        timeout: 超时时间（秒）

    Returns:
        str: 完整的响应文本
    """
    # 创建会话
    if not session_id:
        session_id = create_session()
        if not session_id:
            print("❌ 创建会话失败")
            return None
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

    try:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),
            timeout=timeout,
            stream=True
        )

        full_text = ""
        tool_calls = []

        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    try:
                        data = json.loads(line[6:])
                        msg_type = data.get("type")
                        msg_data = data.get("data", "")
                        chain_type = data.get("chain_type")

                        if msg_type == "plain":
                            if chain_type == "tool_call":
                                # 工具调用开始
                                try:
                                    tool_info = json.loads(msg_data) if isinstance(msg_data, str) else msg_data
                                    tool_name = tool_info.get("name", "unknown")
                                    tool_args = tool_info.get("arguments", {})
                                    print(f"\n[工具调用] {tool_name}")
                                    print(f"  参数: {json.dumps(tool_args, ensure_ascii=False)}")
                                    tool_calls.append(tool_name)
                                except:
                                    pass
                            elif chain_type == "tool_call_result":
                                # 工具返回
                                print(f"[工具返回]")
                            elif chain_type == "reasoning":
                                # 思考过程
                                print(f"\r[思考] {msg_data}", end="", flush=True)
                            else:
                                # 普通文本
                                print(msg_data, end="", flush=True)
                                full_text += msg_data

                        elif msg_type == "end":
                            print("\n" + "-" * 50)
                            print("[完成]")
                            break

                    except json.JSONDecodeError:
                        pass

        return full_text

    except requests.exceptions.Timeout:
        print("\n❌ 请求超时")
        return None
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description='发送消息到 AstrBot（流式响应）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python send_message_stream.py "你好"
  python send_message_stream.py "今天北京天气怎么样？"
  python send_message_stream.py "/help"
        """
    )
    parser.add_argument('message', help='消息内容')
    parser.add_argument('--session', '-s', help='会话ID（可选）')
    parser.add_argument('--timeout', '-t', type=int, default=300, help='超时时间（秒，默认300）')

    args = parser.parse_args()

    # 检查服务
    if not check_astrbot_running():
        print("❌ AstrBot 未运行")
        print("   请先启动: ./start_astrbot.sh")
        sys.exit(1)

    # 发送消息
    result = send_message_stream(
        message=args.message,
        session_id=args.session,
        timeout=args.timeout
    )

    if result is None:
        sys.exit(1)


if __name__ == "__main__":
    main()

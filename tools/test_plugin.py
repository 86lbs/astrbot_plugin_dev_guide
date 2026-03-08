#!/usr/bin/env python3
"""
test_plugin.py - AstrBot 插件自动化测试脚本

用法:
    python test_plugin.py <插件名>
    python test_plugin.py <插件名> --tool <工具名>
    python test_plugin.py <插件名> --command "/help" --command "/test"
"""

import requests
import json
import sys
import time
import argparse
import os

ASTRBOT_URL = "http://localhost:6185"
LOG_FILE = os.environ.get("ASTRBOT_LOG", "/opt/astrbot/logs/astrbot.log")
DEFAULT_TIMEOUT = 180


class PluginTester:
    """插件测试器"""

    def __init__(self, plugin_name: str, verbose: bool = True):
        self.plugin_name = plugin_name
        self.session_id = None
        self.results = []
        self.verbose = verbose

    def log(self, msg: str):
        """打印日志"""
        if self.verbose:
            print(msg)

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
            lower_content = content.lower()
            return f"plugin {self.plugin_name.lower()}" in lower_content or \
                   f"loading plugin: {self.plugin_name.lower()}" in lower_content
        except:
            return False

    def check_llm_tool_registered(self, tool_name: str) -> bool:
        """检查 LLM Tool 是否注册"""
        try:
            with open(LOG_FILE, 'r') as f:
                content = f.read()
            return f"llm tool: {tool_name}" in content.lower() or \
                   f"registered llm tool: {tool_name}" in content.lower()
        except:
            return False

    def create_session(self) -> str:
        """创建新会话"""
        try:
            response = requests.get(
                f"{ASTRBOT_URL}/api/chat/new_session",
                timeout=10
            )
            data = response.json()
            if data.get("status") == "ok":
                self.session_id = data["data"]["session_id"]
                return self.session_id
        except Exception as e:
            self.log(f"创建会话失败: {e}")
        return None

    def send_message(self, message: str, timeout: int = DEFAULT_TIMEOUT) -> dict:
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

            messages = []
            full_text = ""

            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        try:
                            data = json.loads(line[6:])
                            messages.append(data)
                            if data.get("type") == "plain":
                                full_text += data.get("data", "")
                        except json.JSONDecodeError:
                            pass

            return {
                "success": True,
                "messages": messages,
                "text": full_text
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def test_command(self, command: str, expected_contains: str = None) -> dict:
        """测试指令"""
        result = {
            "test": f"指令测试: {command}",
            "command": command,
            "status": "unknown",
            "response": None,
            "error": None
        }

        self.log(f"\n测试指令: {command}")

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
            # 没有预期内容，只要成功就通过
            result["status"] = "passed"

        status_icon = "✅" if result["status"] == "passed" else "❌"
        self.log(f"{status_icon} {result['test']}")
        if result.get("error"):
            self.log(f"   错误: {result['error']}")
        if result["status"] == "passed" and response.get("text"):
            self.log(f"   响应: {response['text'][:100]}...")

        self.results.append(result)
        return result

    def test_llm_tool(self, message: str, tool_name: str, timeout: int = 180) -> dict:
        """测试 LLM Tool"""
        result = {
            "test": f"LLM Tool 测试: {message}",
            "tool": tool_name,
            "trigger_message": message,
            "status": "unknown",
            "tool_called": False,
            "response": None
        }

        self.log(f"\n测试 LLM Tool: {message}")
        self.log(f"预期工具: {tool_name}")

        # 记录日志大小
        log_size_before = 0
        try:
            log_size_before = os.path.getsize(LOG_FILE)
        except:
            pass

        # 发送消息
        response = self.send_message(message, timeout=timeout)
        result["response"] = response

        # 等待处理
        time.sleep(2)

        # 检查日志中是否有工具调用
        try:
            with open(LOG_FILE, 'r') as f:
                f.seek(log_size_before)
                new_logs = f.read().lower()

            # 检查工具调用
            if tool_name.lower() in new_logs and "tool" in new_logs:
                result["tool_called"] = True
                result["status"] = "passed"
            else:
                result["status"] = "failed"
                result["error"] = "工具未被调用"

        except Exception as e:
            result["status"] = "failed"
            result["error"] = f"日志读取失败: {e}"

        status_icon = "✅" if result["status"] == "passed" else "❌"
        self.log(f"{status_icon} {result['test']}")
        if result.get("error"):
            self.log(f"   错误: {result['error']}")
        if result["tool_called"]:
            self.log(f"   工具已调用: {tool_name}")

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
    parser = argparse.ArgumentParser(
        description='AstrBot 插件自动化测试工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python test_plugin.py my_plugin
  python test_plugin.py my_plugin --tool get_weather
  python test_plugin.py my_plugin --command "/help" --command "/test"
  python test_plugin.py my_plugin --command "/help" --tool my_tool
        """
    )
    parser.add_argument('plugin_name', help='插件名称')
    parser.add_argument('--tool', '-t', help='LLM Tool 名称')
    parser.add_argument('--command', '-c', action='append', help='测试指令（可多次使用）')
    parser.add_argument('--message', '-m', action='append', help='触发 LLM Tool 的消息（可多次使用）')
    parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT, help=f'超时时间（秒，默认{DEFAULT_TIMEOUT}）')
    parser.add_argument('--quiet', '-q', action='store_true', help='安静模式')

    args = parser.parse_args()

    tester = PluginTester(args.plugin_name, verbose=not args.quiet)

    # 检查环境
    print("检查测试环境...")

    if not tester.check_astrbot_running():
        print("❌ AstrBot 未运行")
        print("   请先启动: ./start_astrbot.sh")
        sys.exit(1)
    print("✅ AstrBot 运行中")

    if not tester.check_plugin_loaded():
        print(f"⚠️ 插件 {args.plugin_name} 未加载")
        print("   请确认插件已部署到 data/plugins/ 目录")
    else:
        print(f"✅ 插件 {args.plugin_name} 已加载")

    # 创建会话
    session_id = tester.create_session()
    if session_id:
        print(f"✅ 创建会话: {session_id}")
    else:
        print("❌ 创建会话失败")
        sys.exit(1)

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
        messages = args.message or ["今天天气怎么样？"]
        for msg in messages:
            tester.test_llm_tool(msg, args.tool, timeout=args.timeout)

    # 打印报告
    success = tester.print_report()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
模拟 LLM API 服务
用于测试 AstrBot 的 LLM Tool 功能，无需运行真实的 LLM 模型。

使用方法：
1. 运行此脚本：python mock_llm_server.py
2. 在 AstrBot 中配置 OpenAI 兼容 API：
   - API Base: http://localhost:8000/v1
   - API Key: mock-key
   - Model: mock-model
3. 当用户发送消息时，会自动触发注册的 LLM Tool

原理：
- 模拟 OpenAI API 格式
- 返回预设的响应，包含 tool_calls
- AstrBot 收到响应后会执行对应的 Tool
"""

import json
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime


class MockLLMHandler(BaseHTTPRequestHandler):
    """模拟 LLM API 处理器"""

    # 预设的 Tool 调用响应
    # 可以根据需要修改 tool_name 和 arguments
    TOOL_RESPONSES = [
        {
            "tool_name": "get_weather",
            "arguments": '{"city": "北京"}'
        },
        {
            "tool_name": "search_web",
            "arguments": '{"query": "今天新闻"}'
        }
    ]

    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")

    def send_json_response(self, data):
        """发送 JSON 响应"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_OPTIONS(self):
        """处理 CORS 预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_GET(self):
        """处理 GET 请求"""
        if self.path == '/v1/models':
            # 返回可用模型列表
            self.send_json_response({
                "object": "list",
                "data": [
                    {
                        "id": "mock-model",
                        "object": "model",
                        "created": int(datetime.now().timestamp()),
                        "owned_by": "mock"
                    }
                ]
            })
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        """处理 POST 请求"""
        if self.path == '/v1/chat/completions':
            self.handle_chat_completion()
        else:
            self.send_response(404)
            self.end_headers()

    def handle_chat_completion(self):
        """处理聊天补全请求"""
        # 读取请求体
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode()
        
        try:
            request_data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            return

        # 打印请求信息
        messages = request_data.get('messages', [])
        tools = request_data.get('tools', [])
        
        print(f"\n{'='*50}")
        print(f"收到聊天请求")
        print(f"消息数: {len(messages)}")
        print(f"可用 Tools: {[t.get('function', {}).get('name') for t in tools] if tools else '无'}")
        
        if messages:
            last_msg = messages[-1]
            print(f"最后消息: {last_msg.get('content', '')[:100]}...")

        # 生成响应
        if tools:
            # 有 Tools，返回 Tool 调用
            response = self.generate_tool_call_response(tools)
        else:
            # 无 Tools，返回普通文本
            response = self.generate_text_response()

        self.send_json_response(response)

    def generate_tool_call_response(self, tools):
        """生成 Tool 调用响应"""
        # 获取第一个可用的 Tool
        available_tools = [t['function']['name'] for t in tools]
        
        # 选择要调用的 Tool
        tool_to_call = None
        tool_args = "{}"
        
        # 优先使用预设的 Tool
        for preset in self.TOOL_RESPONSES:
            if preset['tool_name'] in available_tools:
                tool_to_call = preset['tool_name']
                tool_args = preset['arguments']
                break
        
        # 如果没有预设的，使用第一个可用的 Tool
        if not tool_to_call and available_tools:
            tool_to_call = available_tools[0]
            # 尝试从 Tool 定义中获取参数 schema
            for t in tools:
                if t['function']['name'] == tool_to_call:
                    params = t['function'].get('parameters', {})
                    props = params.get('properties', {})
                    # 生成默认参数
                    args = {}
                    for prop_name, prop_def in props.items():
                        prop_type = prop_def.get('type', 'string')
                        if prop_type == 'string':
                            args[prop_name] = 'mock_value'
                        elif prop_type == 'integer' or prop_type == 'number':
                            args[prop_name] = 1
                        elif prop_type == 'boolean':
                            args[prop_name] = True
                        elif prop_type == 'array':
                            args[prop_name] = []
                        elif prop_type == 'object':
                            args[prop_name] = {}
                    tool_args = json.dumps(args)
                    break

        tool_call_id = f"call_{uuid.uuid4().hex[:24]}"
        
        print(f"\n触发 Tool 调用:")
        print(f"  Tool: {tool_to_call}")
        print(f"  参数: {tool_args}")
        print(f"{'='*50}\n")

        return {
            "id": f"chatcmpl-{uuid.uuid4().hex[:29]}",
            "object": "chat.completion",
            "created": int(datetime.now().timestamp()),
            "model": "mock-model",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": tool_call_id,
                                "type": "function",
                                "function": {
                                    "name": tool_to_call,
                                    "arguments": tool_args
                                }
                            }
                        ]
                    },
                    "finish_reason": "tool_calls"
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 20,
                "total_tokens": 30
            }
        }

    def generate_text_response(self):
        """生成普通文本响应"""
        return {
            "id": f"chatcmpl-{uuid.uuid4().hex[:29]}",
            "object": "chat.completion",
            "created": int(datetime.now().timestamp()),
            "model": "mock-model",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "这是一个模拟的 LLM 响应。如需测试 Tool 功能，请在 AstrBot 中注册 LLM Tool。"
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 20,
                "total_tokens": 30
            }
        }


def main():
    """启动模拟服务"""
    host = 'localhost'
    port = 8000

    print(f"""
╔═══════════════════════════════════════════════════════════╗
║           模拟 LLM API 服务                                ║
╠═══════════════════════════════════════════════════════════╣
║  服务地址: http://{host}:{port}                            ║
║  API Base: http://{host}:{port}/v1                        ║
║  API Key:  mock-key (任意值均可)                          ║
║  Model:    mock-model                                     ║
╠═══════════════════════════════════════════════════════════╣
║  功能说明:                                                 ║
║  - 模拟 OpenAI API 格式                                    ║
║  - 自动触发注册的 LLM Tool                                 ║
║  - 无需运行真实的 LLM 模型                                 ║
╠═══════════════════════════════════════════════════════════╣
║  AstrBot 配置:                                            ║
║  1. 进入 AstrBot 管理面板                                  ║
║  2. 配置 OpenAI 兼容 API                                   ║
║  3. API Base: http://localhost:8000/v1                    ║
║  4. API Key: mock-key                                     ║
║  5. Model: mock-model                                     ║
╚═══════════════════════════════════════════════════════════╝
""")

    server = HTTPServer((host, port), MockLLMHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n服务已停止")
        server.shutdown()


if __name__ == '__main__':
    main()

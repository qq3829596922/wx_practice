"""
AI Agent + MCP 完整 Demo

展示 AI 如何自主决定调用工具

流程:
1. 用户说: "帮我算 3+5 再乘以 2"
2. AI 发现有 add_numbers 和 multiply_numbers 工具
3. AI 自己决定: 先调用 add(3,5)=8, 再调用 multiply(8,2)=16
4. AI 返回答案
"""

import asyncio
import json
import httpx
import logging
from openai import OpenAI
from mcp import ClientSession
from mcp.client.sse import sse_client

# 关闭 openai 和 httpx 的 debug 日志
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

# 配置
DEBUG = True  # 设为 False 关闭调试输出
MCP_URL = "http://localhost:9999/sse"
OPENAI_API_KEY = "sk-PqL9YtC4qTLxyF37pektFPwXsfD9DTBg4P2tX9Evf9wtlS0T"
OPENAI_BASE_URL = "https://sappscie.com/v1"
AI_MODEL = "anthropic/claude-sonnet-4.5"


def log_request(request: httpx.Request):
    """格式化打印请求"""
    if not DEBUG:
        return
    print(f"\n{'=' * 60}")
    print(f"📤 REQUEST: {request.method} {request.url}")
    print('=' * 60)
    if request.content:
        try:
            body = json.loads(request.content.decode())
            print(json.dumps(body, indent=2, ensure_ascii=False))
        except:
            print(request.content.decode()[:500])
    print('=' * 60)


def log_response(response: httpx.Response):
    """格式化打印响应"""
    if not DEBUG:
        return
    print(f"\n{'=' * 60}")
    print(f"📥 RESPONSE: {response.status_code}")
    print('=' * 60)


# 创建带日志的 client
http_client = httpx.Client(
    event_hooks={"request": [log_request], "response": [log_response]}
)
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    http_client=http_client
)


def mcp_tools_to_openai_format(mcp_tools) -> list:
    """把 MCP 工具转成 OpenAI function calling 格式"""
    openai_tools = []
    for tool in mcp_tools:
        openai_tools.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.inputSchema if tool.inputSchema else {"type": "object", "properties": {}},
            }
        })
    return openai_tools


async def main():
    print("=" * 60)
    print("AI Agent + MCP Demo")
    print("=" * 60)

    # 连接 MCP 服务器
    async with sse_client(MCP_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 1. 获取可用工具
            tools_result = await session.list_tools()
            openai_tools = mcp_tools_to_openai_format(tools_result.tools)

            print("\n【可用工具】")
            for t in openai_tools:
                print(f"  - {t['function']['name']}: {t['function']['description']}")

            # 2. 用户输入
            user_input = "帮我算 3+5 的结果，然后把结果乘以 2"
            print(f"\n【用户】{user_input}")

            messages = [{"role": "user", "content": user_input}]

            # 3. AI 决策循环
            while True:
                print("\n【AI 思考中...】")
                response = client.chat.completions.create(
                    model=AI_MODEL,
                    messages=messages,
                    tools=openai_tools,
                    tool_choice="auto",
                )

                assistant_message = response.choices[0].message

                # 如果 AI 决定调用工具
                if assistant_message.tool_calls:
                    # 转成 dict 方便打印
                    messages.append(assistant_message.model_dump())

                    for tool_call in assistant_message.tool_calls:
                        tool_name = tool_call.function.name
                        tool_args = json.loads(tool_call.function.arguments)

                        print(f"\n【AI 调用工具】{tool_name}({tool_args})")

                        # 通过 MCP 调用工具
                        result = await session.call_tool(tool_name, tool_args)
                        tool_result = result.content[0].text if result.content else ""

                        print(f"【工具返回】{tool_result}")

                        # 把结果告诉 AI
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": tool_result,
                        })
                else:
                    # AI 不再调用工具，输出最终答案
                    print(f"\n【AI 回答】{assistant_message.content}")
                    break

    print("\n" + "=" * 60)
    print("这就是 MCP 的核心价值:")
    print("1. AI 自动发现工具 (list_tools)")
    print("2. AI 自己决定调用什么工具")
    print("3. AI 可以多次调用，串联结果")
    print("4. 你只需要提供工具，不用写调用逻辑!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

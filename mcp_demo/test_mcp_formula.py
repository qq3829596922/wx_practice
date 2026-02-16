"""
测试配方搜索 MCP 服务

通过 MCP 调用配方搜索工具
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
DEBUG = True
MCP_URL = "http://localhost:8460/sse"  # 配方服务的 MCP 端点
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
            # 只打印 messages 部分
            if "messages" in body:
                print("【messages】")
                print(json.dumps(body["messages"], indent=2, ensure_ascii=False))
            if "tools" in body:
                print(f"\n【tools】共 {len(body['tools'])} 个工具")
                for t in body["tools"]:
                    print(f"  - {t['function']['name']}")
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
    print("配方搜索 MCP 测试")
    print("=" * 60)

    # 连接 MCP 服务器
    print(f"\n连接 MCP 服务: {MCP_URL}")

    try:
        async with sse_client(MCP_URL) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                # 1. 获取可用工具
                tools_result = await session.list_tools()
                openai_tools = mcp_tools_to_openai_format(tools_result.tools)
                print(json.dumps({"openai_tools": openai_tools}, indent=4, ensure_ascii=False))
                # print("\n【可用工具】")
                # for t in tools_result.tools:
                #     print(f"  - {t.name}")
                #     print(f"    描述: {t.description[:100] if t.description else '无'}...")
                #     if t.inputSchema and "properties" in t.inputSchema:
                #         print(f"    参数: {list(t.inputSchema['properties'].keys())}")

                # # 2. 用户输入
                # user_input = "帮我搜索 含有 鲸蜡硬脂醇 的配方"
                # print(f"\n【用户】{user_input}")

                # messages = [{"role": "user", "content": user_input}]

                # # 3. AI 决策循环
                # max_turns = 5
                # turn = 0
                # while turn < max_turns:
                #     turn += 1
                #     print(f"\n【AI 思考中... (第 {turn} 轮)】")

                #     response = client.chat.completions.create(
                #         model=AI_MODEL,
                #         messages=messages,
                #         tools=openai_tools,
                #         tool_choice="auto",
                #     )

                #     assistant_message = response.choices[0].message

                #     # 如果 AI 决定调用工具
                #     if assistant_message.tool_calls:
                #         messages.append(assistant_message.model_dump())

                #         for tool_call in assistant_message.tool_calls:
                #             tool_name = tool_call.function.name
                #             tool_args = json.loads(tool_call.function.arguments)

                #             print(f"\n【AI 调用工具】{tool_name}")
                #             print(f"【参数】{json.dumps(tool_args, indent=2, ensure_ascii=False)}")

                #             # 通过 MCP 调用工具
                #             result = await session.call_tool(tool_name, tool_args)
                #             tool_result = result.content[0].text if result.content else ""

                #             # 打印工具返回（截断显示）
                #             print(f"\n【工具返回】(长度: {len(tool_result)} 字符)")
                #             if len(tool_result) > 500:
                #                 print(tool_result[:500] + "...")
                #             else:
                #                 print(tool_result)

                #             messages.append({
                #                 "role": "tool",
                #                 "tool_call_id": tool_call.id,
                #                 "content": tool_result,
                #             })
                #     else:
                #         # AI 不再调用工具，输出最终答案
                #         print(f"\n【AI 回答】\n{assistant_message.content}")
                #         break

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

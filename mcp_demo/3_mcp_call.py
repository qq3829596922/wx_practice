"""
MCP 方式调用 Demo

特点：
- AI 自动发现可用工具
- AI 根据用户意图决定调用什么
- 你不需要写调用代码
- 工具调用由 AI 自主完成
"""

import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client
import json

MCP_URL = "http://localhost:9999/sse"

async def main():
    print("=" * 50)
    print("MCP 方式调用")
    print("=" * 50)

    # 连接 MCP 服务器
    async with sse_client(MCP_URL) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化连接
            await session.initialize()

            # ========== 1. 自动发现工具 ==========
            print("\n【1. 自动发现工具】")
            tools = await session.list_tools()
            print(f"发现 {len(tools.tools)} 个工具:")
            print(tools.tools)

            for tool in tools.tools:
                print(f"\n  工具名: {tool.name}")
                print(f"  描述: {tool.description}")  # 只取第一行
                print(f"  参数: {json.dumps(tool.inputSchema, indent=4, ensure_ascii=False)}")

            # # ========== 2. 调用工具 ==========
            # print("\n【2. 调用工具】")

            # # 调用加法
            # print("\n调用 add_numbers(3, 5):")
            result = await session.call_tool("add_numbers", {"a": 3, "b": 5})
            # print(f"结果: {result.content}")

            # # 调用乘法
            # print("\n调用 multiply_numbers(4, 6):")
            result = await session.call_tool("multiply_numbers", {"a": 4, "b": 6})
            # print(f"结果: {result.content}")

    # print("\n" + "=" * 50)
    # print("MCP 方式的特点:")
    # print("1. 工具是自动发现的 (list_tools)")
    # print("2. AI 可以看到工具描述，自己决定用哪个")
    # print("3. 调用是标准化的 (call_tool)")
    # print("4. 这就是 Claude/GPT 调用工具的方式!")
    # print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())

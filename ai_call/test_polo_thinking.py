"""
NewAPI Thinking 测试脚本

=== NewAPI 启用 Thinking 的两种方式 ===
1. 模型名加 -thinking 后缀: claude-sonnet-4-5-20250929-thinking
2. 使用 reasoning_effort 参数: extra_body={"reasoning_effort": "medium"}  # low / medium / high

=== 返回格式 ===
NewAPI 返回字段: reasoning_content (字符串)
OpenRouter 返回字段: reasoning + reasoning_details (列表)

=== 流式响应阶段 ===
阶段1: Thinking
    - reasoning_content 有值
    - content = None
    - finish_reason = None

阶段2: 过渡 (thinking 结束标志)
    - reasoning_content 消失 (不在 delta 中)
    - content = '' (空字符串)

阶段3: Response
    - reasoning_content 无
    - content 有值

阶段4: 结束
    - finish_reason = 'stop'

阶段5: Usage (最后一个 chunk)
    - choices = []
    - usage 包含 token 统计

=== 判断 Thinking 结束 ===
方式1: 检测到 content 字段出现 (推荐)
方式2: reasoning_content 从有值变为无值
"""

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

print(f"base_url: {os.getenv('OPENAI_BASE_URL')}")
print(f"model: {os.getenv('AI_MODEL')}")
print("-" * 50)

stream = client.chat.completions.create(
    model=os.getenv("AI_MODEL"),
    messages=[{"role": "user", "content": "1+1等于几？简短回答"}],
    stream=True,
    extra_body={
        "reasoning_effort": "medium"  # low / medium / high
    }
)

reasoning = ""
content = ""
in_thinking = False
thinking_ended = False

print("\n[Thinking]")
for chunk in stream:
    if not chunk.choices:
        # 最后一个 chunk 包含 usage 信息
        if chunk.usage:
            print(f"\n[Usage] tokens: {chunk.usage.total_tokens}")
        continue

    delta = chunk.choices[0].delta
    finish_reason = chunk.choices[0].finish_reason

    # 获取 reasoning_content (NewAPI 格式)
    reasoning_content = getattr(delta, "reasoning_content", None)

    # 阶段1: Thinking
    if reasoning_content:
        if not in_thinking:
            in_thinking = True
        reasoning += reasoning_content
        print(reasoning_content, end="", flush=True)

    # 阶段2: 过渡 - thinking 结束
    # 判断方式: content 字段出现 (即使是空字符串)
    if hasattr(delta, "content") and delta.content is not None and not thinking_ended:
        if in_thinking:
            print("\n\n[Response]")
            in_thinking = False
            thinking_ended = True

    # 阶段3: Response
    if delta.content:
        content += delta.content
        print(delta.content, end="", flush=True)

    # 阶段4: 结束
    if finish_reason == "stop":
        print("\n")

print("=" * 50)
print(f"Reasoning ({len(reasoning)} chars): {reasoning[:100]}..." if len(reasoning) > 100 else f"Reasoning: {reasoning}")
print(f"Content: {content}")

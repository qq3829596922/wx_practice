"""
title: Test Thinking Event Pipeline
description: 测试 thinking + event + content 混合输出，固定返回，不调用大模型

=== 官方 thinking 格式 ===
用 <think>...</think> 标签包裹，open-webui 会自动转成折叠面板

参考: https://github.com/open-webui/pipelines/blob/main/examples/pipelines/providers/anthropic_manifold_pipeline.py
"""

from typing import List, Generator, Union
from pydantic import BaseModel
import time


class Pipeline:
    class Valves(BaseModel):
        pass

    def __init__(self):
        self.name = "Test Thinking Event"

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Generator[Union[str, dict], None, None]:
        """
        测试输出顺序:
        1. event: 开始处理
        2. <think>...</think> thinking 内容
        3. event: 思考完成
        4. content 内容
        5. event: 完成
        """

        # ========== 1. Event: 开始 ==========
        yield self._make_event("正在分析问题...", done=False)
        time.sleep(0.3)

        # ========== 2. Thinking (用 <think> 标签) ==========
        yield "<think>"
        time.sleep(0.1)

        # thinking 内容 (逐字输出)
        thinking_text = f"用户问了: {user_message}\n\n让我思考一下...\n首先，我需要理解问题的核心。\n然后，我会分析可能的解决方案。\n最后，我会给出一个清晰的答案。"
        for char in thinking_text:
            yield char
            time.sleep(0.03)

        # thinking 结束
        yield "\n</think>\n\n"
        time.sleep(0.2)

        # ========== 3. Event: 思考完成 ==========
        yield self._make_event("思考完成，正在生成回答...", done=False)
        time.sleep(0.3)

        # ========== 4. Content 内容 (逐字输出) ==========
        content_text = f"根据我的分析，这是一个关于「{user_message[:20]}」的问题。\n\n**回答：**\n这是测试输出的固定回答内容。\n用于验证 thinking + event + content 的混合显示效果。"
        for char in content_text:
            yield char
            time.sleep(0.02)

        # ========== 5. Event: 完成 ==========
        yield self._make_event("回答完成", done=True)

    def _make_event(self, description: str, done: bool = False) -> dict:
        """构造 event 消息"""
        return {
            "event": {
                "type": "status",
                "data": {
                    "description": description,
                    "done": done,
                },
            }
        }

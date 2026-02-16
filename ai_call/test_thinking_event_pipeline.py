"""
title: Test Thinking Event Pipeline
description: 测试多段 thinking + event + content 混合输出

=== 官方 thinking 格式 ===
用 <think>...</think> 标签包裹，open-webui 会自动转成折叠面板
支持多段交替输出

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
        测试多段交替输出:
        1. event: 开始
        2. thinking 1
        3. content 1
        4. event: 继续思考
        5. thinking 2
        6. content 2
        7. event: 完成
        """

        # ========== 1. Event: 开始 ==========
        yield self._make_event("正在分析问题...", done=False)
        time.sleep(0.2)

        # ========== 2. Thinking 第一段 ==========
        yield "<think>"
        thinking1 = f"用户问了: {user_message}\n\n首先，我来理解问题..."
        for char in thinking1:
            yield char
            time.sleep(0.02)
        yield "\n</think>\n\n"
        time.sleep(0.1)

        # ========== 3. Content 第一段 ==========
        content1 = "**第一步分析：**\n这个问题的核心是..."
        for char in content1:
            yield char
            time.sleep(0.02)
        yield "\n\n"
        time.sleep(0.2)

        # ========== 4. Event: 继续思考 ==========
        yield self._make_event("深入分析中...", done=False)
        time.sleep(0.2)

        # ========== 5. Thinking 第二段 ==========
        yield "<think>"
        thinking2 = "让我进一步思考解决方案...\n考虑到各种因素..."
        for char in thinking2:
            yield char
            time.sleep(0.02)
        yield "\n</think>\n\n"
        time.sleep(0.1)

        # ========== 6. Content 第二段 ==========
        content2 = "**第二步结论：**\n综合以上分析，答案是...\n\n这是测试多段 thinking + content 的效果。"
        for char in content2:
            yield char
            time.sleep(0.02)

        # ========== 7. Event: 完成 ==========
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

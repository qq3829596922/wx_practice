"""
简单的 MCP 服务器 Demo
同时支持 HTTP 和 MCP 两种调用方式

运行: python 1_simple_server.py
服务地址: http://localhost:9999
MCP 地址: http://localhost:9999/sse
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="计算器服务")

# ========== 数据模型 ==========
class AddRequest(BaseModel):
    a: float = Field(description="第一个加数")
    b: float = Field(description="第二个加数")

class MultiplyRequest(BaseModel):
    a: float = Field(description="被乘数")
    b: float = Field(description="乘数")

class CalcResponse(BaseModel):
    result: float = Field(description="计算结果")
    operation: str = Field(description="运算表达式")

# ========== HTTP 接口 ==========
@app.post("/add", operation_id="add_numbers", description="加法运算：计算两个数字的和，返回 a + b 的结果")
async def add(req: AddRequest) -> CalcResponse:
    """加法运算接口"""
    return CalcResponse(result=req.a + req.b, operation=f"{req.a} + {req.b}")

@app.post("/multiply", operation_id="multiply_numbers", description="乘法运算：计算两个数字的乘积，返回 a × b 的结果")
async def multiply(req: MultiplyRequest) -> CalcResponse:
    """乘法运算接口"""
    return CalcResponse(result=req.a * req.b, operation=f"{req.a} × {req.b}")

@app.get("/health")
async def health():
    return {"status": "ok"}

# ========== MCP 支持 ==========
from fastapi_mcp import FastApiMCP

mcp = FastApiMCP(
    app,
    include_operations=["add_numbers", "multiply_numbers"],  # 暴露为 MCP 工具
)
mcp.mount_sse()  # 挂载到 /sse 路径

print("""
========================================
服务已启动！

HTTP 接口:
  POST http://localhost:9999/add
  POST http://localhost:9999/multiply

MCP 接口:
  http://localhost:9999/sse

测试:
  python 2_http_call.py   # HTTP 方式
  python 3_mcp_call.py    # MCP 方式
========================================
""")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9999)

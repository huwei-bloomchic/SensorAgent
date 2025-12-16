#!/usr/bin/env python3
"""
神策数据分析助手 - OpenAPI服务器
提供兼容OpenAI格式的 /v1/chat/completions 接口
"""
import sys
import json
import asyncio
import uuid
from pathlib import Path
from typing import Optional, List, Dict, Any, AsyncGenerator
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import os

from config.settings import get_settings
from src.agents.orchestrator import create_agent


# ============ Pydantic模型定义 ============

class Message(BaseModel):
    """聊天消息"""
    role: str = Field(..., description="角色: system/user/assistant")
    content: str = Field(..., description="消息内容")


class ChatCompletionRequest(BaseModel):
    """Chat Completion请求"""
    model: str = Field(default="sensors-agent", description="模型名称")
    messages: List[Message] = Field(..., description="消息列表")
    stream: bool = Field(default=False, description="是否流式返回")
    temperature: Optional[float] = Field(default=0.7, description="温度参数")
    max_tokens: Optional[int] = Field(default=None, description="最大token数")
    top_p: Optional[float] = Field(default=1.0, description="Top-p采样")


class ChatCompletionChoice(BaseModel):
    """Chat Completion选择"""
    index: int
    message: Message
    finish_reason: str


class Usage(BaseModel):
    """Token使用统计"""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class ChatCompletionResponse(BaseModel):
    """Chat Completion响应"""
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: Usage


class DeltaMessage(BaseModel):
    """流式响应的增量消息"""
    role: Optional[str] = None
    content: Optional[str] = None


class ChatCompletionStreamChoice(BaseModel):
    """流式响应的选择"""
    index: int
    delta: DeltaMessage
    finish_reason: Optional[str] = None


class ChatCompletionStreamResponse(BaseModel):
    """流式响应"""
    id: str
    object: str = "chat.completion.chunk"
    created: int
    model: str
    choices: List[ChatCompletionStreamChoice]


# ============ FastAPI应用 ============

app = FastAPI(
    title="神策数据分析助手 API",
    description="提供兼容OpenAI格式的聊天API，支持神策数据分析",
    version="2.0.0"
)

# 添加CORS支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局Agent实例
agent = None
settings = None


# ============ API端点 ============

@app.on_event("startup")
async def startup_event():
    """启动时初始化Agent"""
    global agent, settings

    logger.info("初始化神策数据分析Agent...")
    settings = get_settings()

    try:
        agent = create_agent()
        logger.info("Agent初始化完成")
    except Exception as e:
        logger.error(f"Agent初始化失败: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """关闭时清理资源"""
    global agent

    if agent:
        logger.info("关闭Agent资源...")
        agent.close()


@app.get("/")
async def root():
    """健康检查"""
    return {
        "status": "ok",
        "service": "神策数据分析助手 API",
        "version": "2.0.0"
    }


@app.get("/v1/models")
async def list_models():
    """列出可用模型"""
    return {
        "object": "list",
        "data": [
            {
                "id": "sensors-agent",
                "object": "model",
                "created": int(datetime.now().timestamp()),
                "owned_by": "sensors-analytics"
            }
        ]
    }


@app.post("/v1/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest):
    """
    创建聊天补全

    支持流式和非流式两种模式：
    - 流式(stream=true): 实时返回thinking步骤和最终答案
    - 非流式(stream=false): 返回最终完整答案
    """
    global agent

    if not agent:
        raise HTTPException(status_code=503, detail="Agent未初始化")

    # 提取用户最后一条消息
    user_messages = [msg for msg in request.messages if msg.role == "user"]
    if not user_messages:
        raise HTTPException(status_code=400, detail="未找到用户消息")

    user_input = user_messages[-1].content

    # 生成请求ID
    request_id = f"chatcmpl-{uuid.uuid4().hex[:8]}"
    created_at = int(datetime.now().timestamp())

    # 流式响应
    if request.stream:
        async def generate_stream():
            """生成SSE流 - 简化版本，直接调用agent并分块返回结果"""
            loop = asyncio.get_event_loop()

            # 首先发送role
            chunk = ChatCompletionStreamResponse(
                id=request_id,
                created=created_at,
                model=request.model,
                choices=[
                    ChatCompletionStreamChoice(
                        index=0,
                        delta=DeltaMessage(role="assistant"),
                        finish_reason=None
                    )
                ]
            )
            yield f"data: {chunk.model_dump_json()}\n\n"

            try:
                # 在线程池中执行查询
                def run_query():
                    # 设置 matplotlib 使用非交互式后端，避免在后台线程中创建 GUI 窗口
                    import matplotlib
                    matplotlib.use('Agg')  # 使用非交互式后端
                    return agent.query(user_input)
                
                result = await loop.run_in_executor(None, run_query)

                # 确保result是字符串类型
                if not isinstance(result, str):
                    if isinstance(result, dict):
                        # 如果是字典，转换为JSON字符串
                        result = json.dumps(result, ensure_ascii=False, indent=2)
                    else:
                        # 其他类型直接转换为字符串
                        result = str(result)

                # 直接发送完整结果
                chunk = ChatCompletionStreamResponse(
                    id=request_id,
                    created=created_at,
                    model=request.model,
                    choices=[
                        ChatCompletionStreamChoice(
                            index=0,
                            delta=DeltaMessage(content=result),
                            finish_reason=None
                        )
                    ]
                )
                yield f"data: {chunk.model_dump_json()}\n\n"

            except Exception as e:
                logger.exception("流式查询处理失败")
                error_content = f"\n\n❌ 错误: {str(e)}"
                chunk = ChatCompletionStreamResponse(
                    id=request_id,
                    created=created_at,
                    model=request.model,
                    choices=[
                        ChatCompletionStreamChoice(
                            index=0,
                            delta=DeltaMessage(content=error_content),
                            finish_reason="error"
                        )
                    ]
                )
                yield f"data: {chunk.model_dump_json()}\n\n"

            # 发送结束标记
            chunk = ChatCompletionStreamResponse(
                id=request_id,
                created=created_at,
                model=request.model,
                choices=[
                    ChatCompletionStreamChoice(
                        index=0,
                        delta=DeltaMessage(),
                        finish_reason="stop"
                    )
                ]
            )
            yield f"data: {chunk.model_dump_json()}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream"
        )

    # 非流式响应
    else:
        try:
            # 在线程池中异步执行同步的query方法，避免阻塞事件循环
            loop = asyncio.get_event_loop()
            
            # 使用lambda包装，因为run_in_executor不支持关键字参数
            def run_query():
                # 设置 matplotlib 使用非交互式后端，避免在后台线程中创建 GUI 窗口
                import matplotlib
                matplotlib.use('Agg')  # 使用非交互式后端
                return agent.query(user_input)
            
            result = await loop.run_in_executor(None, run_query)

            response = ChatCompletionResponse(
                id=request_id,
                created=created_at,
                model=request.model,
                choices=[
                    ChatCompletionChoice(
                        index=0,
                        message=Message(role="assistant", content=result),
                        finish_reason="stop"
                    )
                ],
                usage=Usage(
                    prompt_tokens=0,
                    completion_tokens=0,
                    total_tokens=0
                )
            )

            return response

        except Exception as e:
            logger.exception("查询处理失败")
            raise HTTPException(status_code=500, detail=f"查询处理失败: {str(e)}")


@app.post("/reset")
async def reset_agent():
    """重置Agent对话状态"""
    global agent

    if not agent:
        raise HTTPException(status_code=503, detail="Agent未初始化")

    agent.reset()
    return {"status": "ok", "message": "Agent状态已重置"}


@app.get("/files/{filename}")
async def download_file(filename: str):
    """
    下载或展示文件（支持CSV和图片文件）

    Args:
        filename: 文件名（支持 .csv, .png, .jpg, .jpeg 等）

    Returns:
        文件响应（CSV文件下载，图片文件直接展示）

    Example:
        GET /files/refund_events_cdp_tag_fill_rate.csv
        GET /files/chart_analysis.png
    """
    global settings

    # 获取配置的输出目录
    output_dir = settings.SQL_OUTPUT_DIR if settings else "/tmp/sensors_data"

    # 构建完整文件路径
    file_path = os.path.join(output_dir, filename)

    # 安全检查：确保文件路径在允许的目录内（防止路径遍历攻击）
    output_dir_abs = os.path.abspath(output_dir)
    file_path_abs = os.path.abspath(file_path)

    if not file_path_abs.startswith(output_dir_abs):
        logger.warning(f"拒绝访问非法路径: {filename}")
        raise HTTPException(status_code=403, detail="访问被拒绝")

    # 检查文件是否存在
    if not os.path.exists(file_path):
        logger.warning(f"文件不存在: {file_path}")
        raise HTTPException(status_code=404, detail="文件不存在")

    # 根据文件类型确定 media_type 和 Content-Disposition
    filename_lower = filename.lower()
    
    if filename_lower.endswith('.csv'):
        media_type = "text/csv"
        content_disposition = f"attachment; filename={filename}"  # CSV文件下载
    elif filename_lower.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
        # 图片文件直接展示
        if filename_lower.endswith('.png'):
            media_type = "image/png"
        elif filename_lower.endswith(('.jpg', '.jpeg')):
            media_type = "image/jpeg"
        elif filename_lower.endswith('.gif'):
            media_type = "image/gif"
        elif filename_lower.endswith('.webp'):
            media_type = "image/webp"
        else:
            media_type = "application/octet-stream"
        content_disposition = f"inline; filename={filename}"  # 图片直接展示
    else:
        logger.warning(f"不支持的文件类型: {filename}")
        raise HTTPException(status_code=400, detail="只支持 CSV 和图片文件（png, jpg, jpeg, gif, webp）")

    logger.info(f"提供文件访问: {filename} (类型: {media_type})")

    # 返回文件响应
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type=media_type,
        headers={
            "Content-Disposition": content_disposition,
            "Cache-Control": "no-cache"
        }
    )


@app.get("/files")
async def list_files():
    """
    列出所有可用的CSV文件

    Returns:
        文件列表，包含文件名、大小、修改时间等信息

    Example:
        GET /files
    """
    global settings

    csv_dir = settings.SQL_OUTPUT_DIR if settings else "/tmp/sensors_data"

    # 检查目录是否存在
    if not os.path.exists(csv_dir):
        return {"files": [], "message": "输出目录不存在"}

    try:
        files_info = []

        for filename in os.listdir(csv_dir):
            if not filename.endswith('.csv'):
                continue

            file_path = os.path.join(csv_dir, filename)

            # 获取文件信息
            stat = os.stat(file_path)

            files_info.append({
                "filename": filename,
                "size_bytes": stat.st_size,
                "size_human": f"{stat.st_size / 1024:.2f} KB",
                "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "download_url": f"/files/{filename}"
            })

        # 按修改时间倒序排序
        files_info.sort(key=lambda x: x["modified_time"], reverse=True)

        return {
            "files": files_info,
            "total_count": len(files_info),
            "directory": csv_dir
        }

    except Exception as e:
        logger.error(f"列出文件失败: {e}")
        raise HTTPException(status_code=500, detail=f"列出文件失败: {str(e)}")


# ============ 主函数 ============

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )

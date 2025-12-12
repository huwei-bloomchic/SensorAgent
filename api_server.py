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
from src.agents.orchestrator_v2 import create_agent_v2


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


# ============ Agent包装器 ============

class StreamingAgentWrapper:
    """
    Agent包装器，支持流式返回thinking步骤和最终结果
    """

    def __init__(self, agent):
        self.agent = agent

    async def query_streaming(
        self,
        user_input: str,
        task_id: Optional[str] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        流式执行查询，yield中间步骤和最终结果

        Args:
            user_input: 用户输入的查询
            task_id: 任务ID，用于CSV文件命名

        Yields:
            {"type": "thinking", "content": "思考步骤内容"}
            {"type": "answer", "content": "最终答案"}
        """
        try:
            # 如果没有提供task_id，生成一个
            if not task_id:
                task_id = uuid.uuid4().hex[:8]
            # 发送开始思考信号
            yield {
                "type": "thinking",
                "content": "🤔 开始分析您的问题...\n"
            }
            await asyncio.sleep(0)  # 让出控制权，确保立即发送

            # 阶段1: 初步分析
            yield {
                "type": "thinking",
                "content": "\n【阶段1】上层分析Agent - 理解问题并制定计划\n"
            }
            await asyncio.sleep(0)

            # 在线程池中调用同步方法
            loop = asyncio.get_event_loop()
            analysis_result = await loop.run_in_executor(
                None,
                self.agent.analyst_agent.analyze,
                user_input,
                "initial"
            )
            analysis_plan = analysis_result.get("analysis_plan", "")

            # 发送分析计划
            plan_summary = self._extract_plan_summary(analysis_plan)
            yield {
                "type": "thinking",
                "content": f"📋 分析计划:\n{plan_summary}\n"
            }
            await asyncio.sleep(0)

            # 解析指令
            instructions = self.agent._parse_instructions(analysis_plan)

            if instructions:
                yield {
                    "type": "thinking",
                    "content": f"\n📝 识别到 {len(instructions)} 个查询任务\n"
                }
            else:
                yield {
                    "type": "thinking",
                    "content": "\n⚠️ 未能提取具体指令，将直接执行查询\n"
                }
                instructions = [{
                    "task": user_input,
                    "time_range": "last_7_days"
                }]
            await asyncio.sleep(0)

            # 阶段2: 执行初步查询
            yield {
                "type": "thinking",
                "content": "\n【阶段2】下层SQL执行Agent - 执行数据查询\n"
            }
            await asyncio.sleep(0)

            initial_results = []
            for i, inst in enumerate(instructions, 1):
                inst_str = inst.get("task", str(inst)) if isinstance(inst, dict) else str(inst)

                yield {
                    "type": "thinking",
                    "content": f"🔍 执行任务 {i}/{len(instructions)}: {inst_str[:80]}...\n"
                }
                await asyncio.sleep(0)

                # 流式执行查询，实时输出 thinking
                result = None
                async for event in self._execute_engineer_streaming(inst_str, task_id):
                    if event["type"] == "thinking":
                        # 转发 EngineerAgent 的 thinking
                        yield event
                        await asyncio.sleep(0)
                    elif event["type"] == "result":
                        result = event["data"]

                if result:
                    initial_results.append(result)

                if result.get("status") == "success":
                    # 提取关键信息进行反馈
                    feedback_parts = [f"✅ 任务 {i} 完成"]

                    # 尝试提取行数信息
                    if "rows" in result:
                        feedback_parts.append(f"数据行数: {result['rows']}")

                    # 尝试提取CSV路径
                    if "csv_path" in result:
                        csv_name = result['csv_path'].split('/')[-1]
                        feedback_parts.append(f"文件: {csv_name}")

                    yield {
                        "type": "thinking",
                        "content": f"{', '.join(feedback_parts)}\n"
                    }

                    # 提取并显示SQL语句和CSV文件路径
                    sql_info = self._extract_sql_and_csv(result)
                    if sql_info:
                        yield {
                            "type": "thinking",
                            "content": sql_info
                        }
                else:
                    yield {
                        "type": "thinking",
                        "content": f"❌ 任务 {i} 失败: {result.get('error', '未知错误')}\n"
                    }
                await asyncio.sleep(0)

            # 阶段3: 评估是否需要下钻
            success_count = sum(1 for r in initial_results if r.get("status") == "success")

            drilldown_results = []
            drilldown_instructions = []

            if success_count > 0:
                yield {
                    "type": "thinking",
                    "content": "\n【阶段3】评估是否需要深入分析\n"
                }
                await asyncio.sleep(0)

                decision = await loop.run_in_executor(
                    None,
                    self.agent.analyst_agent.evaluate_and_decide_drilldown,
                    user_input,
                    initial_results
                )

                if decision["need_drilldown"]:
                    yield {
                        "type": "thinking",
                        "content": f"🔬 需要深入分析\n理由: {decision['reasoning']}\n"
                    }
                    await asyncio.sleep(0)

                    # 生成下钻指令
                    context = {
                        "initial_results": self.agent.analyst_agent._extract_results_summary(initial_results),
                        "suggested_dimensions": decision["suggested_dimensions"]
                    }

                    def analyze_drilldown():
                        return self.agent.analyst_agent.analyze(
                            user_question=user_input,
                            context=context,
                            stage="drilldown"
                        )

                    drilldown_analysis = await loop.run_in_executor(None, analyze_drilldown)
                    drilldown_plan = drilldown_analysis.get("analysis_plan", "")
                    drilldown_instructions = self.agent._parse_instructions(drilldown_plan)

                    if drilldown_instructions:
                        yield {
                            "type": "thinking",
                            "content": f"\n📊 执行 {len(drilldown_instructions)} 个深入查询\n"
                        }
                        await asyncio.sleep(0)

                        for i, inst in enumerate(drilldown_instructions, 1):
                            inst_str = inst.get("task", str(inst)) if isinstance(inst, dict) else str(inst)

                            yield {
                                "type": "thinking",
                                "content": f"🔍 深入查询 {i}/{len(drilldown_instructions)}: {inst_str[:80]}...\n"
                            }
                            await asyncio.sleep(0)

                            # 流式执行下钻查询，实时输出 thinking
                            result = None
                            async for event in self._execute_engineer_streaming(inst_str, task_id):
                                if event["type"] == "thinking":
                                    # 转发 EngineerAgent 的 thinking
                                    yield event
                                    await asyncio.sleep(0)
                                elif event["type"] == "result":
                                    result = event["data"]

                            if result:
                                drilldown_results.append(result)

                            if result.get("status") == "success":
                                # 提取关键信息进行反馈
                                feedback_parts = [f"✅ 深入查询 {i} 完成"]

                                # 尝试提取行数信息
                                if "rows" in result:
                                    feedback_parts.append(f"数据行数: {result['rows']}")

                                # 尝试提取CSV路径
                                if "csv_path" in result:
                                    csv_name = result['csv_path'].split('/')[-1]
                                    feedback_parts.append(f"文件: {csv_name}")

                                yield {
                                    "type": "thinking",
                                    "content": f"{', '.join(feedback_parts)}\n"
                                }

                                # 提取并显示SQL语句和CSV文件路径
                                sql_info = self._extract_sql_and_csv(result)
                                if sql_info:
                                    yield {
                                        "type": "thinking",
                                        "content": sql_info
                                    }
                            else:
                                yield {
                                    "type": "thinking",
                                    "content": f"❌ 深入查询 {i} 失败: {result.get('error', '未知错误')}\n"
                                }
                            await asyncio.sleep(0)
                else:
                    yield {
                        "type": "thinking",
                        "content": "✓ 初步结果已足够，无需深入分析\n"
                    }
                    await asyncio.sleep(0)

            # 阶段4: 生成最终答案
            yield {
                "type": "thinking",
                "content": "\n【阶段4】综合分析并生成报告\n"
            }
            await asyncio.sleep(0)

            all_results = initial_results + drilldown_results
            all_instructions = instructions + drilldown_instructions

            # 统计成功的查询数量
            total_success = sum(1 for r in all_results if r.get("status") == "success")
            yield {
                "type": "thinking",
                "content": f"📊 汇总数据: 共 {len(all_results)} 个查询, {total_success} 个成功\n"
            }
            await asyncio.sleep(0)

            # 生成最终答案
            if len(all_results) == 1 and all_results[0].get("status") == "success" and not drilldown_results:
                yield {
                    "type": "thinking",
                    "content": "✍️ 生成单一查询结果报告...\n"
                }
                await asyncio.sleep(0)

                from src.utils.report_formatter import ReportFormatter
                final_answer = await loop.run_in_executor(
                    None,
                    ReportFormatter.format_single_result,
                    user_input,
                    all_results[0]
                )
            else:
                yield {
                    "type": "thinking",
                    "content": f"✍️ 综合分析 {len(all_results)} 个查询结果...\n"
                }
                await asyncio.sleep(0)

                def generate_final():
                    from src.utils.report_formatter import ReportFormatter
                    synthesis_report = self.agent.analyst_agent.synthesize_results(
                        instructions=all_instructions,
                        results=all_results
                    )
                    return ReportFormatter.format_multiple_results(
                        user_question=user_input,
                        analysis_plan=analysis_plan,
                        initial_results=initial_results,
                        drilldown_results=drilldown_results,
                        synthesis_report=synthesis_report,
                        extract_plan_summary=self.agent._extract_plan_summary
                    )

                final_answer = await loop.run_in_executor(None, generate_final)

            yield {
                "type": "thinking",
                "content": "✅ 报告生成完成\n"
            }
            await asyncio.sleep(0)

            # 发送最终答案
            yield {
                "type": "answer",
                "content": final_answer
            }

        except Exception as e:
            logger.exception("流式查询处理失败")
            yield {
                "type": "error",
                "content": f"处理查询时发生错误: {str(e)}"
            }

    def _extract_plan_summary(self, analysis_plan: str) -> str:
        """提取分析计划摘要"""
        lines = analysis_plan.split('\n')
        summary_lines = []

        for line in lines:
            line = line.strip()
            if line.startswith('```') or line.startswith('{') or line.startswith('['):
                continue
            if line and not line.startswith('#'):
                summary_lines.append(line)
                if len(summary_lines) >= 3:
                    break

        return '\n'.join(summary_lines) if summary_lines else "分析用户问题并生成查询计划"

    async def _execute_engineer_streaming(self, instruction: str, task_id: Optional[str] = None):
        """
        在异步上下文中流式执行 EngineerAgent 的指令

        Args:
            instruction: 指令内容
            task_id: 任务ID

        Yields:
            Dict: 事件字典，包含 type 和相关数据
        """
        import asyncio
        from concurrent.futures import ThreadPoolExecutor

        loop = asyncio.get_event_loop()

        # 创建一个队列用于线程间通信
        import queue
        event_queue = queue.Queue()

        def run_streaming():
            """在线程中运行流式执行"""
            try:
                for event in self.agent.engineer_agent.execute_instruction_streaming(
                    instruction,
                    context=None,
                    task_id=task_id
                ):
                    event_queue.put(("event", event))
            except Exception as e:
                event_queue.put(("error", str(e)))
            finally:
                event_queue.put(("done", None))

        # 在线程池中启动执行
        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(run_streaming)

        # 持续从队列中读取事件
        while True:
            try:
                # 非阻塞地检查队列
                msg_type, data = await loop.run_in_executor(None, event_queue.get, True, 0.1)

                if msg_type == "done":
                    break
                elif msg_type == "error":
                    yield {
                        "type": "result",
                        "data": {
                            "status": "error",
                            "error": data,
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                    break
                elif msg_type == "event":
                    yield data

            except:
                # 队列为空，继续等待
                await asyncio.sleep(0.05)

        executor.shutdown(wait=False)

    def _extract_sql_and_csv(self, result: Dict[str, Any]) -> Optional[str]:
        """
        从查询结果中提取SQL语句和CSV文件路径

        Args:
            result: 查询结果字典

        Returns:
            格式化的SQL和CSV信息字符串，如果提取失败返回None
        """
        import re

        try:
            result_text = result.get("result", "")
            if not result_text:
                return None

            # 确保result_text是字符串
            if not isinstance(result_text, str):
                result_text = str(result_text)

            info_lines = []

            # 提取SQL语句 - 从结果文本中查找SQL
            sql_match = re.search(r'(?:执行SQL|SQL查询|生成的SQL)[:\s]*\n?```(?:sql)?\s*\n?(.*?)\n?```', result_text, re.DOTALL | re.IGNORECASE)
            if not sql_match:
                # 尝试其他模式
                sql_match = re.search(r'SELECT\s+.*?FROM\s+.*?(?:WHERE|GROUP|ORDER|LIMIT|;|\n\n)', result_text, re.DOTALL | re.IGNORECASE)

            if sql_match:
                sql_text = sql_match.group(1) if sql_match.lastindex else sql_match.group(0)
                sql_text = sql_text.strip()
                # 清理SQL文本
                sql_text = re.sub(r'\s+', ' ', sql_text)  # 压缩多余空格
                if len(sql_text) > 200:
                    sql_text = sql_text[:200] + "..."
                info_lines.append(f"📝 SQL: {sql_text}")

            # 提取CSV文件路径
            csv_match = re.search(r'CSV\s*文件[:\s]*(?:\[([^\]]+)\]|\`([^\`]+)\`|([^\n]+))', result_text, re.IGNORECASE)
            if csv_match:
                csv_path = csv_match.group(1) or csv_match.group(2) or csv_match.group(3)
                csv_path = csv_path.strip()
                # 提取文件名
                csv_filename = csv_path.split('/')[-1]

                # 如果有base_url，生成下载链接
                if hasattr(self.agent, 'base_url') and self.agent.base_url:
                    download_url = f"{self.agent.base_url.rstrip('/')}/files/{csv_filename}"
                    info_lines.append(f"💾 CSV文件: {csv_filename}")
                    info_lines.append(f"📥 下载链接: {download_url}")
                else:
                    info_lines.append(f"💾 CSV文件: {csv_path}")

            if info_lines:
                return "\n".join(info_lines) + "\n"

            return None

        except Exception as e:
            logger.warning(f"提取SQL和CSV信息失败: {e}")
            return None


# ============ API端点 ============

@app.on_event("startup")
async def startup_event():
    """启动时初始化Agent"""
    global agent, settings

    logger.info("初始化神策数据分析Agent...")
    settings = get_settings()

    try:
        # 从环境变量获取base_url，或使用默认值
        base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        logger.info(f"API Base URL: {base_url}")

        agent = create_agent_v2(base_url=base_url)
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
            """生成SSE流"""
            wrapper = StreamingAgentWrapper(agent)
            # 使用request_id作为task_id
            task_id = request_id.replace("chatcmpl-", "")

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

            # 流式处理查询，传递task_id
            async for step in wrapper.query_streaming(user_input, task_id=task_id):
                step_type = step.get("type")
                content = step.get("content", "")

                if step_type == "thinking":
                    # 发送thinking步骤
                    chunk = ChatCompletionStreamResponse(
                        id=request_id,
                        created=created_at,
                        model=request.model,
                        choices=[
                            ChatCompletionStreamChoice(
                                index=0,
                                delta=DeltaMessage(content=content),
                                finish_reason=None
                            )
                        ]
                    )
                    yield f"data: {chunk.model_dump_json()}\n\n"

                elif step_type == "answer":
                    # 发送分隔符
                    separator = "\n\n" + "=" * 60 + "\n\n"
                    chunk = ChatCompletionStreamResponse(
                        id=request_id,
                        created=created_at,
                        model=request.model,
                        choices=[
                            ChatCompletionStreamChoice(
                                index=0,
                                delta=DeltaMessage(content=separator),
                                finish_reason=None
                            )
                        ]
                    )
                    yield f"data: {chunk.model_dump_json()}\n\n"

                    # 发送最终答案
                    chunk = ChatCompletionStreamResponse(
                        id=request_id,
                        created=created_at,
                        model=request.model,
                        choices=[
                            ChatCompletionStreamChoice(
                                index=0,
                                delta=DeltaMessage(content=content),
                                finish_reason=None
                            )
                        ]
                    )
                    yield f"data: {chunk.model_dump_json()}\n\n"

                elif step_type == "error":
                    # 发送错误信息
                    chunk = ChatCompletionStreamResponse(
                        id=request_id,
                        created=created_at,
                        model=request.model,
                        choices=[
                            ChatCompletionStreamChoice(
                                index=0,
                                delta=DeltaMessage(content=f"\n\n❌ 错误: {content}"),
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
            # 同步调用Agent，传递task_id
            task_id = request_id.replace("chatcmpl-", "")
            result = agent.query(user_input, task_id=task_id)

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
    下载CSV文件

    Args:
        filename: CSV文件名

    Returns:
        文件下载响应

    Example:
        GET /files/refund_events_cdp_tag_fill_rate.csv
    """
    global settings

    # 获取配置的CSV输出目录
    csv_dir = settings.SQL_OUTPUT_DIR if settings else "/tmp/sensors_data"

    # 构建完整文件路径
    file_path = os.path.join(csv_dir, filename)

    # 安全检查：确保文件路径在允许的目录内（防止路径遍历攻击）
    csv_dir_abs = os.path.abspath(csv_dir)
    file_path_abs = os.path.abspath(file_path)

    if not file_path_abs.startswith(csv_dir_abs):
        logger.warning(f"拒绝访问非法路径: {filename}")
        raise HTTPException(status_code=403, detail="访问被拒绝")

    # 检查文件是否存在
    if not os.path.exists(file_path):
        logger.warning(f"文件不存在: {file_path}")
        raise HTTPException(status_code=404, detail="文件不存在")

    # 检查是否为CSV文件
    if not filename.lower().endswith('.csv'):
        logger.warning(f"非CSV文件访问请求: {filename}")
        raise HTTPException(status_code=400, detail="只支持下载CSV文件")

    logger.info(f"提供文件下载: {filename}")

    # 返回文件响应
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
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

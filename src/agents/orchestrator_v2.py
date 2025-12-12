"""
Agent编排器 V2 - 双层架构
主要的智能代理，协调上层分析Agent和下层SQL执行Agent
"""
from typing import Optional, Dict, Any
from loguru import logger
from datetime import datetime
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from config.settings import get_settings
from src.sensors.client import SensorsClient
from src.agents.analyst_agent import AnalystAgent
from src.agents.engineer_agent import EngineerAgent
from src.models.task_context import TaskContext
from src.utils.report_formatter import ReportFormatter


class SensorsAnalyticsAgentV2:
    """
    神策数据分析智能助手 V2 - 双层架构

    架构:
    - 上层: AnalystAgent (分析规划) - 懂业务，不懂SQL
    - 下层: EngineerAgent (SQL执行) - 懂SQL，不懂业务归因
    - 协调: Orchestrator - 负责上下层通信和流程控制

    功能:
    - 理解用户自然语言查询
    - 上层Agent生成分析计划
    - 下层Agent执行SQL查询
    - 上层Agent综合结果并生成洞察
    """

    def __init__(
        self,
        sensors_client: Optional[SensorsClient] = None,
        analyst_model_name: Optional[str] = None,
        engineer_model_name: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        """
        初始化双层Agent架构

        Args:
            sensors_client: 神策API客户端(可选)
            analyst_model_name: 上层Agent模型名称(可选)
            engineer_model_name: 下层Agent模型名称(可选)
            api_key: API密钥(可选)
            base_url: API服务器基础URL，用于生成CSV下载链接(可选)
        """
        self.settings = get_settings()
        self.base_url = base_url

        # 初始化神策客户端
        if sensors_client is None:
            sensors_client = self._create_sensors_client()
        self.sensors_client = sensors_client

        # 初始化上层分析Agent
        logger.info("初始化上层分析Agent (AnalystAgent)...")
        self.analyst_agent = AnalystAgent(
            model_name=analyst_model_name or self.settings.LITELLM_MODEL,
            api_key=api_key or self.settings.LITELLM_API_KEY
        )

        # 初始化下层SQL执行Agent
        logger.info("初始化下层SQL执行Agent (EngineerAgent)...")
        self.engineer_agent = EngineerAgent(
            sensors_client=sensors_client,
            model_name=engineer_model_name or self.settings.LITELLM_MODEL,
            api_key=api_key or self.settings.LITELLM_API_KEY,
            base_url=base_url
        )

        logger.info("=" * 80)
        logger.info("双层Agent架构初始化完成")
        logger.info("  ├─ 上层: AnalystAgent (业务分析)")
        logger.info("  └─ 下层: EngineerAgent (SQL执行)")
        logger.info("=" * 80)

    def _create_sensors_client(self) -> SensorsClient:
        """创建神策API客户端"""
        logger.info("创建神策API客户端...")

        client = SensorsClient(
            api_url=self.settings.SENSORS_API_URL,
            project=self.settings.SENSORS_PROJECT,
            api_key=self.settings.SENSORS_API_KEY,
            timeout=self.settings.REQUEST_TIMEOUT,
            max_retries=self.settings.MAX_RETRIES
        )

        return client

    def query(
        self,
        user_input: str,
        enable_progressive_analysis: bool = True,
        task_id: Optional[str] = None,
        task_context: Optional[TaskContext] = None
    ) -> str:
        """
        处理用户查询 - 渐进式双层架构协作流程

        渐进式分析流程:
        1. 上层Agent生成初步查询指令
        2. 下层Agent执行初步查询
        3. 上层Agent评估结果，决定是否需要下钻
        4. 如果需要，生成下钻指令并执行
        5. 综合所有结果，生成洞察

        Args:
            user_input: 用户输入的自然语言查询
            enable_progressive_analysis: 是否启用渐进式分析 (默认True)
            task_id: 任务ID，用于CSV文件命名 (可选)
            task_context: 任务上下文，如果提供则使用，否则创建新的 (可选)

        Returns:
            分析结果和洞察
        """
        # 如果没有提供task_id，生成一个
        import uuid
        if not task_id:
            task_id = uuid.uuid4().hex[:8]

        # 创建或使用提供的TaskContext
        if task_context is None:
            task_context = TaskContext(
                task_id=task_id,
                user_question=user_input
            )
        self.task_context = task_context  # 保存为实例变量，方便其他方法访问

        logger.info("=" * 80)
        logger.info(f"[Orchestrator V2] 开始处理查询: {user_input}")
        logger.info(f"[渐进式分析] {'启用' if enable_progressive_analysis else '禁用'}")
        logger.info(f"[TaskContext] 任务ID: {task_id}")
        logger.info("=" * 80)

        try:
            # ============ 阶段1: 初步分析和规划 ============
            logger.info("\n" + "=" * 80)
            logger.info("【阶段1】上层分析Agent - 生成初步查询")
            logger.info("=" * 80)

            # 开始初始迭代
            task_context.start_iteration(
                iteration_type="initial",
                name="初步查询",
                description="根据用户问题生成初步查询计划"
            )

            analysis_result = self.analyst_agent.analyze(user_input, stage="initial")
            analysis_plan = analysis_result.get("analysis_plan", "")

            logger.info(f"[初步分析计划]\n{analysis_plan}")

            # 解析分析计划，提取初步指令
            initial_instructions = self._parse_instructions(analysis_plan)

            if not initial_instructions:
                logger.warning("未能从分析计划中提取到具体指令，使用默认指令")
                initial_instructions = [{
                    "task": user_input,
                    "time_range": "last_7_days",
                    "description": "直接执行用户查询"
                }]

            logger.info(f"\n提取到 {len(initial_instructions)} 条初步查询指令:")
            for i, inst in enumerate(initial_instructions, 1):
                logger.info(f"  {i}. {inst.get('task', inst)}")

            # ============ 阶段2: 执行初步查询 ============
            logger.info("\n" + "=" * 80)
            logger.info("【阶段2】下层执行Agent - 执行初步查询")
            logger.info("=" * 80)

            initial_results = self._execute_instructions(
                initial_instructions,
                task_id=task_id,
                task_context=task_context
            )

            # 检查初步查询是否成功
            success_count = sum(1 for r in initial_results if r.get("status") == "success")
            logger.info(f"\n初步查询完成: {success_count}/{len(initial_results)} 成功")

            # 完成初始迭代
            task_context.complete_iteration()

            # ============ 阶段3: 评估是否需要下钻 ============
            drilldown_results = []
            drilldown_instructions = []

            if enable_progressive_analysis and success_count > 0:
                logger.info("\n" + "=" * 80)
                logger.info("【阶段3】上层分析Agent - 评估是否需要下钻")
                logger.info("=" * 80)

                decision = self.analyst_agent.evaluate_and_decide_drilldown(
                    user_question=user_input,
                    initial_results=initial_results
                )

                logger.info(f"\n[下钻决策] {'需要下钻' if decision['need_drilldown'] else '不需要下钻'}")
                logger.info(f"[决策理由] {decision['reasoning']}")

                # ============ 阶段4: 执行下钻查询 (如果需要) ============
                if decision["need_drilldown"]:
                    logger.info("\n" + "=" * 80)
                    logger.info("【阶段4】生成并执行下钻查询")
                    logger.info("=" * 80)

                    # 开始下钻迭代
                    task_context.start_iteration(
                        iteration_type="drilldown",
                        name="深入分析",
                        description="基于初步结果进行深入分析"
                    )

                    # 准备上下文信息
                    context = {
                        "initial_results": self.analyst_agent._extract_results_summary(initial_results),
                        "suggested_dimensions": decision["suggested_dimensions"]
                    }

                    # 生成下钻指令
                    drilldown_analysis = self.analyst_agent.analyze(
                        user_question=user_input,
                        context=context,
                        stage="drilldown"
                    )
                    drilldown_plan = drilldown_analysis.get("analysis_plan", "")
                    drilldown_instructions = self._parse_instructions(drilldown_plan)

                    if drilldown_instructions:
                        logger.info(f"\n提取到 {len(drilldown_instructions)} 条下钻指令:")
                        for i, inst in enumerate(drilldown_instructions, 1):
                            logger.info(f"  {i}. {inst.get('task', inst)}")

                        # 执行下钻查询，传递task_id和task_context
                        drilldown_results = self._execute_instructions(
                            drilldown_instructions,
                            task_id=task_id,
                            task_context=task_context
                        )

                        # 完成下钻迭代
                        task_context.complete_iteration()

                        drilldown_success = sum(1 for r in drilldown_results if r.get("status") == "success")
                        logger.info(f"\n下钻查询完成: {drilldown_success}/{len(drilldown_results)} 成功")
                    else:
                        logger.info("未能生成有效的下钻指令")
                else:
                    logger.info("\n初步结果已足够，跳过下钻分析")

            # ============ 阶段5: 综合分析 ============
            logger.info("\n" + "=" * 80)
            logger.info("【阶段5】上层分析Agent - 综合所有结果")
            logger.info("=" * 80)

            # 合并所有结果
            all_results = initial_results + drilldown_results
            all_instructions = initial_instructions + drilldown_instructions

            # 标记任务完成
            task_context.completed_at = datetime.now()

            # 如果只有一个初步查询且成功，且不需要下钻，转换为Markdown格式返回
            if len(all_results) == 1 and all_results[0].get("status") == "success" and not drilldown_results:
                logger.info("单一查询成功且不需要下钻，转换为Markdown格式")
                final_result = ReportFormatter.format_single_result(
                    user_question=user_input,
                    result=all_results[0]
                )
                logger.info("=" * 80)
                logger.info("[Orchestrator V2] 查询处理完成")
                logger.info("=" * 80)
                return final_result

            # 需要综合分析
            logger.info("开始综合多个查询结果...")
            synthesis_report = self.analyst_agent.synthesize_results(
                instructions=all_instructions,
                results=all_results
            )

            # ============ 返回最终结果 ============
            logger.info("=" * 80)
            logger.info("[Orchestrator V2] 查询处理完成")
            logger.info("=" * 80)

            # 构建最终输出
            return ReportFormatter.format_multiple_results(
                user_question=user_input,
                analysis_plan=analysis_plan,
                initial_results=initial_results,
                drilldown_results=drilldown_results,
                synthesis_report=synthesis_report,
                extract_plan_summary=self._extract_plan_summary
            )

        except Exception as e:
            error_msg = f"查询处理失败: {str(e)}"
            logger.error("=" * 80)
            logger.error(f"[Orchestrator V2] {error_msg}")
            logger.error("=" * 80)
            logger.exception("详细错误信息:")
            return error_msg

    def _generate_instruction_hash(self, instruction: str) -> str:
        """
        生成指令的唯一标识hash

        用于查询去重：相同的指令会生成相同的hash

        Args:
            instruction: 指令字符串

        Returns:
            32位的MD5 hash字符串
        """
        import hashlib

        # 标准化指令文本（去除空格、转小写）以便更好地匹配
        normalized = instruction.strip().lower()

        # 生成MD5 hash
        hash_obj = hashlib.md5(normalized.encode('utf-8'))
        return hash_obj.hexdigest()

    def _parse_instructions(self, analysis_plan: str) -> list:
        """
        从分析计划中解析指令

        Args:
            analysis_plan: 分析计划文本

        Returns:
            指令列表
        """
        instructions = []

        try:
            # 尝试从JSON代码块中提取
            json_pattern = r'```(?:json|python)?\s*(\{.*?\})\s*```'
            matches = re.finditer(json_pattern, analysis_plan, re.DOTALL)

            for match in matches:
                try:
                    json_str = match.group(1)
                    # 移除Python变量赋值
                    json_str = re.sub(r'^\s*\w+\s*=\s*', '', json_str)
                    instruction = json.loads(json_str)
                    instructions.append(instruction)
                except json.JSONDecodeError:
                    continue

            # 如果没有找到JSON，尝试从文本中提取关键信息
            if not instructions:
                # 查找"查询"、"分析"等关键词开头的行
                lines = analysis_plan.split('\n')
                for line in lines:
                    line = line.strip()
                    if any(keyword in line for keyword in ["查询", "分析", "统计", "计算"]):
                        if len(line) > 10 and not line.startswith('#'):
                            instructions.append({"task": line})

        except Exception as e:
            logger.error(f"解析指令失败: {e}")

        return instructions

    def _extract_plan_summary(self, analysis_plan: str) -> str:
        """
        从分析计划中提取摘要

        Args:
            analysis_plan: 分析计划文本

        Returns:
            计划摘要
        """
        # 提取前500字符作为摘要
        lines = analysis_plan.split('\n')
        summary_lines = []

        for line in lines:
            line = line.strip()
            # 跳过代码块
            if line.startswith('```') or line.startswith('{') or line.startswith('['):
                continue
            if line:
                summary_lines.append(line)
                if len(summary_lines) >= 5:  # 只要前5行非空行
                    break

        return '\n'.join(summary_lines) if summary_lines else "自动分析"

    def _execute_instructions(
        self,
        instructions: list,
        task_id: Optional[str] = None,
        task_context: Optional[TaskContext] = None,
        max_concurrent: int = 6
    ) -> list:
        """
        执行一组指令，支持查询去重和缓存，并记录到TaskContext
        支持并发执行，最多同时执行 max_concurrent 个任务

        Args:
            instructions: 指令列表
            task_id: 任务ID，用于CSV文件命名 (可选)
            task_context: 任务上下文，用于记录中间数据 (可选)
            max_concurrent: 最大并发任务数，默认6

        Returns:
            执行结果列表（保持与输入指令相同的顺序）
        """
        if not instructions:
            return []

        # 线程安全的缓存和计数器
        query_cache = {}  # 查询缓存: {指令hash: 结果}
        cache_lock = threading.Lock()
        deduplicated_count = [0]  # 使用列表以便在闭包中修改

        # 预处理所有指令，准备执行参数
        execution_tasks = []
        for i, instruction in enumerate(instructions):
            # 将指令转换为字符串(如果是字典)
            if isinstance(instruction, dict):
                instruction_str = instruction.get("task", json.dumps(instruction, ensure_ascii=False))
                instruction_params = instruction
            else:
                instruction_str = str(instruction)
                instruction_params = {}

            # 生成指令的唯一标识
            instruction_hash = self._generate_instruction_hash(instruction_str)

            # 在TaskContext中创建查询记录
            query_ctx = None
            if task_context and task_context.current_iteration:
                query_ctx = task_context.create_query(
                    instruction=instruction_str,
                    context=None,
                    parameters=instruction_params
                )

            execution_tasks.append({
                "index": i,
                "instruction": instruction,
                "instruction_str": instruction_str,
                "instruction_params": instruction_params,
                "instruction_hash": instruction_hash,
                "query_ctx": query_ctx
            })

        # 定义单个指令的执行函数
        def execute_single_instruction(task_info: dict) -> tuple:
            """执行单个指令，返回 (索引, 结果)"""
            i = task_info["index"]
            instruction_str = task_info["instruction_str"]
            instruction_hash = task_info["instruction_hash"]
            query_ctx = task_info["query_ctx"]

            logger.info(f"\n--- 执行指令 {i+1}/{len(instructions)} ---")

            # 检查缓存（需要加锁）
            with cache_lock:
                if instruction_hash in query_cache:
                    logger.info(f"⚡ 检测到重复指令，使用缓存结果 (hash: {instruction_hash[:8]}...)")
                    result = query_cache[instruction_hash].copy()
                    result["from_cache"] = True
                    if query_ctx:
                        query_ctx.from_cache = True
                    deduplicated_count[0] += 1
                    return (i, result)

            # 执行新指令（不在锁内执行，避免阻塞其他任务）
            logger.info(f"🔍 执行新指令 (hash: {instruction_hash[:8]}...)")
            result = self.engineer_agent.execute_instruction(
                instruction_str,
                context=None,
                task_id=task_id
            )
            result["query_hash"] = instruction_hash
            result["instruction"] = instruction_str

            # 记录结果到TaskContext
            if query_ctx:
                self._record_result_to_context(query_ctx, result)

            # 缓存成功的查询结果（需要加锁）
            if result.get("status") == "success":
                with cache_lock:
                    query_cache[instruction_hash] = result.copy()

            return (i, result)

        # 使用线程池并发执行
        execution_results = [None] * len(instructions)  # 预分配结果列表，保持顺序

        logger.info(f"🚀 开始并发执行 {len(instructions)} 个指令，最大并发数: {max_concurrent}")

        with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            # 提交所有任务
            future_to_task = {
                executor.submit(execute_single_instruction, task): task
                for task in execution_tasks
            }

            # 收集结果
            completed_count = 0
            for future in as_completed(future_to_task):
                try:
                    index, result = future.result()
                    execution_results[index] = result

                    completed_count += 1
                    status = result.get("status")
                    cache_info = " (缓存)" if result.get("from_cache") else ""
                    
                    if status == "success":
                        logger.info(f"✅ 指令 {index+1}/{len(instructions)} 执行成功{cache_info} [{completed_count}/{len(instructions)}]")
                    elif status == "partial":
                        logger.warning(f"⚠️  指令 {index+1}/{len(instructions)} 部分完成: {result.get('result', result.get('error'))} [{completed_count}/{len(instructions)}]")
                    else:
                        logger.error(f"❌ 指令 {index+1}/{len(instructions)} 执行失败: {result.get('error')} [{completed_count}/{len(instructions)}]")
                except Exception as e:
                    # 处理执行异常
                    task = future_to_task[future]
                    logger.exception(f"❌ 指令 {task['index']+1} 执行异常: {e}")
                    execution_results[task["index"]] = {
                        "status": "error",
                        "instruction": task["instruction_str"],
                        "error": str(e),
                        "timestamp": datetime.now().isoformat()
                    }

        # 记录去重统计
        if deduplicated_count[0] > 0:
            logger.info(f"\n💾 查询去重: 避免了 {deduplicated_count[0]} 次重复执行")

        logger.info(f"✨ 所有指令执行完成: {len(execution_results)} 个结果")

        return execution_results

    def _record_result_to_context(self, query_ctx: Any, result: Dict[str, Any]):
        """
        将查询结果记录到TaskContext

        Args:
            query_ctx: QueryContext对象
            result: 查询结果字典
        """
        try:
            # 解析result中的JSON数据
            result_data = result.get("result", "")
            if isinstance(result_data, str):
                import json
                try:
                    result_data = json.loads(result_data)
                except:
                    pass

            # 记录SQL
            if isinstance(result_data, dict):
                sql = result_data.get("sql_executed") or result_data.get("sql")
                if sql:
                    query_ctx.set_sql(sql)
                    query_ctx.mark_sql_executed()

                # 记录CSV数据
                csv_path = result_data.get("csv_path")
                if csv_path:
                    query_ctx.set_data(
                        csv_path=csv_path,
                        row_count=result_data.get("rows", 0),
                        column_count=result_data.get("column_count"),
                        columns=result_data.get("columns"),
                        data_preview=result_data.get("data_preview", []),
                        download_url=result_data.get("download_url")
                    )

            # 记录状态
            status = result.get("status", "unknown")
            error = result.get("error")
            query_ctx.complete(status=status, error=error)

        except Exception as e:
            logger.warning(f"记录结果到上下文失败: {e}")

    def get_task_context(self) -> Optional[TaskContext]:
        """
        获取当前任务的TaskContext

        Returns:
            TaskContext对象，如果不存在则返回None
        """
        return getattr(self, 'task_context', None)


    def reset(self):
        """重置对话状态"""
        logger.info("重置双层Agent状态")
        # 重新初始化两个Agent
        self.analyst_agent = AnalystAgent(
            model_name=self.settings.LITELLM_MODEL,
            api_key=self.settings.LITELLM_API_KEY
        )
        self.engineer_agent = EngineerAgent(
            sensors_client=self.sensors_client,
            model_name=self.settings.LITELLM_MODEL,
            api_key=self.settings.LITELLM_API_KEY
        )

    def close(self):
        """关闭资源"""
        logger.info("关闭双层Agent资源")
        if self.engineer_agent:
            self.engineer_agent.close()
        if self.sensors_client:
            self.sensors_client.close()


def create_agent_v2(
    analyst_model_name: Optional[str] = None,
    engineer_model_name: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None
) -> SensorsAnalyticsAgentV2:
    """
    工厂函数: 创建双层架构的神策分析Agent

    Args:
        analyst_model_name: 上层Agent模型名称
        engineer_model_name: 下层Agent模型名称
        api_key: API密钥
        base_url: API服务器基础URL，用于生成CSV下载链接

    Returns:
        SensorsAnalyticsAgentV2实例
    """
    return SensorsAnalyticsAgentV2(
        analyst_model_name=analyst_model_name,
        engineer_model_name=engineer_model_name,
        api_key=api_key,
        base_url=base_url
    )

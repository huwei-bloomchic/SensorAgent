"""
Agent编排器 V2 - 双层架构
主要的智能代理，协调上层分析Agent和下层SQL执行Agent
"""
from typing import Optional, Dict, Any
from loguru import logger
from datetime import datetime
import json
import re

from config.settings import get_settings
from src.sensors.client import SensorsClient
from src.agents.analyst_agent import AnalystAgent
from src.agents.engineer_agent import EngineerAgent


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
        api_key: Optional[str] = None
    ):
        """
        初始化双层Agent架构

        Args:
            sensors_client: 神策API客户端(可选)
            analyst_model_name: 上层Agent模型名称(可选)
            engineer_model_name: 下层Agent模型名称(可选)
            api_key: API密钥(可选)
        """
        self.settings = get_settings()

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
            api_key=api_key or self.settings.LITELLM_API_KEY
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

    def query(self, user_input: str, enable_progressive_analysis: bool = True) -> str:
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

        Returns:
            分析结果和洞察
        """
        logger.info("=" * 80)
        logger.info(f"[Orchestrator V2] 开始处理查询: {user_input}")
        logger.info(f"[渐进式分析] {'启用' if enable_progressive_analysis else '禁用'}")
        logger.info("=" * 80)

        try:
            # ============ 阶段1: 初步分析和规划 ============
            logger.info("\n" + "=" * 80)
            logger.info("【阶段1】上层分析Agent - 生成初步查询")
            logger.info("=" * 80)

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

            initial_results = self._execute_instructions(initial_instructions)

            # 检查初步查询是否成功
            success_count = sum(1 for r in initial_results if r.get("status") == "success")
            logger.info(f"\n初步查询完成: {success_count}/{len(initial_results)} 成功")

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

                        # 执行下钻查询
                        drilldown_results = self._execute_instructions(drilldown_instructions)

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

            # 如果只有一个初步查询且成功，且不需要下钻，转换为Markdown格式返回
            if len(all_results) == 1 and all_results[0].get("status") == "success" and not drilldown_results:
                logger.info("单一查询成功且不需要下钻，转换为Markdown格式")
                final_result = self._format_single_result_to_markdown(
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
            return self._format_final_output(
                analysis_plan=analysis_plan,
                initial_results=initial_results,
                drilldown_results=drilldown_results,
                synthesis_report=synthesis_report
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

    def _execute_instructions(self, instructions: list) -> list:
        """
        执行一组指令，支持查询去重和缓存

        Args:
            instructions: 指令列表

        Returns:
            执行结果列表
        """
        execution_results = []
        query_cache = {}  # 查询缓存: {指令hash: 结果}
        deduplicated_count = 0

        for i, instruction in enumerate(instructions, 1):
            logger.info(f"\n--- 执行指令 {i}/{len(instructions)} ---")

            # 将指令转换为字符串(如果是字典)
            if isinstance(instruction, dict):
                instruction_str = instruction.get("task", json.dumps(instruction, ensure_ascii=False))
            else:
                instruction_str = str(instruction)

            # 生成指令的唯一标识
            instruction_hash = self._generate_instruction_hash(instruction_str)

            # 检查是否已经执行过相同的指令
            if instruction_hash in query_cache:
                logger.info(f"⚡ 检测到重复指令，使用缓存结果 (hash: {instruction_hash[:8]}...)")
                result = query_cache[instruction_hash].copy()
                result["from_cache"] = True  # 标记为缓存结果
                deduplicated_count += 1
            else:
                # 调用下层Agent执行
                logger.info(f"🔍 执行新指令 (hash: {instruction_hash[:8]}...)")
                result = self.engineer_agent.execute_instruction(instruction_str)
                result["query_hash"] = instruction_hash  # 添加查询标识
                result["instruction"] = instruction_str  # 记录原始指令

                # 缓存成功的查询结果
                if result.get("status") == "success":
                    query_cache[instruction_hash] = result.copy()

            execution_results.append(result)

            # 记录执行状态
            status = result.get("status")
            if status == "success":
                cache_info = " (缓存)" if result.get("from_cache") else ""
                logger.info(f"✅ 指令 {i} 执行成功{cache_info}")
            elif status == "partial":
                logger.warning(f"⚠️  指令 {i} 部分完成: {result.get('result', result.get('error'))}")
            else:
                logger.error(f"❌ 指令 {i} 执行失败: {result.get('error')}")

        # 记录去重统计
        if deduplicated_count > 0:
            logger.info(f"\n💾 查询去重: 避免了 {deduplicated_count} 次重复执行")

        return execution_results

    def _format_single_result_to_markdown(
        self,
        user_question: str,
        result: Dict[str, Any]
    ) -> str:
        """
        将单个查询结果转换为Markdown格式

        Args:
            user_question: 用户原始问题
            result: 查询结果 (包含JSON格式的result字段)

        Returns:
            Markdown格式的报告
        """
        import json

        # 解析result字段中的JSON数据
        result_data = result.get("result", "")

        try:
            # 尝试解析JSON
            if isinstance(result_data, str):
                data = json.loads(result_data)
            else:
                data = result_data

            # 构建Markdown报告
            lines = []
            lines.append("# 数据分析结果")
            lines.append("")
            lines.append(f"**查询问题:** {user_question}")
            lines.append("")
            lines.append("---")
            lines.append("")

            # 添加核心指标
            lines.append("## 核心指标")
            lines.append("")

            summary = data.get("summary", {})
            if summary:
                # 时间范围
                if "date_range" in summary:
                    date_range = summary["date_range"]
                    lines.append(f"- **查询时间范围:** {date_range[0]} 至 {date_range[1]}")

                # 订单总数
                if "total_orders" in summary:
                    lines.append(f"- **订单总数:** {summary['total_orders']:,}")

                # 渠道数量
                if "total_channels" in summary:
                    lines.append(f"- **渠道数量:** {summary['total_channels']}")

                # Top渠道
                if "top_channel" in summary:
                    top = summary["top_channel"]
                    lines.append(f"- **最大渠道:** {top['name']} (订单数: {top['orders']:,}, GMV: ${top['gmv']:,.2f})")

                lines.append("")

            # 添加数据预览
            lines.append("## 数据预览")
            lines.append("")

            preview = data.get("preview", "")
            if preview:
                # 解析预览文本并转换为表格
                preview_lines = preview.strip().split('\n')

                # 查找表格部分
                table_start = -1
                for i, line in enumerate(preview_lines):
                    if '渠道' in line and '订单数量' in line:
                        table_start = i
                        break

                if table_start >= 0:
                    # 输出标题
                    lines.append("| 排名 | 渠道 | 订单数量 | GMV |")
                    lines.append("|------|------|----------|-----|")

                    # 输出数据行
                    data_lines = preview_lines[table_start + 2:]  # 跳过标题和分隔线
                    for line in data_lines:
                        if line.strip() and not line.startswith('-') and not line.startswith('...'):
                            # 解析每一行: "1. facebook      57,385    $4,084,836.73"
                            parts = line.strip().split()
                            if len(parts) >= 3:
                                rank = parts[0].rstrip('.')
                                channel = parts[1]
                                orders = parts[2] if len(parts) > 2 else '-'
                                gmv = parts[3] if len(parts) > 3 else '-'
                                lines.append(f"| {rank} | {channel} | {orders} | {gmv} |")
                else:
                    # 如果无法解析为表格，直接输出原始预览
                    lines.append("```")
                    lines.append(preview)
                    lines.append("```")

            lines.append("")

            # 添加完整数据文件信息
            lines.append("## 完整数据")
            lines.append("")
            lines.append(f"- **CSV文件路径:** `{data.get('csv_path', 'N/A')}`")
            lines.append(f"- **数据行数:** {data.get('rows', 'N/A')}")
            lines.append(f"- **数据列:** {', '.join(data.get('columns', []))}")
            lines.append("")

            # 添加查询信息
            if "query_info" in summary:
                query_info = summary["query_info"]
                lines.append("## 查询详情")
                lines.append("")
                lines.append(f"- **事件类型:** {query_info.get('event', 'N/A')}")
                lines.append(f"- **国家筛选:** {query_info.get('country_filter', 'N/A')}")
                lines.append(f"- **爬虫过滤:** {query_info.get('spider_filter', 'N/A')}")
                lines.append("")

            lines.append("---")
            lines.append("")
            lines.append(f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

            return "\n".join(lines)

        except json.JSONDecodeError as e:
            logger.warning(f"无法解析JSON结果: {e}")
            # 如果JSON解析失败，返回原始结果
            return f"# 查询结果\n\n```json\n{result_data}\n```"
        except Exception as e:
            logger.error(f"格式化结果失败: {e}", exc_info=True)
            return f"# 查询结果\n\n格式化失败: {str(e)}\n\n```\n{result_data}\n```"

    def _format_final_output(
        self,
        analysis_plan: str,
        initial_results: list,
        drilldown_results: list,
        synthesis_report: str
    ) -> str:
        """
        格式化最终输出报告（Markdown格式）

        Args:
            analysis_plan: 分析计划
            initial_results: 初步查询结果
            drilldown_results: 下钻查询结果
            synthesis_report: 综合分析报告（已经是Markdown格式）

        Returns:
            Markdown格式的完整报告
        """
        # 如果综合报告已经是完整的Markdown格式，直接返回
        # （因为analyst_agent的synthesize_results已经生成了完整的Markdown报告）
        if synthesis_report.strip().startswith("#"):
            return synthesis_report

        # 如果不是Markdown格式，使用传统格式作为后备
        output_lines = []
        output_lines.append("# 神策数据分析报告")
        output_lines.append("")
        output_lines.append("> **分析方法:** 渐进式双层智能分析")
        output_lines.append("")
        output_lines.append("---")
        output_lines.append("")

        # 添加分析方法摘要
        output_lines.append("## 分析方法")
        output_lines.append("")
        output_lines.append(self._extract_plan_summary(analysis_plan))
        output_lines.append("")

        # 添加初步查询结果
        output_lines.append("## 初步查询结果")
        output_lines.append("")
        for i, result in enumerate(initial_results, 1):
            if result.get("status") == "success":
                output_lines.append(f"### 查询 {i}")
                output_lines.append("")
                output_lines.append(str(result.get("result", "")))
                output_lines.append("")
            else:
                output_lines.append(f"### 查询 {i} ❌")
                output_lines.append("")
                output_lines.append(f"**错误:** {result.get('error')}")
                output_lines.append("")

        # 如果有下钻查询，添加下钻结果
        if drilldown_results:
            output_lines.append("## 深入分析结果")
            output_lines.append("")
            for i, result in enumerate(drilldown_results, 1):
                if result.get("status") == "success":
                    output_lines.append(f"### 深入查询 {i}")
                    output_lines.append("")
                    output_lines.append(str(result.get("result", "")))
                    output_lines.append("")
                else:
                    output_lines.append(f"### 深入查询 {i} ❌")
                    output_lines.append("")
                    output_lines.append(f"**错误:** {result.get('error')}")
                    output_lines.append("")

        # 添加综合分析
        output_lines.append("## 业务洞察与建议")
        output_lines.append("")
        output_lines.append(synthesis_report)
        output_lines.append("")
        output_lines.append("---")

        return "\n".join(output_lines)

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
    api_key: Optional[str] = None
) -> SensorsAnalyticsAgentV2:
    """
    工厂函数: 创建双层架构的神策分析Agent

    Args:
        analyst_model_name: 上层Agent模型名称
        engineer_model_name: 下层Agent模型名称
        api_key: API密钥

    Returns:
        SensorsAnalyticsAgentV2实例
    """
    return SensorsAnalyticsAgentV2(
        analyst_model_name=analyst_model_name,
        engineer_model_name=engineer_model_name,
        api_key=api_key
    )

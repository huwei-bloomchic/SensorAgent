"""
报告格式化工具

提供统一的Markdown报告格式化功能，支持：
- 单个查询结果格式化
- 多个查询结果综合格式化
- 从TaskContext生成报告
"""
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from loguru import logger


class ReportFormatter:
    """报告格式化器"""

    @staticmethod
    def format_single_result(
        user_question: str,
        result: Dict[str, Any],
        title: str = "数据分析结果"
    ) -> str:
        """
        将单个查询结果转换为Markdown格式

        Args:
            user_question: 用户原始问题
            result: 查询结果 (包含JSON格式的result字段)
            title: 报告标题

        Returns:
            Markdown格式的报告
        """
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
            lines.append(f"# {title}")
            lines.append("")
            lines.append(f"**查询问题:** {user_question}")
            lines.append("")
            lines.append("---")
            lines.append("")

            # 添加核心指标
            ReportFormatter._add_core_metrics(lines, data)

            # 添加数据预览
            ReportFormatter._add_data_preview(lines, data)

            # 添加关键发现
            ReportFormatter._add_key_findings(lines, data)

            # 添加完整数据文件信息
            ReportFormatter._add_data_files(lines, data)

            # 添加执行的SQL
            ReportFormatter._add_sql_section(lines, data)

            # 添加页脚
            lines.append("---")
            lines.append("")
            lines.append(f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

            return "\n".join(lines)

        except json.JSONDecodeError as e:
            logger.warning(f"无法解析JSON结果: {e}")
            return ReportFormatter._format_error_result(result_data, "JSON解析失败")
        except Exception as e:
            logger.error(f"格式化结果失败: {e}", exc_info=True)
            return ReportFormatter._format_error_result(result_data, f"格式化失败: {str(e)}")

    @staticmethod
    def format_multiple_results(
        user_question: str,
        analysis_plan: str,
        initial_results: List[Dict[str, Any]],
        drilldown_results: Optional[List[Dict[str, Any]]] = None,
        synthesis_report: Optional[str] = None,
        extract_plan_summary: Optional[callable] = None
    ) -> str:
        """
        格式化多个查询结果的综合报告（Markdown格式）

        Args:
            user_question: 用户原始问题
            analysis_plan: 分析计划
            initial_results: 初步查询结果列表
            drilldown_results: 下钻查询结果列表（可选）
            synthesis_report: 综合分析报告（可选，已经是Markdown格式）
            extract_plan_summary: 提取计划摘要的函数（可选）

        Returns:
            Markdown格式的完整报告
        """
        # 如果综合报告已经是完整的Markdown格式，直接返回
        if synthesis_report and synthesis_report.strip().startswith("#"):
            return synthesis_report

        drilldown_results = drilldown_results or []

        # 构建报告
        lines = []
        lines.append("# 神策数据分析报告")
        lines.append("")
        lines.append(f"**查询问题:** {user_question}")
        lines.append("")
        lines.append("> **分析方法:** 渐进式双层智能分析")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 添加分析方法摘要
        if analysis_plan:
            lines.append("## 分析方法")
            lines.append("")
            if extract_plan_summary:
                plan_summary = extract_plan_summary(analysis_plan)
            else:
                plan_summary = ReportFormatter._extract_plan_summary(analysis_plan)
            lines.append(plan_summary)
            lines.append("")

        # 添加初步查询结果
        if initial_results:
            lines.append("## 初步查询结果")
            lines.append("")
            ReportFormatter._add_query_results_section(lines, initial_results, "查询")
            lines.append("")

        # 如果有下钻查询，添加下钻结果
        if drilldown_results:
            lines.append("## 深入分析结果")
            lines.append("")
            ReportFormatter._add_query_results_section(lines, drilldown_results, "深入查询")
            lines.append("")

        # 添加综合分析
        if synthesis_report:
            lines.append("## 业务洞察与建议")
            lines.append("")
            lines.append(synthesis_report)
            lines.append("")

        lines.append("---")
        lines.append("")
        lines.append(f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

        return "\n".join(lines)

    @staticmethod
    def format_from_task_context(
        task_context: Any,
        include_details: bool = True
    ) -> str:
        """
        从TaskContext生成Markdown报告

        Args:
            task_context: TaskContext对象
            include_details: 是否包含详细信息

        Returns:
            Markdown格式的报告
        """
        lines = []
        lines.append("# 数据分析报告")
        lines.append("")
        lines.append(f"**任务ID:** {task_context.task_id}")
        lines.append(f"**用户问题:** {task_context.user_question}")
        lines.append(f"**创建时间:** {task_context.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        if task_context.completed_at:
            lines.append(f"**完成时间:** {task_context.completed_at.strftime('%Y-%m-%d %H:%M:%S')}")
            duration = (task_context.completed_at - task_context.created_at).total_seconds()
            lines.append(f"**执行时长:** {duration:.2f}秒")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 迭代摘要
        for iteration in task_context.iterations:
            lines.append(f"## {iteration.name} (迭代 {iteration.iteration_id})")
            lines.append("")
            lines.append(f"- **类型:** {iteration.iteration_type}")
            lines.append(f"- **查询数量:** {len(iteration.queries)}")
            lines.append(f"- **成功查询:** {sum(1 for q in iteration.queries if q.status == 'success')}")
            lines.append("")

            if include_details:
                # 查询详情
                for query in iteration.queries:
                    lines.append(f"### 查询 {query.query_sequence}")
                    lines.append("")
                    lines.append(f"- **查询ID:** {query.query_id}")
                    lines.append(f"- **指令:** {query.instruction}")
                    lines.append(f"- **状态:** {query.status}")
                    if query.sql:
                        lines.append(f"- **SQL:**")
                        lines.append("```sql")
                        lines.append(query.sql)
                        lines.append("```")
                    if query.csv_path:
                        lines.append(f"- **CSV文件:** {query.csv_path}")
                        lines.append(f"- **数据行数:** {query.data_result_row_count:,}")
                    lines.append("")

        lines.append("---")
        return "\n".join(lines)

    # ========== 私有辅助方法 ==========

    @staticmethod
    def _add_core_metrics(lines: List[str], data: Dict[str, Any]):
        """添加核心指标"""
        lines.append("## 核心指标")
        lines.append("")

        query_info = data.get("query_info", {})
        if query_info:
            if "date_range" in query_info:
                lines.append(f"- **查询时间范围:** {query_info['date_range']}")

            if "total_records" in query_info:
                lines.append(f"- **总记录数:** {query_info['total_records']:,}")

            if "events_analyzed" in query_info:
                events = query_info["events_analyzed"]
                if isinstance(events, list):
                    lines.append(f"- **分析事件:** {', '.join(events)}")
                else:
                    lines.append(f"- **分析事件:** {events}")

            lines.append("")

    @staticmethod
    def _add_data_preview(lines: List[str], data: Dict[str, Any]):
        """添加数据预览"""
        data_preview = data.get("data_preview")
        if not data_preview:
            return

        lines.append("## 数据预览")
        lines.append("")

        # 处理列表类型的数据预览
        if isinstance(data_preview, list):
            # 如果是列表，直接显示为表格
            if len(data_preview) > 0:
                # 获取第一行作为表头
                first_item = data_preview[0]
                if isinstance(first_item, dict):
                    # 构建表头
                    headers = list(first_item.keys())
                    lines.append("| " + " | ".join(headers) + " |")
                    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
                    
                    # 添加数据行
                    for item in data_preview[:10]:  # 只显示前10行
                        if isinstance(item, dict):
                            values = [str(item.get(key, "")) for key in headers]
                            lines.append("| " + " | ".join(values) + " |")
                    
                    if len(data_preview) > 10:
                        lines.append(f"\n*（仅显示前10行，共 {len(data_preview)} 行）*")
                else:
                    # 如果不是字典，直接显示
                    for i, item in enumerate(data_preview[:10], 1):
                        lines.append(f"{i}. {item}")
                    if len(data_preview) > 10:
                        lines.append(f"\n*（仅显示前10项，共 {len(data_preview)} 项）*")
            lines.append("")
            return

        # 处理字典类型的数据预览
        if not isinstance(data_preview, dict):
            # 如果既不是列表也不是字典，直接显示
            lines.append(f"{data_preview}")
            lines.append("")
            return

        # 遍历事件
        for event_name, event_data in data_preview.items():
            lines.append(f"### {event_name}")
            lines.append("")

            # 如果事件数据是字典（可能包含平台分组）
            if isinstance(event_data, dict):
                # 检查是否有平台分组
                first_value = next(iter(event_data.values())) if event_data else None

                if isinstance(first_value, dict) and 'total' in first_value:
                    # 有平台分组
                    lines.append("| 平台 | 总记录数 | 填充率 |")
                    lines.append("|------|----------|--------|")

                    for platform, metrics in event_data.items():
                        total = metrics.get('total', '-')
                        # 提取填充率（可能有多个填充率字段）
                        fill_rates = []
                        for key, value in metrics.items():
                            if 'fill_rate' in key or '填充率' in key:
                                fill_rates.append(str(value))

                        fill_rate_str = ', '.join(fill_rates) if fill_rates else '-'
                        lines.append(f"| {platform} | {total:,} | {fill_rate_str} |")
                else:
                    # 没有平台分组，直接显示指标
                    for key, value in event_data.items():
                        lines.append(f"- **{key}:** {value}")
            elif isinstance(event_data, list):
                # 如果事件数据是列表
                for i, item in enumerate(event_data[:10], 1):
                    if isinstance(item, dict):
                        # 如果是字典列表，显示为表格
                        if i == 1:
                            headers = list(item.keys())
                            lines.append("| " + " | ".join(headers) + " |")
                            lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
                        values = [str(item.get(key, "")) for key in headers]
                        lines.append("| " + " | ".join(values) + " |")
                    else:
                        lines.append(f"{i}. {item}")
                if len(event_data) > 10:
                    lines.append(f"\n*（仅显示前10项，共 {len(event_data)} 项）*")

            lines.append("")

    @staticmethod
    def _add_key_findings(lines: List[str], data: Dict[str, Any]):
        """添加关键发现"""
        key_findings = data.get("key_findings", [])
        if key_findings:
            lines.append("## 关键发现")
            lines.append("")
            for finding in key_findings:
                lines.append(f"- {finding}")
            lines.append("")

    @staticmethod
    def _add_data_files(lines: List[str], data: Dict[str, Any]):
        """添加完整数据文件信息"""
        lines.append("## 完整数据")
        lines.append("")

        # 添加下载链接
        if "download_url" in data:
            csv_filename = data.get('csv_path', '').split('/')[-1]
            download_url = data.get('download_url')
            lines.append(f"- **CSV文件:** [{csv_filename}]({download_url})")
        else:
            lines.append(f"- **CSV文件路径:** `{data.get('csv_path', 'N/A')}`")

        lines.append(f"- **数据行数:** {data.get('rows', 'N/A'):,}")
        lines.append(f"- **数据列:** {', '.join(data.get('columns', []))}")
        lines.append("")

    @staticmethod
    def _add_sql_section(lines: List[str], data: Dict[str, Any]):
        """添加执行的SQL"""
        sql = data.get("sql_executed") or data.get("sql")
        if sql:
            lines.append("## 执行的SQL")
            lines.append("")
            lines.append("```sql")
            lines.append(sql)
            lines.append("```")
            lines.append("")

    @staticmethod
    def _add_query_results_section(
        lines: List[str],
        results: List[Dict[str, Any]],
        query_label: str = "查询"
    ):
        """添加查询结果部分"""
        for i, result in enumerate(results, 1):
            if result.get("status") == "success":
                lines.append(f"### {query_label} {i}")
                lines.append("")
                result_content = result.get("result", "")
                if isinstance(result_content, str):
                    lines.append(result_content)
                else:
                    lines.append(str(result_content))
                lines.append("")
            else:
                lines.append(f"### {query_label} {i} ❌")
                lines.append("")
                lines.append(f"**错误:** {result.get('error', '未知错误')}")
                lines.append("")

    @staticmethod
    def _extract_plan_summary(analysis_plan: str) -> str:
        """从分析计划中提取摘要"""
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

    @staticmethod
    def _format_error_result(result_data: Any, error_msg: str) -> str:
        """格式化错误结果"""
        lines = []
        lines.append("# 查询结果")
        lines.append("")
        lines.append(f"**错误:** {error_msg}")
        lines.append("")
        lines.append("```json")
        if isinstance(result_data, str):
            lines.append(result_data)
        else:
            lines.append(json.dumps(result_data, ensure_ascii=False, indent=2))
        lines.append("```")
        return "\n".join(lines)


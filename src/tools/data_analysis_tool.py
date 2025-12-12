"""
数据分析工具

对查询结果进行深度数据分析，生成趋势、异常和统计洞察
"""

from typing import List, Optional, Dict, Any
from smolagents import Tool
from loguru import logger
import json

from src.analysis import TrendAnalyzer, StatisticsAnalyzer, AnomalyDetector, InsightGenerator
from src.analysis.utils import (
    parse_data_to_dataframe,
    extract_structured_data,
    prepare_timeseries_data,
    validate_analysis_params,
    detect_data_quality_issues,
    calculate_confidence_level,
    sample_large_dataset
)


class DataAnalysisTool(Tool):
    """
    数据分析工具

    对查询结果进行深度分析，包括趋势分析、异常检测、统计分析等
    """

    name = "analyze_data"

    description = """对查询结果进行深度数据分析，生成趋势、异常和统计洞察。

    【使用场景】
    - 用户询问"趋势"、"变化"、"增长"、"下降" → 使用trend分析
    - 用户询问"异常"、"突然"、"波动"、"峰值" → 使用anomaly检测
    - 用户询问"统计"、"平均"、"分布" → 使用statistics分析
    - 用户询问"对比"、"差异" → 使用comparison分析

    【输入格式】
    data: JSON格式的结构化数据，应包含columns和rows字段
    例如：{"columns": ["date", "count"], "rows": [["2024-01-01", 100], ["2024-01-02", 120]]}

    也可以直接从SQLQueryTool的返回结果中提取<structured_data>标签内的JSON数据。

    analysis_types: 分析类型列表，可选值：
    - "trend": 趋势分析（增长率、移动平均、拐点）
    - "anomaly": 异常检测（突变点、异常值）
    - "statistics": 统计分析（均值、分位数、分布）

    metric_columns: 要分析的指标列名列表（必填）
    time_column: 时间列名（可选，用于时间序列分析）
    context: 业务上下文描述（可选，帮助生成更准确的洞察）

    【输出】
    结构化的分析报告，包含：
    - 趋势方向、增长率、峰值/谷值、周期性模式
    - 异常点、突变点
    - 统计指标、分布特征
    - 关键洞察和可行建议

    【示例】
    analyze_data(
        data='{"columns": ["date", "purchases"], "rows": [["2024-11-01", 1234], ["2024-11-02", 1456], ...]}',
        analysis_types=["trend", "anomaly"],
        metric_columns=["purchases"],
        time_column="date",
        context="30天购买趋势分析"
    )
    """

    inputs = {
        "data": {
            "type": "string",
            "description": "JSON格式的结构化数据，包含columns和rows字段"
        },
        "analysis_types": {
            "type": "array",
            "description": "分析类型列表，可选: trend, anomaly, statistics"
        },
        "metric_columns": {
            "type": "array",
            "description": "要分析的指标列名列表"
        },
        "time_column": {
            "type": "string",
            "description": "时间列名（可选）",
            "nullable": True
        },
        "context": {
            "type": "string",
            "description": "业务上下文描述（可选）",
            "nullable": True
        }
    }

    output_type = "string"

    def __init__(self):
        """初始化数据分析工具"""
        super().__init__()

        # 初始化各个分析器
        self.trend_analyzer = TrendAnalyzer()
        self.statistics_analyzer = StatisticsAnalyzer()
        self.anomaly_detector = AnomalyDetector()
        self.insight_generator = InsightGenerator()

        logger.info("DataAnalysisTool 初始化完成")

    def forward(
        self,
        data: str,
        analysis_types: List[str],
        metric_columns: List[str],
        time_column: Optional[str] = None,
        context: Optional[str] = None
    ) -> str:
        """
        执行数据分析

        Args:
            data: JSON格式的结构化数据
            analysis_types: 分析类型列表
            metric_columns: 要分析的指标列名列表
            time_column: 时间列名
            context: 业务上下文

        Returns:
            分析报告（格式化的字符串）
        """
        try:
            logger.info(f"开始数据分析，分析类型: {analysis_types}, 指标列: {metric_columns}")

            # 1. 参数验证
            valid_types = ["trend", "anomaly", "statistics"]
            is_valid, error_msg = validate_analysis_params(data, analysis_types, valid_types)
            if not is_valid:
                return f"❌ 参数验证失败: {error_msg}"

            # 2. 解析数据
            # 首先尝试提取<structured_data>标签
            structured_data = extract_structured_data(data)
            if structured_data:
                data = json.dumps(structured_data)

            df = parse_data_to_dataframe(data)

            if len(df) == 0:
                return "❌ 数据为空，无法进行分析"

            logger.info(f"解析数据成功，行数: {len(df)}, 列数: {len(df.columns)}")

            # 3. 数据质量检查
            quality_report = detect_data_quality_issues(df)
            if quality_report['has_issues']:
                logger.warning(f"数据质量问题: {quality_report['issues']}")

            # 4. 采样大数据集
            if len(df) > 1000:
                logger.info(f"数据量较大({len(df)}行)，进行采样分析")
                original_size = len(df)
                df = sample_large_dataset(df, max_rows=1000)
                logger.info(f"采样后数据量: {len(df)}行")

            # 5. 准备数据
            all_results = {}

            # 对每个指标列进行分析
            for metric_column in metric_columns:
                if metric_column not in df.columns:
                    logger.warning(f"指标列不存在: {metric_column}")
                    continue

                logger.info(f"分析指标: {metric_column}")

                # 准备时间序列数据
                try:
                    value_series, time_series = prepare_timeseries_data(
                        df, time_column, metric_column
                    )
                except Exception as e:
                    logger.error(f"数据准备失败: {str(e)}")
                    return f"❌ 数据准备失败: {str(e)}"

                # 6. 执行各类分析
                metric_results = {}

                # 趋势分析
                if "trend" in analysis_types:
                    logger.info("执行趋势分析...")
                    try:
                        trend_result = self.trend_analyzer.comprehensive_analysis(
                            value_series,
                            time_index=time_series,
                            metric_name=metric_column
                        )
                        metric_results["trend_analysis"] = trend_result
                    except Exception as e:
                        logger.error(f"趋势分析失败: {str(e)}")
                        metric_results["trend_analysis"] = {"error": str(e)}

                # 异常检测
                if "anomaly" in analysis_types:
                    logger.info("执行异常检测...")
                    try:
                        anomaly_result = self.anomaly_detector.comprehensive_detection(
                            value_series,
                            methods=["zscore", "iqr", "sudden_change"],
                            time_index=time_series
                        )
                        metric_results["anomaly_detection"] = anomaly_result
                    except Exception as e:
                        logger.error(f"异常检测失败: {str(e)}")
                        metric_results["anomaly_detection"] = {"error": str(e)}

                # 统计分析
                if "statistics" in analysis_types:
                    logger.info("执行统计分析...")
                    try:
                        stats_result = self.statistics_analyzer.comprehensive_analysis(
                            value_series,
                            metric_name=metric_column
                        )
                        metric_results["statistics"] = stats_result
                    except Exception as e:
                        logger.error(f"统计分析失败: {str(e)}")
                        metric_results["statistics"] = {"error": str(e)}

                all_results[metric_column] = metric_results

            # 7. 生成洞察
            logger.info("生成分析洞察...")

            # 8. 格式化输出
            output = self._format_analysis_report(
                all_results,
                analysis_types,
                context,
                quality_report,
                len(df)
            )

            logger.info("数据分析完成")
            return output

        except Exception as e:
            error_msg = f"数据分析失败: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return f"❌ {error_msg}"

    def _format_analysis_report(
        self,
        results: Dict[str, Any],
        analysis_types: List[str],
        context: Optional[str],
        quality_report: Dict[str, Any],
        data_size: int
    ) -> str:
        """
        格式化分析报告

        Args:
            results: 分析结果
            analysis_types: 分析类型
            context: 业务上下文
            quality_report: 数据质量报告
            data_size: 数据量

        Returns:
            格式化的报告字符串
        """
        lines = []

        # 标题
        lines.append("=" * 60)
        lines.append("📊 数据分析报告")
        if context:
            lines.append(f"分析对象: {context}")
        lines.append("=" * 60)
        lines.append("")

        # 数据概览
        lines.append("【数据概览】")
        lines.append(f"  数据量: {data_size} 行")
        lines.append(f"  分析指标: {', '.join(results.keys())}")
        lines.append(f"  分析类型: {', '.join(analysis_types)}")

        # 置信度
        confidence = calculate_confidence_level(data_size, "general")
        lines.append(f"  分析置信度: {confidence}")

        # 数据质量警告
        if quality_report.get('warnings'):
            for warning in quality_report['warnings']:
                lines.append(f"  ⚠️  {warning}")

        lines.append("")

        # 遍历每个指标的分析结果
        for metric_name, metric_results in results.items():
            lines.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            lines.append(f"指标: {metric_name}")
            lines.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            lines.append("")

            # 趋势分析结果
            if "trend_analysis" in metric_results:
                trend_result = metric_results["trend_analysis"]

                if "error" not in trend_result:
                    lines.append("【趋势分析】")

                    # 整体趋势
                    if "trend" in trend_result:
                        trend = trend_result["trend"]
                        lines.append(f"  整体趋势: {trend.get('description', '未知')} {trend.get('emoji', '')}")

                        if "growth" in trend_result:
                            growth = trend_result["growth"]
                            lines.append(f"  {growth.get('description', '')}")

                            if "daily_growth_rate_pct" in growth:
                                lines.append(f"  日均增长率: {growth['daily_growth_rate_pct']:.2f}%")

                    # 峰值/谷值
                    if "turning_points" in trend_result:
                        tp = trend_result["turning_points"]

                        if tp.get("max_peak"):
                            peak = tp["max_peak"]
                            lines.append(f"  📈 峰值: 第 {peak['index']} 个点, 值: {peak['value']:.2f}")

                        if tp.get("min_trough"):
                            trough = tp["min_trough"]
                            lines.append(f"  📉 谷值: 第 {trough['index']} 个点, 值: {trough['value']:.2f}")

                    # 周期性
                    if "periodicity" in trend_result:
                        periodicity = trend_result["periodicity"]
                        if periodicity.get("has_periodicity"):
                            lines.append(f"  🔄 周期性: {periodicity.get('description', '')}")

                    lines.append("")

            # 异常检测结果
            if "anomaly_detection" in metric_results:
                anomaly_result = metric_results["anomaly_detection"]

                if "error" not in anomaly_result:
                    lines.append("【异常检测】")

                    if "summary" in anomaly_result:
                        summary = anomaly_result["summary"]
                        total_anomalies = summary.get("total_anomaly_points", 0)

                        if total_anomalies > 0:
                            lines.append(f"  检测到 {total_anomalies} 个异常数据点")

                            # 显示各方法的检测结果
                            results_by_method = anomaly_result.get("results_by_method", {})

                            # Z-score异常
                            if "zscore" in results_by_method:
                                zscore = results_by_method["zscore"]
                                anomalies = zscore.get("anomalies", [])
                                if len(anomalies) > 0:
                                    top = anomalies[0]
                                    lines.append(f"  ⚠️  统计异常: 第 {top['index']} 个点偏离 {abs(top['deviation']):.1f}%")

                            # 突变检测
                            if "sudden_change" in results_by_method:
                                changes = results_by_method["sudden_change"].get("changes", [])
                                if len(changes) > 0:
                                    top = changes[0]
                                    change_type = "激增" if top['type'] == 'surge' else "骤降"
                                    lines.append(f"  ⚠️  突变点: 第 {top['index']} 个点{change_type} {abs(top['change_rate_pct']):.1f}%")

                        else:
                            lines.append("  ✓ 未检测到明显异常")

                    lines.append("")

            # 统计分析结果
            if "statistics" in metric_results:
                stats_result = metric_results["statistics"]

                if "error" not in stats_result and "basic_stats" in stats_result:
                    lines.append("【统计分析】")
                    stats = stats_result["basic_stats"]

                    lines.append(f"  平均值: {stats.get('mean', 0):.2f}")
                    lines.append(f"  中位数: {stats.get('median', 0):.2f}")
                    lines.append(f"  标准差: {stats.get('std', 0):.2f}")
                    lines.append(f"  范围: [{stats.get('min', 0):.2f}, {stats.get('max', 0):.2f}]")

                    quantiles = stats.get('quantiles', {})
                    lines.append(f"  分位数 (25%/50%/75%): {quantiles.get('q25', 0):.2f} / {quantiles.get('q50', 0):.2f} / {quantiles.get('q75', 0):.2f}")

                    lines.append("")

        # 生成综合洞察
        lines.append("【综合洞察】")

        # 提取所有指标的洞察
        all_insights = []
        for metric_name, metric_results in results.items():
            if "trend_analysis" in metric_results:
                trend_insights = self.insight_generator.generate_trend_insights(metric_results["trend_analysis"])
                all_insights.extend(trend_insights)

            if "anomaly_detection" in metric_results:
                anomaly_insights = self.insight_generator.generate_anomaly_insights(metric_results["anomaly_detection"])
                all_insights.extend(anomaly_insights)

        # 显示高优先级洞察
        high_priority_insights = [i for i in all_insights if i.get('priority') == 'high']
        if high_priority_insights:
            for insight in high_priority_insights[:5]:  # 最多显示5条
                lines.append(f"  • {insight['insight']}")
        else:
            lines.append("  数据表现正常，未发现显著异常或趋势变化")

        lines.append("")

        # 行动建议
        recommendations = self.insight_generator.generate_recommendations(all_insights, context)
        if recommendations:
            lines.append("【行动建议】")
            for i, rec in enumerate(recommendations[:5], 1):
                lines.append(f"  {i}. {rec}")
            lines.append("")

        lines.append("=" * 60)

        # 附加结构化数据供LLM解读
        lines.append("")
        lines.append("<analysis_insights>")
        insight_json = self.insight_generator.format_for_llm(
            {metric: results[metric] for metric in results.keys()},
            context
        )
        lines.append(insight_json)
        lines.append("</analysis_insights>")

        return "\n".join(lines)

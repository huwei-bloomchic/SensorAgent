"""
洞察生成模块

将分析结果转化为易理解的业务洞察和建议
"""

from typing import Dict, List, Optional, Any
import json


class InsightGenerator:
    """洞察生成器"""

    def __init__(self):
        """初始化洞察生成器"""
        pass

    def generate_trend_insights(self, trend_analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        生成趋势洞察

        Args:
            trend_analysis: 趋势分析结果

        Returns:
            洞察列表
        """
        insights = []

        # 整体趋势洞察
        if 'trend' in trend_analysis:
            trend = trend_analysis['trend']
            direction = trend.get('direction_desc', '未知')
            emoji = trend.get('emoji', '')
            strength = trend.get('strength_desc', '')

            insights.append({
                "type": "trend_direction",
                "priority": "high",
                "insight": f"整体趋势: {direction} {emoji}",
                "detail": f"趋势强度: {strength}"
            })

        # 增长率洞察
        if 'growth' in trend_analysis:
            growth = trend_analysis['growth']
            growth_rate = growth.get('growth_rate', 0)

            if growth_rate != 0 and growth_rate != float('inf'):
                growth_pct = growth_rate * 100
                if abs(growth_pct) > 50:
                    priority = "high"
                    insight = f"显著{'增长' if growth_rate > 0 else '下降'}: {abs(growth_pct):.1f}%"
                elif abs(growth_pct) > 20:
                    priority = "medium"
                    insight = f"{'增长' if growth_rate > 0 else '下降'}: {abs(growth_pct):.1f}%"
                else:
                    priority = "low"
                    insight = f"{'小幅增长' if growth_rate > 0 else '小幅下降'}: {abs(growth_pct):.1f}%"

                insights.append({
                    "type": "growth_rate",
                    "priority": priority,
                    "insight": insight,
                    "detail": f"从 {growth.get('first_value', 0):.0f} 到 {growth.get('last_value', 0):.0f}"
                })

        # 峰值/谷值洞察
        if 'turning_points' in trend_analysis:
            turning_points = trend_analysis['turning_points']

            # 最大峰值
            if turning_points.get('max_peak'):
                peak = turning_points['max_peak']
                insights.append({
                    "type": "peak",
                    "priority": "high",
                    "insight": f"峰值出现在第 {peak['index']} 个数据点",
                    "detail": f"值: {peak['value']:.2f}, 变化: {peak['change_pct']:+.1f}%"
                })

            # 最小谷值
            if turning_points.get('min_trough'):
                trough = turning_points['min_trough']
                insights.append({
                    "type": "trough",
                    "priority": "high",
                    "insight": f"谷值出现在第 {trough['index']} 个数据点",
                    "detail": f"值: {trough['value']:.2f}, 变化: {trough['change_pct']:+.1f}%"
                })

        # 周期性洞察
        if 'periodicity' in trend_analysis:
            periodicity = trend_analysis['periodicity']

            if periodicity.get('has_periodicity'):
                if periodicity.get('pattern') == 'weekly':
                    max_day = periodicity.get('max_day_name', '未知')
                    min_day = periodicity.get('min_day_name', '未知')

                    insights.append({
                        "type": "periodicity",
                        "priority": "medium",
                        "insight": f"周期性模式: {max_day}最高，{min_day}最低",
                        "detail": f"峰值: {periodicity.get('max_value', 0):.0f}, 谷值: {periodicity.get('min_value', 0):.0f}"
                    })

        return insights

    def generate_anomaly_insights(self, anomaly_detection: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        生成异常洞察

        Args:
            anomaly_detection: 异常检测结果

        Returns:
            洞察列表
        """
        insights = []

        # 处理综合检测结果
        if 'results_by_method' in anomaly_detection:
            results = anomaly_detection['results_by_method']

            # Z-score异常
            if 'zscore' in results:
                zscore_result = results['zscore']
                anomalies = zscore_result.get('anomalies', [])

                if len(anomalies) > 0:
                    top_anomaly = anomalies[0]
                    insights.append({
                        "type": "zscore_anomaly",
                        "priority": "high",
                        "insight": f"检测到 {len(anomalies)} 个统计异常值",
                        "detail": f"最显著: 第 {top_anomaly['index']} 个点, 偏离 {abs(top_anomaly['deviation']):.1f}%"
                    })

            # IQR异常
            if 'iqr' in results:
                iqr_result = results['iqr']
                anomalies = iqr_result.get('anomalies', [])

                if len(anomalies) > 0:
                    high_count = sum(1 for a in anomalies if a['type'] == 'high')
                    low_count = sum(1 for a in anomalies if a['type'] == 'low')

                    insights.append({
                        "type": "iqr_anomaly",
                        "priority": "medium",
                        "insight": f"异常值: {high_count} 个过高, {low_count} 个过低",
                        "detail": f"正常范围: [{iqr_result.get('lower_bound', 0):.2f}, {iqr_result.get('upper_bound', 0):.2f}]"
                    })

            # 突变检测
            if 'sudden_change' in results:
                change_result = results['sudden_change']
                changes = change_result.get('changes', [])

                if len(changes) > 0:
                    top_change = changes[0]
                    change_type = "激增" if top_change['type'] == 'surge' else "骤降"

                    insights.append({
                        "type": "sudden_change",
                        "priority": "high",
                        "insight": f"检测到 {len(changes)} 个突变点",
                        "detail": f"最显著: 第 {top_change['index']} 个点 {change_type} {abs(top_change['change_rate_pct']):.1f}%"
                    })

        # 处理单一方法结果
        elif 'anomalies' in anomaly_detection:
            anomalies = anomaly_detection['anomalies']
            method = anomaly_detection.get('method', 'Unknown')

            if len(anomalies) > 0:
                insights.append({
                    "type": "anomaly",
                    "priority": "high",
                    "insight": f"使用{method}方法检测到 {len(anomalies)} 个异常值",
                    "detail": anomaly_detection.get('description', '')
                })

        return insights

    def generate_statistics_insights(self, statistics: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        生成统计洞察

        Args:
            statistics: 统计分析结果

        Returns:
            洞察列表
        """
        insights = []

        # 基础统计洞察
        if 'basic_stats' in statistics:
            stats = statistics['basic_stats']

            mean = stats.get('mean', 0)
            median = stats.get('median', 0)
            std = stats.get('std', 0)
            cv = stats.get('coefficient_of_variation', 0)

            # 均值vs中位数
            if abs(mean - median) / median > 0.2 if median != 0 else False:
                skew_type = "右偏" if mean > median else "左偏"
                insights.append({
                    "type": "distribution_skew",
                    "priority": "medium",
                    "insight": f"数据分布{skew_type}",
                    "detail": f"均值: {mean:.2f}, 中位数: {median:.2f}"
                })

            # 变异系数
            if cv > 0.5:
                insights.append({
                    "type": "high_variability",
                    "priority": "medium",
                    "insight": "数据波动较大",
                    "detail": f"变异系数: {cv:.2f}, 标准差: {std:.2f}"
                })

        # 分布特征洞察
        if 'distribution' in statistics:
            dist = statistics['distribution']

            skewness = dist.get('skewness', 0)
            kurtosis = dist.get('kurtosis', 0)

            if abs(skewness) > 1:
                insights.append({
                    "type": "distribution",
                    "priority": "low",
                    "insight": dist.get('skewness_desc', ''),
                    "detail": f"偏度: {skewness:.2f}"
                })

        return insights

    def generate_recommendations(
        self,
        all_insights: List[Dict[str, str]],
        context: Optional[str] = None
    ) -> List[str]:
        """
        根据洞察生成可行建议

        Args:
            all_insights: 所有洞察
            context: 业务上下文

        Returns:
            建议列表
        """
        recommendations = []

        # 根据不同类型的洞察生成建议
        for insight in all_insights:
            insight_type = insight.get('type')
            priority = insight.get('priority')

            if insight_type == 'trend_direction' and priority == 'high':
                if '下降' in insight.get('insight', ''):
                    recommendations.append("趋势下降，建议分析根本原因并制定改善措施")
                elif '上升' in insight.get('insight', ''):
                    recommendations.append("趋势上升，建议保持当前策略并寻找扩大效果的机会")

            elif insight_type in ['zscore_anomaly', 'sudden_change'] and priority == 'high':
                recommendations.append("检测到异常波动，建议排查对应时间点的业务活动或技术问题")

            elif insight_type == 'peak':
                recommendations.append("峰值时段表现优异，建议分析成功因素并复制到其他时段")

            elif insight_type == 'trough':
                recommendations.append("谷值时段表现不佳，建议重点优化该时段的运营策略")

            elif insight_type == 'periodicity':
                recommendations.append("存在周期性规律，建议根据周期性调整资源分配和营销策略")

            elif insight_type == 'high_variability':
                recommendations.append("数据波动较大，建议稳定核心指标或分段分析不同场景")

        # 去重
        recommendations = list(set(recommendations))

        return recommendations

    def format_for_llm(
        self,
        analysis_results: Dict[str, Any],
        context: Optional[str] = None
    ) -> str:
        """
        将分析结果格式化为结构化JSON，供LLM解读和生成自然语言报告

        Args:
            analysis_results: 完整的分析结果
            context: 业务上下文

        Returns:
            格式化的JSON字符串
        """
        # 提取各类洞察
        insights = {
            "trend": [],
            "anomaly": [],
            "statistics": []
        }

        # 趋势洞察
        if 'trend_analysis' in analysis_results:
            insights['trend'] = self.generate_trend_insights(analysis_results['trend_analysis'])

        # 异常洞察
        if 'anomaly_detection' in analysis_results:
            insights['anomaly'] = self.generate_anomaly_insights(analysis_results['anomaly_detection'])

        # 统计洞察
        if 'statistics' in analysis_results:
            insights['statistics'] = self.generate_statistics_insights(analysis_results['statistics'])

        # 合并所有洞察
        all_insights = insights['trend'] + insights['anomaly'] + insights['statistics']

        # 按优先级排序
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        all_insights.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 3))

        # 生成建议
        recommendations = self.generate_recommendations(all_insights, context)

        # 构建最终结果
        output = {
            "context": context or "数据分析",
            "insights": {
                "key_findings": [i for i in all_insights if i.get('priority') == 'high'],
                "additional_insights": [i for i in all_insights if i.get('priority') != 'high'],
                "all": all_insights
            },
            "recommendations": recommendations,
            "raw_analysis": {
                "trend": analysis_results.get('trend_analysis', {}),
                "anomaly": analysis_results.get('anomaly_detection', {}),
                "statistics": analysis_results.get('statistics', {})
            }
        }

        return json.dumps(output, ensure_ascii=False, indent=2)

    def generate_summary(
        self,
        analysis_results: Dict[str, Any],
        context: Optional[str] = None
    ) -> str:
        """
        生成简洁的分析摘要（纯文本格式，适合直接展示）

        Args:
            analysis_results: 完整的分析结果
            context: 业务上下文

        Returns:
            分析摘要文本
        """
        lines = []

        # 标题
        lines.append("=" * 60)
        lines.append(f"数据分析报告")
        if context:
            lines.append(f"分析对象: {context}")
        lines.append("=" * 60)
        lines.append("")

        # 趋势分析
        if 'trend_analysis' in analysis_results:
            lines.append("【趋势分析】")
            trend_insights = self.generate_trend_insights(analysis_results['trend_analysis'])

            for insight in trend_insights:
                if insight.get('priority') == 'high':
                    lines.append(f"  ✓ {insight['insight']}")
                    if insight.get('detail'):
                        lines.append(f"    {insight['detail']}")

            lines.append("")

        # 异常检测
        if 'anomaly_detection' in analysis_results:
            lines.append("【异常检测】")
            anomaly_insights = self.generate_anomaly_insights(analysis_results['anomaly_detection'])

            if len(anomaly_insights) > 0:
                for insight in anomaly_insights[:3]:  # 最多显示3个
                    lines.append(f"  ⚠️  {insight['insight']}")
                    if insight.get('detail'):
                        lines.append(f"    {insight['detail']}")
            else:
                lines.append("  ✓ 未检测到明显异常")

            lines.append("")

        # 统计概览
        if 'statistics' in analysis_results and 'basic_stats' in analysis_results['statistics']:
            lines.append("【统计概览】")
            stats = analysis_results['statistics']['basic_stats']

            lines.append(f"  数据点数: {stats.get('count', 0)}")
            lines.append(f"  平均值: {stats.get('mean', 0):.2f}")
            lines.append(f"  中位数: {stats.get('median', 0):.2f}")
            lines.append(f"  标准差: {stats.get('std', 0):.2f}")
            lines.append(f"  范围: [{stats.get('min', 0):.2f}, {stats.get('max', 0):.2f}]")

            lines.append("")

        # 行动建议
        all_insights = []
        if 'trend_analysis' in analysis_results:
            all_insights.extend(self.generate_trend_insights(analysis_results['trend_analysis']))
        if 'anomaly_detection' in analysis_results:
            all_insights.extend(self.generate_anomaly_insights(analysis_results['anomaly_detection']))

        recommendations = self.generate_recommendations(all_insights, context)

        if len(recommendations) > 0:
            lines.append("【行动建议】")
            for i, rec in enumerate(recommendations[:5], 1):  # 最多显示5条
                lines.append(f"  {i}. {rec}")

            lines.append("")

        lines.append("=" * 60)

        return "\n".join(lines)

"""
统计分析模块

提供数据的统计分析功能，包括：
- 基础统计量
- 分布分析
- 期间对比
- 分组统计
"""

from typing import Dict, List, Optional, Any, Union
import pandas as pd
import numpy as np
from scipy import stats


class StatisticsAnalyzer:
    """统计分析器"""

    def __init__(self):
        """初始化统计分析器"""
        pass

    def calculate_basic_stats(self, data: pd.Series) -> Dict[str, Any]:
        """
        计算基础统计量

        Args:
            data: 数值序列

        Returns:
            基础统计结果
        """
        if len(data) == 0:
            return {"error": "数据为空"}

        # 去除NaN值
        clean_data = data.dropna()

        if len(clean_data) == 0:
            return {"error": "有效数据为空"}

        result = {
            "count": len(clean_data),
            "mean": float(clean_data.mean()),
            "median": float(clean_data.median()),
            "mode": float(clean_data.mode().iloc[0]) if len(clean_data.mode()) > 0 else None,
            "std": float(clean_data.std()),
            "variance": float(clean_data.var()),
            "min": float(clean_data.min()),
            "max": float(clean_data.max()),
            "range": float(clean_data.max() - clean_data.min()),
            "sum": float(clean_data.sum()),
            "quantiles": {
                "q25": float(clean_data.quantile(0.25)),
                "q50": float(clean_data.quantile(0.50)),
                "q75": float(clean_data.quantile(0.75)),
            },
            "iqr": float(clean_data.quantile(0.75) - clean_data.quantile(0.25))
        }

        # 计算变异系数
        if result["mean"] != 0:
            result["coefficient_of_variation"] = result["std"] / result["mean"]

        return result

    def calculate_distribution_metrics(self, data: pd.Series) -> Dict[str, Any]:
        """
        计算分布特征

        Args:
            data: 数值序列

        Returns:
            分布特征结果
        """
        if len(data) < 3:
            return {"error": "数据不足，需要至少3个数据点"}

        clean_data = data.dropna()

        if len(clean_data) < 3:
            return {"error": "有效数据不足"}

        # 计算偏度和峰度
        skewness = float(stats.skew(clean_data))
        kurtosis = float(stats.kurtosis(clean_data))

        # 正态性检验（如果数据量足够）
        normality_test = None
        if len(clean_data) >= 8:
            try:
                stat, p_value = stats.shapiro(clean_data[:5000])  # Shapiro-Wilk检验最多支持5000个样本
                normality_test = {
                    "test": "Shapiro-Wilk",
                    "statistic": float(stat),
                    "p_value": float(p_value),
                    "is_normal": p_value > 0.05
                }
            except:
                pass

        # 解释偏度
        if abs(skewness) < 0.5:
            skewness_desc = "接近对称"
        elif skewness > 0.5:
            skewness_desc = "右偏（长尾在右侧）"
        else:
            skewness_desc = "左偏（长尾在左侧）"

        # 解释峰度
        if abs(kurtosis) < 0.5:
            kurtosis_desc = "接近正态分布"
        elif kurtosis > 0.5:
            kurtosis_desc = "尖峰分布（比正态分布更集中）"
        else:
            kurtosis_desc = "平峰分布（比正态分布更分散）"

        result = {
            "skewness": skewness,
            "skewness_desc": skewness_desc,
            "kurtosis": kurtosis,
            "kurtosis_desc": kurtosis_desc
        }

        if normality_test:
            result["normality_test"] = normality_test

        return result

    def calculate_period_comparison(
        self,
        current_data: pd.Series,
        previous_data: pd.Series,
        comparison_type: str = "mean"
    ) -> Dict[str, Any]:
        """
        计算期间对比

        Args:
            current_data: 当前期间数据
            previous_data: 对比期间数据
            comparison_type: 对比类型 ('mean', 'sum', 'median')

        Returns:
            期间对比结果
        """
        if len(current_data) == 0 or len(previous_data) == 0:
            return {"error": "数据不足"}

        # 根据对比类型计算值
        if comparison_type == "mean":
            current_value = current_data.mean()
            previous_value = previous_data.mean()
            metric_name = "平均值"
        elif comparison_type == "sum":
            current_value = current_data.sum()
            previous_value = previous_data.sum()
            metric_name = "总和"
        elif comparison_type == "median":
            current_value = current_data.median()
            previous_value = previous_data.median()
            metric_name = "中位数"
        else:
            return {"error": f"不支持的对比类型: {comparison_type}"}

        # 计算变化
        if previous_value == 0:
            if current_value > 0:
                change_rate = float('inf')
                change_desc = "从零开始增长"
            else:
                change_rate = 0
                change_desc = "无变化"
        else:
            change_rate = (current_value - previous_value) / previous_value
            change_desc = f"{'增长' if change_rate > 0 else '下降'} {abs(change_rate):.1%}"

        absolute_change = current_value - previous_value

        return {
            "metric_name": metric_name,
            "current_value": float(current_value),
            "previous_value": float(previous_value),
            "absolute_change": float(absolute_change),
            "change_rate": float(change_rate) if change_rate != float('inf') else None,
            "change_rate_pct": float(change_rate * 100) if change_rate != float('inf') else None,
            "description": change_desc
        }

    def calculate_segment_stats(
        self,
        data: pd.DataFrame,
        groupby_column: str,
        value_column: str
    ) -> Dict[str, Any]:
        """
        计算分组统计

        Args:
            data: 数据框
            groupby_column: 分组列名
            value_column: 数值列名

        Returns:
            分组统计结果
        """
        if groupby_column not in data.columns:
            return {"error": f"分组列不存在: {groupby_column}"}

        if value_column not in data.columns:
            return {"error": f"数值列不存在: {value_column}"}

        # 分组统计
        grouped = data.groupby(groupby_column)[value_column].agg([
            'count', 'mean', 'median', 'sum', 'std', 'min', 'max'
        ])

        # 转换为字典
        result = {
            "groupby_column": groupby_column,
            "value_column": value_column,
            "segments": []
        }

        for group_name, row in grouped.iterrows():
            result["segments"].append({
                "group": str(group_name),
                "count": int(row['count']),
                "mean": float(row['mean']),
                "median": float(row['median']),
                "sum": float(row['sum']),
                "std": float(row['std']) if not pd.isna(row['std']) else 0,
                "min": float(row['min']),
                "max": float(row['max'])
            })

        # 找到最大和最小的组
        if len(result["segments"]) > 0:
            max_segment = max(result["segments"], key=lambda x: x['mean'])
            min_segment = min(result["segments"], key=lambda x: x['mean'])

            result["max_segment"] = max_segment
            result["min_segment"] = min_segment

        return result

    def calculate_correlation(
        self,
        data: pd.DataFrame,
        columns: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        计算相关性

        Args:
            data: 数据框
            columns: 要分析的列名列表（如果为None，分析所有数值列）

        Returns:
            相关性分析结果
        """
        # 选择数值列
        if columns:
            numeric_data = data[columns].select_dtypes(include=[np.number])
        else:
            numeric_data = data.select_dtypes(include=[np.number])

        if numeric_data.shape[1] < 2:
            return {"error": "数值列不足，需要至少2列"}

        # 计算相关系数矩阵
        corr_matrix = numeric_data.corr()

        # 转换为易读格式
        correlations = []
        columns_list = corr_matrix.columns.tolist()

        for i, col1 in enumerate(columns_list):
            for j, col2 in enumerate(columns_list):
                if i < j:  # 只取上三角
                    corr_value = corr_matrix.loc[col1, col2]
                    if not pd.isna(corr_value):
                        # 判断相关性强度
                        abs_corr = abs(corr_value)
                        if abs_corr > 0.7:
                            strength = "强"
                        elif abs_corr > 0.4:
                            strength = "中等"
                        else:
                            strength = "弱"

                        direction = "正相关" if corr_value > 0 else "负相关"

                        correlations.append({
                            "column1": col1,
                            "column2": col2,
                            "correlation": float(corr_value),
                            "strength": strength,
                            "direction": direction,
                            "description": f"{col1} 与 {col2} {direction}（{strength}，r={corr_value:.3f}）"
                        })

        # 按相关系数绝对值排序
        correlations.sort(key=lambda x: abs(x['correlation']), reverse=True)

        return {
            "correlations": correlations,
            "correlation_matrix": corr_matrix.to_dict() if len(correlations) > 0 else {}
        }

    def calculate_percentile_ranks(
        self,
        data: pd.Series,
        values: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """
        计算百分位数排名

        Args:
            data: 数值序列
            values: 要查询排名的值列表（如果为None，返回所有数据的排名）

        Returns:
            百分位数排名结果
        """
        if len(data) == 0:
            return {"error": "数据为空"}

        clean_data = data.dropna()

        if values is None:
            # 计算所有值的百分位排名
            ranks = clean_data.rank(pct=True)
            return {
                "percentile_ranks": ranks.to_dict() if len(ranks) <= 100 else {}
            }
        else:
            # 计算指定值的百分位排名
            results = []
            for value in values:
                rank = (clean_data < value).sum() / len(clean_data)
                results.append({
                    "value": value,
                    "percentile_rank": float(rank * 100),
                    "description": f"超过{rank*100:.1f}%的数据"
                })

            return {"results": results}

    def comprehensive_analysis(
        self,
        data: pd.Series,
        metric_name: str = "指标"
    ) -> Dict[str, Any]:
        """
        综合统计分析

        Args:
            data: 数值序列
            metric_name: 指标名称

        Returns:
            综合统计分析结果
        """
        if len(data) == 0:
            return {
                "status": "error",
                "message": "数据为空"
            }

        # 基础统计
        basic_stats = self.calculate_basic_stats(data)

        # 分布特征
        distribution = self.calculate_distribution_metrics(data)

        return {
            "metric_name": metric_name,
            "basic_stats": basic_stats,
            "distribution": distribution
        }

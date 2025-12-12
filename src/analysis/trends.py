"""
趋势分析模块

提供时间序列数据的趋势分析功能，包括：
- 趋势方向识别（上升/下降/平稳）
- 增长率计算
- 移动平均
- 拐点识别
- 趋势线拟合
"""

from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
import numpy as np
from scipy import stats
from scipy.signal import find_peaks


class TrendAnalyzer:
    """趋势分析器"""

    def __init__(self):
        """初始化趋势分析器"""
        pass

    def detect_trend(self, data: pd.Series, time_index: Optional[pd.Series] = None) -> Dict[str, Any]:
        """
        检测时间序列的整体趋势

        Args:
            data: 数值序列
            time_index: 时间索引（可选）

        Returns:
            趋势分析结果
        """
        if len(data) < 2:
            return {
                "direction": "insufficient_data",
                "strength": 0,
                "description": "数据不足，无法分析趋势"
            }

        # 线性回归分析趋势
        x = np.arange(len(data))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, data)

        # 判断趋势方向
        if p_value > 0.05:
            # 不显著
            direction = "stable"
            description = "平稳"
            emoji = "→"
        elif slope > 0:
            direction = "increasing"
            description = "上升"
            emoji = "↗️" if abs(r_value) > 0.7 else "↗"
        else:
            direction = "decreasing"
            description = "下降"
            emoji = "↘️" if abs(r_value) > 0.7 else "↘"

        # 趋势强度（基于R²值）
        r_squared = r_value ** 2
        if r_squared > 0.8:
            strength = "strong"
            strength_desc = "强"
        elif r_squared > 0.5:
            strength = "moderate"
            strength_desc = "中等"
        else:
            strength = "weak"
            strength_desc = "弱"

        return {
            "direction": direction,
            "direction_desc": description,
            "emoji": emoji,
            "strength": strength,
            "strength_desc": strength_desc,
            "slope": slope,
            "r_squared": r_squared,
            "p_value": p_value,
            "description": f"{description}趋势，强度{strength_desc}"
        }

    def calculate_growth_rate(
        self,
        data: pd.Series,
        period: str = 'total',
        time_index: Optional[pd.Series] = None
    ) -> Dict[str, Any]:
        """
        计算增长率

        Args:
            data: 数值序列
            period: 计算周期 ('total', 'daily', 'weekly', 'monthly')
            time_index: 时间索引

        Returns:
            增长率分析结果
        """
        if len(data) < 2:
            return {"growth_rate": 0, "description": "数据不足"}

        first_value = data.iloc[0]
        last_value = data.iloc[-1]

        if first_value == 0:
            if last_value > 0:
                growth_rate = float('inf')
                description = "从零开始增长"
            else:
                growth_rate = 0
                description = "无变化"
        else:
            growth_rate = (last_value - first_value) / first_value
            description = f"{'增长' if growth_rate > 0 else '下降'} {abs(growth_rate):.1%}"

        # 计算日均增长率（如果是时间序列）
        daily_growth_rate = None
        if period == 'daily' and len(data) > 1:
            # 计算每日增长率
            daily_changes = data.pct_change().dropna()
            daily_growth_rate = daily_changes.mean()

        result = {
            "growth_rate": growth_rate,
            "growth_rate_pct": growth_rate * 100 if growth_rate != float('inf') else None,
            "first_value": first_value,
            "last_value": last_value,
            "absolute_change": last_value - first_value,
            "description": description
        }

        if daily_growth_rate is not None:
            result["daily_growth_rate"] = daily_growth_rate
            result["daily_growth_rate_pct"] = daily_growth_rate * 100

        return result

    def calculate_moving_average(
        self,
        data: pd.Series,
        window: int = 7,
        center: bool = True
    ) -> pd.Series:
        """
        计算移动平均

        Args:
            data: 数值序列
            window: 窗口大小
            center: 是否居中对齐

        Returns:
            移动平均序列
        """
        return data.rolling(window=window, center=center, min_periods=1).mean()

    def identify_turning_points(
        self,
        data: pd.Series,
        prominence: float = None
    ) -> Dict[str, Any]:
        """
        识别拐点、峰值和谷值

        Args:
            data: 数值序列
            prominence: 峰值显著性阈值

        Returns:
            拐点分析结果
        """
        if len(data) < 3:
            return {
                "peaks": [],
                "troughs": [],
                "description": "数据不足，无法识别拐点"
            }

        # 自动设置prominence为标准差
        if prominence is None:
            prominence = data.std() * 0.5

        # 识别峰值
        peaks, peak_properties = find_peaks(data.values, prominence=prominence)

        # 识别谷值（反转数据）
        troughs, trough_properties = find_peaks(-data.values, prominence=prominence)

        # 构建结果
        peak_list = []
        for idx in peaks:
            value = data.iloc[idx]
            # 计算相对于前一个值的增长
            if idx > 0:
                prev_value = data.iloc[idx - 1]
                change = (value - prev_value) / prev_value if prev_value != 0 else 0
            else:
                change = 0

            peak_list.append({
                "index": int(idx),
                "value": float(value),
                "change_pct": float(change * 100) if change != 0 else 0
            })

        trough_list = []
        for idx in troughs:
            value = data.iloc[idx]
            # 计算相对于前一个值的下降
            if idx > 0:
                prev_value = data.iloc[idx - 1]
                change = (value - prev_value) / prev_value if prev_value != 0 else 0
            else:
                change = 0

            trough_list.append({
                "index": int(idx),
                "value": float(value),
                "change_pct": float(change * 100) if change != 0 else 0
            })

        # 找到最大峰值和最小谷值
        max_peak = max(peak_list, key=lambda x: x['value']) if peak_list else None
        min_trough = min(trough_list, key=lambda x: x['value']) if trough_list else None

        return {
            "peaks": peak_list,
            "troughs": trough_list,
            "peak_count": len(peak_list),
            "trough_count": len(trough_list),
            "max_peak": max_peak,
            "min_trough": min_trough,
            "description": f"识别到{len(peak_list)}个峰值和{len(trough_list)}个谷值"
        }

    def fit_trend_line(self, data: pd.Series) -> Dict[str, Any]:
        """
        拟合线性趋势线

        Args:
            data: 数值序列

        Returns:
            趋势线拟合结果
        """
        if len(data) < 2:
            return {
                "slope": 0,
                "intercept": 0,
                "description": "数据不足"
            }

        x = np.arange(len(data))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, data)

        # 生成拟合值
        fitted_values = slope * x + intercept

        return {
            "slope": slope,
            "intercept": intercept,
            "r_squared": r_value ** 2,
            "p_value": p_value,
            "std_err": std_err,
            "fitted_values": fitted_values.tolist(),
            "description": f"斜率: {slope:.2f}, R²: {r_value**2:.3f}"
        }

    def analyze_periodicity(
        self,
        data: pd.Series,
        time_index: Optional[pd.Series] = None
    ) -> Dict[str, Any]:
        """
        分析周期性模式

        Args:
            data: 数值序列
            time_index: 时间索引（应包含日期信息）

        Returns:
            周期性分析结果
        """
        if time_index is None or len(data) < 14:
            return {
                "has_periodicity": False,
                "description": "数据不足或无时间索引"
            }

        # 如果time_index是日期类型，分析星期几的模式
        if hasattr(time_index.iloc[0], 'dayofweek'):
            # 按星期几分组
            df = pd.DataFrame({'value': data.values, 'dayofweek': time_index.dt.dayofweek})
            weekday_avg = df.groupby('dayofweek')['value'].mean()

            # 计算星期几的差异
            weekday_std = weekday_avg.std()
            weekday_mean = weekday_avg.mean()

            if weekday_std / weekday_mean > 0.2:  # 变异系数 > 20%
                # 找到最高和最低的星期几
                max_day = weekday_avg.idxmax()
                min_day = weekday_avg.idxmin()

                day_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

                return {
                    "has_periodicity": True,
                    "pattern": "weekly",
                    "weekday_avg": weekday_avg.to_dict(),
                    "max_day": int(max_day),
                    "max_day_name": day_names[max_day],
                    "max_value": float(weekday_avg.iloc[max_day]),
                    "min_day": int(min_day),
                    "min_day_name": day_names[min_day],
                    "min_value": float(weekday_avg.iloc[min_day]),
                    "description": f"{day_names[max_day]}最高，{day_names[min_day]}最低"
                }

        return {
            "has_periodicity": False,
            "description": "未检测到明显周期性"
        }

    def comprehensive_analysis(
        self,
        data: pd.Series,
        time_index: Optional[pd.Series] = None,
        metric_name: str = "指标"
    ) -> Dict[str, Any]:
        """
        综合趋势分析

        Args:
            data: 数值序列
            time_index: 时间索引
            metric_name: 指标名称

        Returns:
            综合趋势分析结果
        """
        if len(data) == 0:
            return {
                "status": "error",
                "message": "数据为空"
            }

        # 基础统计
        mean_value = data.mean()
        median_value = data.median()
        std_value = data.std()

        # 趋势检测
        trend = self.detect_trend(data, time_index)

        # 增长率
        growth = self.calculate_growth_rate(data, period='daily' if time_index is not None else 'total', time_index=time_index)

        # 拐点识别
        turning_points = self.identify_turning_points(data)

        # 周期性分析
        periodicity = self.analyze_periodicity(data, time_index)

        # 移动平均（平滑）
        ma_window = min(7, len(data))
        moving_avg = self.calculate_moving_average(data, window=ma_window)

        return {
            "metric_name": metric_name,
            "summary": {
                "mean": float(mean_value),
                "median": float(median_value),
                "std": float(std_value),
                "min": float(data.min()),
                "max": float(data.max()),
                "count": len(data)
            },
            "trend": trend,
            "growth": growth,
            "turning_points": turning_points,
            "periodicity": periodicity,
            "moving_average": moving_avg.tolist() if len(moving_avg) <= 100 else []
        }

"""
异常检测模块

提供多种异常检测方法，包括：
- Z-score方法
- IQR（四分位距）方法
- 突变检测
- 时间序列异常
"""

from typing import Dict, List, Optional, Any, Tuple
import pandas as pd
import numpy as np
from scipy import stats


class AnomalyDetector:
    """异常检测器"""

    def __init__(self):
        """初始化异常检测器"""
        pass

    def detect_zscore_anomalies(
        self,
        data: pd.Series,
        threshold: float = 3.0
    ) -> Dict[str, Any]:
        """
        使用Z-score方法检测异常值

        Args:
            data: 数值序列
            threshold: Z-score阈值（默认3.0）

        Returns:
            异常检测结果
        """
        if len(data) < 3:
            return {
                "method": "Z-score",
                "anomalies": [],
                "anomaly_count": 0,
                "description": "数据不足"
            }

        clean_data = data.dropna()

        if len(clean_data) < 3:
            return {
                "method": "Z-score",
                "anomalies": [],
                "anomaly_count": 0,
                "description": "有效数据不足"
            }

        # 计算Z-score
        mean = clean_data.mean()
        std = clean_data.std()

        if std == 0:
            return {
                "method": "Z-score",
                "anomalies": [],
                "anomaly_count": 0,
                "description": "数据无变化，标准差为0"
            }

        z_scores = np.abs((clean_data - mean) / std)

        # 识别异常值
        anomalies = []
        for idx, z_score in z_scores.items():
            if z_score > threshold:
                value = clean_data[idx]
                anomalies.append({
                    "index": int(idx) if isinstance(idx, (int, np.integer)) else str(idx),
                    "value": float(value),
                    "z_score": float(z_score),
                    "deviation": float((value - mean) / mean * 100) if mean != 0 else 0,
                    "description": f"偏离均值{abs((value - mean) / mean * 100):.1f}% (Z={z_score:.2f})"
                })

        # 按Z-score排序
        anomalies.sort(key=lambda x: abs(x['z_score']), reverse=True)

        return {
            "method": "Z-score",
            "threshold": threshold,
            "mean": float(mean),
            "std": float(std),
            "anomalies": anomalies,
            "anomaly_count": len(anomalies),
            "anomaly_rate": len(anomalies) / len(clean_data),
            "description": f"检测到{len(anomalies)}个异常值（阈值={threshold}σ）"
        }

    def detect_iqr_anomalies(
        self,
        data: pd.Series,
        multiplier: float = 1.5
    ) -> Dict[str, Any]:
        """
        使用IQR（四分位距）方法检测异常值

        Args:
            data: 数值序列
            multiplier: IQR倍数（默认1.5）

        Returns:
            异常检测结果
        """
        if len(data) < 4:
            return {
                "method": "IQR",
                "anomalies": [],
                "anomaly_count": 0,
                "description": "数据不足"
            }

        clean_data = data.dropna()

        if len(clean_data) < 4:
            return {
                "method": "IQR",
                "anomalies": [],
                "anomaly_count": 0,
                "description": "有效数据不足"
            }

        # 计算四分位数
        q1 = clean_data.quantile(0.25)
        q3 = clean_data.quantile(0.75)
        iqr = q3 - q1

        if iqr == 0:
            return {
                "method": "IQR",
                "anomalies": [],
                "anomaly_count": 0,
                "description": "IQR为0，数据集中度过高"
            }

        # 计算异常值边界
        lower_bound = q1 - multiplier * iqr
        upper_bound = q3 + multiplier * iqr

        # 识别异常值
        anomalies = []
        for idx, value in clean_data.items():
            if value < lower_bound or value > upper_bound:
                median = clean_data.median()
                anomalies.append({
                    "index": int(idx) if isinstance(idx, (int, np.integer)) else str(idx),
                    "value": float(value),
                    "type": "low" if value < lower_bound else "high",
                    "deviation": float((value - median) / median * 100) if median != 0 else 0,
                    "description": f"{'低于' if value < lower_bound else '高于'}正常范围"
                })

        # 按偏离程度排序
        anomalies.sort(key=lambda x: abs(x['deviation']), reverse=True)

        return {
            "method": "IQR",
            "multiplier": multiplier,
            "q1": float(q1),
            "q3": float(q3),
            "iqr": float(iqr),
            "lower_bound": float(lower_bound),
            "upper_bound": float(upper_bound),
            "anomalies": anomalies,
            "anomaly_count": len(anomalies),
            "anomaly_rate": len(anomalies) / len(clean_data),
            "description": f"检测到{len(anomalies)}个异常值（范围: [{lower_bound:.2f}, {upper_bound:.2f}]）"
        }

    def detect_sudden_changes(
        self,
        data: pd.Series,
        threshold: float = 0.5,
        window: int = 1
    ) -> Dict[str, Any]:
        """
        检测时间序列中的突变

        Args:
            data: 数值序列
            threshold: 变化率阈值（默认0.5，即50%）
            window: 窗口大小（默认1，比较相邻值）

        Returns:
            突变检测结果
        """
        if len(data) < window + 1:
            return {
                "method": "Sudden Change",
                "changes": [],
                "change_count": 0,
                "description": "数据不足"
            }

        clean_data = data.dropna()

        if len(clean_data) < window + 1:
            return {
                "method": "Sudden Change",
                "changes": [],
                "change_count": 0,
                "description": "有效数据不足"
            }

        # 计算变化率
        pct_changes = clean_data.pct_change(periods=window)

        # 识别突变
        changes = []
        for idx, pct_change in pct_changes.items():
            if pd.notna(pct_change) and abs(pct_change) > threshold:
                current_value = clean_data[idx]
                previous_idx = clean_data.index[clean_data.index.get_loc(idx) - window]
                previous_value = clean_data[previous_idx]

                change_type = "surge" if pct_change > 0 else "drop"
                change_desc = "激增" if pct_change > 0 else "骤降"

                changes.append({
                    "index": int(idx) if isinstance(idx, (int, np.integer)) else str(idx),
                    "value": float(current_value),
                    "previous_value": float(previous_value),
                    "change_rate": float(pct_change),
                    "change_rate_pct": float(pct_change * 100),
                    "type": change_type,
                    "description": f"{change_desc} {abs(pct_change * 100):.1f}%"
                })

        # 按变化率绝对值排序
        changes.sort(key=lambda x: abs(x['change_rate']), reverse=True)

        return {
            "method": "Sudden Change",
            "threshold": threshold,
            "threshold_pct": threshold * 100,
            "window": window,
            "changes": changes,
            "change_count": len(changes),
            "description": f"检测到{len(changes)}个突变点（阈值={threshold*100:.0f}%）"
        }

    def detect_timeseries_anomalies(
        self,
        data: pd.Series,
        window_size: int = 7,
        n_std: float = 2.5
    ) -> Dict[str, Any]:
        """
        使用移动窗口检测时间序列异常

        Args:
            data: 数值序列
            window_size: 移动窗口大小（默认7）
            n_std: 标准差倍数（默认2.5）

        Returns:
            时间序列异常检测结果
        """
        if len(data) < window_size * 2:
            return {
                "method": "Timeseries Anomaly",
                "anomalies": [],
                "anomaly_count": 0,
                "description": f"数据不足，需要至少{window_size * 2}个数据点"
            }

        clean_data = data.dropna()

        if len(clean_data) < window_size * 2:
            return {
                "method": "Timeseries Anomaly",
                "anomalies": [],
                "anomaly_count": 0,
                "description": "有效数据不足"
            }

        # 计算移动平均和移动标准差
        rolling_mean = clean_data.rolling(window=window_size, center=True, min_periods=1).mean()
        rolling_std = clean_data.rolling(window=window_size, center=True, min_periods=1).std()

        # 计算异常边界
        upper_bound = rolling_mean + n_std * rolling_std
        lower_bound = rolling_mean - n_std * rolling_std

        # 识别异常值
        anomalies = []
        for idx, value in clean_data.items():
            expected_mean = rolling_mean[idx]
            expected_std = rolling_std[idx]
            upper = upper_bound[idx]
            lower = lower_bound[idx]

            if pd.notna(upper) and pd.notna(lower):
                if value > upper or value < lower:
                    # 计算偏离度
                    if expected_std > 0:
                        deviation_std = abs(value - expected_mean) / expected_std
                    else:
                        deviation_std = 0

                    anomalies.append({
                        "index": int(idx) if isinstance(idx, (int, np.integer)) else str(idx),
                        "value": float(value),
                        "expected_mean": float(expected_mean),
                        "expected_std": float(expected_std),
                        "upper_bound": float(upper),
                        "lower_bound": float(lower),
                        "deviation_std": float(deviation_std),
                        "type": "high" if value > upper else "low",
                        "description": f"{'高于' if value > upper else '低于'}预期范围（偏离{deviation_std:.1f}σ）"
                    })

        # 按偏离度排序
        anomalies.sort(key=lambda x: abs(x['deviation_std']), reverse=True)

        return {
            "method": "Timeseries Anomaly",
            "window_size": window_size,
            "n_std": n_std,
            "anomalies": anomalies,
            "anomaly_count": len(anomalies),
            "anomaly_rate": len(anomalies) / len(clean_data),
            "description": f"检测到{len(anomalies)}个时序异常点"
        }

    def comprehensive_detection(
        self,
        data: pd.Series,
        methods: Optional[List[str]] = None,
        time_index: Optional[pd.Series] = None
    ) -> Dict[str, Any]:
        """
        综合异常检测

        Args:
            data: 数值序列
            methods: 检测方法列表 ['zscore', 'iqr', 'sudden_change', 'timeseries']
            time_index: 时间索引（用于时间序列分析）

        Returns:
            综合异常检测结果
        """
        if len(data) == 0:
            return {
                "status": "error",
                "message": "数据为空"
            }

        # 默认使用所有方法
        if methods is None:
            methods = ['zscore', 'iqr', 'sudden_change']
            if time_index is not None and len(data) >= 14:
                methods.append('timeseries')

        results = {}

        # Z-score检测
        if 'zscore' in methods:
            results['zscore'] = self.detect_zscore_anomalies(data)

        # IQR检测
        if 'iqr' in methods:
            results['iqr'] = self.detect_iqr_anomalies(data)

        # 突变检测
        if 'sudden_change' in methods:
            results['sudden_change'] = self.detect_sudden_changes(data)

        # 时间序列异常检测
        if 'timeseries' in methods and len(data) >= 14:
            results['timeseries'] = self.detect_timeseries_anomalies(data)

        # 汇总所有异常
        all_anomaly_indices = set()
        for method_name, method_result in results.items():
            if 'anomalies' in method_result:
                for anomaly in method_result['anomalies']:
                    all_anomaly_indices.add(anomaly['index'])
            elif 'changes' in method_result:
                for change in method_result['changes']:
                    all_anomaly_indices.add(change['index'])

        # 统计各方法检测到的异常数量
        summary = {
            "total_anomaly_points": len(all_anomaly_indices),
            "methods_used": len(results),
            "details": {
                method: result.get('anomaly_count', result.get('change_count', 0))
                for method, result in results.items()
            }
        }

        return {
            "summary": summary,
            "results_by_method": results,
            "anomaly_indices": sorted(list(all_anomaly_indices))
        }

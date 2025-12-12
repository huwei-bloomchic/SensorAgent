"""
数据分析模块

提供趋势分析、统计分析、异常检测和洞察生成功能
"""

from .trends import TrendAnalyzer
from .statistics import StatisticsAnalyzer
from .anomaly import AnomalyDetector
from .insights import InsightGenerator
from . import utils

__all__ = [
    'TrendAnalyzer',
    'StatisticsAnalyzer',
    'AnomalyDetector',
    'InsightGenerator',
    'utils'
]

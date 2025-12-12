"""
分析工具函数模块

提供数据解析、转换等辅助功能
"""

from typing import Dict, List, Optional, Any, Union, Tuple
import pandas as pd
import numpy as np
import json
import re
from datetime import datetime


def parse_data_to_dataframe(data: Union[str, Dict, List, pd.DataFrame]) -> pd.DataFrame:
    """
    将各种格式的数据转换为DataFrame

    Args:
        data: 输入数据（JSON字符串、字典、列表或DataFrame）

    Returns:
        pandas DataFrame

    Raises:
        ValueError: 数据格式不支持
    """
    # 如果已经是DataFrame
    if isinstance(data, pd.DataFrame):
        return data

    # 如果是JSON字符串
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"无效的JSON字符串: {str(e)}")

    # 如果是字典
    if isinstance(data, dict):
        # 检查是否是{columns: [...], rows: [...]}格式
        if 'columns' in data and 'rows' in data:
            df = pd.DataFrame(data['rows'], columns=data['columns'])
        else:
            # 尝试直接转换
            df = pd.DataFrame(data)
    # 如果是列表
    elif isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        raise ValueError(f"不支持的数据类型: {type(data)}")

    return df


def extract_structured_data(text: str) -> Optional[Dict]:
    """
    从文本中提取<structured_data>标签内的JSON数据

    Args:
        text: 包含structured_data标签的文本

    Returns:
        提取的结构化数据（字典），如果没有找到则返回None
    """
    # 检查text是否为None
    if text is None:
        return None

    # 使用正则表达式提取<structured_data>标签内容
    pattern = r'<structured_data>(.*?)</structured_data>'
    match = re.search(pattern, text, re.DOTALL)

    if match:
        json_str = match.group(1).strip()
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None

    return None


def infer_time_column(df: pd.DataFrame) -> Optional[str]:
    """
    自动推断DataFrame中的时间列

    Args:
        df: 数据框

    Returns:
        时间列名，如果没有找到则返回None
    """
    # 常见的时间列名
    time_column_names = ['date', 'time', 'datetime', 'timestamp', '日期', '时间']

    # 首先检查列名
    for col in df.columns:
        if col.lower() in time_column_names:
            return col

    # 检查数据类型
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            return col

        # 尝试解析为日期
        if df[col].dtype == 'object':
            try:
                pd.to_datetime(df[col].head(5))
                return col
            except:
                continue

    return None


def infer_numeric_columns(df: pd.DataFrame) -> List[str]:
    """
    推断DataFrame中的数值列

    Args:
        df: 数据框

    Returns:
        数值列名列表
    """
    numeric_cols = []

    for col in df.columns:
        # 直接是数值类型
        if pd.api.types.is_numeric_dtype(df[col]):
            numeric_cols.append(col)
        # 尝试转换为数值
        elif df[col].dtype == 'object':
            try:
                pd.to_numeric(df[col].head(5))
                numeric_cols.append(col)
            except:
                continue

    return numeric_cols


def prepare_timeseries_data(
    df: pd.DataFrame,
    time_column: Optional[str] = None,
    value_column: Optional[str] = None
) -> Tuple[pd.Series, Optional[pd.Series]]:
    """
    准备时间序列数据用于分析

    Args:
        df: 数据框
        time_column: 时间列名（可选，会自动推断）
        value_column: 数值列名（可选，会自动选择第一个数值列）

    Returns:
        (数值序列, 时间索引序列)
    """
    # 推断时间列
    if time_column is None:
        time_column = infer_time_column(df)

    # 推断数值列
    if value_column is None:
        numeric_cols = infer_numeric_columns(df)
        if len(numeric_cols) == 0:
            raise ValueError("未找到数值列")
        value_column = numeric_cols[0]

    if value_column not in df.columns:
        raise ValueError(f"数值列不存在: {value_column}")

    # 提取数值序列
    value_series = df[value_column]

    # 提取时间序列（如果存在）
    time_series = None
    if time_column and time_column in df.columns:
        time_series = pd.to_datetime(df[time_column])

    return value_series, time_series


def validate_analysis_params(
    data: Any,
    analysis_types: List[str],
    valid_types: List[str]
) -> Tuple[bool, Optional[str]]:
    """
    验证分析参数

    Args:
        data: 数据
        analysis_types: 分析类型列表
        valid_types: 有效的分析类型列表

    Returns:
        (是否有效, 错误消息)
    """
    # 检查数据
    if data is None:
        return False, "数据不能为空"

    # 检查分析类型
    if not analysis_types:
        return False, "分析类型不能为空"

    for analysis_type in analysis_types:
        if analysis_type not in valid_types:
            return False, f"不支持的分析类型: {analysis_type}，支持的类型: {', '.join(valid_types)}"

    return True, None


def format_number(value: float, precision: int = 2) -> str:
    """
    格式化数字为易读格式

    Args:
        value: 数值
        precision: 小数位数

    Returns:
        格式化后的字符串
    """
    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.{precision}f}B"
    elif abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.{precision}f}M"
    elif abs(value) >= 1_000:
        return f"{value / 1_000:.{precision}f}K"
    else:
        return f"{value:.{precision}f}"


def format_percentage(value: float, precision: int = 1) -> str:
    """
    格式化百分比

    Args:
        value: 数值（0-1之间或已经是百分比）
        precision: 小数位数

    Returns:
        格式化后的百分比字符串
    """
    # 如果值在0-1之间，转换为百分比
    if abs(value) <= 1:
        value = value * 100

    sign = "+" if value > 0 else ""
    return f"{sign}{value:.{precision}f}%"


def sample_large_dataset(df: pd.DataFrame, max_rows: int = 1000) -> pd.DataFrame:
    """
    对大数据集进行采样

    Args:
        df: 数据框
        max_rows: 最大行数

    Returns:
        采样后的数据框
    """
    if len(df) <= max_rows:
        return df

    # 均匀采样
    step = len(df) // max_rows
    return df.iloc[::step].head(max_rows)


def detect_data_quality_issues(df: pd.DataFrame) -> Dict[str, Any]:
    """
    检测数据质量问题

    Args:
        df: 数据框

    Returns:
        数据质量报告
    """
    issues = []
    warnings = []

    # 检查空值
    null_counts = df.isnull().sum()
    if null_counts.sum() > 0:
        null_cols = null_counts[null_counts > 0].to_dict()
        issues.append(f"存在空值: {null_cols}")

    # 检查重复行
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        warnings.append(f"存在{duplicate_count}行重复数据")

    # 检查数据量
    if len(df) < 10:
        warnings.append(f"数据量较少（{len(df)}行），分析结果可能不可靠")

    return {
        "row_count": len(df),
        "column_count": len(df.columns),
        "null_count": int(null_counts.sum()),
        "duplicate_count": int(duplicate_count),
        "issues": issues,
        "warnings": warnings,
        "has_issues": len(issues) > 0
    }


def calculate_confidence_level(data_size: int, metric_type: str = "general") -> str:
    """
    根据数据量计算置信度

    Args:
        data_size: 数据量
        metric_type: 指标类型

    Returns:
        置信度描述
    """
    if metric_type == "trend":
        if data_size >= 30:
            return "高"
        elif data_size >= 14:
            return "中"
        else:
            return "低"
    elif metric_type == "anomaly":
        if data_size >= 50:
            return "高"
        elif data_size >= 20:
            return "中"
        else:
            return "低"
    else:  # general
        if data_size >= 100:
            return "高"
        elif data_size >= 30:
            return "中"
        else:
            return "低"

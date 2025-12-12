"""
基础工具类
所有神策分析工具的基类
"""
from typing import Any, Dict, Optional
from smolagents import Tool
from loguru import logger
from src.sensors.client import SensorsClient


class BaseSensorsTool(Tool):
    """
    神策分析工具基类

    所有神策相关工具都应继承此类
    提供统一的客户端访问、错误处理、结果格式化等功能
    """

    def __init__(self, sensors_client: SensorsClient):
        """
        初始化工具

        Args:
            sensors_client: 神策API客户端实例
        """
        super().__init__()
        self.client = sensors_client
        logger.debug(f"初始化工具: {self.__class__.__name__}")

    def validate_params(self, **kwargs) -> bool:
        """
        验证输入参数

        子类应重写此方法来实现特定的参数验证逻辑

        Args:
            **kwargs: 工具参数

        Returns:
            是否验证通过

        Raises:
            ValueError: 参数验证失败
        """
        return True

    def format_result(self, data: Any) -> str:
        """
        格式化结果为字符串

        将API返回的数据格式化为人类可读的字符串
        子类可以重写此方法来自定义格式化逻辑

        Args:
            data: API返回的原始数据

        Returns:
            格式化后的字符串
        """
        if isinstance(data, dict):
            return self._format_dict(data)
        elif isinstance(data, (list, tuple)):
            return self._format_list(data)
        else:
            return str(data)

    def _format_dict(self, data: Dict, indent: int = 0) -> str:
        """格式化字典"""
        lines = []
        prefix = "  " * indent

        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{prefix}{key}:")
                lines.append(self._format_dict(value, indent + 1))
            elif isinstance(value, (list, tuple)):
                lines.append(f"{prefix}{key}:")
                lines.append(self._format_list(value, indent + 1))
            else:
                lines.append(f"{prefix}{key}: {value}")

        return "\n".join(lines)

    def _format_list(self, data: list, indent: int = 0) -> str:
        """格式化列表"""
        lines = []
        prefix = "  " * indent

        for i, item in enumerate(data):
            if isinstance(item, dict):
                lines.append(f"{prefix}[{i}]:")
                lines.append(self._format_dict(item, indent + 1))
            elif isinstance(item, (list, tuple)):
                lines.append(f"{prefix}[{i}]:")
                lines.append(self._format_list(item, indent + 1))
            else:
                lines.append(f"{prefix}- {item}")

        return "\n".join(lines)

    def handle_error(self, error: Exception) -> str:
        """
        处理错误

        Args:
            error: 异常对象

        Returns:
            错误信息字符串
        """
        error_msg = f"工具执行失败: {str(error)}"
        logger.error(error_msg)
        return error_msg

    def execute_with_error_handling(self, func, *args, **kwargs) -> str:
        """
        带错误处理的执行函数

        Args:
            func: 要执行的函数
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            执行结果或错误信息
        """
        try:
            # 验证参数
            if not self.validate_params(**kwargs):
                return "参数验证失败"

            # 执行函数
            result = func(*args, **kwargs)

            # 格式化结果
            return self.format_result(result)

        except Exception as e:
            return self.handle_error(e)

    def parse_date_range(self, date_range: str) -> tuple[str, str]:
        """
        解析日期范围字符串

        支持的格式:
        - "last_7_days" -> 最近7天
        - "last_30_days" -> 最近30天
        - "today" -> 今天
        - "yesterday" -> 昨天
        - "2024-01-01,2024-01-31" -> 指定日期范围

        Args:
            date_range: 日期范围字符串

        Returns:
            (start_date, end_date) 元组，格式为 "YYYY-MM-DD"

        Raises:
            ValueError: 日期格式不正确
        """
        from datetime import datetime, timedelta

        today = datetime.now().date()

        if date_range == "today":
            date_str = today.strftime("%Y-%m-%d")
            return (date_str, date_str)
        elif date_range == "yesterday":
            yesterday = today - timedelta(days=1)
            date_str = yesterday.strftime("%Y-%m-%d")
            return (date_str, date_str)
        elif date_range.startswith("last_"):
            # 解析 "last_N_days" 格式
            try:
                days = int(date_range.split("_")[1])
                end_date = today
                start_date = today - timedelta(days=days - 1)
                return (
                    start_date.strftime("%Y-%m-%d"),
                    end_date.strftime("%Y-%m-%d")
                )
            except (IndexError, ValueError):
                raise ValueError(f"无效的日期范围格式: {date_range}")
        elif "," in date_range:
            # 解析 "start,end" 格式
            parts = date_range.split(",")
            if len(parts) != 2:
                raise ValueError(f"无效的日期范围格式: {date_range}")
            start_date, end_date = parts[0].strip(), parts[1].strip()
            # 验证日期格式
            try:
                datetime.strptime(start_date, "%Y-%m-%d")
                datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"日期格式必须为 YYYY-MM-DD: {date_range}")
            return (start_date, end_date)
        else:
            raise ValueError(f"不支持的日期范围格式: {date_range}")

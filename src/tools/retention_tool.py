"""
留存分析工具
用于分析用户留存率
"""
from typing import Optional, Dict, Any
from loguru import logger
from src.tools.base_tool import BaseSensorsTool


class RetentionTool(BaseSensorsTool):
    """
    留存分析工具

    分析用户在不同时间段的留存情况
    例如：次日留存、7日留存、30日留存
    """

    name = "retention_analysis"
    description = """分析用户留存率。

    用于分析用户在执行某个起始事件后，在后续时间段内回访的比例。

    参数说明：
    - start_event: 起始事件名称（必填）
      定义留存分析的起点，例如: "AppLaunch", "UserRegistration"
    - return_event: 回访事件名称（必填）
      用于判断用户是否回访的事件，例如: "AppLaunch", "ViewProduct"
    - date_range: 分析日期范围（必填）
      支持格式: "today", "yesterday", "last_7_days", "last_30_days", "2024-01-01,2024-01-31"
    - retention_type: 留存类型（可选）
      可选值: "daily"（日留存）, "weekly"（周留存）, "monthly"（月留存）
      默认: "daily"
    - filters: 过滤条件，JSON格式（可选）
      例如: {"platform": "iOS", "country": "CN"}

    返回：
    - 各时间段的留存率（例如：次日留存、3日留存、7日留存等）
    - 留存用户数
    - 起始用户数

    示例查询：
    - "查看最近30天的用户留存情况"
    - "分析iOS用户的7日留存率"
    - "展示不同平台的留存对比"
    """

    inputs = {
        "start_event": {
            "type": "string",
            "description": "起始事件名称，例如: AppLaunch, UserRegistration"
        },
        "return_event": {
            "type": "string",
            "description": "回访事件名称，例如: AppLaunch"
        },
        "date_range": {
            "type": "string",
            "description": "日期范围，支持: today, yesterday, last_7_days, last_30_days, YYYY-MM-DD,YYYY-MM-DD"
        },
        "retention_type": {
            "type": "string",
            "description": "留存类型: daily（日留存）, weekly（周留存）, monthly（月留存），默认: daily",
            "nullable": True
        },
        "filters": {
            "type": "string",
            "description": "过滤条件（JSON格式），例如: {\"platform\": \"iOS\"}",
            "nullable": True
        }
    }

    output_type = "string"

    def __init__(self, sensors_client):
        super().__init__(sensors_client)
        logger.info("RetentionTool 初始化完成")

    def validate_params(self, **kwargs) -> bool:
        """验证参数"""
        # 验证必填参数
        if "start_event" not in kwargs or not kwargs["start_event"]:
            raise ValueError("start_event 参数是必填的")
        if "return_event" not in kwargs or not kwargs["return_event"]:
            raise ValueError("return_event 参数是必填的")
        if "date_range" not in kwargs or not kwargs["date_range"]:
            raise ValueError("date_range 参数是必填的")

        # 验证留存类型
        if "retention_type" in kwargs and kwargs["retention_type"]:
            valid_types = ["daily", "weekly", "monthly"]
            if kwargs["retention_type"] not in valid_types:
                raise ValueError(f"retention_type 必须是以下之一: {', '.join(valid_types)}")

        return True

    def forward(
        self,
        start_event: str,
        return_event: str,
        date_range: str,
        retention_type: Optional[str] = None,
        filters: Optional[str] = None
    ) -> str:
        """
        执行留存分析

        Args:
            start_event: 起始事件名称
            return_event: 回访事件名称
            date_range: 日期范围
            retention_type: 留存类型（daily/weekly/monthly）
            filters: 过滤条件（JSON字符串）

        Returns:
            留存分析结果
        """
        logger.info(
            f"执行留存分析: start_event={start_event}, return_event={return_event}, "
            f"date_range={date_range}, retention_type={retention_type}"
        )

        try:
            import json

            # 解析参数
            start_date, end_date = self.parse_date_range(date_range)
            ret_type = retention_type if retention_type else "daily"

            # 解析过滤条件
            filters_dict = None
            if filters:
                try:
                    filters_dict = json.loads(filters)
                except json.JSONDecodeError:
                    logger.warning(f"无法解析过滤条件: {filters}")

            logger.debug(
                f"解析后的参数: start_event={start_event}, return_event={return_event}, "
                f"dates={start_date}~{end_date}, type={ret_type}"
            )

            # 调用神策API
            result = self.client.query_retention(
                start_event=start_event,
                return_event=return_event,
                start_date=start_date,
                end_date=end_date,
                retention_type=ret_type,
                filters=filters_dict
            )

            # 格式化结果
            return self._format_retention_result(result, start_event, return_event, ret_type)

        except Exception as e:
            return self.handle_error(e)

    def _format_retention_result(
        self,
        data: Dict[str, Any],
        start_event: str,
        return_event: str,
        retention_type: str
    ) -> str:
        """
        格式化留存分析结果

        Args:
            data: API返回的原始数据
            start_event: 起始事件
            return_event: 回访事件
            retention_type: 留存类型

        Returns:
            格式化后的结果字符串
        """
        lines = ["=" * 60]
        lines.append("留存分析结果")
        lines.append("=" * 60)
        lines.append("")

        # 如果API返回了错误
        if "error" in data:
            lines.append(f"❌ 查询失败: {data['error']}")
            return "\n".join(lines)

        # 显示分析参数
        type_name = {"daily": "日留存", "weekly": "周留存", "monthly": "月留存"}.get(
            retention_type, retention_type
        )
        lines.append(f"📊 分析类型: {type_name}")
        lines.append(f"   起始事件: {start_event}")
        lines.append(f"   回访事件: {return_event}")
        lines.append("")

        # 提取留存数据（根据实际API响应结构调整）
        if "data" in data:
            retention_data = data["data"]

            # 显示起始用户数
            initial_users = retention_data.get("initial_users", 0)
            lines.append(f"👥 起始用户数: {initial_users:,}")
            lines.append("")

            # 显示留存率数据
            if "retention_rates" in retention_data:
                lines.append("📈 留存率:")
                lines.append("")

                rates = retention_data["retention_rates"]
                for period, rate_data in rates.items():
                    if isinstance(rate_data, dict):
                        retained_users = rate_data.get("retained_users", 0)
                        retention_rate = rate_data.get("rate", 0)
                    else:
                        # 如果只是一个数字
                        retention_rate = rate_data
                        retained_users = int(initial_users * retention_rate / 100)

                    # 格式化周期名称
                    period_name = self._format_period_name(period, retention_type)

                    lines.append(f"  {period_name}:")
                    lines.append(f"    留存率: {retention_rate:.2f}%")
                    lines.append(f"    留存用户: {retained_users:,}")
                    lines.append("")

            # 显示留存趋势（如果有）
            if "trend" in retention_data:
                trend = retention_data["trend"]
                lines.append("-" * 60)
                lines.append(f"📉 留存趋势: {trend}")

        else:
            # 如果数据结构不符合预期，显示原始数据
            lines.append("原始数据:")
            lines.append(self.format_result(data))

        lines.append("")
        lines.append("=" * 60)

        return "\n".join(lines)

    def _format_period_name(self, period: str, retention_type: str) -> str:
        """
        格式化周期名称

        Args:
            period: 周期标识（如 "day_1", "day_7"）
            retention_type: 留存类型

        Returns:
            格式化后的周期名称
        """
        try:
            if retention_type == "daily":
                if period.startswith("day_"):
                    day_num = period.split("_")[1]
                    return f"第{day_num}天"
            elif retention_type == "weekly":
                if period.startswith("week_"):
                    week_num = period.split("_")[1]
                    return f"第{week_num}周"
            elif retention_type == "monthly":
                if period.startswith("month_"):
                    month_num = period.split("_")[1]
                    return f"第{month_num}月"
        except (IndexError, ValueError):
            pass

        # 如果无法解析，返回原始值
        return period

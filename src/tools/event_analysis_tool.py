"""
事件分析工具
用于查询和分析神策事件数据
"""
from typing import Optional
from loguru import logger
from src.tools.base_tool import BaseSensorsTool


class EventAnalysisTool(BaseSensorsTool):
    """
    事件分析工具

    用于查询事件数据，包括事件次数、用户数、属性分布等
    支持按日期、维度分组，以及各种过滤条件
    """

    name = "event_analysis"
    description = """分析神策事件数据。

    使用此工具可以：
    - 查询事件的发生次数
    - 查询触发事件的用户数
    - 按日期、平台、地域等维度分组
    - 应用过滤条件筛选数据

    参数说明：
    - event_name: 事件名称（必填），如 "$AppStart"（应用启动）, "$PageView"（页面浏览）, "purchase"（购买）等
    - date_range: 日期范围（必填），支持格式：
        * "today" - 今天
        * "yesterday" - 昨天
        * "last_7_days" - 最近7天
        * "last_30_days" - 最近30天
        * "2024-01-01,2024-01-31" - 指定日期范围
    - group_by: 分组维度（可选），如 "date"（按日期）, "platform"（按平台）, "province"（按省份）等
    - filters: 过滤条件（可选），JSON字符串格式

    示例：
    1. 查询最近7天的应用启动次数：
       event_name="$AppStart", date_range="last_7_days"

    2. 按日期查询最近30天的购买事件：
       event_name="purchase", date_range="last_30_days", group_by="date"

    3. 查询今天iOS平台的页面浏览：
       event_name="$PageView", date_range="today", filters='{"platform": "iOS"}'
    """

    inputs = {
        "event_name": {
            "type": "string",
            "description": "事件名称，如 $AppStart, $PageView, purchase 等"
        },
        "date_range": {
            "type": "string",
            "description": "日期范围，如 last_7_days, today, 2024-01-01,2024-01-31"
        },
        "group_by": {
            "type": "string",
            "description": "分组维度（可选），如 date, platform, province",
            "nullable": True
        },
        "filters": {
            "type": "string",
            "description": "过滤条件JSON字符串（可选）",
            "nullable": True
        }
    }

    output_type = "string"

    def forward(
        self,
        event_name: str,
        date_range: str,
        group_by: Optional[str] = None,
        filters: Optional[str] = None
    ) -> str:
        """
        执行事件分析

        Args:
            event_name: 事件名称
            date_range: 日期范围
            group_by: 分组维度
            filters: 过滤条件

        Returns:
            分析结果字符串
        """
        logger.info(f"执行事件分析: event={event_name}, date_range={date_range}")

        def _analyze():
            # 解析日期范围
            start_date, end_date = self.parse_date_range(date_range)

            # 解析过滤条件
            filter_dict = None
            if filters:
                import json
                try:
                    filter_dict = json.loads(filters)
                except json.JSONDecodeError as e:
                    raise ValueError(f"过滤条件JSON解析失败: {str(e)}")

            # 准备分组维度
            group_by_list = None
            if group_by:
                group_by_list = [g.strip() for g in group_by.split(",")]

            # 调用API
            result = self.client.query_events(
                event_name=event_name,
                start_date=start_date,
                end_date=end_date,
                metrics=["total", "unique_users"],  # 查询总次数和独立用户数
                group_by=group_by_list,
                filters=filter_dict
            )

            # 格式化结果
            return self._format_event_result(result, event_name, start_date, end_date)

        return self.execute_with_error_handling(
            _analyze,
            event_name=event_name,
            date_range=date_range,
            group_by=group_by,
            filters=filters
        )

    def _format_event_result(
        self,
        result: dict,
        event_name: str,
        start_date: str,
        end_date: str
    ) -> str:
        """
        格式化事件分析结果

        Args:
            result: API返回结果
            event_name: 事件名称
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            格式化的字符串结果
        """
        lines = []
        lines.append(f"=== 事件分析结果 ===")
        lines.append(f"事件: {event_name}")
        lines.append(f"时间范围: {start_date} 至 {end_date}")
        lines.append("")

        # 提取数据
        if isinstance(result, dict):
            # 总计数据
            if "total" in result:
                lines.append(f"总次数: {result['total']:,}")
            if "unique_users" in result:
                lines.append(f"独立用户数: {result['unique_users']:,}")

            # 分组数据
            if "data" in result and isinstance(result["data"], list):
                lines.append("")
                lines.append("详细数据:")
                lines.append("-" * 50)

                for item in result["data"]:
                    if isinstance(item, dict):
                        # 格式化每一行数据
                        line_parts = []
                        for key, value in item.items():
                            if key not in ["total", "unique_users"]:
                                line_parts.append(f"{key}={value}")

                        dimension_str = ", ".join(line_parts) if line_parts else "总计"

                        total = item.get("total", 0)
                        users = item.get("unique_users", 0)

                        lines.append(f"  {dimension_str}")
                        lines.append(f"    次数: {total:,}, 用户数: {users:,}")
            elif "error" in result:
                lines.append(f"错误: {result['error']}")
        else:
            lines.append("原始结果:")
            lines.append(str(result))

        return "\n".join(lines)

    def validate_params(self, **kwargs) -> bool:
        """验证参数"""
        event_name = kwargs.get("event_name")
        date_range = kwargs.get("date_range")

        if not event_name:
            raise ValueError("event_name 不能为空")
        if not date_range:
            raise ValueError("date_range 不能为空")

        # 验证日期范围格式
        try:
            self.parse_date_range(date_range)
        except ValueError as e:
            raise ValueError(f"日期范围格式错误: {str(e)}")

        return True

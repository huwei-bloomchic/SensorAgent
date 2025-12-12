"""
漏斗分析工具
用于分析用户转化漏斗，计算各步骤转化率
"""
from typing import Optional, List, Dict, Any
from loguru import logger
from src.tools.base_tool import BaseSensorsTool


class FunnelTool(BaseSensorsTool):
    """
    漏斗分析工具

    分析用户在多个步骤之间的转化情况
    例如：注册 -> 首次登录 -> 首次购买
    """

    name = "funnel_analysis"
    description = """分析用户转化漏斗。

    用于分析用户在多个步骤之间的转化率，帮助识别流失环节。

    参数说明：
    - steps: 漏斗步骤列表，使用JSON格式的事件名称列表（必填）
      例如: ["AppLaunch", "ViewProduct", "AddToCart", "Purchase"]
    - date_range: 日期范围（必填）
      支持格式: "today", "yesterday", "last_7_days", "last_30_days", "2024-01-01,2024-01-31"
    - window: 转化窗口期（天数），默认7天（可选）
      用户需要在多少天内完成所有步骤才算转化
    - filters: 过滤条件，JSON格式（可选）
      例如: {"platform": "iOS", "country": "CN"}

    返回：
    - 各步骤的用户数
    - 各步骤转化率
    - 总体转化率

    示例查询：
    - "分析从注册到首次购买的转化漏斗"
    - "查看iOS平台上最近7天的购买漏斗"
    - "分析产品浏览到加购的转化率"
    """

    inputs = {
        "steps": {
            "type": "string",
            "description": "漏斗步骤列表（JSON格式的事件名称数组），例如: [\"Step1\", \"Step2\", \"Step3\"]"
        },
        "date_range": {
            "type": "string",
            "description": "日期范围，支持: today, yesterday, last_7_days, last_30_days, YYYY-MM-DD,YYYY-MM-DD"
        },
        "window": {
            "type": "integer",
            "description": "转化窗口期（天数），默认7天",
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
        logger.info("FunnelTool 初始化完成")

    def validate_params(self, **kwargs) -> bool:
        """验证参数"""
        # 验证必填参数
        if "steps" not in kwargs or not kwargs["steps"]:
            raise ValueError("steps 参数是必填的")
        if "date_range" not in kwargs or not kwargs["date_range"]:
            raise ValueError("date_range 参数是必填的")

        # 验证 steps 格式
        import json
        try:
            steps = json.loads(kwargs["steps"])
            if not isinstance(steps, list):
                raise ValueError("steps 必须是一个数组")
            if len(steps) < 2:
                raise ValueError("漏斗至少需要2个步骤")
        except json.JSONDecodeError:
            raise ValueError("steps 必须是有效的JSON数组格式")

        return True

    def forward(
        self,
        steps: str,
        date_range: str,
        window: Optional[int] = None,
        filters: Optional[str] = None
    ) -> str:
        """
        执行漏斗分析

        Args:
            steps: 漏斗步骤列表（JSON字符串）
            date_range: 日期范围
            window: 转化窗口期（天数）
            filters: 过滤条件（JSON字符串）

        Returns:
            漏斗分析结果
        """
        logger.info(f"执行漏斗分析: steps={steps}, date_range={date_range}")

        try:
            import json

            # 解析参数
            steps_list = json.loads(steps)
            start_date, end_date = self.parse_date_range(date_range)
            window_days = window if window is not None else 7

            # 解析过滤条件
            filters_dict = None
            if filters:
                try:
                    filters_dict = json.loads(filters)
                except json.JSONDecodeError:
                    logger.warning(f"无法解析过滤条件: {filters}")

            logger.debug(f"解析后的参数: steps={steps_list}, dates={start_date}~{end_date}, window={window_days}")

            # 将步骤名称转换为API需要的格式
            formatted_steps = [{"event_name": step} for step in steps_list]

            # 调用神策API
            result = self.client.query_funnel(
                steps=formatted_steps,
                start_date=start_date,
                end_date=end_date,
                window=window_days,
                filters=filters_dict
            )

            # 格式化结果
            return self._format_funnel_result(result, steps_list)

        except Exception as e:
            return self.handle_error(e)

    def _format_funnel_result(self, data: Dict[str, Any], steps: List[str]) -> str:
        """
        格式化漏斗分析结果

        Args:
            data: API返回的原始数据
            steps: 步骤列表

        Returns:
            格式化后的结果字符串
        """
        lines = ["=" * 60]
        lines.append("漏斗分析结果")
        lines.append("=" * 60)
        lines.append("")

        # 如果API返回了错误
        if "error" in data:
            lines.append(f"❌ 查询失败: {data['error']}")
            return "\n".join(lines)

        # 提取漏斗数据（根据实际API响应结构调整）
        # 这里使用示例数据结构，实际需要根据神策API文档调整
        if "data" in data:
            funnel_data = data["data"]

            # 显示各步骤数据
            lines.append("📊 各步骤统计:")
            lines.append("")

            if isinstance(funnel_data, list):
                total_users = None
                for i, step_data in enumerate(funnel_data):
                    step_name = steps[i] if i < len(steps) else f"步骤{i+1}"
                    user_count = step_data.get("user_count", 0)

                    if i == 0:
                        total_users = user_count
                        lines.append(f"  {i+1}. {step_name}")
                        lines.append(f"     用户数: {user_count:,}")
                        lines.append(f"     转化率: 100.00%")
                    else:
                        conversion_rate = (user_count / total_users * 100) if total_users > 0 else 0
                        prev_count = funnel_data[i-1].get("user_count", 0)
                        step_rate = (user_count / prev_count * 100) if prev_count > 0 else 0

                        lines.append(f"  {i+1}. {step_name}")
                        lines.append(f"     用户数: {user_count:,}")
                        lines.append(f"     整体转化率: {conversion_rate:.2f}%")
                        lines.append(f"     上一步转化率: {step_rate:.2f}%")

                    lines.append("")

                # 计算总体转化率
                if len(funnel_data) > 1 and total_users:
                    final_users = funnel_data[-1].get("user_count", 0)
                    overall_rate = (final_users / total_users * 100) if total_users > 0 else 0
                    lines.append("-" * 60)
                    lines.append(f"🎯 总体转化率: {overall_rate:.2f}% ({final_users:,}/{total_users:,})")

                    # 计算流失情况
                    lost_users = total_users - final_users
                    if lost_users > 0:
                        lines.append(f"⚠️  流失用户: {lost_users:,} ({(lost_users/total_users*100):.2f}%)")

        else:
            # 如果数据结构不符合预期，显示原始数据
            lines.append("原始数据:")
            lines.append(self.format_result(data))

        lines.append("")
        lines.append("=" * 60)

        return "\n".join(lines)

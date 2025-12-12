"""
SQL查询工具
用于执行神策SQL查询，支持基于事件文档的智能查询
"""
import os
from loguru import logger
from src.tools.base_tool import BaseSensorsTool


class SQLQueryTool(BaseSensorsTool):
    """
    SQL查询工具

    执行神策SQL查询，可以直接查询事件表和用户表
    支持复杂的分析场景，如多事件关联、自定义计算等
    """

    name = "sql_query"
    description = """执行神策SQL查询。

使用此工具可以：
- 执行复杂的SQL查询
- 多事件关联分析
- 自定义指标计算
- 灵活的数据筛选和聚合

参数说明：
- sql: SQL查询语句（必填）
  可以查询events表（事件表）和users表（用户表）
- limit: 返回结果数量限制（可选）
  不提供时返回所有结果

SQL查询示例（所有示例都包含必要的优化条件）：

1. 查询最近7天的应用启动次数（含爬虫过滤）：
   SELECT COUNT(*) as total_count, COUNT(DISTINCT distinct_id) as user_count
   FROM events
   WHERE event = '$AppStart'
   AND date BETWEEN '2024-12-02' AND '2024-12-09'
   AND is_spider_user = '正常用户'

2. 按日期分组查询商品点击（含爬虫过滤）：
   SELECT
     date,
     COUNT(*) as clicks,
     COUNT(DISTINCT distinct_id) as users
   FROM events
   WHERE event = 'ProductClick'
   AND date BETWEEN '2024-12-02' AND '2024-12-09'
   AND is_spider_user = '正常用户'
   GROUP BY date
   ORDER BY date

3. 查询购买转化漏斗（含爬虫过滤）：
   SELECT
     COUNT(DISTINCT CASE WHEN event = 'ProductClick' THEN distinct_id END) as click_users,
     COUNT(DISTINCT CASE WHEN event = 'AddToCartClick' THEN distinct_id END) as cart_users,
     COUNT(DISTINCT CASE WHEN event = 'PurchaseSuccess' THEN distinct_id END) as purchase_users
   FROM events
   WHERE date BETWEEN '2024-12-02' AND '2024-12-09'
   AND is_spider_user = '正常用户'
   AND event IN ('ProductClick', 'AddToCartClick', 'PurchaseSuccess')

重要提示：
- 事件名使用 event 字段，不是 event_name
- 常用事件名参考：$AppStart, ProductClick, AddToCartClick, PurchaseSuccess 等
- 事件属性通过 properties 访问，如: properties['product_spu']
- 日期字段使用 date，时间戳使用 time
- 用户ID使用 distinct_id 字段

SQL 性能优化建议（必须遵守）：
⚠️ 为避免查询超时和资源浪费，编写 SQL 时必须：
1. 【必须】添加时间范围过滤：WHERE date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
   - 不指定时间范围会导致全表扫描，查询极慢
   - 建议查询最近 7-30 天的数据
2. 【必须】指定事件名：WHERE event = '具体事件名' 或者 event in ('','')
   - 避免查询所有事件，提高查询效率
3. 【强烈建议】过滤爬虫数据：AND is_spider_user = '正常用户'
   - Web 端有大量爬虫数据，会严重影响统计准确性
   - is_spider_user 值：'正常用户' 或 '爬虫用户'
4. 使用 LIMIT 限制返回结果数量，避免返回过多数据
"""

    inputs = {
        "sql": {
            "type": "string",
            "description": "SQL查询语句"
        },
        "limit": {
            "type": "integer",
            "description": "返回结果数量限制，默认1000000000（建议保持默认值）",
            "nullable": True
        }
    }

    output_type = "string"

    def __init__(self, sensors_client):
        super().__init__(sensors_client)
        self.events_doc = self._load_events_doc()
        logger.info("SQLQueryTool 初始化完成")

    def _load_events_doc(self) -> str:
        """加载事件文档作为上下文"""
        try:
            # 获取项目根目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            events_doc_path = os.path.join(project_root, "events.md")

            if os.path.exists(events_doc_path):
                with open(events_doc_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    logger.info(f"成功加载事件文档: {len(content)} 字符")
                    return content
            else:
                logger.warning(f"事件文档不存在: {events_doc_path}")
                return ""
        except Exception as e:
            logger.error(f"加载事件文档失败: {str(e)}")
            return ""

    def get_events_context(self) -> str:
        """获取事件文档上下文，供AI参考"""
        return self.events_doc

    def validate_params(self, **kwargs) -> bool:
        """验证参数"""
        if "sql" not in kwargs or not kwargs["sql"]:
            raise ValueError("sql 参数是必填的")

        sql = kwargs["sql"].strip()
        if not sql:
            raise ValueError("SQL语句不能为空")

        sql_upper = sql.upper()

        # 基本的SQL安全检查
        dangerous_keywords = ["DROP", "DELETE", "TRUNCATE", "ALTER", "CREATE", "INSERT", "UPDATE"]
        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                raise ValueError(f"不允许执行 {keyword} 操作，仅支持 SELECT 查询")

        # 性能优化检查（警告但不阻止）
        warnings = []

        # 检查是否包含时间范围过滤
        if "DATE" not in sql_upper and "`DATE`" not in sql_upper:
            warnings.append("⚠️ 建议添加时间范围过滤 (date BETWEEN ... AND ...) 以提高查询性能")

        # 检查是否指定事件名
        if "EVENT" not in sql_upper and "`EVENT`" not in sql_upper:
            warnings.append("⚠️ 建议指定事件名 (event = '...') 以提高查询效率")

        # 检查是否过滤爬虫
        if "IS_SPIDER_USER" not in sql_upper and "`IS_SPIDER_USER`" not in sql_upper:
            warnings.append("⚠️ 建议过滤爬虫数据 (is_spider_user = '正常用户') 以确保数据准确性")

        # 如果有警告，记录到日志
        if warnings:
            logger.warning("SQL查询优化建议：")
            for warning in warnings:
                logger.warning(f"  {warning}")

        return True

    def forward(self, sql: str, limit: int = 1000000000) -> str:
        """
        执行SQL查询

        Args:
            sql: SQL查询语句
            limit: 返回结果数量限制，默认1000000000（神策API要求必填）

        Returns:
            查询结果
        """
        logger.info(f"执行SQL查询:\n{sql}")

        try:
            # 执行SQL查询（limit是必填参数）
            result = self.client.execute_sql(sql, limit=limit)

            # 格式化结果
            return self._format_sql_result(result, sql)

        except Exception as e:
            logger.error(f"SQL查询执行失败")
            logger.error(f"失败的SQL:\n{sql}")
            if limit is not None:
                logger.error(f"限制条数: {limit}")
            return self.handle_error(e)

    def _format_sql_result(self, data: dict, sql: str) -> str:
        """
        格式化SQL查询结果

        Args:
            data: API返回的原始数据
            sql: 执行的SQL语句

        Returns:
            格式化后的结果字符串（包含可读表格和结构化数据）
        """
        lines = ["=" * 60]
        lines.append("SQL查询结果")
        lines.append("=" * 60)
        lines.append("")

        # 显示执行的SQL（截断过长的SQL）
        sql_display = sql if len(sql) <= 200 else sql[:200] + "..."
        lines.append(f"执行的SQL:")
        lines.append(f"  {sql_display}")
        lines.append("")

        # 如果API返回了错误
        if "error" in data:
            lines.append(f"❌ 查询失败: {data['error']}")
            return "\n".join(lines)

        # 提取查询结果
        if "rows" in data:
            rows = data["rows"]
            columns = data.get("columns", [])

            if not rows:
                lines.append("查询结果为空")
            else:
                lines.append(f"📊 查询结果: {len(rows)} 行")
                lines.append("")

                # 如果有列名，显示列名
                if columns:
                    header = " | ".join(str(col) for col in columns)
                    lines.append(header)
                    lines.append("-" * len(header))

                # 显示数据行（限制显示前100行）
                max_display_rows = 100
                for i, row in enumerate(rows[:max_display_rows]):
                    if isinstance(row, dict):
                        row_str = " | ".join(f"{k}: {v}" for k, v in row.items())
                    elif isinstance(row, (list, tuple)):
                        row_str = " | ".join(str(v) for v in row)
                    else:
                        row_str = str(row)
                    lines.append(row_str)

                if len(rows) > max_display_rows:
                    lines.append("")
                    lines.append(f"... 还有 {len(rows) - max_display_rows} 行未显示")

        elif "data" in data:
            # 其他格式的数据
            lines.append("查询结果:")
            lines.append(self.format_result(data["data"]))
        else:
            # 未知格式
            lines.append("原始结果:")
            lines.append(self.format_result(data))

        lines.append("")
        lines.append("=" * 60)

        # 【新增】添加结构化数据供分析工具使用
        # 只有当查询成功并有rows数据时才添加
        if "rows" in data and data["rows"]:
            import json

            structured_data = {
                "columns": data.get("columns", []),
                "rows": data["rows"],
                "row_count": len(data["rows"])
            }

            # 添加元数据（如果可以推断）
            metadata = {}

            # 尝试推断日期范围（如果有date列）
            if "columns" in data and "date" in data["columns"]:
                try:
                    date_idx = data["columns"].index("date")
                    dates = [row[date_idx] for row in data["rows"] if len(row) > date_idx]
                    if dates:
                        metadata["date_range"] = [min(dates), max(dates)]
                except:
                    pass

            if metadata:
                structured_data["metadata"] = metadata

            lines.append("")
            lines.append("<structured_data>")
            lines.append(json.dumps(structured_data, ensure_ascii=False, indent=2))
            lines.append("</structured_data>")

        return "\n".join(lines)

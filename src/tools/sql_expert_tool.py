"""
SQL生成专家工具
使用LLM根据事件Schema和用户查询生成优化的Impala SQL
"""
import os
import re
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta

from smolagents import Tool
from loguru import logger


class SQLExpertTool(Tool):
    """
    SQL生成专家子代理

    使用LLM根据事件schemas和用户查询生成Impala 4.0.0.4258兼容的SQL
    """

    name = "sql_expert"

    description = """基于事件Schema和用户查询生成优化的Impala SQL查询。

使用此工具可以：
- 根据事件定义智能生成SQL
- 自动包含必需的性能优化条件
- 生成Impala 4.0.0.4258兼容语法
- 验证SQL完整性和正确性

参数说明：
- event_schemas: 事件Schema文档（来自event_schema_tool的输出）
- user_query: 用户的查询问题
- date_range: 日期范围（可选），如"last_7_days"或"2024-12-01 to 2024-12-07"

返回：
- 经过验证的SQL查询语句
- SQL元数据（使用的事件、日期范围等）

示例：
sql_expert(
    event_schemas="[从event_schema_tool获取的schemas]",
    user_query="查询最近7天每天的商品点击次数和用户数",
    date_range="last_7_days"
)

注意：
- 自动添加必需的WHERE条件（date, event, spider filter）
- 自动进行SQL语法验证
- 返回格式化的SQL及元数据
"""

    inputs = {
        "event_schemas": {
            "type": "string",
            "description": "事件Schema文档（来自event_schema_tool）"
        },
        "user_query": {
            "type": "string",
            "description": "用户的查询问题"
        },
        "date_range": {
            "type": "string",
            "description": "日期范围，如'last_7_days'或'2024-12-01 to 2024-12-07'",
            "nullable": True
        }
    }

    output_type = "string"

    def __init__(self, model):
        """
        初始化SQL专家工具

        Args:
            model: LLM模型实例
        """
        super().__init__()
        self.model = model
        self.doc_root = "docs/Bloomchic埋点"

        # 加载上下文文档
        self.context_docs = self._load_context_docs()

        logger.info("SQLExpertTool 初始化完成")

    def _load_context_docs(self) -> Dict[str, str]:
        """加载所有上下文文档"""
        docs = {}

        try:
            # 加载预置属性
            preset_path = os.path.join(self.doc_root, "预置属性.md")
            if os.path.exists(preset_path):
                with open(preset_path, 'r', encoding='utf-8') as f:
                    docs['preset_attrs'] = f.read()
                logger.info(f"已加载预置属性文档: {len(docs['preset_attrs'])} 字符")
            else:
                logger.warning(f"预置属性文档不存在: {preset_path}")
                docs['preset_attrs'] = ""

            # 加载公共属性
            common_path = os.path.join(self.doc_root, "公共属性.md")
            if os.path.exists(common_path):
                with open(common_path, 'r', encoding='utf-8') as f:
                    docs['common_attrs'] = f.read()
                logger.info(f"已加载公共属性文档: {len(docs['common_attrs'])} 字符")
            else:
                logger.warning(f"公共属性文档不存在: {common_path}")
                docs['common_attrs'] = ""

            # 加载虚拟属性
            virtual_path = os.path.join(self.doc_root, "虚拟属性.md")
            if os.path.exists(virtual_path):
                with open(virtual_path, 'r', encoding='utf-8') as f:
                    docs['virtual_attrs'] = f.read()
                logger.info(f"已加载虚拟属性文档: {len(docs['virtual_attrs'])} 字符")
            else:
                logger.warning(f"虚拟属性文档不存在: {virtual_path}")
                docs['virtual_attrs'] = ""

            # Impala语法规则
            docs['impala_rules'] = self._get_impala_rules()

        except Exception as e:
            logger.error(f"加载上下文文档失败: {e}")
            docs['preset_attrs'] = ""
            docs['common_attrs'] = ""
            docs['virtual_attrs'] = ""
            docs['impala_rules'] = ""

        return docs

    def _get_impala_rules(self) -> str:
        """获取Impala语法规则"""
        return """
Impala 4.0.0.4258 语法规则:
- 版本: 4.0.0.4258-[develop/4.0.x]-x86_64-el7 RELEASE
- 表名: events (事件数据), users (用户画像), items(商品属性, 已通过events.product_id关联)
- 事件名字段: event (不是event_name)
- 事件属性访问: '属性名'，如 'product_spu', `order`
- 用户ID: distinct_id
- 日期字段: date (格式: YYYY-MM-DD)
- 时间戳字段: time (Unix时间戳，毫秒)
- 爬虫标识: is_spider_user ('正常用户' 或 '爬虫用户')

常用聚合函数:
- COUNT(*): 计算事件总数
- COUNT(DISTINCT distinct_id): 计算独立用户数
- SUM(expression): 求和
- AVG(expression): 平均值
- MAX(expression): 最大值
- MIN(expression): 最小值

条件聚合:
- COUNT(DISTINCT CASE WHEN condition THEN distinct_id END): 条件计数用户
- SUM(CASE WHEN condition THEN 1 ELSE 0 END): 条件计数事件
"""

    def _parse_event_list(self, event_schemas: str) -> List[str]:
        """
        从event_schemas中提取事件列表

        Args:
            event_schemas: 事件Schema文档

        Returns:
            事件名称列表
        """
        logger.debug(f"[解析事件列表] 输入类型: {type(event_schemas)}")

        # 检查event_schemas是否为None或空
        if not event_schemas:
            logger.warning("[解析事件列表] event_schemas为空，无法提取事件列表")
            return []

        logger.debug(f"[解析事件列表] event_schemas长度: {len(event_schemas)}")
        logger.debug(f"[解析事件列表] event_schemas内容前1000字符:\n{event_schemas[:1000]}")

        # 尝试从<event_list>标签提取
        match = re.search(r'<event_list>\s*([^<]+)\s*</event_list>', event_schemas)
        if match:
            event_list_str = match.group(1).strip()
            events = [e.strip() for e in event_list_str.split(',') if e.strip()]
            logger.info(f"[解析事件列表] 从<event_list>标签提取到事件: {events}")
            return events
        else:
            logger.debug("[解析事件列表] 未找到<event_list>标签")

        # 备用方案：从"已选择以下事件"行提取
        match = re.search(r'已选择以下事件:\s*([^\n]+)', event_schemas)
        if match:
            event_list_str = match.group(1).strip()
            events = [e.strip() for e in event_list_str.split(',') if e.strip()]
            logger.info(f"[解析事件列表] 从文本中提取到事件: {events}")
            return events
        else:
            logger.debug("[解析事件列表] 未找到'已选择以下事件'文本")

        logger.warning("[解析事件列表] 无法从event_schemas中提取事件列表")
        return []

    def _parse_date_range(self, date_range: str) -> tuple:
        """
        解析日期范围

        Args:
            date_range: 日期范围字符串

        Returns:
            (start_date, end_date) 元组
        """
        today = datetime.now().date()

        # 检查date_range是否为None或空
        if not date_range:
            logger.warning("date_range为空，使用默认值last_7_days")
            date_range = "last_7_days"

        # 处理相对日期
        if date_range.lower() == "last_7_days":
            end_date = today
            start_date = end_date - timedelta(days=6)
        elif date_range.lower() == "last_30_days":
            end_date = today
            start_date = end_date - timedelta(days=29)
        elif date_range.lower() == "yesterday":
            start_date = end_date = today - timedelta(days=1)
        elif date_range.lower() == "today":
            start_date = end_date = today
        else:
            # 尝试解析具体日期范围 "YYYY-MM-DD to YYYY-MM-DD"
            match = re.search(r'(\d{4}-\d{2}-\d{2})\s+to\s+(\d{4}-\d{2}-\d{2})', date_range)
            if match:
                start_date = datetime.strptime(match.group(1), '%Y-%m-%d').date()
                end_date = datetime.strptime(match.group(2), '%Y-%m-%d').date()
            else:
                # 默认最近7天
                logger.warning(f"无法解析日期范围'{date_range}'，使用默认值last_7_days")
                end_date = today
                start_date = end_date - timedelta(days=6)

        return (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

    def _build_sql_generation_prompt(self, event_schemas: str, user_query: str,
                                     start_date: str, end_date: str, events: List[str]) -> str:
        """
        构建SQL生成的LLM提示词

        Args:
            event_schemas: 事件Schema文档
            user_query: 用户查询
            start_date: 开始日期
            end_date: 结束日期
            events: 事件列表

        Returns:
            LLM提示词
        """
        # 添加当前时间信息作为参考
        now = datetime.now()
        current_time_info = f"""
⏰ 当前日期: {now.strftime('%Y-%m-%d')}
⏰ 当前年份: {now.year}
⏰ 当前月份: {now.month}月
"""

        prompt = f"""你是Impala 4.0.0.4258和神策数据分析的专家SQL分析师。

{current_time_info}

任务: 根据用户问题生成SQL查询语句。

用户问题: {user_query}

日期范围: {start_date} 到 {end_date}
（注意：这个日期范围已经由系统根据当前时间计算好了，请直接使用）

⚠️ 【重要】必须使用的事件: {', '.join(events)}
注意：你只能使用上面列出的事件名称，不能使用其他事件！不能自己推测或创造事件名！

事件Schema定义:
{event_schemas}

公共属性、预置属性和虚拟属性:
{self.context_docs['common_attrs']}

{self.context_docs['preset_attrs']}

{self.context_docs['virtual_attrs']}

{self.context_docs['impala_rules']}

必须遵守的规则 (⚠️ 非常重要):
1. 【必须】包含日期范围过滤: WHERE date BETWEEN '{start_date}' AND '{end_date}'
2. 【必须】只使用提供的事件名: event = '{events[0]}' (单个事件) 或 event IN {tuple(events)} (多个事件)
   ⚠️ 绝对不能使用其他事件名！只能使用: {', '.join(events)}
3. 【强烈建议】过滤爬虫: AND is_spider_user = '正常用户' (Web端数据必须加此条件)
4. 属性字段只能使用事件的属性，公共属性和预制属性

SQL最佳实践:
- 使用 COUNT(*) 计算事件总数
- 使用 COUNT(DISTINCT distinct_id) 计算独立用户数
- select中 as的别名 如果有中文或其它关键词 需要用'`', eg: `订单数`,`order`
- 使用 GROUP BY date 进行按日统计（时间序列分析）
- 使用 CASE WHEN 进行条件聚合
- 访问事件属性使用 属性名 eg: `order`, total
- 使用 ORDER BY 对结果排序（通常按date或count排序）

输出要求:
- 只输出SQL语句，不要添加任何解释
- SQL语句要完整、可直接执行
- 确保包含上述必需的性能优化条件
- 如果用户问题涉及多个事件，考虑使用CASE WHEN或多表查询

现在请生成SQL查询:"""

        return prompt

    def _generate_sql_with_llm(self, prompt: str) -> str:
        """
        使用LLM生成SQL

        Args:
            prompt: LLM提示词

        Returns:
            生成的SQL语句
        """
        try:
            logger.info("正在调用LLM生成SQL...")

            # 调用LLM
            response = self.model([{"role": "user", "content": prompt}])

            # 检查response是否为None
            if response is None:
                raise ValueError("LLM返回None响应")

            # 提取SQL（移除可能的markdown代码块标记）
            sql = response.content.strip()

            # 移除markdown代码块标记
            sql = re.sub(r'^```sql\s*', '', sql, flags=re.MULTILINE)
            sql = re.sub(r'^```\s*', '', sql, flags=re.MULTILINE)
            sql = re.sub(r'```\s*$', '', sql, flags=re.MULTILINE)

            sql = sql.strip()

            logger.info(f"LLM生成的SQL (前200字符): {sql[:200]}...")
            return sql

        except Exception as e:
            logger.error(f"LLM生成SQL失败: {e}")
            raise ValueError(f"SQL生成失败: {str(e)}")

    def _validate_sql(self, sql: str, expected_events: List[str] = None) -> Dict[str, Any]:
        """
        验证SQL语句

        Args:
            sql: SQL语句
            expected_events: 期望使用的事件列表（用于验证）

        Returns:
            验证结果字典 {"valid": bool, "warnings": List[str], "errors": List[str]}
        """
        validation = {
            "valid": True,
            "warnings": [],
            "errors": []
        }

        sql_upper = sql.upper()

        # 检查必需条件
        if "WHERE" not in sql_upper:
            validation["errors"].append("❌ 缺少WHERE子句")
            validation["valid"] = False

        if "DATE BETWEEN" not in sql_upper and "DATE =" not in sql_upper and "`DATE`" not in sql_upper:
            validation["errors"].append("❌ 缺少日期范围过滤（WHERE date BETWEEN ... AND ...）")
            validation["valid"] = False

        if "EVENT" not in sql_upper and "`EVENT`" not in sql_upper:
            validation["errors"].append("❌ 缺少事件名筛选（WHERE event = '...' 或 event IN (...)）")
            validation["valid"] = False

        # 验证SQL中使用的事件是否与预期一致
        if expected_events:
            # 提取SQL中使用的事件名（从 event = 'XXX' 或 event IN ('XXX', 'YYY') 中提取）
            event_pattern = r"event\s*=\s*'([^']+)'|event\s+IN\s*\(([^)]+)\)"
            matches = re.finditer(event_pattern, sql, re.IGNORECASE)

            sql_events = set()
            for match in matches:
                if match.group(1):  # event = 'XXX'
                    sql_events.add(match.group(1))
                elif match.group(2):  # event IN ('XXX', 'YYY')
                    events_str = match.group(2)
                    # 提取所有引号中的事件名
                    event_names = re.findall(r"'([^']+)'", events_str)
                    sql_events.update(event_names)

            expected_events_set = set(expected_events)

            # 检查SQL中的事件是否都在预期事件列表中
            unexpected_events = sql_events - expected_events_set
            if unexpected_events:
                validation["errors"].append(
                    f"❌ SQL使用了未预期的事件: {', '.join(unexpected_events)}。"
                    f"应该只使用: {', '.join(expected_events)}"
                )
                validation["valid"] = False
                logger.error(f"SQL验证失败: 使用了错误的事件名 {unexpected_events}，期望的事件: {expected_events}")

        # 检查建议条件
        if "IS_SPIDER_USER" not in sql_upper and "`IS_SPIDER_USER`" not in sql_upper:
            validation["warnings"].append("⚠️ 建议添加爬虫过滤（is_spider_user = '正常用户'）以确保数据准确性")

        # 检查危险操作
        dangerous_keywords = ["DROP", "DELETE", "TRUNCATE", "ALTER", "INSERT", "UPDATE"]
        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                validation["errors"].append(f"❌ 不允许的操作: {keyword}")
                validation["valid"] = False

        # 检查是否是SELECT查询
        if not sql_upper.strip().startswith("SELECT"):
            validation["errors"].append("❌ SQL必须是SELECT查询")
            validation["valid"] = False

        return validation

    def _format_sql_result(self, sql: str, events: List[str], start_date: str,
                          end_date: str, validation: Dict[str, Any]) -> str:
        """
        格式化SQL生成结果

        Args:
            sql: 生成的SQL
            events: 使用的事件列表
            start_date: 开始日期
            end_date: 结束日期
            validation: 验证结果

        Returns:
            格式化的结果字符串
        """
        lines = ["=" * 60]
        lines.append("生成的 SQL 查询")
        lines.append("=" * 60)
        lines.append("")

        # SQL语句
        lines.append("SQL:")
        lines.append("-" * 60)
        lines.append(sql)
        lines.append("")

        # 元数据
        lines.append("元数据:")
        lines.append(f"  使用事件: {', '.join(events)}")
        lines.append(f"  日期范围: {start_date} 到 {end_date}")
        lines.append(f"  包含爬虫过滤: {'是' if 'is_spider_user' in sql.lower() else '否'}")
        lines.append("")

        # 验证结果
        if validation["valid"]:
            lines.append("✅ SQL验证通过")
        else:
            lines.append("❌ SQL验证失败:")
            for error in validation["errors"]:
                lines.append(f"  {error}")

        if validation["warnings"]:
            lines.append("")
            lines.append("验证警告:")
            for warning in validation["warnings"]:
                lines.append(f"  {warning}")

        lines.append("")
        lines.append("=" * 60)

        return "\n".join(lines)

    def forward(self, event_schemas: str, user_query: str, date_range: str = "last_7_days") -> str:
        """
        生成SQL查询

        Args:
            event_schemas: 事件Schema文档
            user_query: 用户查询问题
            date_range: 日期范围

        Returns:
            生成的SQL及元数据
        """
        import time
        tool_start_time = time.time()

        logger.info("=" * 60)
        logger.info("[SQLExpertTool] 开始生成SQL")
        logger.info("=" * 60)
        logger.info(f"[用户查询] {user_query}")
        logger.info(f"[日期范围] {date_range}")
        logger.info(f"[模型] {self.model.__class__.__name__}")
        logger.info("-" * 60)

        # 记录event_schemas参数
        logger.debug(f"[event_schemas类型] {type(event_schemas)}")
        if event_schemas:
            logger.debug(f"[event_schemas长度] {len(event_schemas)} 字符")
            logger.debug(f"[event_schemas前500字符]\n{event_schemas[:500]}...")
        else:
            logger.warning("[event_schemas] 参数为空或None")

        try:
            # 1. 解析事件列表
            step_start = time.time()
            logger.info("[步骤 1/5] 解析事件列表...")
            events = self._parse_event_list(event_schemas)
            step_elapsed = time.time() - step_start
            if not events:
                logger.warning(f"[步骤 1/5] ⚠ 未能从event_schemas提取事件列表 (耗时: {step_elapsed:.2f}秒)")
            else:
                logger.info(f"[步骤 1/5] ✓ 提取到 {len(events)} 个事件: {', '.join(events)} (耗时: {step_elapsed:.2f}秒)")

            # 2. 解析日期范围
            step_start = time.time()
            logger.info("[步骤 2/5] 解析日期范围...")
            start_date, end_date = self._parse_date_range(date_range)
            step_elapsed = time.time() - step_start
            logger.info(f"[步骤 2/5] ✓ 日期范围: {start_date} 到 {end_date} (耗时: {step_elapsed:.2f}秒)")

            # 3. 构建LLM提示词
            step_start = time.time()
            logger.info("[步骤 3/5] 构建LLM提示词...")
            prompt = self._build_sql_generation_prompt(
                event_schemas, user_query, start_date, end_date, events
            )
            step_elapsed = time.time() - step_start
            logger.info(f"[步骤 3/5] ✓ 提示词已构建 (长度: {len(prompt)} 字符, 耗时: {step_elapsed:.2f}秒)")

            # 4. 使用LLM生成SQL
            step_start = time.time()
            logger.info("[步骤 4/5] 调用LLM生成SQL...")
            sql = self._generate_sql_with_llm(prompt)
            step_elapsed = time.time() - step_start
            logger.info(f"[步骤 4/5] ✓ SQL已生成 (长度: {len(sql)} 字符, LLM耗时: {step_elapsed:.2f}秒)")

            # 5. 验证SQL
            step_start = time.time()
            logger.info("[步骤 5/5] 验证SQL语句...")
            validation = self._validate_sql(sql, expected_events=events)
            step_elapsed = time.time() - step_start

            if not validation["valid"]:
                logger.error(f"[步骤 5/5] ✗ SQL验证失败 (耗时: {step_elapsed:.2f}秒): {validation['errors']}")
                error_list = "\n".join(validation["errors"])
                # 直接抛出异常，中断执行流程
                raise ValueError(f"SQL生成失败（验证未通过）:\n{error_list}")

            logger.info(f"[步骤 5/5] ✓ SQL验证通过 (耗时: {step_elapsed:.2f}秒)")
            if validation["warnings"]:
                for warning in validation["warnings"]:
                    logger.warning(f"[验证警告] {warning}")

            # 6. 格式化返回结果
            result = self._format_sql_result(sql, events, start_date, end_date, validation)

            tool_elapsed = time.time() - tool_start_time
            logger.info("=" * 60)
            logger.info(f"[SQLExpertTool] SQL生成完成 (总耗时: {tool_elapsed:.2f}秒)")
            logger.info("=" * 60)
            return result

        except Exception as e:
            error_msg = f"SQL生成失败: {str(e)}"
            logger.error(error_msg, exc_info=True)
            # 直接抛出异常，中断执行流程
            raise RuntimeError(error_msg) from e

"""
自动SQL查询工具
将事件Schema检索、SQL生成和SQL执行的完整流程封装为一个工具
支持SQL语法错误自动重试
"""
import re
from typing import Optional
from smolagents import Tool
from smolagents.models import OpenAIServerModel
from loguru import logger

from config.settings import get_settings
from src.sensors.client import SensorsClient, SensorsAPIError
from src.tools.event_schema_tool import EventSchemaTool
from src.tools.sql_expert_tool import SQLExpertTool
from src.tools.sql_execution_tool import SQLExecutionTool


class AutoSQLQueryTool(Tool):
    """
    自动SQL查询工具
    
    自动完成以下流程：
    1. 调用EventSchemaTool检索事件Schema
    2. 调用SQLExpertTool生成SQL
    3. 调用SQLExecutionTool执行SQL并生成CSV
    4. 如果执行失败且是语法错误，自动重试SQL生成（最多重试2次）
    """

    name = "auto_sql_query"

    description = """自动完成SQL查询的完整流程：从用户查询需求到CSV结果文件。

此工具会自动完成以下步骤：
1. 根据查询需求检索相关事件的Schema定义
2. 基于Schema和查询需求生成优化的SQL语句
3. 执行SQL查询并将结果保存为CSV文件
4. 如果SQL执行失败且是语法错误，会自动重新生成SQL并重试（最多重试2次）

参数说明：
- user_query: 用户的查询需求描述，例如"查询最近7天每天的商品点击次数"
- date_range: 日期范围（可选），如"last_7_days"或"2024-12-01 to 2024-12-07"，默认"last_7_days"
- filename: CSV文件名（可选），不提供则自动生成
- max_retries: SQL语法错误最大重试次数（可选），默认2

返回值：
返回JSON格式字符串，包含：
- csv_path: CSV文件路径
- download_url: 文件下载URL（如果配置了base_url）
- rows: 数据行数
- columns: 列名列表
- query_info: 查询信息（日期范围、事件等）
- data_preview: 数据预览（如果有）

使用示例：
result = auto_sql_query(
    user_query="查询最近7天每天的商品点击次数和用户数",
    date_range="last_7_days",
    filename="product_clicks.csv"
)

注意：
- 工具会自动处理事件Schema检索和SQL生成
- 如果SQL执行失败，会根据错误类型决定是否重试
- 只有语法错误会触发重试，其他错误（如网络错误、权限错误）会直接抛出异常
"""

    inputs = {
        "user_query": {
            "type": "string",
            "description": "用户的查询需求描述，例如'查询最近7天每天的商品点击次数'"
        },
        "date_range": {
            "type": "string",
            "description": "日期范围，如'last_7_days'或'2024-12-01 to 2024-12-07'",
            "nullable": True
        },
        "filename": {
            "type": "string",
            "description": "CSV文件名（可选），不提供则自动生成",
            "nullable": True
        },
        "max_retries": {
            "type": "integer",
            "description": "SQL语法错误最大重试次数（可选），默认2",
            "nullable": True
        }
    }

    output_type = "string"

    def __init__(
        self,
        sensors_client: Optional[SensorsClient] = None,
        event_schema_model: Optional[OpenAIServerModel] = None,
        sql_expert_model: Optional[OpenAIServerModel] = None,
        base_url: Optional[str] = None
    ):
        """
        初始化自动SQL查询工具

        Args:
            sensors_client: 神策客户端（可选）
            event_schema_model: 事件Schema检索使用的LLM模型（可选，默认使用轻量模型）
            sql_expert_model: SQL生成使用的LLM模型（可选）
            base_url: API服务器基础URL，用于生成CSV下载链接（可选）
        """
        super().__init__()
        self.settings = get_settings()
        self.base_url = base_url

        # 初始化神策客户端
        if sensors_client is None:
            sensors_client = self._create_sensors_client()
        self.sensors_client = sensors_client

        # 初始化事件Schema检索工具（使用轻量模型）
        if event_schema_model is None:
            event_schema_model = OpenAIServerModel(
                model_id="gemini-2.5-flash-lite",
                api_key=self.settings.LITELLM_API_KEY,
                api_base=self.settings.LITELLM_BASE_URL,
            )
        self.event_schema_tool = EventSchemaTool(event_schema_model)

        # 初始化SQL生成工具
        if sql_expert_model is None:
            sql_expert_model = OpenAIServerModel(
                model_id=self.settings.LITELLM_MODEL,
                api_key=self.settings.LITELLM_API_KEY,
                api_base=self.settings.LITELLM_BASE_URL,
            )
        self.sql_expert_tool = SQLExpertTool(sql_expert_model)

        # 初始化SQL执行工具
        self.sql_execution_tool = SQLExecutionTool(
            self.sensors_client,
            base_url=self.base_url
        )

        logger.info("AutoSQLQueryTool 初始化完成")

    def _create_sensors_client(self) -> SensorsClient:
        """创建神策API客户端"""
        logger.info("创建神策API客户端...")
        return SensorsClient(
            api_url=self.settings.SENSORS_API_URL,
            project=self.settings.SENSORS_PROJECT,
            api_key=self.settings.SENSORS_API_KEY,
            timeout=self.settings.REQUEST_TIMEOUT,
            max_retries=self.settings.MAX_RETRIES
        )

    def _extract_sql_from_result(self, sql_result: str) -> str:
        """
        从SQLExpertTool的返回结果中提取SQL语句

        Args:
            sql_result: SQLExpertTool返回的格式化字符串

        Returns:
            提取的SQL语句
        """
        # SQLExpertTool返回格式：
        # ============================================================
        # 生成的 SQL 查询
        # ============================================================
        #
        # SQL:
        # ------------------------------------------------------------
        # SELECT ...
        # (空行)
        # 元数据:
        #   使用事件: ...
        #   日期范围: ...
        #   包含爬虫过滤: ...
        #
        # ✅ SQL验证通过
        #
        # ============================================================

        # 方案1: 查找"SQL:"后面的内容，停止在分隔线、空行+"元数据:"、或空行+验证信息之前
        # 匹配格式: SQL:\n---\n(内容)\n(空行或分隔线)\n元数据: 或 \n✅ 或 \n❌
        # 使用非贪婪匹配，停止在第一个匹配的边界之前
        sql_match = re.search(
            r'SQL:\s*\n-+\s*\n(.*?)(?=\n\s*\n(?:元数据|验证|✅|❌)|\n-+\s*\n|$)',
            sql_result,
            re.DOTALL
        )
        if sql_match:
            sql = sql_match.group(1).strip()
            # 移除末尾可能的分隔线
            sql = re.sub(r'\n-+\s*$', '', sql, flags=re.MULTILINE)
            # 移除末尾可能的空行和非SQL内容（双重保险）
            sql = re.sub(r'\n\s*\n(?:元数据|验证|✅|❌|使用事件|日期范围|包含爬虫).*$', '', sql, flags=re.DOTALL)
            sql = sql.strip()
            # 验证SQL不包含非SQL内容
            if sql and sql.startswith('SELECT') and not any(keyword in sql for keyword in ['元数据:', '验证', '使用事件', '日期范围', '包含爬虫', '✅', '❌']):
                logger.debug(f"从结果中提取SQL (长度: {len(sql)} 字符)")
                logger.debug(f"提取的SQL前100字符: {sql[:100]}...")
                return sql

        # 方案2: 查找SELECT开头的代码块，停止在"元数据:"或验证信息之前
        sql_match = re.search(
            r'(SELECT[\s\S]+?)(?=\n\s*\n(?:元数据|验证|✅|❌)|\n-+\s*\n|$)',
            sql_result,
            re.IGNORECASE | re.DOTALL
        )
        if sql_match:
            sql = sql_match.group(1).strip()
            # 移除末尾可能的分隔线和非SQL内容
            sql = re.sub(r'\n-+\s*$', '', sql, flags=re.MULTILINE)
            sql = re.sub(r'\n\s*\n(?:元数据|验证|✅|❌|使用事件|日期范围|包含爬虫).*$', '', sql, flags=re.DOTALL)
            sql = sql.strip()
            # 验证SQL不包含非SQL内容
            if sql and sql.startswith('SELECT') and not any(keyword in sql for keyword in ['元数据:', '验证', '使用事件', '日期范围', '包含爬虫', '✅', '❌']):
                logger.debug(f"使用备用方案提取SQL (长度: {len(sql)} 字符)")
                logger.debug(f"提取的SQL前100字符: {sql[:100]}...")
                return sql

        # 方案3: 提取第一个SELECT语句，但需要更严格的边界检测
        sql_match = re.search(
            r'(SELECT[\s\S]+?)(?=\n\s*(?:元数据|验证|✅|❌|={60})|$)',
            sql_result,
            re.IGNORECASE | re.DOTALL
        )
        if sql_match:
            sql = sql_match.group(1).strip()
            # 移除可能的markdown代码块标记
            sql = re.sub(r'^```sql\s*', '', sql, flags=re.MULTILINE)
            sql = re.sub(r'^```\s*', '', sql, flags=re.MULTILINE)
            sql = re.sub(r'```\s*$', '', sql, flags=re.MULTILINE)
            # 移除末尾可能的分隔线和非SQL内容
            sql = re.sub(r'\n-+\s*$', '', sql, flags=re.MULTILINE)
            sql = re.sub(r'\n\s*\n(?:元数据|验证|✅|❌|使用事件|日期范围|包含爬虫).*$', '', sql, flags=re.DOTALL)
            sql = sql.strip()
            # 验证SQL不包含非SQL内容
            if sql and sql.startswith('SELECT') and not any(keyword in sql for keyword in ['元数据:', '验证', '使用事件', '日期范围', '包含爬虫', '✅', '❌']):
                logger.warning(f"使用最后备用方案提取SQL (长度: {len(sql)} 字符)")
                logger.debug(f"提取的SQL前100字符: {sql[:100]}...")
                return sql

        # 如果还是找不到，返回错误
        logger.error(f"无法从SQLExpertTool结果中提取SQL")
        logger.error(f"结果内容前500字符:\n{sql_result[:500]}...")
        raise ValueError("无法从SQL生成结果中提取SQL语句")

    def _is_syntax_error(self, error: Exception) -> bool:
        """
        判断错误是否是SQL语法错误

        Args:
            error: 异常对象

        Returns:
            是否是语法错误
        """
        error_msg = str(error).lower()
        error_type = type(error).__name__

        # 检查是否是SensorsAPIError
        if isinstance(error, SensorsAPIError):
            # 检查错误消息中是否包含错误代码
            # 神策API可能返回的错误代码格式：error_code 或 code
            # 语法错误相关的错误代码可能包含：SYNTAX_ERROR, PARSE_ERROR, SQL_ERROR等
            error_code_patterns = [
                r'错误代码:\s*([A-Z_]+)',
                r'\(错误代码:\s*([A-Z_]+)\)',
                r'error_code["\']?\s*:\s*["\']?([A-Z_]+)',
                r'code["\']?\s*:\s*["\']?([A-Z_]+)',
            ]

            for pattern in error_code_patterns:
                match = re.search(pattern, str(error), re.IGNORECASE)
                if match:
                    error_code = match.group(1).upper()
                    # 判断是否是语法错误相关的错误代码
                    syntax_error_codes = [
                        'SYNTAX_ERROR',
                        'PARSE_ERROR',
                        'SQL_ERROR',
                        'SQL_SYNTAX_ERROR',
                        'SQL_PARSE_ERROR',
                        'INVALID_SQL',
                        'SQL_INVALID',
                    ]
                    if any(code in error_code for code in syntax_error_codes):
                        logger.info(f"检测到语法错误代码: {error_code}")
                        return True

        # 检查错误消息中是否包含语法错误关键词
        syntax_error_keywords = [
            'syntax error',
            '语法错误',
            'parse error',
            '解析错误',
            'invalid sql',
            'sql语法',
            'sql syntax',
            'unexpected token',
            'unexpected character',
            'missing',
            'expected',
            'near',
            'at line',
            'at position',
        ]

        for keyword in syntax_error_keywords:
            if keyword in error_msg:
                logger.info(f"检测到语法错误关键词: {keyword}")
                return True

        # 检查是否是ValueError且包含SQL相关错误
        if isinstance(error, ValueError):
            if any(keyword in error_msg for keyword in ['sql', 'syntax', 'parse', '语法']):
                logger.info("检测到ValueError中的SQL语法错误")
                return True

        logger.debug(f"错误不是语法错误: {error_type} - {error_msg[:200]}")
        return False

    def forward(
        self,
        user_query: str,
        date_range: Optional[str] = "last_7_days",
        filename: Optional[str] = None,
        max_retries: Optional[int] = 2
    ) -> str:
        """
        执行自动SQL查询流程

        Args:
            user_query: 用户的查询需求描述
            date_range: 日期范围，默认"last_7_days"
            filename: CSV文件名（可选）
            max_retries: SQL语法错误最大重试次数，默认2

        Returns:
            JSON格式字符串，包含CSV文件路径和数据摘要
        """
        import time
        tool_start_time = time.time()

        logger.info("=" * 60)
        logger.info("[AutoSQLQueryTool] 开始执行自动SQL查询")
        logger.info("=" * 60)
        logger.info(f"[用户查询] {user_query}")
        logger.info(f"[日期范围] {date_range}")
        logger.info(f"[最大重试次数] {max_retries}")
        logger.info("-" * 60)

        if max_retries is None:
            max_retries = 2

        try:
            # 步骤1: 调用EventSchemaTool获取事件Schema
            step_start = time.time()
            logger.info("[步骤 1/3] 检索事件Schema...")
            event_schemas = self.event_schema_tool.forward(query=user_query)
            step_elapsed = time.time() - step_start
            logger.info(f"[步骤 1/3] ✓ Schema检索完成 (耗时: {step_elapsed:.2f}秒)")

            # 步骤2: 调用SQLExpertTool生成SQL
            step_start = time.time()
            logger.info("[步骤 2/3] 生成SQL语句...")
            sql_result = self.sql_expert_tool.forward(
                event_schemas=event_schemas,
                user_query=user_query,
                date_range=date_range or "last_7_days"
            )
            sql = self._extract_sql_from_result(sql_result)
            step_elapsed = time.time() - step_start
            logger.info(f"[步骤 2/3] ✓ SQL生成完成 (耗时: {step_elapsed:.2f}秒)")
            logger.debug(f"[生成的SQL]\n{sql}")

            # 步骤3: 执行SQL（带重试机制）
            retry_count = 0
            last_error = None

            while retry_count <= max_retries:
                try:
                    step_start = time.time()
                    logger.info(f"[步骤 3/3] 执行SQL查询 (尝试 {retry_count + 1}/{max_retries + 1})...")
                    result = self.sql_execution_tool.forward(sql=sql, filename=filename)
                    step_elapsed = time.time() - step_start
                    logger.info(f"[步骤 3/3] ✓ SQL执行成功 (耗时: {step_elapsed:.2f}秒)")

                    tool_elapsed = time.time() - tool_start_time
                    logger.info("=" * 60)
                    logger.info(f"[AutoSQLQueryTool] 执行完成 (总耗时: {tool_elapsed:.2f}秒)")
                    logger.info("=" * 60)
                    return result

                except Exception as e:
                    last_error = e
                    error_msg = str(e)

                    # 判断是否是语法错误
                    if self._is_syntax_error(e) and retry_count < max_retries:
                        retry_count += 1
                        logger.warning(f"[步骤 3/3] ✗ SQL执行失败（语法错误），准备重试 ({retry_count}/{max_retries})")
                        logger.warning(f"[错误信息] {error_msg[:500]}")

                        # 重新生成SQL（将错误信息传递给SQLExpertTool以帮助改进）
                        step_start = time.time()
                        logger.info(f"[重试 {retry_count}] 重新生成SQL（考虑之前的错误）...")
                        
                        # 构建包含错误信息的查询
                        enhanced_query = f"{user_query}\n\n[之前的SQL执行失败，错误信息: {error_msg[:300]}]"
                        
                        sql_result = self.sql_expert_tool.forward(
                            event_schemas=event_schemas,
                            user_query=enhanced_query,
                            date_range=date_range or "last_7_days"
                        )
                        sql = self._extract_sql_from_result(sql_result)
                        step_elapsed = time.time() - step_start
                        logger.info(f"[重试 {retry_count}] ✓ 新SQL已生成 (耗时: {step_elapsed:.2f}秒)")
                        logger.debug(f"[新生成的SQL]\n{sql}")
                    else:
                        # 非语法错误或达到最大重试次数
                        if retry_count >= max_retries:
                            logger.error(f"[步骤 3/3] ✗ SQL执行失败，已达到最大重试次数 ({max_retries})")
                        else:
                            logger.error(f"[步骤 3/3] ✗ SQL执行失败（非语法错误），不重试")
                        logger.error(f"[错误信息] {error_msg}")
                        raise

            # 如果循环结束仍未成功，抛出最后的错误
            if last_error:
                raise last_error
            else:
                raise RuntimeError("SQL执行失败，未知错误")

        except Exception as e:
            error_msg = f"自动SQL查询失败: {str(e)}"
            logger.error(error_msg, exc_info=True)
            tool_elapsed = time.time() - tool_start_time
            logger.info("=" * 60)
            logger.info(f"[AutoSQLQueryTool] 执行失败 (总耗时: {tool_elapsed:.2f}秒)")
            logger.info("=" * 60)
            raise RuntimeError(error_msg) from e


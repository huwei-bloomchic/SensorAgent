"""
神策数据分析API客户端
封装神策Analytics API调用，处理认证、重试、错误处理等
"""
import time
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from loguru import logger


class SensorsAPIError(Exception):
    """神策API错误"""
    pass


class SensorsClient:
    """
    神策数据分析API客户端

    Args:
        api_url: API基础URL
        project: 项目名称
        api_key: API密钥
        timeout: 请求超时时间（秒）
        max_retries: 最大重试次数
    """

    def __init__(
        self,
        api_url: str,
        project: str,
        api_key: str,
        timeout: int = 30,
        max_retries: int = 3
    ):
        self.api_url = api_url.rstrip('/')
        self.project = project
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries

        # 创建session并配置重试策略
        self.session = self._create_session()

        logger.info(f"初始化神策客户端: {api_url}, 项目: {project}")

    def _create_session(self) -> requests.Session:
        """创建配置了重试策略的HTTP session"""
        session = requests.Session()

        # 配置重试策略
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,  # 指数退避因子
            status_forcelist=[429, 500, 502, 503, 504],  # 需要重试的HTTP状态码
            allowed_methods=["GET", "POST"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # 设置默认headers
        session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

        return session

    def _make_request(
        self,
        endpoint: str,
        method: str = "POST",
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        use_header_auth: bool = True
    ) -> Dict[str, Any]:
        """
        发送HTTP请求

        Args:
            endpoint: API端点
            method: HTTP方法
            data: 请求体数据
            params: URL查询参数
            use_header_auth: 是否使用 header 认证（默认True）

        Returns:
            API响应数据

        Raises:
            SensorsAPIError: API请求失败
        """
        url = f"{self.api_url}/{endpoint.lstrip('/')}"

        # 设置请求头
        headers = {}
        if use_header_auth:
            # 使用 header 方式认证（神策 v3 API）
            headers["sensorsdata-project"] = self.project
            headers["api-key"] = self.api_key
        else:
            # 使用 query 参数认证（旧版 API）
            if params is None:
                params = {}
            params["project"] = self.project
            params["token"] = self.api_key

        try:
            logger.debug(f"请求神策API: {method} {url}")
            logger.debug(f"Headers: {headers}")
            logger.debug(f"参数: {params}")
            logger.debug(f"数据: {data}")

            if method.upper() == "GET":
                response = self.session.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=self.timeout
                )
            else:
                response = self.session.post(
                    url,
                    params=params,
                    json=data,
                    headers=headers,
                    timeout=self.timeout
                )

            # 检查HTTP状态码
            response.raise_for_status()

            # 获取原始响应文本
            response_text = response.text
            logger.debug(f"原始响应: {response_text[:500]}...")

            # 解析响应 - 优先检测JSONL格式（神策SQL API的默认格式）
            # JSONL格式特征：包含多行JSON，每行是独立的JSON对象
            if '\n' in response_text.strip():
                # 检测到多行，直接使用JSONL解析
                logger.debug("检测到多行响应，使用JSONL格式解析...")

                lines = response_text.strip().split('\n')
                parsed_lines = []

                for i, line in enumerate(lines):
                    line = line.strip()
                    if line:
                        try:
                            line_data = json.loads(line)
                            parsed_lines.append(line_data)
                            logger.debug(f"解析第 {i+1} 行成功")
                        except json.JSONDecodeError as line_error:
                            logger.warning(f"第 {i+1} 行解析失败: {str(line_error)}")
                            continue

                if not parsed_lines:
                    # 如果JSONL解析失败，尝试标准JSON
                    logger.warning("JSONL解析失败，尝试标准JSON格式...")
                    try:
                        result = json.loads(response_text)
                    except json.JSONDecodeError as e:
                        logger.error(f"无法解析响应: {response_text[:200]}")
                        raise SensorsAPIError(f"响应解析失败: {str(e)}")
                else:
                    # 组合JSONL结果
                    # 第一行通常包含columns/types等元数据
                    # 后续行包含data数据
                    result = self._combine_jsonl_response(parsed_lines)
                    logger.info(f"成功解析JSONL格式响应，共 {len(parsed_lines)} 行")
            else:
                # 单行响应，使用标准JSON解析
                logger.debug("检测到单行响应，使用标准JSON格式解析...")
                try:
                    result = json.loads(response_text)
                except json.JSONDecodeError as e:
                    logger.error(f"JSON解析失败: {str(e)}")
                    raise SensorsAPIError(f"响应解析失败: {str(e)}")

            # 检查业务状态码
            if not self._is_success(result):
                error_msg = result.get("error", result.get("message", "未知错误"))
                error_detail = result.get("error_detail", result.get("detail", ""))
                error_code = result.get("error_code", result.get("code", ""))

                # 记录完整的错误信息
                logger.error(f"神策API错误: {error_msg}")
                if error_code:
                    logger.error(f"错误代码: {error_code}")
                if error_detail:
                    logger.error(f"错误详情: {error_detail}")
                logger.error(f"完整响应: {result}")

                # 构造详细的错误消息
                full_error_msg = f"{error_msg}"
                if error_code:
                    full_error_msg += f" (错误代码: {error_code})"
                if error_detail:
                    full_error_msg += f"\n详情: {error_detail}"

                raise SensorsAPIError(full_error_msg)

            logger.debug(f"API响应成功")
            return result

        except requests.exceptions.Timeout:
            logger.error(f"API请求超时: {url}")
            raise SensorsAPIError(f"请求超时: {url}")
        except requests.exceptions.RequestException as e:
            logger.error(f"API请求异常: {str(e)}")
            raise SensorsAPIError(f"请求失败: {str(e)}")
        except SensorsAPIError:
            # 重新抛出 SensorsAPIError，不要包装
            raise
        except Exception as e:
            logger.error(f"未预期的错误: {str(e)}", exc_info=True)
            raise SensorsAPIError(f"请求处理失败: {str(e)}")

    def _combine_jsonl_response(self, parsed_lines: List[Dict]) -> Dict[str, Any]:
        """
        组合JSONL格式的响应数据

        神策 API 在 GROUP BY 查询时，汇总行（总计行）可能比明细行少列，
        因为分组字段为 NULL 时会被省略。需要收集所有列名，并对缺少列的行进行填充。

        Args:
            parsed_lines: 解析后的JSON行列表

        Returns:
            组合后的结构化数据
        """
        if not parsed_lines:
            return {}

        # 初始化结果结构
        result = {
            "columns": [],
            "types": [],
            "rows": []
        }

        # 临时存储：每行的原始数据和对应的列名
        raw_rows = []  # [(columns, data), ...]

        # 第一遍：收集所有数据和列名
        for line in parsed_lines:
            # 检查是否有错误
            if "error" in line or "error_code" in line:
                return line

            # 检查code字段（神策v3 API）
            if "code" in line and line["code"] != "SUCCESS":
                logger.error(f"API返回错误: {line}")
                return {"error": line.get("message", "API请求失败")}

            # 神策v3 API格式: {"code": "SUCCESS", "data": {"data": [...], "columns": [...]}}
            if "data" in line and isinstance(line["data"], dict):
                data_obj = line["data"]
                line_columns = data_obj.get("columns", [])
                line_data = data_obj.get("data", [])

                # 提取types（如果有，选择最完整的）
                if "types" in data_obj:
                    if not result["types"] or len(data_obj["types"]) > len(result["types"]):
                        result["types"] = data_obj["types"]

                # 处理数据行
                if line_data and isinstance(line_data, list):
                    if line_data and isinstance(line_data[0], list):
                        # 多行数据：[[val1, val2], [val3, val4], ...]
                        for row in line_data:
                            raw_rows.append((line_columns, row))
                    else:
                        # 单行数据：[val1, val2, ...]
                        raw_rows.append((line_columns, line_data))

        if not raw_rows:
            logger.warning("没有解析到任何数据行")
            return result

        # 第二遍：确定最完整的列集合（选择列数最多的）
        all_columns_sets = [cols for cols, _ in raw_rows if cols]
        if all_columns_sets:
            # 选择列数最多的作为标准列
            result["columns"] = max(all_columns_sets, key=len)
            logger.debug(f"选择最完整的列名（{len(result['columns'])} 列）: {result['columns']}")

        # 第三遍：对齐所有行的数据到标准列
        final_columns = result["columns"]
        for row_columns, row_data in raw_rows:
            if len(row_columns) == len(final_columns):
                # 列数一致，直接使用
                result["rows"].append(row_data)
            elif len(row_columns) < len(final_columns):
                # 列数较少（如汇总行），需要根据列名映射填充 None
                aligned_row = []
                row_dict = dict(zip(row_columns, row_data))
                for col in final_columns:
                    aligned_row.append(row_dict.get(col, None))
                result["rows"].append(aligned_row)
                logger.debug(f"对齐行数据：原 {len(row_columns)} 列 -> {len(final_columns)} 列，填充 {len(final_columns) - len(row_columns)} 个 None")
            else:
                # 列数更多（理论上不应该发生），截断
                logger.warning(f"行列数({len(row_columns)})超过标准列数({len(final_columns)})，截断处理")
                result["rows"].append(row_data[:len(final_columns)])

        logger.debug(f"组合后的结果: {len(result['rows'])} 行数据, 列: {result['columns']}")
        return result

    def _is_success(self, response: Dict) -> bool:
        """检查API响应是否成功"""
        # 不同神策API版本可能有不同的成功标识
        # 这里需要根据实际API响应格式调整
        if "success" in response:
            return response["success"] is True
        if "code" in response:
            return response["code"] == 0
        # 如果没有明确的错误标识，假定成功
        if "error" not in response and "data" in response:
            return True
        # JSONL格式的SQL查询结果（包含columns或rows）也视为成功
        if "columns" in response or "rows" in response:
            return True
        return True

    def query_events(
        self,
        event_name: str,
        start_date: str,
        end_date: str,
        metrics: Optional[List[str]] = None,
        group_by: Optional[List[str]] = None,
        filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        查询事件数据

        Args:
            event_name: 事件名称
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            metrics: 指标列表，如 ['total', 'unique_users']
            group_by: 分组维度，如 ['date', 'platform']
            filters: 过滤条件

        Returns:
            事件数据
        """
        logger.info(f"查询事件: {event_name}, 日期范围: {start_date} ~ {end_date}")

        # 构建查询参数
        query = {
            "event": event_name,
            "from_date": start_date,
            "to_date": end_date
        }

        if metrics:
            query["metrics"] = metrics
        if group_by:
            query["group_by"] = group_by
        if filters:
            query["filters"] = filters

        # 调用事件分析API
        # 注意：实际端点需要根据神策API文档调整
        result = self._make_request(
            endpoint="/api/events/analyze",
            method="POST",
            data=query
        )

        return result.get("data", result)

    def query_funnel(
        self,
        steps: List[Dict[str, Any]],
        start_date: str,
        end_date: str,
        window: int = 7,
        filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        查询漏斗数据

        Args:
            steps: 漏斗步骤列表，每个步骤包含 event_name 等信息
            start_date: 开始日期
            end_date: 结束日期
            window: 转化窗口期（天）
            filters: 过滤条件

        Returns:
            漏斗数据
        """
        logger.info(f"查询漏斗: {len(steps)}个步骤, 日期范围: {start_date} ~ {end_date}")

        query = {
            "steps": steps,
            "from_date": start_date,
            "to_date": end_date,
            "window": window
        }

        if filters:
            query["filters"] = filters

        result = self._make_request(
            endpoint="/api/funnels/analyze",
            method="POST",
            data=query
        )

        return result.get("data", result)

    def query_retention(
        self,
        start_event: str,
        return_event: str,
        start_date: str,
        end_date: str,
        retention_type: str = "day",
        periods: int = 7,
        filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        查询留存数据

        Args:
            start_event: 起始事件
            return_event: 回访事件
            start_date: 开始日期
            end_date: 结束日期
            retention_type: 留存类型 (day/daily, week/weekly, month/monthly)
            periods: 留存周期数
            filters: 过滤条件

        Returns:
            留存数据
        """
        logger.info(f"查询留存: {start_event} -> {return_event}, 日期范围: {start_date} ~ {end_date}")

        # 标准化留存类型（支持 daily/day, weekly/week, monthly/month）
        retention_type_mapping = {
            "daily": "day",
            "weekly": "week",
            "monthly": "month",
            "day": "day",
            "week": "week",
            "month": "month"
        }
        normalized_type = retention_type_mapping.get(retention_type.lower(), retention_type)

        query = {
            "start_event": start_event,
            "return_event": return_event,
            "from_date": start_date,
            "to_date": end_date,
            "retention_type": normalized_type,
            "periods": periods
        }

        if filters:
            query["filters"] = filters

        result = self._make_request(
            endpoint="/api/retention/analyze",
            method="POST",
            data=query
        )

        return result.get("data", result)

    def query_user_profile(
        self,
        user_id: Optional[str] = None,
        distinct_id: Optional[str] = None,
        properties: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        查询用户画像

        Args:
            user_id: 用户ID
            distinct_id: 设备ID
            properties: 需要查询的属性列表

        Returns:
            用户画像数据
        """
        if not user_id and not distinct_id:
            raise ValueError("必须提供 user_id 或 distinct_id")

        logger.info(f"查询用户画像: user_id={user_id}, distinct_id={distinct_id}")

        query = {}
        if user_id:
            query["user_id"] = user_id
        if distinct_id:
            query["distinct_id"] = distinct_id
        if properties:
            query["properties"] = properties

        result = self._make_request(
            endpoint="/api/users/profile",
            method="POST",
            data=query
        )

        return result.get("data", result)

    def execute_sql(self, sql: str, limit: int = 1000000000) -> Dict[str, Any]:
        """
        执行SQL查询

        Args:
            sql: SQL查询语句
            limit: 返回结果限制，默认1000000000（神策API要求必须传此参数）

        Returns:
            查询结果
        """
        import time
        api_start_time = time.time()

        logger.info("=" * 60)
        logger.info("[SensorsClient] 执行SQL查询")
        logger.info("=" * 60)
        logger.info(f"[SQL]\n{sql}")
        logger.info(f"[Limit] {limit}")
        logger.info(f"[API URL] {self.api_url}")
        logger.info("-" * 60)

        # 构建请求数据（limit是必填参数）
        data = {
            "sql": sql,
            "limit": str(limit)
        }

        # 使用神策 v3 API 端点
        request_start = time.time()
        logger.info("[请求] 调用神策API: /api/v3/analytics/v1/model/sql/query")
        result = self._make_request(
            endpoint="/api/v3/analytics/v1/model/sql/query",
            method="POST",
            data=data,
            use_header_auth=True
        )
        request_elapsed = time.time() - request_start

        api_elapsed = time.time() - api_start_time
        logger.info(f"[响应] 查询成功，返回 {len(result.get('rows', []))} 行数据")
        logger.info(f"[性能] API请求耗时: {request_elapsed:.2f}秒, 总耗时: {api_elapsed:.2f}秒")
        logger.info("=" * 60)
        return result.get("data", result)

    def get_event_list(self) -> List[str]:
        """
        获取项目中所有事件列表

        Returns:
            事件名称列表
        """
        logger.info("获取事件列表")

        result = self._make_request(
            endpoint="/api/events/list",
            method="GET"
        )

        events = result.get("data", {}).get("events", [])
        return [event["name"] for event in events] if isinstance(events, list) else []

    def health_check(self) -> bool:
        """
        健康检查

        Returns:
            是否连接正常
        """
        try:
            logger.info("执行健康检查")
            # 尝试获取事件列表作为健康检查
            self.get_event_list()
            logger.info("健康检查通过")
            return True
        except Exception as e:
            logger.error(f"健康检查失败: {str(e)}")
            return False

    def close(self):
        """关闭session"""
        if self.session:
            self.session.close()
            logger.info("神策客户端session已关闭")

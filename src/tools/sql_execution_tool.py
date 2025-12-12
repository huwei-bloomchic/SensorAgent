"""
SQL执行工具
执行神策SQL查询并将结果转换为CSV文件
"""
import os
import json
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from pathlib import Path

import pandas as pd
from smolagents import Tool
from loguru import logger

from config.settings import get_settings


class SQLExecutionTool(Tool):
    """
    SQL执行和CSV转换工具

    执行神策SQL查询，将流式JSONL响应转换为CSV文件并保存到本地
    """

    name = "sql_execution"

    description = """执行神策SQL查询并将结果保存为CSV文件。

使用此工具可以：
- 执行SQL查询并获取结果
- 将结果自动转换为CSV格式
- 保存到本地文件系统
- 返回格式化的字符串结果，包含CSV文件路径、数据摘要和预览

参数说明：
- sql: SQL查询语句（必填）
- output_dir: CSV输出目录（可选，默认使用配置值）
- filename: CSV文件名（可选，不提供则自动生成）

返回值：
返回一个格式化的字符串，包含：
- CSV文件路径
- 数据行数和列信息
- 数据预览（前10行）
- <structured_data>标签内的JSON数据（包含csv_path、rows、columns等结构化信息）

使用示例：
result = sql_execution(
    sql="SELECT date, COUNT(*) as count FROM events WHERE event='ProductClick' AND date BETWEEN '2024-12-01' AND '2024-12-07' GROUP BY date",
    filename="product_clicks.csv"
)
# result 是字符串，包含所有信息
# 可以从 <structured_data> 标签中提取结构化数据

注意：
- 自动创建输出目录
- 自动清理超过24小时的旧CSV文件
- 返回的是字符串，不是元组！不要尝试解包！
- 如需提取CSV路径，请从返回字符串的 <structured_data> 部分解析JSON
"""

    inputs = {
        "sql": {
            "type": "string",
            "description": "要执行的SQL查询语句"
        },
        "output_dir": {
            "type": "string",
            "description": "CSV输出目录（可选，默认使用配置值）",
            "nullable": True
        },
        "filename": {
            "type": "string",
            "description": "CSV文件名（可选，不提供则自动生成）",
            "nullable": True
        }
    }

    output_type = "string"

    def __init__(self, sensors_client, base_url: Optional[str] = None):
        """
        初始化SQL执行工具

        Args:
            sensors_client: 神策API客户端
            base_url: API服务器的基础URL，用于生成下载链接（可选）
                     例如: "http://localhost:8000" 或 "https://api.example.com"
        """
        super().__init__()
        self.client = sensors_client
        self.settings = get_settings()
        self.base_url = base_url

        # 设置默认输出目录
        self.default_output_dir = self.settings.SQL_OUTPUT_DIR if hasattr(self.settings, 'SQL_OUTPUT_DIR') else "/tmp/sensors_data"

        # 确保输出目录存在
        self._ensure_output_dir(self.default_output_dir)

        logger.info(f"SQLExecutionTool 初始化完成，输出目录: {self.default_output_dir}")
        if self.base_url:
            logger.info(f"文件下载URL基础: {self.base_url}")

    def _ensure_output_dir(self, directory: str):
        """确保输出目录存在"""
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            logger.debug(f"输出目录已准备: {directory}")
        except Exception as e:
            logger.error(f"创建输出目录失败: {directory}, 错误: {e}")
            raise

    def _generate_filename(self, sql: str) -> str:
        """
        生成CSV文件名

        格式: query_{timestamp}_{hash}.csv

        Args:
            sql: SQL查询语句

        Returns:
            生成的文件名
        """
        # 生成时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 生成SQL的hash（取前8位）
        sql_hash = hashlib.md5(sql.encode()).hexdigest()[:8]

        filename = f"query_{timestamp}_{sql_hash}.csv"
        logger.debug(f"生成文件名: {filename}")

        return filename

    def _result_to_dataframe(self, result: Dict[str, Any]) -> pd.DataFrame:
        """
        将神策API返回的结果转换为pandas DataFrame

        Args:
            result: API返回的结果字典

        Returns:
            pandas DataFrame
        """
        # 提取列名和行数据
        # 神策API可能返回两种格式:
        # 1. {'columns': [...], 'rows': [[...], [...]]}  (标准JSONL组合格式)
        # 2. {'columns': [...], 'data': [[...], [...]]}  (v3 API格式)
        columns = result.get('columns', [])

        # 尝试从'rows'或'data'字段获取数据
        rows = result.get('rows')
        if rows is None:
            rows = result.get('data', [])

        # 如果data是单行数据（不是列表的列表），需要转换为二维数组
        if rows and isinstance(rows, list) and len(rows) > 0:
            # 检查是否是单行数据 (例如: [161611.0] 而不是 [[161611.0]])
            if not isinstance(rows[0], list):
                logger.debug(f"检测到单行数据格式，转换为二维数组: {rows}")
                rows = [rows]  # 将 [161611.0] 转换为 [[161611.0]]

        # 检测并修复列数不一致的问题
        if rows and isinstance(rows, list) and len(rows) > 0:
            # 统计每行的列数
            row_lengths = [len(row) if isinstance(row, list) else 1 for row in rows]
            max_cols = max(row_lengths)
            min_cols = min(row_lengths)

            if max_cols != min_cols:
                logger.warning(f"检测到数据行列数不一致: 最小{min_cols}列, 最大{max_cols}列")
                logger.warning(f"前5行数据: {rows[:5]}")

                # 如果columns数量与最大列数不匹配，重新推断columns
                if len(columns) != max_cols:
                    logger.warning(f"列名数量({len(columns)})与实际数据列数({max_cols})不匹配，重新推断列名")
                    # 从数据中推断实际的列数
                    columns = [f"col_{i}" for i in range(max_cols)]

                # 填充较短的行，使所有行长度一致
                normalized_rows = []
                for row in rows:
                    if isinstance(row, list):
                        if len(row) < max_cols:
                            # 用None填充缺失的列
                            normalized_row = row + [None] * (max_cols - len(row))
                            normalized_rows.append(normalized_row)
                        else:
                            normalized_rows.append(row)
                    else:
                        # 单个值，转换为列表并填充
                        normalized_rows.append([row] + [None] * (max_cols - 1))

                rows = normalized_rows
                logger.info(f"已标准化数据行，所有行现在都有{max_cols}列")

        if not columns:
            logger.warning("结果中没有列名信息")
            # 如果没有列名，尝试从第一行推断
            if rows and len(rows) > 0:
                columns = [f"col_{i}" for i in range(len(rows[0]))]
            else:
                raise ValueError("无法创建DataFrame: 缺少列信息且数据为空")

        # 创建DataFrame
        try:
            df = pd.DataFrame(rows, columns=columns)
            logger.info(f"成功创建DataFrame: {len(df)} 行 x {len(df.columns)} 列")
            return df
        except Exception as e:
            logger.error(f"创建DataFrame失败: {e}")
            logger.error(f"数据结构: columns={columns}, rows={rows[:5] if rows else []}")
            raise ValueError(f"数据格式错误，无法创建DataFrame: {str(e)}")

    def _save_csv(self, df: pd.DataFrame, output_path: str) -> str:
        """
        保存DataFrame为CSV文件

        Args:
            df: pandas DataFrame
            output_path: 输出文件路径

        Returns:
            保存的文件路径
        """
        try:
            df.to_csv(output_path, index=False, encoding='utf-8')
            file_size = os.path.getsize(output_path)
            logger.info(f"CSV文件已保存: {output_path}, 大小: {file_size} 字节")
            return output_path
        except Exception as e:
            logger.error(f"保存CSV文件失败: {output_path}, 错误: {e}")
            # 尝试备用位置
            backup_path = f"/tmp/{os.path.basename(output_path)}"
            try:
                df.to_csv(backup_path, index=False, encoding='utf-8')
                logger.warning(f"已保存到备用位置: {backup_path}")
                return backup_path
            except Exception as e2:
                logger.error(f"备用位置也保存失败: {e2}")
                raise ValueError(f"无法保存CSV文件: {str(e)}")

    def _cleanup_old_files(self, directory: str, hours: int = 24):
        """
        清理旧的CSV文件

        Args:
            directory: 要清理的目录
            hours: 文件保留时间（小时）
        """
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            removed_count = 0

            for filename in os.listdir(directory):
                if not filename.endswith('.csv'):
                    continue

                filepath = os.path.join(directory, filename)

                # 检查文件修改时间
                file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))

                if file_mtime < cutoff_time:
                    try:
                        os.remove(filepath)
                        removed_count += 1
                        logger.debug(f"已删除旧文件: {filename}")
                    except Exception as e:
                        logger.warning(f"删除文件失败: {filename}, 错误: {e}")

            if removed_count > 0:
                logger.info(f"清理完成，删除了 {removed_count} 个超过 {hours} 小时的CSV文件")
        except Exception as e:
            logger.warning(f"清理旧文件时出错: {e}")

    def _format_result(self, csv_path: str, df: pd.DataFrame, raw_result: Dict[str, Any], sql: str = "") -> str:
        """
        格式化输出结果，返回JSON格式的字符串

        Args:
            csv_path: CSV文件路径
            df: DataFrame
            raw_result: 原始API结果
            sql: 执行的SQL语句

        Returns:
            JSON格式的结果字符串
        """
        csv_filename = os.path.basename(csv_path)

        # 如果配置了base_url，生成HTTP下载链接
        if self.base_url:
            download_url = f"{self.base_url.rstrip('/')}/files/{csv_filename}"
        else:
            download_url = f"file://{csv_path}"

        # 构建结构化数据
        result_data = {
            "status": "success",
            "task_id": self._extract_task_id_from_filename(csv_filename),
            "csv_path": csv_path,
            "download_url": download_url,
            "rows": len(df),
            "columns": list(df.columns),
        }

        # 提取查询信息
        query_info = {}

        # 尝试提取日期范围
        if 'date' in df.columns and len(df) > 0:
            try:
                dates = df['date'].dropna().tolist()
                if dates:
                    min_date = min(dates)
                    max_date = max(dates)
                    query_info["date_range"] = f"{min_date} 到 {max_date}"
            except:
                pass

        # 尝试从SQL提取事件信息
        if sql:
            import re
            # 提取事件名称
            event_match = re.findall(r"event\s*(?:=|IN)\s*\(?'([^']+)'", sql, re.IGNORECASE)
            if event_match:
                query_info["events_analyzed"] = event_match

        # 统计总记录数
        if len(df) > 0:
            query_info["total_records"] = len(df)

        if query_info:
            result_data["query_info"] = query_info

        # 生成数据预览（分组展示）
        data_preview = {}
        if len(df) > 0:
            # 检查是否有事件分组
            if 'event' in df.columns or '事件名称' in df.columns:
                event_col = 'event' if 'event' in df.columns else '事件名称'

                # 按事件和平台分组
                if 'web_platform_type' in df.columns or '平台类型' in df.columns:
                    platform_col = 'web_platform_type' if 'web_platform_type' in df.columns else '平台类型'

                    for event in df[event_col].unique():
                        event_data = df[df[event_col] == event]
                        event_preview = {}

                        for platform in event_data[platform_col].unique():
                            platform_data = event_data[event_data[platform_col] == platform]

                            # 提取关键指标
                            preview_item = {}
                            if '总记录数' in platform_data.columns:
                                preview_item['total'] = int(platform_data['总记录数'].iloc[0])

                            # 提取填充率信息
                            for col in platform_data.columns:
                                if '填充率' in col:
                                    preview_item[col.replace('%', '')] = f"{platform_data[col].iloc[0]}%"

                            event_preview[str(platform)] = preview_item

                        data_preview[str(event)] = event_preview
                else:
                    # 只有事件分组，没有平台
                    for event in df[event_col].unique():
                        event_data = df[df[event_col] == event]
                        preview_item = {}

                        if '总记录数' in event_data.columns:
                            preview_item['total'] = int(event_data['总记录数'].iloc[0])

                        for col in event_data.columns:
                            if '填充率' in col:
                                preview_item[col.replace('%', '')] = f"{event_data[col].iloc[0]}%"

                        data_preview[str(event)] = preview_item

        if data_preview:
            result_data["data_preview"] = data_preview

        # 生成关键发现
        key_findings = []
        if len(df) > 0:
            # 根据数据特点自动生成关键发现
            if 'event' in df.columns or '事件名称' in df.columns:
                event_col = 'event' if 'event' in df.columns else '事件名称'
                key_findings.append(f"📊 分析了 {df[event_col].nunique()} 个事件，共 {len(df)} 条记录")

            # 检查填充率字段
            fill_rate_cols = [col for col in df.columns if '填充率' in col]
            if fill_rate_cols:
                for col in fill_rate_cols:
                    try:
                        avg_rate = df[col].mean()
                        key_findings.append(f"📈 {col}平均值: {avg_rate:.2f}%")
                    except:
                        pass

        if key_findings:
            result_data["key_findings"] = key_findings

        # 添加执行的SQL
        if sql:
            result_data["sql_executed"] = sql

        # 返回JSON字符串
        return json.dumps(result_data, ensure_ascii=False, indent=2)

    def _extract_task_id_from_filename(self, filename: str) -> str:
        """
        从文件名中提取task_id

        Args:
            filename: 文件名，例如 "task_b72c690f_cdp_tag_fill_rate.csv"

        Returns:
            task_id，如果无法提取则返回空字符串
        """
        import re
        match = re.match(r'task_([a-f0-9]+)_', filename)
        if match:
            return match.group(1)
        return ""

    def forward(self, sql: str, output_dir: Optional[str] = None, filename: Optional[str] = None) -> str:
        """
        执行SQL查询并保存为CSV

        Args:
            sql: SQL查询语句
            output_dir: 输出目录（可选）
            filename: 文件名（可选）

        Returns:
            格式化的结果字符串，包含CSV路径和数据摘要
        """
        import time
        tool_start_time = time.time()

        logger.info("=" * 60)
        logger.info("[SQLExecutionTool] 开始执行SQL查询")
        logger.info("=" * 60)
        logger.info(f"[SQL查询]\n{sql}")
        logger.info("-" * 60)

        try:
            # 1. 执行SQL查询
            step_start = time.time()
            logger.info("[步骤 1/5] 执行SQL查询...")
            result = self.client.execute_sql(sql)
            step_elapsed = time.time() - step_start
            logger.info(f"[步骤 1/5] ✓ SQL查询执行成功 (API耗时: {step_elapsed:.2f}秒)")

            # 检查是否有错误
            if "error" in result:
                error_msg = result.get("error", "未知错误")
                logger.error(f"SQL执行失败: {error_msg}")
                raise ValueError(f"SQL执行失败: {error_msg}")

            # 2. 转换为DataFrame
            step_start = time.time()
            logger.info("[步骤 2/5] 转换数据为DataFrame...")
            df = self._result_to_dataframe(result)
            step_elapsed = time.time() - step_start
            logger.info(f"[步骤 2/5] ✓ DataFrame创建成功: {len(df)} 行 x {len(df.columns)} 列 (耗时: {step_elapsed:.2f}秒)")

            # 3. 确定输出路径
            step_start = time.time()
            logger.info("[步骤 3/5] 确定输出路径...")
            output_directory = output_dir if output_dir else self.default_output_dir
            self._ensure_output_dir(output_directory)

            if not filename:
                filename = self._generate_filename(sql)

            if not filename.endswith('.csv'):
                filename += '.csv'

            csv_path = os.path.join(output_directory, filename)
            step_elapsed = time.time() - step_start
            logger.info(f"[步骤 3/5] ✓ 输出路径: {csv_path} (耗时: {step_elapsed:.2f}秒)")

            # 4. 保存CSV
            step_start = time.time()
            logger.info("[步骤 4/5] 保存CSV文件...")
            csv_path = self._save_csv(df, csv_path)
            step_elapsed = time.time() - step_start
            logger.info(f"[步骤 4/5] ✓ CSV文件已保存 (耗时: {step_elapsed:.2f}秒)")

            # 5. 清理旧文件
            step_start = time.time()
            logger.info("[步骤 5/5] 清理旧文件...")
            cleanup_hours = getattr(self.settings, 'CSV_CLEANUP_HOURS', 24)
            self._cleanup_old_files(output_directory, hours=cleanup_hours)
            step_elapsed = time.time() - step_start
            logger.info(f"[步骤 5/5] ✓ 清理完成 (耗时: {step_elapsed:.2f}秒)")

            # 6. 格式化返回结果
            output = self._format_result(csv_path, df, result, sql=sql)

            tool_elapsed = time.time() - tool_start_time
            logger.info("=" * 60)
            logger.info(f"[SQLExecutionTool] 执行完成 (总耗时: {tool_elapsed:.2f}秒)")
            logger.info("=" * 60)
            return output

        except Exception as e:
            error_msg = f"SQL执行或CSV转换失败: {str(e)}"
            logger.error(error_msg, exc_info=True)
            # 直接抛出异常，中断执行流程
            raise RuntimeError(error_msg) from e

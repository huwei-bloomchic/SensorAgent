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

    def __init__(self, sensors_client):
        """
        初始化SQL执行工具

        Args:
            sensors_client: 神策API客户端
        """
        super().__init__()
        self.client = sensors_client
        self.settings = get_settings()

        # 设置默认输出目录
        self.default_output_dir = self.settings.SQL_OUTPUT_DIR if hasattr(self.settings, 'SQL_OUTPUT_DIR') else "/tmp/sensors_data"

        # 确保输出目录存在
        self._ensure_output_dir(self.default_output_dir)

        logger.info(f"SQLExecutionTool 初始化完成，输出目录: {self.default_output_dir}")

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
            logger.error(f"数据结构: columns={columns}, rows={rows}")
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

    def _format_result(self, csv_path: str, df: pd.DataFrame, raw_result: Dict[str, Any]) -> str:
        """
        格式化输出结果

        Args:
            csv_path: CSV文件路径
            df: DataFrame
            raw_result: 原始API结果

        Returns:
            格式化的结果字符串
        """
        lines = ["=" * 60]
        lines.append("SQL 查询执行完成")
        lines.append("=" * 60)
        lines.append("")

        # CSV文件信息
        lines.append(f"✅ CSV 文件: {csv_path}")
        lines.append(f"📊 行数: {len(df)}")
        lines.append(f"📋 列: {list(df.columns)}")
        lines.append("")

        # 数据预览（前10行）
        if len(df) > 0:
            lines.append("数据预览（前10行）:")
            lines.append("-" * 60)

            # 格式化显示前10行
            preview_df = df.head(10)
            preview_str = preview_df.to_string(index=False)
            lines.append(preview_str)

            if len(df) > 10:
                lines.append("")
                lines.append(f"... 还有 {len(df) - 10} 行未显示")
        else:
            lines.append("⚠️ 查询结果为空")

        lines.append("")
        lines.append("=" * 60)

        # 添加结构化数据供后续处理
        structured_data = {
            "csv_path": csv_path,
            "rows": len(df),
            "columns": list(df.columns)
        }

        # 尝试提取日期范围
        if 'date' in df.columns and len(df) > 0:
            try:
                dates = df['date'].dropna().tolist()
                if dates:
                    structured_data["date_range"] = [min(dates), max(dates)]
            except:
                pass

        # 添加基本统计信息
        if len(df) > 0:
            summary_stats = {}
            for col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    try:
                        summary_stats[col] = {
                            "mean": float(df[col].mean()),
                            "min": float(df[col].min()),
                            "max": float(df[col].max()),
                            "sum": float(df[col].sum())
                        }
                    except:
                        pass

            if summary_stats:
                structured_data["summary_stats"] = summary_stats

        lines.append("")
        lines.append("<structured_data>")
        lines.append(json.dumps(structured_data, ensure_ascii=False, indent=2))
        lines.append("</structured_data>")

        return "\n".join(lines)

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
            output = self._format_result(csv_path, df, result)

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

"""
任务执行上下文

这是一个在任务执行过程中逐步填充的数据结构
各个Agent和工具可以直接向这个上下文中添加数据
最后用这个上下文生成完整的报告
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pathlib import Path
import json

from loguru import logger


class ExecutionStats:
    """执行统计"""
    def __init__(self):
        self.total_queries = 0
        self.successful_queries = 0
        self.failed_queries = 0
        self.cached_queries = 0
        self.total_execution_time_ms = 0.0


class TaskContext:
    """
    任务执行上下文

    这是一个可变的上下文对象，在任务执行过程中逐步填充数据
    设计原则：
    1. 在任务开始时创建
    2. 各个Agent和工具直接向其中添加数据
    3. 支持流式更新
    4. 任务结束时生成完整报告
    """

    def __init__(
        self,
        task_id: str,
        user_question: str,
        parsed_intent: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None
    ):
        """
        初始化任务上下文

        Args:
            task_id: 任务ID
            user_question: 用户问题
            parsed_intent: 解析的意图
            parameters: 参数
        """
        self.task_id = task_id
        self.user_question = user_question
        self.parsed_intent = parsed_intent
        self.parameters = parameters or {}

        # 时间记录
        self.created_at = datetime.now()
        self.completed_at: Optional[datetime] = None

        # 迭代列表
        self.iterations: List['IterationContext'] = []
        self.current_iteration: Optional['IterationContext'] = None

        # 执行统计
        self.stats = ExecutionStats()

        logger.info(f"[TaskContext] 创建任务上下文: {task_id}")

    # ========== 迭代管理 ==========

    def start_iteration(
        self,
        iteration_type: str,
        name: str,
        description: Optional[str] = None
    ) -> 'IterationContext':
        """
        开始新的迭代

        Args:
            iteration_type: 迭代类型 (initial/drilldown/refinement/comparison)
            name: 迭代名称
            description: 迭代描述

        Returns:
            IterationContext对象
        """
        iteration_id = len(self.iterations) + 1
        iteration = IterationContext(
            iteration_id=iteration_id,
            iteration_type=iteration_type,
            name=name,
            description=description
        )
        self.iterations.append(iteration)
        self.current_iteration = iteration
        logger.info(f"[TaskContext] 开始迭代: {name} (ID: {iteration_id})")
        return iteration

    def complete_iteration(self):
        """完成当前迭代"""
        if self.current_iteration:
            self.current_iteration.complete()
            logger.info(f"[TaskContext] 完成迭代: {self.current_iteration.name}")

    def create_query(
        self,
        instruction: str,
        context: Optional[Dict[str, Any]] = None,
        parameters: Optional[Dict[str, Any]] = None
    ) -> 'QueryContext':
        """
        创建新的查询

        Args:
            instruction: 指令
            context: 上下文
            parameters: 参数

        Returns:
            QueryContext对象
        """
        if not self.current_iteration:
            raise ValueError("没有活动的迭代，请先调用 start_iteration()")

        return self.current_iteration.create_query(
            instruction=instruction,
            context=context,
            parameters=parameters
        )

    # ========== 中间数据获取方法 ==========

    def get_all_queries(self) -> List['QueryContext']:
        """获取所有查询"""
        queries = []
        for iteration in self.iterations:
            queries.extend(iteration.queries)
        return queries

    def get_successful_queries(self) -> List['QueryContext']:
        """获取所有成功的查询"""
        return [q for q in self.get_all_queries() if q.status == "success"]

    def get_failed_queries(self) -> List['QueryContext']:
        """获取所有失败的查询"""
        return [q for q in self.get_all_queries() if q.status == "failed"]

    def get_current_iteration_queries(self) -> List['QueryContext']:
        """获取当前迭代的所有查询"""
        if self.current_iteration:
            return self.current_iteration.queries
        return []

    def get_all_csv_files(self) -> List[Dict[str, Any]]:
        """获取所有CSV文件信息"""
        csv_files = []
        for query in self.get_successful_queries():
            if query.csv_path:
                csv_files.append({
                    "query_id": query.query_id,
                    "csv_path": query.csv_path,
                    "download_url": query.download_url,
                    "row_count": query.data_result_row_count,
                    "column_count": query.data_result_column_count,
                    "columns": query.data_result_columns or [],
                    "instruction": query.instruction,
                    "sql": query.sql,
                    "iteration_id": self._get_query_iteration_id(query.query_id),
                    "query_sequence": query.query_sequence
                })
        return csv_files

    def get_all_sql_statements(self) -> List[Dict[str, Any]]:
        """获取所有SQL语句"""
        sql_statements = []
        for query in self.get_all_queries():
            if query.sql:
                sql_statements.append({
                    "query_id": query.query_id,
                    "sql": query.sql,
                    "execution_time_ms": query.sql_execution_time_ms,
                    "executed_at": query.sql_executed_at.isoformat() if query.sql_executed_at else None,
                    "instruction": query.instruction,
                    "status": query.status,
                    "iteration_id": self._get_query_iteration_id(query.query_id),
                    "query_sequence": query.query_sequence
                })
        return sql_statements

    def get_task_summary(self) -> Dict[str, Any]:
        """获取任务摘要"""
        all_queries = self.get_all_queries()
        successful = self.get_successful_queries()
        failed = self.get_failed_queries()

        return {
            "task_id": self.task_id,
            "user_question": self.user_question,
            "status": "completed" if self.completed_at else "running",
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_seconds": (self.completed_at - self.created_at).total_seconds() if self.completed_at else None,
            "iterations": {
                "total": len(self.iterations),
                "completed": len([it for it in self.iterations if it.completed_at]),
                "details": [
                    {
                        "iteration_id": it.iteration_id,
                        "type": it.iteration_type,
                        "name": it.name,
                        "queries_count": len(it.queries),
                        "successful_queries": sum(1 for q in it.queries if q.status == "success"),
                        "started_at": it.started_at.isoformat(),
                        "completed_at": it.completed_at.isoformat() if it.completed_at else None
                    }
                    for it in self.iterations
                ]
            },
            "queries": {
                "total": len(all_queries),
                "successful": len(successful),
                "failed": len(failed),
                "cached": sum(1 for q in all_queries if q.from_cache)
            },
            "data": {
                "total_csv_files": len(self.get_all_csv_files()),
                "total_rows": sum(q.data_result_row_count for q in successful),
                "total_sql_statements": len(self.get_all_sql_statements())
            }
        }

    def get_intermediate_results(self, format: str = "dict") -> Any:
        """
        获取中间结果

        Args:
            format: 输出格式，可选值: "dict", "json", "markdown"

        Returns:
            中间结果，格式根据format参数决定
        """
        if format == "json":
            return json.dumps(self.get_task_summary(), ensure_ascii=False, indent=2)
        elif format == "markdown":
            return self._format_intermediate_results_markdown()
        else:
            return self.get_task_summary()

    def _format_intermediate_results_markdown(self) -> str:
        """格式化中间结果为Markdown"""
        lines = []
        lines.append(f"# 任务执行中间结果")
        lines.append("")
        lines.append(f"**任务ID:** {self.task_id}")
        lines.append(f"**用户问题:** {self.user_question}")
        lines.append(f"**创建时间:** {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**状态:** {'已完成' if self.completed_at else '执行中'}")
        lines.append("")

        # 迭代摘要
        lines.append("## 迭代摘要")
        lines.append("")
        for iteration in self.iterations:
            lines.append(f"### {iteration.name} (迭代 {iteration.iteration_id})")
            lines.append("")
            lines.append(f"- **类型:** {iteration.iteration_type}")
            lines.append(f"- **查询数量:** {len(iteration.queries)}")
            lines.append(f"- **成功查询:** {sum(1 for q in iteration.queries if q.status == 'success')}")
            lines.append(f"- **开始时间:** {iteration.started_at.strftime('%Y-%m-%d %H:%M:%S')}")
            if iteration.completed_at:
                lines.append(f"- **完成时间:** {iteration.completed_at.strftime('%Y-%m-%d %H:%M:%S')}")
            lines.append("")

        # 查询详情
        lines.append("## 查询详情")
        lines.append("")
        for iteration in self.iterations:
            for query in iteration.queries:
                lines.append(f"### 查询 {query.query_sequence} (迭代 {iteration.iteration_id})")
                lines.append("")
                lines.append(f"- **查询ID:** {query.query_id}")
                lines.append(f"- **指令:** {query.instruction}")
                lines.append(f"- **状态:** {query.status}")
                if query.sql:
                    lines.append(f"- **SQL:**")
                    lines.append("```sql")
                    lines.append(query.sql)
                    lines.append("```")
                if query.csv_path:
                    lines.append(f"- **CSV文件:** {query.csv_path}")
                    lines.append(f"- **数据行数:** {query.data_result_row_count:,}")
                if query.insights:
                    lines.append(f"- **洞察数量:** {len(query.insights)}")
                lines.append("")

        return "\n".join(lines)

    def _get_query_iteration_id(self, query_id: str) -> Optional[int]:
        """获取查询所属的迭代ID"""
        for iteration in self.iterations:
            for query in iteration.queries:
                if query.query_id == query_id:
                    return iteration.iteration_id
        return None

    def get_progress_updates(self) -> List[Dict[str, Any]]:
        """
        获取进度更新列表，用于流式输出

        Returns:
            进度更新列表，每个更新包含类型、时间戳和内容
        """
        updates = []

        # 任务开始
        updates.append({
            "type": "task_started",
            "timestamp": self.created_at.isoformat(),
            "content": {
                "task_id": self.task_id,
                "user_question": self.user_question
            }
        })

        # 迭代开始和完成
        for iteration in self.iterations:
            updates.append({
                "type": "iteration_started",
                "timestamp": iteration.started_at.isoformat(),
                "content": {
                    "iteration_id": iteration.iteration_id,
                    "iteration_type": iteration.iteration_type,
                    "name": iteration.name
                }
            })

            # 查询进度
            for query in iteration.queries:
                if query.sql:
                    updates.append({
                        "type": "sql_generated",
                        "timestamp": query.sql_executed_at.isoformat() if query.sql_executed_at else None,
                        "content": {
                            "query_id": query.query_id,
                            "sql": query.sql,
                            "instruction": query.instruction
                        }
                    })

                if query.csv_path:
                    updates.append({
                        "type": "data_ready",
                        "timestamp": datetime.now().isoformat(),
                        "content": {
                            "query_id": query.query_id,
                            "csv_path": query.csv_path,
                            "row_count": query.data_result_row_count,
                            "download_url": query.download_url
                        }
                    })

                if query.status != "pending":
                    updates.append({
                        "type": "query_completed",
                        "timestamp": datetime.now().isoformat(),
                        "content": {
                            "query_id": query.query_id,
                            "status": query.status,
                            "error": query.error
                        }
                    })

            if iteration.completed_at:
                updates.append({
                    "type": "iteration_completed",
                    "timestamp": iteration.completed_at.isoformat(),
                    "content": {
                        "iteration_id": iteration.iteration_id,
                        "queries_count": len(iteration.queries),
                        "successful_count": sum(1 for q in iteration.queries if q.status == "success")
                    }
                })

        # 任务完成
        if self.completed_at:
            updates.append({
                "type": "task_completed",
                "timestamp": self.completed_at.isoformat(),
                "content": {
                    "task_id": self.task_id,
                    "duration_seconds": (self.completed_at - self.created_at).total_seconds()
                }
            })

        return updates


class IterationContext:
    """迭代上下文"""

    def __init__(
        self,
        iteration_id: int,
        iteration_type: str,
        name: str,
        description: Optional[str] = None
    ):
        self.iteration_id = iteration_id
        self.iteration_type = iteration_type
        self.name = name
        self.description = description

        self.started_at = datetime.now()
        self.completed_at: Optional[datetime] = None

        self.queries: List['QueryContext'] = []
        self.current_query: Optional['QueryContext'] = None

        logger.debug(f"[IterationContext] 创建迭代上下文: {iteration_id}")

    def create_query(
        self,
        instruction: str,
        context: Optional[Dict[str, Any]] = None,
        parameters: Optional[Dict[str, Any]] = None
    ) -> 'QueryContext':
        """创建新查询"""
        query_sequence = len(self.queries) + 1

        query_ctx = QueryContext(
            query_id=f"q{query_sequence}_iter{self.iteration_id}",
            query_sequence=query_sequence,
            instruction=instruction,
            context=context,
            parameters=parameters
        )

        self.queries.append(query_ctx)
        self.current_query = query_ctx

        logger.debug(f"[IterationContext] 创建查询: {query_ctx.query_id}")
        return query_ctx

    def complete(self):
        """完成迭代"""
        self.completed_at = datetime.now()


class QueryContext:
    """查询上下文
    
    完整记录每个查询任务的所有数据：
    - 输入：指令、参数、上下文
    - SQL：生成的SQL语句、执行时间、执行结果
    - CSV：数据文件路径、行数、列信息、数据预览
    - 分析：洞察、指标、摘要
    """

    def __init__(
        self,
        query_id: str,
        query_sequence: int,
        instruction: str,
        context: Optional[Dict[str, Any]] = None,
        parameters: Optional[Dict[str, Any]] = None
    ):
        self.query_id = query_id
        self.query_sequence = query_sequence
        self.instruction = instruction
        self.context = context or {}
        self.parameters = parameters or {}

        # 状态
        self.status = "pending"
        self.from_cache = False
        self.error: Optional[str] = None

        # SQL相关
        self.sql: Optional[str] = None
        self.sql_executed_at: Optional[datetime] = None
        self.sql_execution_time_ms: Optional[float] = None

        # CSV数据相关
        self.csv_path: Optional[str] = None
        self.download_url: Optional[str] = None
        self.data_result_row_count = 0
        self.data_result_column_count: Optional[int] = None
        self.data_result_columns: Optional[List[Dict[str, Any]]] = None
        self.data_preview: List[Dict[str, Any]] = []

        # 分析相关
        self.insights: List[Dict[str, Any]] = []
        self.metrics: List[Dict[str, Any]] = []
        self.summary: Optional[Dict[str, Any]] = None

        logger.debug(f"[QueryContext] 创建查询上下文: {query_id}")

    def set_sql(self, sql: str):
        """设置SQL语句"""
        self.sql = sql

    def mark_sql_executed(self, execution_time_ms: Optional[float] = None):
        """标记SQL已执行"""
        self.sql_executed_at = datetime.now()
        if execution_time_ms is not None:
            self.sql_execution_time_ms = execution_time_ms

    def set_data(
        self,
        csv_path: str,
        row_count: int = 0,
        column_count: Optional[int] = None,
        columns: Optional[List[Dict[str, Any]]] = None,
        data_preview: Optional[List[Dict[str, Any]]] = None,
        download_url: Optional[str] = None
    ):
        """设置CSV数据信息"""
        self.csv_path = csv_path
        self.data_result_row_count = row_count
        self.data_result_column_count = column_count
        self.data_result_columns = columns
        if data_preview is not None:
            self.data_preview = data_preview
        if download_url:
            self.download_url = download_url

    def complete(self, status: str = "success", error: Optional[str] = None):
        """完成查询"""
        self.status = status
        if error:
            self.error = error


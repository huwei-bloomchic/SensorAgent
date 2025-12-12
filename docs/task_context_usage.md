# TaskContext 使用指南

## 概述

`TaskContext` 是一个增强的数据结构，用于在整个Agent处理流程中记录和管理所有中间数据。它提供了便捷的方法来获取中间数据、输出中间结果给用户，以及生成最终报告。

## 核心功能

### 1. 完整的任务追踪

每个查询任务都完整记录了：
- **输入数据**：指令、上下文、参数
- **SQL数据**：生成的SQL、执行时间、执行结果、警告
- **CSV数据**：文件路径、行数、列信息、数据预览、下载链接
- **分析数据**：洞察、指标、摘要、分析方法

### 2. 便捷的中间数据获取

提供了多种方法来获取中间数据：

```python
# 获取所有查询
all_queries = task_context.get_all_queries()

# 获取成功的查询
successful_queries = task_context.get_successful_queries()

# 获取所有CSV文件信息
csv_files = task_context.get_all_csv_files()

# 获取所有SQL语句
sql_statements = task_context.get_all_sql_statements()

# 获取所有分析结果
analysis_results = task_context.get_all_analysis_results()

# 获取任务摘要
summary = task_context.get_task_summary()
```

### 3. 中间结果输出

支持多种格式输出中间结果：

```python
# 字典格式
intermediate_data = task_context.get_intermediate_results(format="dict")

# JSON格式
intermediate_json = task_context.get_intermediate_results(format="json")

# Markdown格式
intermediate_markdown = task_context.get_intermediate_results(format="markdown")
```

### 4. 流式输出支持

获取进度更新列表，用于流式输出：

```python
progress_updates = task_context.get_progress_updates()
# 返回包含所有进度事件的列表，包括：
# - task_started: 任务开始
# - iteration_started: 迭代开始
# - sql_generated: SQL生成
# - data_ready: 数据就绪
# - query_completed: 查询完成
# - iteration_completed: 迭代完成
# - task_completed: 任务完成
```

## 使用示例

### 基本使用

```python
from src.agents.orchestrator_v2 import create_agent_v2
from src.models.task_context import TaskContext

# 创建Agent
agent = create_agent_v2()

# 创建TaskContext
task_context = TaskContext(
    task_id="task_001",
    user_question="分析最近7天的日活数据"
)

# 执行查询（会自动记录到TaskContext）
result = agent.query(
    user_input="分析最近7天的日活数据",
    task_id="task_001",
    task_context=task_context
)

# 获取中间数据
all_queries = task_context.get_all_queries()
for query in all_queries:
    query_data = query.get_complete_query_data()
    print(f"查询ID: {query_data['query_id']}")
    print(f"指令: {query_data['input']['instruction']}")
    print(f"SQL: {query_data['sql']['sql']}")
    print(f"CSV: {query_data['csv']['csv_path']}")
    print(f"行数: {query_data['csv']['row_count']}")
```

### 获取特定查询的完整数据

```python
# 获取特定查询的完整数据
query = task_context.get_query("q1_iter1")
if query:
    complete_data = query.get_complete_query_data()
    
    # 输入数据
    input_data = complete_data['input']
    print(f"原始指令: {input_data['original_instruction']}")
    print(f"上下文: {input_data['context']}")
    print(f"参数: {input_data['parameters']}")
    
    # SQL数据
    sql_data = complete_data['sql']
    print(f"SQL语句: {sql_data['sql']}")
    print(f"执行时间: {sql_data['sql_execution_time_ms']}ms")
    print(f"警告: {sql_data['sql_warnings']}")
    
    # CSV数据
    csv_data = complete_data['csv']
    print(f"CSV路径: {csv_data['csv_path']}")
    print(f"下载链接: {csv_data['download_url']}")
    print(f"行数: {csv_data['row_count']}")
    print(f"列数: {csv_data['column_count']}")
    print(f"列信息: {csv_data['columns']}")
    print(f"数据预览: {csv_data['data_preview']}")
    
    # 分析数据
    analysis_data = complete_data['analysis']
    print(f"洞察: {analysis_data['insights']}")
    print(f"指标: {analysis_data['metrics']}")
    print(f"摘要: {analysis_data['summary']}")
```

### 流式输出中间结果

```python
# 在API服务器中使用
async def stream_query_results(user_input: str):
    task_context = TaskContext(
        task_id=generate_task_id(),
        user_question=user_input
    )
    
    # 执行查询（在后台）
    # ... 执行查询 ...
    
    # 流式输出进度更新
    progress_updates = task_context.get_progress_updates()
    for update in progress_updates:
        yield {
            "type": update["type"],
            "timestamp": update["timestamp"],
            "content": update["content"]
        }
```

### 生成最终报告

```python
# 生成完整的任务报告
report = task_context.to_report()

# 保存为JSON文件
task_context.save_json(output_dir="./reports")

# 获取报告字典
report_dict = report.to_dict()

# 获取报告JSON字符串
report_json = report.to_json()
```

## 数据结构说明

### QueryContext 完整数据结构

每个查询任务包含以下完整数据：

```python
{
    "query_id": "q1_iter1",
    "query_sequence": 1,
    "query_hash": "abc123...",
    "status": "success",
    "from_cache": False,
    
    "input": {
        "instruction": "查询最近7天的日活",
        "original_instruction": "查询最近7天的日活",
        "context": {},
        "parameters": {"time_range": "last_7_days"},
        "input_recorded_at": "2024-01-01T10:00:00"
    },
    
    "sql": {
        "sql": "SELECT date, COUNT(DISTINCT user_id) ...",
        "sql_generated_at": "2024-01-01T10:00:05",
        "sql_executed_at": "2024-01-01T10:00:06",
        "sql_execution_time_ms": 1234.5,
        "sql_warnings": [],
        "sql_error": None,
        "sql_result_raw": {...}
    },
    
    "csv": {
        "csv_path": "/path/to/file.csv",
        "download_url": "http://.../files/file.csv",
        "row_count": 1000,
        "column_count": 2,
        "columns": [
            {"name": "date", "type": "string"},
            {"name": "dau", "type": "int"}
        ],
        "data_preview": [
            {"date": "2024-01-01", "dau": 10000},
            ...
        ],
        "data_ready_at": "2024-01-01T10:00:10",
        "file_size_bytes": 50000
    },
    
    "analysis": {
        "insights": [
            {
                "type": "info",
                "title": "日活趋势",
                "description": "...",
                "severity": "info",
                "category": "trend",
                "recommendation": None,
                "created_at": "2024-01-01T10:00:15"
            }
        ],
        "metrics": [
            {
                "name": "平均日活",
                "value": 10000,
                "unit": "人",
                "trend": "up"
            }
        ],
        "summary": {
            "total_records": 1000,
            "date_range": {"start": "2024-01-01", "end": "2024-01-07"}
        },
        "analysis_performed_at": "2024-01-01T10:00:15",
        "analysis_method": "pandas"
    }
}
```

## 最佳实践

1. **在任务开始时创建TaskContext**：确保所有数据都被记录
2. **使用TaskContext获取中间数据**：不要直接访问内部数据结构
3. **定期获取进度更新**：用于向用户展示实时进度
4. **在任务完成后生成报告**：使用`to_report()`方法生成完整报告
5. **保存中间结果**：使用`save_json()`保存任务数据，便于后续分析

## 注意事项

- TaskContext是线程安全的，可以在多线程环境中使用
- 所有时间戳都使用ISO 8601格式
- CSV文件路径是绝对路径
- 数据预览默认包含前10行数据
- 查询去重会自动标记`from_cache=True`


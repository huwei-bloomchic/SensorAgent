# 数据结构重新设计说明

## 设计目标

根据主Agent的处理流程，重新设计数据结构，实现以下目标：

1. **方便中间数据获取**：提供便捷的API来获取任何阶段的中间数据
2. **数据输出**：支持输出中间结果给用户（流式输出）
3. **生成最终报告**：整合所有中间数据生成完整报告
4. **完整任务追踪**：每个查询任务包含输入、SQL、CSV、分析等完整数据

## 架构设计

### 核心数据结构

```
TaskContext (任务上下文)
├── TaskMetadata (任务元数据)
├── UserInput (用户输入)
├── Iterations[] (迭代列表)
│   ├── IterationContext (迭代上下文)
│   │   ├── Queries[] (查询列表)
│   │   │   └── QueryContext (查询上下文)
│   │   │       ├── Input (输入数据)
│   │   │       ├── SQL (SQL数据)
│   │   │       ├── CSV (CSV数据)
│   │   │       └── Analysis (分析数据)
│   │   └── IterationSummary (迭代摘要)
├── FinalAnalysis (最终分析)
└── ExecutionSummary (执行摘要)
```

### 数据流

```
用户输入
  ↓
TaskContext创建
  ↓
阶段1: 初步分析 → 记录到TaskContext
  ↓
阶段2: 执行查询 → 记录SQL、CSV到TaskContext
  ↓
阶段3: 评估下钻 → 记录决策到TaskContext
  ↓
阶段4: 下钻查询 → 记录SQL、CSV到TaskContext
  ↓
阶段5: 综合分析 → 记录分析结果到TaskContext
  ↓
生成最终报告
```

## 主要改进

### 1. TaskContext增强

#### 新增方法

- `get_all_queries()` - 获取所有查询
- `get_successful_queries()` - 获取成功的查询
- `get_failed_queries()` - 获取失败的查询
- `get_all_csv_files()` - 获取所有CSV文件信息
- `get_all_sql_statements()` - 获取所有SQL语句
- `get_all_analysis_results()` - 获取所有分析结果
- `get_task_summary()` - 获取任务摘要
- `get_intermediate_results(format)` - 获取中间结果（支持dict/json/markdown）
- `get_progress_updates()` - 获取进度更新列表（用于流式输出）

#### 使用示例

```python
# 获取所有CSV文件
csv_files = task_context.get_all_csv_files()
for csv_file in csv_files:
    print(f"查询ID: {csv_file['query_id']}")
    print(f"CSV路径: {csv_file['csv_path']}")
    print(f"行数: {csv_file['row_count']}")
    print(f"SQL: {csv_file['sql']}")

# 获取中间结果（Markdown格式）
intermediate_markdown = task_context.get_intermediate_results(format="markdown")
print(intermediate_markdown)
```

### 2. QueryContext增强

#### 完整数据记录

每个查询任务现在完整记录：

**输入数据**：
- `instruction` - 查询指令
- `original_instruction` - 原始指令
- `context` - 上下文信息
- `parameters` - 参数
- `input_recorded_at` - 记录时间

**SQL数据**：
- `sql` - SQL语句
- `sql_generated_at` - SQL生成时间
- `sql_executed_at` - SQL执行时间
- `sql_execution_time_ms` - 执行耗时
- `sql_warnings` - SQL警告
- `sql_error` - SQL错误
- `sql_result_raw` - 原始SQL执行结果

**CSV数据**：
- `csv_path` - CSV文件路径
- `download_url` - 下载链接
- `row_count` - 数据行数
- `column_count` - 列数
- `columns` - 列信息
- `data_preview` - 数据预览（前10行）
- `data_ready_at` - 数据就绪时间
- `file_size_bytes` - 文件大小

**分析数据**：
- `insights` - 洞察列表
- `metrics` - 指标列表
- `summary` - 摘要信息
- `analysis_performed_at` - 分析时间
- `analysis_method` - 分析方法

#### 新增方法

- `get_complete_query_data()` - 获取完整的查询数据
- `set_analysis()` - 设置分析结果
- `mark_sql_executed()` - 标记SQL已执行

#### 使用示例

```python
# 获取完整查询数据
query = task_context.get_query("q1_iter1")
complete_data = query.get_complete_query_data()

# 访问各部分数据
input_data = complete_data['input']
sql_data = complete_data['sql']
csv_data = complete_data['csv']
analysis_data = complete_data['analysis']
```

### 3. Orchestrator集成

#### 自动记录

`orchestrator_v2.py`现在自动将所有中间步骤记录到TaskContext：

- 阶段1：记录分析计划
- 阶段2：记录每个查询的SQL、CSV数据
- 阶段3：记录下钻决策
- 阶段4：记录下钻查询的SQL、CSV数据
- 阶段5：记录综合分析结果

#### 使用方式

```python
# 创建TaskContext
task_context = TaskContext(
    task_id="task_001",
    user_question="分析数据"
)

# 执行查询（自动记录）
result = agent.query(
    user_input="分析数据",
    task_id="task_001",
    task_context=task_context
)

# 获取中间数据
all_queries = task_context.get_all_queries()
csv_files = task_context.get_all_csv_files()
sql_statements = task_context.get_all_sql_statements()
```

## 数据输出

### 1. 中间结果输出

支持三种格式：

```python
# 字典格式
data = task_context.get_intermediate_results(format="dict")

# JSON格式
json_str = task_context.get_intermediate_results(format="json")

# Markdown格式
markdown = task_context.get_intermediate_results(format="markdown")
```

### 2. 流式输出

获取进度更新列表，用于流式输出：

```python
progress_updates = task_context.get_progress_updates()

# 更新类型包括：
# - task_started: 任务开始
# - iteration_started: 迭代开始
# - sql_generated: SQL生成
# - data_ready: 数据就绪
# - query_completed: 查询完成
# - iteration_completed: 迭代完成
# - task_completed: 任务完成
```

### 3. 最终报告

生成完整的任务报告：

```python
# 生成报告
report = task_context.to_report()

# 保存为JSON
task_context.save_json(output_dir="./reports")

# 转换为字典
report_dict = report.to_dict()

# 转换为JSON字符串
report_json = report.to_json()
```

## 使用场景

### 场景1：获取中间数据

```python
# 在查询执行过程中，随时获取中间数据
task_context = TaskContext(...)
agent.query(..., task_context=task_context)

# 获取所有CSV文件
csv_files = task_context.get_all_csv_files()
for csv_file in csv_files:
    print(f"文件: {csv_file['csv_path']}")
    print(f"查询: {csv_file['instruction']}")
    print(f"SQL: {csv_file['sql']}")
```

### 场景2：流式输出中间结果

```python
# 在API服务器中流式输出
async def stream_results(user_input: str):
    task_context = TaskContext(...)
    
    # 执行查询（后台）
    # ...
    
    # 流式输出进度
    updates = task_context.get_progress_updates()
    for update in updates:
        yield {
            "type": update["type"],
            "content": update["content"]
        }
```

### 场景3：生成完整报告

```python
# 任务完成后生成报告
task_context = TaskContext(...)
agent.query(..., task_context=task_context)

# 生成报告
report = task_context.to_report()

# 保存报告
task_context.save_json("./reports")

# 获取报告摘要
summary = task_context.get_task_summary()
```

## 数据结构对比

### 改进前

- 数据分散在各个Agent和工具中
- 难以获取中间数据
- 无法流式输出中间结果
- 查询数据不完整

### 改进后

- 所有数据集中在TaskContext中
- 提供便捷的API获取中间数据
- 支持流式输出中间结果
- 每个查询包含完整的输入、SQL、CSV、分析数据

## 总结

重新设计的数据结构实现了以下目标：

1. ✅ **方便中间数据获取**：提供了丰富的API方法
2. ✅ **数据输出**：支持多种格式输出中间结果
3. ✅ **生成最终报告**：整合所有数据生成完整报告
4. ✅ **完整任务追踪**：每个查询任务包含所有相关数据

这使得整个系统更加透明、可追踪、易于调试和分析。


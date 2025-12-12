# 报告格式化方法优化说明

## 优化目标

优化和合并 `_format_single_result_to_markdown` 和 `_format_final_output` 方法，并将它们抽取到独立的模块中，提高代码的可维护性和复用性。

## 优化内容

### 1. 创建独立的报告格式化模块

**新文件**: `src/utils/report_formatter.py`

创建了 `ReportFormatter` 类，提供统一的报告格式化功能：

- `format_single_result()` - 格式化单个查询结果
- `format_multiple_results()` - 格式化多个查询结果的综合报告
- `format_from_task_context()` - 从TaskContext生成报告

### 2. 代码优化

#### 优化前的问题

1. **代码重复**: 两个方法中有很多重复的格式化逻辑
2. **职责不清**: 格式化逻辑混在orchestrator中
3. **难以测试**: 私有方法难以单独测试
4. **难以复用**: 其他模块无法使用这些格式化功能

#### 优化后的改进

1. **统一接口**: 所有格式化功能通过 `ReportFormatter` 类提供
2. **代码复用**: 提取公共方法，减少重复代码
3. **易于测试**: 独立的工具类，便于单元测试
4. **易于扩展**: 可以轻松添加新的格式化方法

### 3. 方法合并策略

将两个方法合并为统一的格式化接口：

```python
# 单个结果格式化
ReportFormatter.format_single_result(
    user_question="...",
    result={...}
)

# 多个结果格式化
ReportFormatter.format_multiple_results(
    user_question="...",
    analysis_plan="...",
    initial_results=[...],
    drilldown_results=[...],
    synthesis_report="..."
)
```

### 4. 代码结构

```
ReportFormatter
├── format_single_result()          # 单个结果格式化
├── format_multiple_results()       # 多个结果格式化
├── format_from_task_context()      # 从TaskContext格式化
└── 私有辅助方法
    ├── _add_core_metrics()         # 添加核心指标
    ├── _add_data_preview()         # 添加数据预览
    ├── _add_key_findings()         # 添加关键发现
    ├── _add_data_files()           # 添加数据文件信息
    ├── _add_sql_section()          # 添加SQL部分
    ├── _add_query_results_section() # 添加查询结果部分
    ├── _extract_plan_summary()     # 提取计划摘要
    └── _format_error_result()      # 格式化错误结果
```

## 使用示例

### 在 orchestrator_v2.py 中使用

```python
from src.utils.report_formatter import ReportFormatter

# 单个结果
final_result = ReportFormatter.format_single_result(
    user_question=user_input,
    result=all_results[0]
)

# 多个结果
final_result = ReportFormatter.format_multiple_results(
    user_question=user_input,
    analysis_plan=analysis_plan,
    initial_results=initial_results,
    drilldown_results=drilldown_results,
    synthesis_report=synthesis_report,
    extract_plan_summary=self._extract_plan_summary
)
```

### 在 api_server.py 中使用

```python
from src.utils.report_formatter import ReportFormatter

# 异步执行
final_answer = await loop.run_in_executor(
    None,
    ReportFormatter.format_single_result,
    user_input,
    all_results[0]
)
```

### 从 TaskContext 生成报告

```python
from src.utils.report_formatter import ReportFormatter

# 从TaskContext生成报告
report = ReportFormatter.format_from_task_context(
    task_context=task_context,
    include_details=True
)
```

## 代码对比

### 优化前

```python
# orchestrator_v2.py 中有两个长方法
def _format_single_result_to_markdown(self, ...):
    # 143行代码
    ...

def _format_final_output(self, ...):
    # 78行代码
    ...
```

### 优化后

```python
# orchestrator_v2.py 中直接调用
from src.utils.report_formatter import ReportFormatter

# 使用统一的格式化接口
ReportFormatter.format_single_result(...)
ReportFormatter.format_multiple_results(...)
```

## 优势

1. **代码减少**: orchestrator_v2.py 减少了约220行代码
2. **职责分离**: 格式化逻辑独立，orchestrator专注于流程控制
3. **易于维护**: 格式化逻辑集中管理，修改更方便
4. **易于测试**: 可以单独测试格式化功能
5. **易于扩展**: 可以轻松添加新的格式化方法（如HTML、PDF等）

## 迁移说明

### 已更新的文件

1. `src/agents/orchestrator_v2.py`
   - 移除了 `_format_single_result_to_markdown()` 方法
   - 移除了 `_format_final_output()` 方法
   - 使用 `ReportFormatter` 替代

2. `api_server.py`
   - 更新了流式输出中的格式化调用
   - 使用 `ReportFormatter` 替代

### 向后兼容

- 功能完全兼容，输出格式保持一致
- 只是内部实现方式改变，不影响外部接口

## 后续优化建议

1. **支持更多格式**: 可以扩展支持HTML、PDF等格式
2. **模板系统**: 可以使用模板引擎（如Jinja2）来管理报告模板
3. **配置化**: 可以将格式化选项配置化，支持自定义样式
4. **国际化**: 支持多语言报告生成


# QueryContext 定义和创建流程

## QueryContext 定义位置

`QueryContext` 定义在：
- **文件**: `src/models/task_context.py`
- **行号**: 第823行
- **类名**: `QueryContext`

```python
class QueryContext:
    """查询上下文
    
    完整记录每个查询任务的所有数据：
    - 输入：指令、参数、上下文
    - SQL：生成的SQL语句、执行时间、执行结果
    - CSV：数据文件路径、行数、列信息、数据预览
    - 分析：洞察、指标、摘要
    """
```

## 创建流程

### 调用链

```
orchestrator_v2._execute_instructions()
  ↓
TaskContext.create_query()
  ↓
IterationContext.create_query()
  ↓
QueryContext.__init__()  ← 实际创建对象
```

### 详细说明

#### 1. 触发点：orchestrator_v2.py

在 `orchestrator_v2.py` 的 `_execute_instructions()` 方法中（第438行），当需要执行指令时：

```python
def _execute_instructions(
    self,
    instructions: list,
    task_id: Optional[str] = None,
    task_context: Optional[TaskContext] = None
) -> list:
    # ...
    for i, instruction in enumerate(instructions, 1):
        # ...
        
        # 在TaskContext中创建查询记录
        query_ctx = None
        if task_context and task_context.current_iteration:
            query_ctx = task_context.create_query(  # ← 调用TaskContext.create_query()
                instruction=instruction_str,
                context=None,
                parameters=instruction_params
            )
```

#### 2. TaskContext.create_query()

在 `task_context.py` 第140行，`TaskContext.create_query()` 方法：

```python
def create_query(
    self,
    instruction: str,
    context: Optional[Dict[str, Any]] = None,
    parameters: Optional[Dict[str, Any]] = None
) -> 'QueryContext':
    """
    创建新的查询
    
    Args:
        instruction: 查询指令
        context: 上下文信息
        parameters: 参数
    
    Returns:
        QueryContext对象
    """
    if not self.current_iteration:
        raise RuntimeError("必须先调用 start_iteration()")
    
    return self.current_iteration.create_query(instruction, context, parameters)  # ← 调用IterationContext.create_query()
```

#### 3. IterationContext.create_query()

在 `task_context.py` 第742行，`IterationContext.create_query()` 方法：

```python
def create_query(
    self,
    instruction: str,
    context: Optional[Dict[str, Any]] = None,
    parameters: Optional[Dict[str, Any]] = None
) -> 'QueryContext':
    """创建新查询"""
    query_sequence = len(self.queries) + 1
    
    # ← 这里实际创建QueryContext对象
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
```

#### 4. QueryContext.__init__()

在 `task_context.py` 第833行，`QueryContext` 的构造函数：

```python
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
    
    # 初始化所有字段...
```

## 完整执行流程示例

```python
# 1. 创建TaskContext
task_context = TaskContext(
    task_id="task_001",
    user_question="分析数据"
)

# 2. 开始迭代
task_context.start_iteration(
    iteration_type="initial",
    name="初步查询"
)

# 3. 执行指令（在orchestrator_v2中）
agent.query(
    user_input="分析数据",
    task_context=task_context
)

# 内部流程：
# 3.1 orchestrator_v2._execute_instructions() 被调用
# 3.2 对于每个指令，调用 task_context.create_query()
# 3.3 TaskContext.create_query() 调用 current_iteration.create_query()
# 3.4 IterationContext.create_query() 创建 QueryContext 对象
# 3.5 QueryContext 被添加到 IterationContext.queries 列表中
# 3.6 返回 QueryContext 对象，用于后续记录SQL、CSV、分析数据
```

## 关键点

1. **QueryContext 不是直接创建的**：必须通过 `TaskContext.create_query()` → `IterationContext.create_query()` 的调用链创建

2. **必须先有迭代**：在创建查询之前，必须先调用 `TaskContext.start_iteration()` 来创建 `IterationContext`

3. **自动管理**：QueryContext 创建后会自动：
   - 添加到 `IterationContext.queries` 列表
   - 设置为 `IterationContext.current_query`
   - 生成唯一的 `query_id`（格式：`q{sequence}_iter{iteration_id}`）

4. **生命周期**：QueryContext 的生命周期与迭代绑定，当迭代完成时，所有查询都会被包含在迭代中

## 使用建议

**正确的方式**：
```python
# ✅ 通过TaskContext创建
task_context.start_iteration(...)
query = task_context.create_query(instruction="...")
```

**错误的方式**：
```python
# ❌ 不要直接创建
query = QueryContext(...)  # 这样创建的对象不会被添加到TaskContext中
```

## 总结

- **定义位置**: `src/models/task_context.py` 第823行
- **创建者**: `IterationContext.create_query()` 方法
- **触发点**: `orchestrator_v2._execute_instructions()` 方法
- **调用链**: orchestrator → TaskContext → IterationContext → QueryContext


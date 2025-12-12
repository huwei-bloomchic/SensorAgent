"""
下层SQL执行Agent (The Engineer / Executor)

职责:
- 懂SQL和表结构，不懂复杂的业务归因
- 接收上层Agent的自然语言指令
- 持有字段白名单和SQL语法规则
- 强制风控: 自动注入LIMIT, 检查WHERE
- 生成并执行SQL
- 返回结构化数据
"""
from typing import List, Dict, Any, Optional
from smolagents import CodeAgent, Tool
from smolagents.models import OpenAIServerModel
from loguru import logger
from datetime import datetime

from config.settings import get_settings
from src.sensors.client import SensorsClient
from src.tools.event_schema_tool import EventSchemaTool
from src.tools.sql_expert_tool import SQLExpertTool
from src.tools.sql_execution_tool import SQLExecutionTool


class EngineerAgent:
    """
    SQL执行Agent

    特点:
    - 专注于SQL生成和执行
    - 持有字段白名单，确保安全
    - 强制风控机制
    - 不负责复杂的业务分析
    - 只返回数据，不做业务解读
    """

    def __init__(
        self,
        sensors_client: Optional[SensorsClient] = None,
        model: Optional[OpenAIServerModel] = None,
        model_name: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        """
        初始化SQL执行Agent

        Args:
            sensors_client: 神策客户端(可选)
            model: LLM模型实例(可选)
            model_name: 模型名称(可选)
            api_key: API密钥(可选)
            base_url: API服务器基础URL，用于生成CSV下载链接(可选)
        """
        self.settings = get_settings()
        self.base_url = base_url

        # 初始化神策客户端
        if sensors_client is None:
            sensors_client = self._create_sensors_client()
        self.sensors_client = sensors_client

        # 初始化模型
        if model is None:
            self.model = self._create_llm_model(model_name, api_key)
        else:
            self.model = model

        # 初始化工具
        self.tools = self._initialize_tools()

        # 初始化Agent
        self.agent = self._create_agent()

        logger.info("EngineerAgent 初始化完成")

    def _create_sensors_client(self) -> SensorsClient:
        """创建神策API客户端"""
        logger.info("创建神策API客户端...")

        client = SensorsClient(
            api_url=self.settings.SENSORS_API_URL,
            project=self.settings.SENSORS_PROJECT,
            api_key=self.settings.SENSORS_API_KEY,
            timeout=self.settings.REQUEST_TIMEOUT,
            max_retries=self.settings.MAX_RETRIES
        )

        return client

    def _create_llm_model(
        self,
        model_name: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> OpenAIServerModel:
        """创建LLM模型"""
        if model_name is None:
            # EngineerAgent可以使用更轻量的模型
            model_name = self.settings.LITELLM_MODEL
        if api_key is None:
            api_key = self.settings.LITELLM_API_KEY

        logger.info(f"创建EngineerAgent LLM模型: {model_name}")

        model = OpenAIServerModel(
            model_id=model_name,
            api_key=api_key,
            api_base=self.settings.LITELLM_BASE_URL,
        )

        return model

    def _initialize_tools(self) -> List[Tool]:
        """初始化工具"""
        logger.info("初始化EngineerAgent工具...")

        # 为EventSchemaTool创建单独的轻量模型
        event_schema_model = OpenAIServerModel(
            model_id="gemini-2.5-flash-lite",  # 使用轻量模型
            api_key=self.settings.LITELLM_API_KEY,
            api_base=self.settings.LITELLM_BASE_URL,
        )

        tools = [
            # 事件Schema检索工具
            EventSchemaTool(event_schema_model),

            # SQL生成专家工具
            SQLExpertTool(self.model),

            # SQL执行工具，传入base_url用于生成下载链接
            SQLExecutionTool(self.sensors_client, base_url=self.base_url),
        ]

        logger.info(f"已加载 {len(tools)} 个工具")
        for tool in tools:
            logger.debug(f"  - {tool.name}")

        return tools

    def _create_agent(self) -> CodeAgent:
        """创建CodeAgent"""
        logger.info("创建EngineerAgent...")

        agent = CodeAgent(
            tools=self.tools,
            model=self.model,
            max_steps=15,  # 增加到15步，给Agent更多时间完成任务
            verbosity_level=2,
            additional_authorized_imports=[
                "json", "datetime", "time",
                "pandas", "numpy", "csv"
            ],
        )

        return agent

    def _get_system_prompt(self) -> str:
        """获取系统提示词"""
        now = datetime.now()
        current_time_info = f"""
⏰ 当前日期: {now.strftime('%Y-%m-%d')}
⏰ 当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}
"""

        return f"""{current_time_info}

你是神策数据的**SQL执行工程师**，专注于生成和执行安全、高效的SQL查询。

【你的身份定位】
- ✅ 你懂SQL、Impala语法、表结构
- ✅ 你持有字段白名单，确保查询安全
- ✅ 你负责SQL生成、验证、执行
- ❌ 你不负责复杂的业务分析和归因
- ❌ 你只返回数据，不做业务解读

【你的核心能力】
1. **指令解析**: 理解上层Agent发来的自然语言指令
2. **Schema查询**: 使用event_schema_tool获取事件定义
3. **SQL生成**: 使用sql_expert工具生成SQL
4. **SQL执行**: 使用sql_execution工具执行查询
5. **数据返回**: 返回结构化的CSV数据

【强制安全规则】
1. ⚠️ 所有SQL必须包含日期范围(WHERE date BETWEEN ...)
2. ⚠️ 所有SQL必须包含事件筛选(WHERE event = ...)
3. ⚠️ Web端数据必须过滤爬虫(WHERE is_spider_user = '正常用户')
4. ⚠️ 禁止DROP、DELETE、UPDATE等写操作
5. ⚠️ 只能查询白名单中的字段

【工作流程】
你的工作分为四个步骤:

**步骤1: 解析指令**
- 从自然语言指令中提取: 事件、时间范围、维度、指标
- 示例指令: "查询最近7天每天的商品点击次数"
  * 事件: ProductClick
  * 时间范围: last_7_days
  * 维度: date
  * 指标: 点击次数(COUNT(*))

**步骤2: 获取Schema**
使用event_schema_tool获取事件定义:
```python
schemas = event_schema_tool(query="商品点击事件")
```

**步骤3: 生成SQL**
使用sql_expert工具生成SQL:
```python
sql_result = sql_expert(
    event_schemas=schemas,
    user_query="查询最近7天每天的商品点击次数",
    date_range="last_7_days"
)
```

**步骤4: 执行SQL**
使用sql_execution工具执行查询:
```python
result = sql_execution(sql=生成的SQL, filename="product_clicks.csv")
```

【返回格式】
你必须返回结构化的数据信息:
```json
{{
    "status": "success",
    "csv_path": "/path/to/file.csv",
    "rows": 100,
    "columns": ["date", "event_count"],
    "preview": "前10行数据预览",
    "summary": {{
        "date_range": ["2024-12-01", "2024-12-07"],
        "total_events": 50000
    }}
}}
```

【重要提示】
1. 你只负责"做"(执行SQL)，不负责"想"(业务分析)
2. 专注于技术实现，确保SQL的正确性和安全性
3. 如果指令不明确，要求上层Agent提供更多信息
4. 所有SQL必须经过验证，不符合安全规则的SQL不能执行

【错误处理】
- 如果SQL生成失败，返回错误信息(不要编造数据)
- 如果SQL执行失败，返回错误详情(不要隐藏错误)
- 如果字段不在白名单中，明确拒绝并说明原因

⚠️ 【重要：步数限制处理】
- 你有最多15步来完成任务
- 如果第12步还没完成，必须在第13-14步总结已完成的工作并返回部分结果
- **绝对不能**在第15步时没有返回任何结果
- 即使任务未完成，也要用final_answer()返回当前进度和已获得的信息
- 如果任务简单，可以在更少的步骤内完成

现在，请根据指令生成并执行SQL查询。
"""

    def execute_instruction(
        self,
        instruction: str,
        context: Optional[Dict[str, Any]] = None,
        task_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        执行来自上层Agent的指令 (非流式版本，用于向后兼容)

        Args:
            instruction: 自然语言指令
            context: 上下文信息(可选)
            task_id: 任务ID，用于CSV文件命名(可选)

        Returns:
            查询结果
        """
        # 使用流式版本，但收集所有结果后返回
        final_result = None
        for event in self.execute_instruction_streaming(instruction, context, task_id):
            if event["type"] == "result":
                final_result = event["data"]

        return final_result if final_result else {
            "status": "error",
            "instruction": instruction,
            "error": "No result returned from streaming execution",
            "timestamp": datetime.now().isoformat()
        }

    def execute_instruction_streaming(
        self,
        instruction: str,
        context: Optional[Dict[str, Any]] = None,
        task_id: Optional[str] = None
    ):
        """
        执行来自上层Agent的指令 (流式版本)

        Args:
            instruction: 自然语言指令
            context: 上下文信息(可选)
            task_id: 任务ID，用于CSV文件命名(可选)

        Yields:
            Dict[str, Any]: 执行过程中的事件
                - {"type": "thinking", "content": str} - 思考过程
                - {"type": "result", "data": Dict} - 最终结果
        """
        logger.info("=" * 80)
        logger.info(f"[EngineerAgent] 收到指令: {instruction}")
        logger.info("=" * 80)

        try:
            # 构建完整的prompt
            system_prompt = self._get_system_prompt()

            # 添加task_id信息
            task_id_info = ""
            if task_id:
                task_id_info = f"\n\n【任务ID】\n{task_id}\n⚠️ 重要: 执行SQL时，请在filename参数中包含此任务ID，格式: task_{task_id}_文件名.csv\n"

            # 添加上下文信息
            context_info = ""
            if context:
                context_info = f"\n\n【上下文信息】\n{context}\n"

            full_prompt = f"{system_prompt}{task_id_info}\n\n【指令】\n{instruction}{context_info}"

            # 调用Agent执行 (流式模式)
            logger.info("[EngineerAgent] 开始执行指令 (流式模式)...")

            yield {
                "type": "thinking",
                "content": f"🔧 EngineerAgent 开始执行: {instruction[:100]}...\n"
            }

            final_result = None
            step_count = 0

            # 使用 stream=True 来获取执行过程
            for step in self.agent.run(full_prompt, stream=True):
                step_count += 1

                # 提取 thinking 信息
                thinking_content = self._extract_thinking_from_step(step, step_count)
                if thinking_content:
                    yield {
                        "type": "thinking",
                        "content": thinking_content
                    }

                # 检查是否是最终结果
                if hasattr(step, 'is_final_answer') and step.is_final_answer:
                    if hasattr(step, 'action_output'):
                        final_result = step.action_output
                    elif hasattr(step, 'output'):
                        final_result = step.output

            logger.info("[EngineerAgent] 指令执行完成")
            logger.debug(f"[执行结果]\n{final_result}")

            # 检查结果是否有效
            if final_result is None or final_result == "":
                logger.warning("[EngineerAgent] Agent返回了空结果，可能达到了最大步数限制")
                yield {
                    "type": "result",
                    "data": {
                        "status": "partial",
                        "instruction": instruction,
                        "result": "任务未完成：达到最大推理步数限制(max_steps=15)。可能原因：任务过于复杂或需要更多步骤。建议简化查询。",
                        "error": "Reached max steps without final answer",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            else:
                # 返回结构化结果
                yield {
                    "type": "result",
                    "data": {
                        "status": "success",
                        "instruction": instruction,
                        "result": final_result,
                        "timestamp": datetime.now().isoformat()
                    }
                }

        except Exception as e:
            error_msg = str(e)
            logger.error(f"[EngineerAgent] 执行失败: {error_msg}", exc_info=True)

            # 检查是否是max_steps错误
            if "max" in error_msg.lower() and "step" in error_msg.lower():
                logger.warning("[EngineerAgent] 达到最大步数限制")
                yield {
                    "type": "result",
                    "data": {
                        "status": "partial",
                        "instruction": instruction,
                        "result": "任务未完成：达到最大推理步数限制(max_steps=15)。可能原因：任务过于复杂或需要更多步骤。建议简化查询。",
                        "error": error_msg,
                        "timestamp": datetime.now().isoformat()
                    }
                }
            else:
                yield {
                    "type": "result",
                    "data": {
                        "status": "error",
                        "instruction": instruction,
                        "error": error_msg,
                        "timestamp": datetime.now().isoformat()
                    }
                }

    def _extract_thinking_from_step(self, step, step_number: int) -> Optional[str]:
        """
        从 Agent 的执行步骤中提取 thinking 内容

        Args:
            step: smolagents 的 step 对象
            step_number: 步骤编号

        Returns:
            thinking 内容字符串，如果没有则返回 None
        """
        from smolagents.agents import ActionStep, PlanningStep, FinalAnswerStep

        thinking_parts = []

        # PlanningStep: 规划阶段
        if isinstance(step, PlanningStep):
            if hasattr(step, 'plan') and step.plan:
                thinking_parts.append(f"📋 步骤 {step_number}: 规划\n{step.plan}\n")

        # ActionStep: 执行动作
        elif isinstance(step, ActionStep):
            # 模型输出 (包含 Thought)
            if hasattr(step, 'model_output') and step.model_output:
                output_str = str(step.model_output)
                # 提取 Thought 部分
                if "Thought:" in output_str or "思考:" in output_str:
                    thinking_parts.append(f"💭 步骤 {step_number}: {output_str[:500]}\n")

            # 工具调用
            if hasattr(step, 'tool_calls') and step.tool_calls:
                for tool_call in step.tool_calls:
                    tool_name = getattr(tool_call, 'name', 'unknown')
                    thinking_parts.append(f"🔧 调用工具: {tool_name}\n")

            # 执行的代码
            if hasattr(step, 'code_action') and step.code_action:
                code_preview = step.code_action[:200]
                thinking_parts.append(f"💻 执行代码:\n{code_preview}...\n")

            # 观察结果
            if hasattr(step, 'observations') and step.observations:
                obs_preview = str(step.observations)[:300]
                thinking_parts.append(f"👁️ 观察结果:\n{obs_preview}...\n")

            # 错误信息
            if hasattr(step, 'error') and step.error:
                thinking_parts.append(f"❌ 错误: {step.error}\n")

        # FinalAnswerStep: 最终答案
        elif isinstance(step, FinalAnswerStep):
            thinking_parts.append(f"✅ 步骤 {step_number}: 生成最终答案\n")

        return "".join(thinking_parts) if thinking_parts else None

    def validate_sql(self, sql: str) -> Dict[str, Any]:
        """
        验证SQL是否符合安全规则

        Args:
            sql: SQL语句

        Returns:
            验证结果
        """
        validation = {
            "valid": True,
            "errors": [],
            "warnings": []
        }

        sql_upper = sql.upper()

        # 检查危险操作
        dangerous_keywords = ["DROP", "DELETE", "TRUNCATE", "ALTER", "INSERT", "UPDATE"]
        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                validation["errors"].append(f"❌ 禁止的操作: {keyword}")
                validation["valid"] = False

        # 检查必需条件
        if "WHERE" not in sql_upper:
            validation["errors"].append("❌ 缺少WHERE子句")
            validation["valid"] = False

        if "DATE" not in sql_upper:
            validation["errors"].append("❌ 缺少日期过滤")
            validation["valid"] = False

        if "EVENT" not in sql_upper:
            validation["errors"].append("❌ 缺少事件筛选")
            validation["valid"] = False

        # 检查建议条件
        if "IS_SPIDER_USER" not in sql_upper:
            validation["warnings"].append("⚠️ 建议添加爬虫过滤")

        return validation

    def close(self):
        """关闭资源"""
        logger.info("关闭EngineerAgent资源")
        if self.sensors_client:
            self.sensors_client.close()

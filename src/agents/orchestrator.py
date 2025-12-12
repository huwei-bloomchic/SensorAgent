"""
Agent编排器
主要的智能代理，协调所有工具并处理用户查询
"""
from typing import List, Optional
from smolagents import CodeAgent
from smolagents.models import OpenAIServerModel
from loguru import logger
import os

from config.settings import get_settings
from src.sensors.client import SensorsClient
from src.tools.event_analysis_tool import EventAnalysisTool
from src.tools.funnel_tool import FunnelTool
from src.tools.retention_tool import RetentionTool
from src.tools.sql_query_tool import SQLQueryTool
from src.tools.event_schema_tool import EventSchemaTool


class SensorsAnalyticsAgent:
    """
    神策数据分析智能助手

    功能：
    - 理解用户自然语言查询
    - 自动选择合适的工具执行分析
    - 返回格式化的分析结果
    - 支持多轮对话和上下文维护
    """

    def __init__(
        self,
        sensors_client: Optional[SensorsClient] = None,
        model_name: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        初始化Agent

        Args:
            sensors_client: 神策API客户端（可选，未提供则自动创建）
            model_name: LLM模型名称（可选，未提供则从配置读取）
            api_key: LLM API密钥（可选，未提供则从配置读取）
        """
        self.settings = get_settings()

        # 初始化神策客户端
        if sensors_client is None:
            sensors_client = self._create_sensors_client()
        self.sensors_client = sensors_client

        # 初始化工具
        self.tools = self._initialize_tools()

        # 初始化LLM模型
        self.model = self._create_llm_model(model_name, api_key)

        # 初始化Agent
        self.agent = self._create_agent()

        logger.info("神策数据分析Agent初始化完成")

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

        # 健康检查
        # if not client.health_check():
        #     logger.warning("神策API健康检查失败，但仍然继续...")

        return client

    def _initialize_tools(self) -> List:
        """初始化所有工具"""
        logger.info("初始化工具...")

        # 导入新的SQL执行工具
        from src.tools.sql_execution_tool import SQLExecutionTool

        # 注意：EventSchemaTool和SQLExpertTool需要model参数，在创建agent后再添加
        tools = [
            # 新架构：使用SQLExecutionTool替代SQLQueryTool
            SQLExecutionTool(self.sensors_client),

            # 已移除DataAnalysisTool - 分析现在由主agent动态完成

            # 保持注释的工具（未来可能启用）:
            # EventAnalysisTool(self.sensors_client),
            # FunnelTool(self.sensors_client),
            # RetentionTool(self.sensors_client),

            # EventSchemaTool 和 SQLExpertTool 将在 _create_agent 中添加（需要model参数）
        ]

        logger.info(f"已加载 {len(tools)} 个工具")
        for tool in tools:
            logger.debug(f"  - {tool.name}")

        return tools

    def _create_llm_model(
        self,
        model_name: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        创建LLM模型

        使用 HfApiModel 连接到 LiteLLM 服务端（OpenAI 兼容 API）

        Args:
            model_name: 模型名称
            api_key: API密钥

        Returns:
            模型实例
        """
        if model_name is None:
            model_name = self.settings.LITELLM_MODEL
        if api_key is None:
            api_key = self.settings.LITELLM_API_KEY

        logger.info(f"创建LLM模型: {model_name}")
        logger.info(f"API 基础 URL: {self.settings.LITELLM_BASE_URL}")

        try:
            # 使用 OpenAIServerModel 连接到 LiteLLM 服务端（OpenAI 兼容 API）
            # OpenAIServerModel 专门用于连接 OpenAI 兼容的服务端
            model = OpenAIServerModel(
                model_id=model_name,
                api_key=api_key,
                api_base=self.settings.LITELLM_BASE_URL,
            )
            logger.info("LLM模型创建成功")
            return model
        except Exception as e:
            logger.error(f"模型创建失败: {e}")
            raise

    def _create_agent(self):
        """
        创建smolagents Agent

        Returns:
            Agent实例
        """
        logger.info("创建Agent...")

        # 导入SQLExpertTool
        from src.tools.sql_expert_tool import SQLExpertTool

        # 为 EventSchemaTool 创建单独的模型实例（使用 gemini-2.5-flash-lite）
        logger.info("为 EventSchemaTool 创建单独的模型...")
        event_schema_model = self._create_llm_model(
            model_name="gemini-2.5-flash-lite",
            api_key=self.settings.LITELLM_API_KEY
        )

        # 添加需要model实例的工具
        event_schema_tool = EventSchemaTool(event_schema_model)  # 使用单独的模型
        sql_expert_tool = SQLExpertTool(self.model)  # 使用主模型

        self.tools.extend([event_schema_tool, sql_expert_tool])
        logger.info("已添加 EventSchemaTool (使用 gemini-2.5-flash-lite) 和 SQLExpertTool")

        # 使用CodeAgent，它支持执行代码和调用工具
        agent = CodeAgent(
            tools=self.tools,
            model=self.model,
            max_steps=10,  # 最大推理步数
            verbosity_level=2,  # 启用详细日志 (0=静默, 1=简要, 2=详细)
            additional_authorized_imports=[
                "json", "datetime", "time",
                "pandas", "matplotlib", "io", "base64",  # 新增数据分析库
                "numpy", "csv"  # 新增辅助库
            ],
        )

        return agent

    def _get_system_prompt(self) -> str:
        """获取系统提示词"""
        from datetime import datetime

        # 获取当前时间信息
        now = datetime.now()
        current_time_info = f"""
==================== 当前时间信息 ====================
⏰ 当前日期: {now.strftime('%Y-%m-%d')}
⏰ 当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}
⏰ 当前年份: {now.year}
⏰ 当前月份: {now.month}月
⏰ 当前星期: 星期{['一', '二', '三', '四', '五', '六', '日'][now.weekday()]}

时间范围处理指南：
1. "今年" = {now.year}年
2. "去年" = {now.year - 1}年
3. "今年11月" = {now.year}-11-01 to {now.year}-11-30
4. "去年11月" = {now.year - 1}-11-01 to {now.year - 1}-11-30
5. "最近7天" = 从今天往前推7天
6. "上个月" = 上一个自然月的完整时间范围
7. "本月" = {now.year}-{now.month:02d}-01 到当前日期

⚠️ 重要：在调用 sql_expert 工具时，必须将用户的模糊时间表述转换为明确的日期范围传递给 date_range 参数！
=====================================================
"""

        return f"""{current_time_info}

你是神策数据分析助手，专门帮助用户分析神策Analytics平台的数据。

你的能力：
1. 事件Schema查询 - 使用 event_schema_tool 智能检索事件定义
2. SQL生成 - 使用 sql_expert 生成优化的Impala SQL查询
3. SQL执行 - 使用 sql_execution 执行查询并获取CSV数据
4. 数据分析 - 使用pandas/matplotlib动态生成分析代码和可视化

工作流程：
【第一步】使用 event_schema_tool 获取事件Schema
   event_schemas = event_schema_tool(query="用户查询需求描述")
   示例：event_schema_tool(query="查询商品点击相关事件")

【第二步】使用 sql_expert 生成SQL查询
   sql_result = sql_expert(
       event_schemas=event_schemas,
       user_query="用户的具体查询问题",
       date_range="last_7_days"  # 或具体日期范围，如 "2024-12-01 to 2024-12-07"
   )
   # sql_result 包含生成的SQL语句和元数据

【第三步】提取SQL并使用 sql_execution 执行查询
   # 从 sql_result 中提取SQL语句（在"SQL:"后面的部分）
   # 然后调用 sql_execution
   result = sql_execution(sql=提取的SQL, filename="可选文件名.csv")
   # 注意：result 是一个字符串
   # result 包含格式化的文本信息和 <structured_data> 标签中的JSON数据

【第四步】使用Python代码分析CSV数据
   import pandas as pd
   import matplotlib.pyplot as plt
   import base64
   import json
   import re
   from io import BytesIO

   # 从 result 的 <structured_data> 标签中提取JSON数据
   # 解析示例：
   # match = re.search(r'<structured_data>(.*?)</structured_data>', result, re.DOTALL)
   # if match:
   #     data = json.loads(match.group(1))
   #     csv_path = data['csv_path']
   # 读取CSV
   df = pd.read_csv(csv_path)

   # 数据分析（根据用户需求）
   # - 计算统计指标
   # - 识别趋势
   # - 发现异常
   # - 生成洞察

   # 生成可视化（可选）
   fig, ax = plt.subplots(figsize=(10, 6))
   ax.plot(df['date'], df['count'])
   ax.set_title('趋势分析')
   ax.set_xlabel('日期')
   ax.set_ylabel('数量')

   # 编码图片用于展示
   buffer = BytesIO()
   plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
   buffer.seek(0)
   img_str = base64.b64encode(buffer.getvalue()).decode()

   # 输出分析结果和图表
   print(f"分析结果: ...")
   print(f"图表: <img src='data:image/png;base64,{{img_str}}' />")

完整示例 - 分析最近7天的商品点击趋势：

步骤1 - 获取Schema:
schemas = event_schema_tool(query="商品点击事件")

步骤2 - 生成SQL:
sql_result = sql_expert(
    event_schemas=schemas,
    user_query="查询最近7天每天的商品点击次数和独立用户数",
    date_range="last_7_days"
)

步骤3 - 执行SQL:
# 从sql_result中提取SQL（在"SQL:"标签后面）
result = sql_execution(sql=提取的SQL, filename="product_clicks.csv")
# 注意：result 是字符串，不要尝试 csv_path, rows, preview = sql_execution(...) 这样解包！

步骤4 - 分析数据:
import pandas as pd
import matplotlib.pyplot as plt
import base64
import json
import re
from io import BytesIO

# 从result的<structured_data>标签中提取JSON数据
match = re.search(r'<structured_data>(.*?)</structured_data>', result, re.DOTALL)
if match:
    data = json.loads(match.group(1))
    csv_path = data['csv_path']
else:
    # 备用方案：直接使用文件名
    csv_path = "./output/product_clicks.csv"

df = pd.read_csv(csv_path)

# 计算增长率
if len(df) > 1:
    growth_rate = (df['event_count'].iloc[-1] - df['event_count'].iloc[0]) / df['event_count'].iloc[0] * 100
else:
    growth_rate = 0

# 计算统计指标
total_clicks = df['event_count'].sum()
avg_clicks = df['event_count'].mean()
max_clicks = df['event_count'].max()

# 生成趋势图
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df['date'], df['event_count'], marker='o', linewidth=2)
ax.set_title('最近7天商品点击趋势', fontsize=14)
ax.set_xlabel('日期', fontsize=12)
ax.set_ylabel('点击次数', fontsize=12)
ax.grid(True, alpha=0.3)

# 编码图片
buffer = BytesIO()
plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
buffer.seek(0)
img_str = base64.b64encode(buffer.getvalue()).decode()

# 输出结果
print("=" * 60)
print("商品点击趋势分析报告")
print("=" * 60)
print(f"\\n分析周期: 最近7天")
print(f"总点击次数: {{total_clicks:,}}")
print(f"日均点击次数: {{avg_clicks:.0f}}")
print(f"最高点击次数: {{max_clicks}}")
print(f"增长率: {{growth_rate:+.2f}}%")
print(f"\\n趋势图:")
print(f"<img src='data:image/png;base64,{{img_str}}' />")

重要提示：
1. 【不要自己编写SQL】- 始终使用 sql_expert 工具生成SQL
2. 【正确提取数据】- 从工具返回的 <structured_data> 标签中提取信息
3. 【使用Python分析】- 用pandas进行所有数据分析，不要依赖预定义工具
4. 【生成可视化】- 分析类问题一定要生成图表
5. 【提供洞察】- 不仅要展示数据，还要给出业务洞察和建议

工作流要点：
- event_schema_tool 的输出直接传给 sql_expert
- sql_expert 自动处理日期范围、事件筛选、爬虫过滤等优化
- sql_execution 返回一个字符串（不是元组！），包含格式化文本和<structured_data>标签中的JSON数据
- 使用正则和json解析从<structured_data>中提取csv_path等结构化信息
- 使用 pandas 进行灵活的数据分析和计算
- 使用 matplotlib 生成专业的可视化图表

注意事项：
- 对于"日活"、"DAU"等概念，通常使用 "$AppStart" 事件
- sql_expert 会自动添加必需的性能优化条件
- 分析结果要清晰明了，突出关键数据
- 如果数据异常，要主动指出并给出可能的原因

⚠️ 错误处理说明（重要）：

工具错误处理机制：
- sql_expert 和 sql_execution 在遇到错误时会**直接抛出异常**
- 异常会自动中断执行流程，你无需手动检查错误
- 如果工具执行成功，会正常返回结果；如果失败，会抛出异常并停止

当异常发生时的正确做法：
1. 异常会自动中断你的执行，你会看到错误信息
2. 你应该向用户报告这个错误
3. 说明可能的原因并给出建议

禁止行为：
❌ 不要在任何情况下编造数据或数字
❌ 不要假设查询成功并继续分析
❌ 不要在没有真实数据的情况下给出分析结果

请用专业但友好的语气与用户交流，提供有价值的数据洞察和行动建议。
"""

    def query(self, user_input: str) -> str:
        """
        处理用户查询

        Args:
            user_input: 用户输入的自然语言查询

        Returns:
            分析结果
        """
        logger.info("=" * 80)
        logger.info(f"[开始处理查询] 用户输入: {user_input}")
        logger.info("=" * 80)

        try:
            # 调用agent处理查询
            import time

            # 包装工具以添加时间追踪
            self._wrap_tools_with_timing()

            start_time = time.time()
            logger.info("[步骤 1/2] 调用Agent开始推理...")
            logger.info(f"系统提示长度: {len(self._get_system_prompt())} 字符")
            logger.info(f"工具数量: {len(self.tools)}")
            logger.info(f"⏱️  [时间戳] Agent.run() 调用开始: {time.strftime('%H:%M:%S')}")

            result = self.agent.run(user_input)

            elapsed_time = time.time() - start_time
            logger.info(f"⏱️  [时间戳] Agent.run() 调用结束: {time.strftime('%H:%M:%S')}")
            logger.info("[步骤 2/2] Agent推理完成")
            logger.info(f"总推理时间: {elapsed_time:.2f} 秒")
            logger.info(f"[查询完成] 返回结果长度: {len(str(result))} 字符")
            logger.info("=" * 80)
            return result

        except Exception as e:
            error_msg = f"查询处理失败: {str(e)}"
            logger.error("=" * 80)
            logger.error(f"[查询失败] {error_msg}")
            logger.error("=" * 80)
            logger.exception("详细错误信息:")
            return error_msg

    def _wrap_tools_with_timing(self):
        """为所有工具添加时间追踪包装器"""
        import time
        from functools import wraps

        for tool in self.tools:
            # 保存原始的forward方法
            if not hasattr(tool, '_original_forward'):
                tool._original_forward = tool.forward

                # 创建带时间追踪的包装器
                @wraps(tool._original_forward)
                def timed_forward(*args, _tool=tool, **kwargs):
                    start = time.time()
                    logger.info(f"⏱️  [{_tool.name}] 工具调用开始: {time.strftime('%H:%M:%S')}")
                    try:
                        result = _tool._original_forward(*args, **kwargs)
                        elapsed = time.time() - start
                        logger.info(f"⏱️  [{_tool.name}] 工具调用结束: {time.strftime('%H:%M:%S')} (耗时: {elapsed:.2f}秒)")
                        return result
                    except Exception:
                        elapsed = time.time() - start
                        logger.error(f"⏱️  [{_tool.name}] 工具调用失败: {time.strftime('%H:%M:%S')} (耗时: {elapsed:.2f}秒)")
                        raise

                # 替换forward方法
                tool.forward = timed_forward

    def reset(self):
        """重置对话状态"""
        logger.info("重置对话状态")
        self.agent = self._create_agent()

    def close(self):
        """关闭资源"""
        logger.info("关闭Agent资源")
        if self.sensors_client:
            self.sensors_client.close()


def create_agent(
    model_name: Optional[str] = None,
    api_key: Optional[str] = None
) -> SensorsAnalyticsAgent:
    """
    工厂函数：创建神策分析Agent

    Args:
        model_name: LLM模型名称
        api_key: API密钥

    Returns:
        SensorsAnalyticsAgent实例
    """
    return SensorsAnalyticsAgent(
        model_name=model_name,
        api_key=api_key
    )

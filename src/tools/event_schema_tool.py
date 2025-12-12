"""
EventSchemaTool - 智能事件Schema检索工具
通过LLM分析用户查询需求，自动选择相关事件并返回完整Schema
"""
import os
from typing import Optional
from smolagents import Tool
from loguru import logger


class EventSchemaTool(Tool):
    """
    事件Schema智能检索工具

    根据用户的查询需求，自动分析并返回相关事件的完整Schema定义（包含公共属性）
    """

    name = "event_schema_tool"
    description = """获取神策埋点事件Schema的智能工具。

功能说明：
- 根据用户的查询需求（如"查询商品点击"、"分析购物车转化"等），自动识别相关事件
- 返回选中事件的完整Schema定义，包括：事件属性、公共属性、预置属性
- 一次调用完成所有工作，无需分阶段查询

使用示例：
- event_schema_tool(query="查询最近7天的商品点击数据")
- event_schema_tool(query="分析用户从商品列表到加购的转化漏斗")
- event_schema_tool(query="统计APP启动和用户登录情况")

注意：
- query参数为必填，描述你的数据查询需求
- 工具会自动选择最相关的事件并返回Schema
"""

    inputs = {
        "query": {
            "type": "string",
            "description": "数据查询需求描述，例如：'查询商品点击事件'、'分析购物车到支付的转化'"
        }
    }

    output_type = "string"

    def __init__(self, model):
        """
        初始化EventSchemaTool

        Args:
            model: LLM模型实例，用于分析查询需求并选择相关事件
        """
        super().__init__()
        self.model = model
        self.doc_root = "docs/Bloomchic埋点"
        logger.info("EventSchemaTool 初始化完成")

    def forward(self, query: str) -> str:
        """
        根据查询需求智能返回相关事件的Schema

        Args:
            query: 用户的查询需求描述

        Returns:
            包含相关事件Schema和公共属性的完整文档
        """
        import time
        tool_start_time = time.time()

        logger.info("=" * 60)
        logger.info("[EventSchemaTool] 开始处理查询")
        logger.info("=" * 60)
        logger.info(f"[查询需求] {query}")
        logger.info(f"[模型] {self.model.__class__.__name__}")
        logger.info("-" * 60)

        try:
            # 1. 加载事件索引
            step_start = time.time()
            logger.info("[步骤 1/3] 加载事件索引...")
            index_content = self._load_index()
            if not index_content:
                logger.error("[步骤 1/3] ✗ 无法加载事件索引文件")
                return "❌ 错误: 无法加载事件索引文件"
            step_elapsed = time.time() - step_start
            logger.info(f"[步骤 1/3] ✓ 索引加载成功 (长度: {len(index_content)} 字符, 耗时: {step_elapsed:.2f}秒)")

            # 2. 调用LLM分析查询需求，选择相关事件
            step_start = time.time()
            logger.info("[步骤 2/3] 调用LLM选择相关事件...")
            selected_events = self._select_events_by_llm(query, index_content)
            step_elapsed = time.time() - step_start
            if not selected_events:
                logger.warning(f"[步骤 2/3] ⚠ 未找到相关事件 (LLM耗时: {step_elapsed:.2f}秒)")
                return f"⚠️  根据查询需求'{query}'未找到相关事件，请尝试更具体的描述"

            logger.info(f"[步骤 2/3] ✓ 选中 {len(selected_events)} 个事件: {', '.join(selected_events)} (LLM耗时: {step_elapsed:.2f}秒)")

            # 3. 加载选中事件的详细Schema
            step_start = time.time()
            logger.info("[步骤 3/3] 加载事件Schema文档...")
            schema_content = self._load_event_schemas(selected_events)
            step_elapsed = time.time() - step_start
            logger.info(f"[步骤 3/3] ✓ Schema加载完成 (长度: {len(schema_content)} 字符, 耗时: {step_elapsed:.2f}秒)")

            # 4. 返回完整内容（添加event_list标签）
            result = f"""
{'='*60}
查询需求: {query}
{'='*60}

已选择以下事件: {', '.join(selected_events)}

{schema_content}

<event_list>
{','.join(selected_events)}
</event_list>
"""
            tool_elapsed = time.time() - tool_start_time
            logger.info("=" * 60)
            logger.info(f"[EventSchemaTool] 处理完成 (总耗时: {tool_elapsed:.2f}秒)")
            logger.info("=" * 60)
            return result

        except Exception as e:
            logger.error("=" * 60)
            logger.error(f"[EventSchemaTool] 执行失败: {e}")
            logger.error("=" * 60)
            logger.exception("详细错误信息:")
            return f"❌ 工具执行失败: {str(e)}"

    def _load_index(self) -> str:
        """加载事件索引文件"""
        index_path = os.path.join(self.doc_root, "index.md")

        logger.debug(f"[加载索引] 索引文件路径: {index_path}")

        if not os.path.exists(index_path):
            logger.error(f"[加载索引] 索引文件不存在: {index_path}")
            return ""

        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 统计事件数量
            event_count = content.count('- **')
            logger.info(f"[加载索引] 成功加载事件索引: {len(content)} 字符, 约 {event_count} 个事件")
            logger.debug(f"[加载索引] 索引内容前500字符:\n{content[:500]}...")

            return content
        except Exception as e:
            logger.error(f"[加载索引] 读取索引文件失败: {e}")
            logger.exception("[加载索引] 详细错误:")
            return ""

    def _select_events_by_llm(self, query: str, index_content: str) -> list:
        """
        使用LLM分析查询需求并选择相关事件

        Args:
            query: 用户查询需求
            index_content: 事件索引内容

        Returns:
            选中的事件名列表
        """
        prompt = f"""你是神策数据分析专家。请根据用户的查询需求，从事件索引中选择最相关的事件。

【用户查询需求】
{query}

【可用事件索引】
{index_content}

【任务要求】
1. 仔细分析用户的查询需求
2. 从索引中选择最相关的事件（通常1-5个事件）
3. 只返回事件的英文名称，用逗号分隔
4. 不要返回其他解释或说明

【输出格式】
只输出事件名称，用逗号分隔，例如：
ProductClick,AddToCartClick,PurchaseSuccess

请选择事件："""

        try:
            logger.debug("=" * 60)
            logger.debug("[LLM调用] 开始调用LLM选择事件")
            logger.debug("=" * 60)
            logger.debug(f"[输入-查询需求] {query}")
            logger.debug(f"[输入-索引长度] {len(index_content)} 字符")
            logger.debug(f"[输入-完整Prompt]\n{prompt}")
            logger.debug("-" * 60)

            # 调用LLM
            response = self.model([{"role": "user", "content": prompt}])

            logger.debug(f"[LLM响应-类型] {type(response)}")
            logger.debug(f"[LLM响应-原始对象] {response}")

            # 检查响应对象的结构
            if hasattr(response, 'content'):
                response_content = response.content
                logger.debug(f"[LLM响应-content类型] {type(response_content)}")
                logger.debug(f"[LLM响应-content值] {response_content}")
            else:
                logger.error(f"[LLM响应] response对象没有content属性")
                logger.error(f"[LLM响应] response对象属性: {dir(response)}")
                return []

            # 解析返回的事件名
            if isinstance(response_content, str):
                event_names = [name.strip() for name in response_content.strip().split(',')]
            else:
                # 如果content不是字符串，尝试转换
                logger.warning(f"[LLM响应] content不是字符串类型，尝试转换: {type(response_content)}")
                event_names = [name.strip() for name in str(response_content).strip().split(',')]

            # 过滤空值
            event_names = [name for name in event_names if name]

            logger.info(f"[LLM选择结果] 成功选择 {len(event_names)} 个事件: {event_names}")
            logger.debug("=" * 60)
            return event_names

        except Exception as e:
            logger.error("=" * 60)
            logger.error(f"[LLM调用失败] {e}")
            logger.exception("[LLM调用失败] 详细错误堆栈:")
            logger.error("=" * 60)
            return []

    def _load_event_schemas(self, event_names: list) -> str:
        """
        加载事件的详细Schema定义

        Args:
            event_names: 事件名列表

        Returns:
            拼接后的Schema文档内容
        """
        parts = []

        # 1. 加载公共属性（所有事件都需要）
        common_files = ["公共属性.md", "预置属性.md"]
        for common_file in common_files:
            path = os.path.join(self.doc_root, common_file)
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    parts.append(f"{'='*60}\n📋 {common_file}\n{'='*60}\n{content}")
                    logger.info(f"加载公共属性: {common_file}")
                except Exception as e:
                    logger.error(f"读取{common_file}失败: {e}")

        # 2. 加载各个事件的详细定义
        for event_name in event_names:
            # 安全处理文件名
            safe_name = event_name.replace("/", "").replace("..", "")
            event_path = os.path.join(self.doc_root, "events", f"{safe_name}.md")

            if os.path.exists(event_path):
                try:
                    with open(event_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    parts.append(f"{'='*60}\n📌 事件: {event_name}\n{'='*60}\n{content}")
                    logger.info(f"✅ 加载事件: {event_name}")
                except Exception as e:
                    logger.error(f"读取事件{event_name}失败: {e}")
                    parts.append(f"⚠️  事件 '{event_name}' 读取失败: {str(e)}")
            else:
                parts.append(f"⚠️  事件 '{event_name}' 的定义文件不存在: {event_path}")
                logger.warning(f"事件文件不存在: {event_path}")

        return "\n\n".join(parts)

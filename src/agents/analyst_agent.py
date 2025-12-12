"""
上层分析规划Agent (The Analyst / Planner)

职责:
- 懂业务，不懂SQL
- 理解用户的模糊问题
- 读取元数据(维度配置表)，决定分析方向
- 生成分析计划，将复杂问题拆解为多个子任务
- 向下层Agent发送自然语言指令
"""
from typing import List, Dict, Any, Optional
from smolagents import CodeAgent
from smolagents.models import OpenAIServerModel
from loguru import logger
from datetime import datetime

from config.settings import get_settings


class AnalystAgent:
    """
    分析规划Agent

    特点:
    - 专注于业务理解和问题分解
    - 不直接操作SQL
    - 通过自然语言与下层Agent交互
    - 负责结果的综合分析和洞察生成
    """

    def __init__(
        self,
        model: Optional[OpenAIServerModel] = None,
        model_name: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        初始化分析规划Agent

        Args:
            model: LLM模型实例(可选)
            model_name: 模型名称(可选)
            api_key: API密钥(可选)
        """
        self.settings = get_settings()

        # 初始化模型
        if model is None:
            self.model = self._create_llm_model(model_name, api_key)
        else:
            self.model = model

        # 初始化Agent
        self.agent = self._create_agent()

        logger.info("AnalystAgent 初始化完成")

    def _create_llm_model(
        self,
        model_name: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> OpenAIServerModel:
        """创建LLM模型"""
        if model_name is None:
            model_name = self.settings.LITELLM_MODEL
        if api_key is None:
            api_key = self.settings.LITELLM_API_KEY

        logger.info(f"创建AnalystAgent LLM模型: {model_name}")

        model = OpenAIServerModel(
            model_id=model_name,
            api_key=api_key,
            api_base=self.settings.LITELLM_BASE_URL,
        )

        return model

    def _create_agent(self) -> CodeAgent:
        """创建CodeAgent"""
        logger.info("创建AnalystAgent...")

        # 上层Agent不需要工具，主要用于分析和规划
        agent = CodeAgent(
            tools=[],  # 上层Agent不直接使用工具
            model=self.model,
            max_steps=10,
            verbosity_level=2,
            additional_authorized_imports=[
                "json", "datetime", "time",
                "pandas", "matplotlib", "io", "base64",
                "numpy", "csv"
            ],
        )

        return agent

    def _get_system_prompt(self, stage: str = "initial") -> str:
        """
        获取系统提示词

        Args:
            stage: 分析阶段 ("initial" 或 "drilldown")
        """
        now = datetime.now()
        current_time_info = f"""
==================== 当前时间信息 ====================
⏰ 当前日期: {now.strftime('%Y-%m-%d')}
⏰ 当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}
⏰ 当前年份: {now.year}
⏰ 当前月份: {now.month}月
⏰ 当前星期: 星期{['一', '二', '三', '四', '五', '六', '日'][now.weekday()]}

时间范围处理指南:
1. "今年" = {now.year}年
2. "去年" = {now.year - 1}年
3. "今年11月" = {now.year}-11-01 to {now.year}-11-30
4. "去年11月" = {now.year - 1}-11-01 to {now.year - 1}-11-30
5. "最近7天" = 从今天往前推7天
6. "上个月" = 上一个自然月的完整时间范围
7. "本月" = {now.year}-{now.month:02d}-01 到当前日期
=====================================================
"""

        # 根据阶段选择不同的指导策略
        if stage == "drilldown":
            stage_guidance = """
【当前阶段：深入分析】
你现在处于**下钻分析**阶段。你已经看到了初步查询的结果，现在需要：
1. 基于初步结果，决定是否需要深入分析某些维度
2. 如果发现异常或需要进一步解释的现象，生成下钻查询
3. 如果初步结果已经足够回答问题，可以不生成新指令

**重要原则：**
- 只有在确实需要更多细节时才生成下钻指令
- 避免过度分析和不必要的查询
- 关注用户问题的核心关切
"""
        else:
            stage_guidance = """
【当前阶段：初步分析】
你现在处于**初始分析**阶段。请：
1. 生成1-2个核心查询来获取整体情况
2. 不要一次性生成所有可能的下钻查询
3. 保持查询范围适中，避免过于宽泛或过于细节

**重要原则：**
- 先看大盘，再决定是否下钻
- 一次只生成最关键的查询
- 为后续可能的下钻分析预留空间
"""

        return f"""{current_time_info}

你是神策数据的**业务分析规划专家**，专注于理解业务问题并生成分析计划。

{stage_guidance}

【你的身份定位】
- ✅ 你懂业务逻辑、数据分析方法
- ✅ 你能理解用户的模糊问题，将其转化为明确的分析任务
- ✅ 你负责制定分析计划、拆解复杂问题
- ❌ 你不懂SQL，不需要编写SQL
- ❌ 你不直接操作数据库

【你的核心能力】
1. **问题理解**: 将用户的模糊需求转化为明确的分析目标
2. **维度分析**: 确定需要分析的维度(渠道、品类、时间等)
3. **计划生成**: 制定分析步骤，决定先查什么、后查什么
4. **指令生成**: 将分析计划转化为自然语言指令(交给下层EngineerAgent执行)
5. **结果综合**: 整合多个查询结果，生成业务洞察

【工作流程】
你的工作分为三个阶段:

**阶段1: 理解问题**
- 分析用户问题，识别关键要素(指标、维度、时间范围)
- 示例: "昨天GMV下降了" -> 需要查询昨天的GMV数据，并与历史对比

**阶段2: 制定计划**
- 决定分析路径: 需要查询哪些维度?
- 示例分析路径:
  * 先查整体GMV趋势(按天)
  * 如果有异常，再查各渠道GMV(按渠道维度)
  * 如果某渠道异常，再查该渠道的品类分布(按品类维度)

**阶段3: 生成指令**
- 将分析计划转化为自然语言指令
- 这些指令会交给EngineerAgent执行(它会生成并执行SQL)

【指令格式示例】
你需要生成如下格式的指令:

```python
# 第一步: 查询整体趋势
instruction_1 = {{
    "task": "查询最近7天每天的GMV总额和订单数",
    "time_range": "last_7_days",
    "dimensions": ["date"],
    "metrics": ["GMV总额", "订单数"]
}}

# 第二步: 如果发现异常，深入分析
instruction_2 = {{
    "task": "查询昨天各渠道的GMV和订单数",
    "time_range": "yesterday",
    "dimensions": ["channel"],
    "metrics": ["GMV", "订单数"]
}}
```

【可用的维度和指标】
常见维度:
- 时间维度: date (日期)
- 渠道维度: channel/source
- 品类维度: category
- 用户维度: user_type
- 地域维度: country/region

常见指标:
- GMV: 成交金额
- 订单数: COUNT(订单)
- 用户数: COUNT(DISTINCT user_id)
- 转化率: 下单用户数/访问用户数
- 客单价: GMV/订单数

【输出要求】
1. 先用自然语言描述你的分析计划
2. 然后生成具体的指令(JSON格式)
3. 每个指令要清晰、可执行

【重要提示】
- 你只负责"想"(分析规划)，不负责"做"(执行SQL)
- 你的指令会交给EngineerAgent，它懂SQL和数据库
- 专注于业务逻辑和分析方法，不要担心技术实现
- 如果问题复杂，可以拆解为多个步骤，逐步分析

现在，请根据用户的问题生成分析计划和指令。
"""

    def analyze(self, user_question: str, context: Optional[Dict[str, Any]] = None, stage: str = "initial") -> Dict[str, Any]:
        """
        分析用户问题，生成分析计划

        支持渐进式分析：先生成初步查询指令，根据结果再决定是否深入

        Args:
            user_question: 用户的业务问题
            context: 上下文信息(可选)，包含之前的查询结果
            stage: 分析阶段，可选值:
                - "initial": 初始分析，生成第一步查询
                - "drilldown": 深入分析，基于初步结果生成下钻查询

        Returns:
            分析计划和指令列表
        """
        logger.info("=" * 80)
        logger.info(f"[AnalystAgent] 开始分析用户问题 (阶段: {stage}): {user_question}")
        logger.info("=" * 80)

        try:
            # 构建完整的prompt
            system_prompt = self._get_system_prompt(stage=stage)

            # 添加上下文信息(如果有)
            context_info = ""
            if context:
                context_info = f"\n\n【上下文信息】\n{context}\n"

            full_prompt = f"{system_prompt}\n\n【用户问题】\n{user_question}{context_info}"

            # 调用LLM分析
            logger.info(f"[AnalystAgent] 调用LLM生成分析计划 (阶段: {stage})...")
            response = self.model([{"role": "user", "content": full_prompt}])

            # 解析响应
            analysis_plan = response.content

            logger.info("[AnalystAgent] 分析计划生成完成")
            logger.debug(f"[分析计划]\n{analysis_plan}")

            # 返回结构化结果
            result = {
                "user_question": user_question,
                "analysis_plan": analysis_plan,
                "stage": stage,
                "timestamp": datetime.now().isoformat()
            }

            logger.info("=" * 80)
            return result

        except Exception as e:
            logger.error(f"[AnalystAgent] 分析失败: {e}", exc_info=True)
            raise

    def synthesize_results(
        self,
        instructions: List[Dict[str, Any]],
        results: List[Dict[str, Any]]
    ) -> str:
        """
        综合多个查询结果，生成业务洞察（Markdown格式）

        Args:
            instructions: 执行的指令列表
            results: 查询结果列表

        Returns:
            Markdown格式的综合分析报告
        """
        logger.info("[AnalystAgent] 开始综合分析结果...")

        try:
            # ⚠️ 优化: 提取摘要信息，避免上下文爆炸
            results_summary = self._extract_results_summary(results)

            # 记录原始大小 vs 摘要大小
            original_size = len(str(results))
            summary_size = len(str(results_summary))
            logger.info(f"[上下文优化] 原始大小: {original_size} 字符, 摘要大小: {summary_size} 字符, 压缩率: {(1 - summary_size/original_size)*100:.1f}%")

            # 构建综合分析prompt (使用摘要信息)
            synthesis_prompt = f"""
你是数据分析专家，请根据以下查询结果生成**Markdown格式**的业务洞察报告。

【执行的分析任务】
{self._format_instructions(instructions)}

【查询结果摘要】
{results_summary}

【输出格式要求】
请生成一个完整的Markdown文档，包含以下部分：

## 1. 执行摘要
- 用2-3句话概括核心发现
- 直接回答用户的问题
- **必须引用上面"查询结果摘要"中的具体数值**

## 2. 数据分析

### 2.1 关键指标
- **必须从"查询结果摘要"的"数据预览"或"统计摘要"中提取实际数值**
- 使用表格展示关键数据
- 示例格式：
  | 指标名称 | 数值 | 单位 |
  |---------|------|------|
  | GMV总额 | 12,818,512.58 | 元 |
  | 订单数 | 143,416 | 单 |

### 2.2 趋势分析
- 识别数据中的趋势、异常或模式
- 如果有时间序列数据，描述变化趋势
- **引用具体数值**，例如："从2023年11月的154,619单下降到2024年11月的143,416单，降幅7.2%"

### 2.3 维度对比
- 如果有多维度数据（如渠道、品类等），进行对比分析
- 指出表现突出或异常的维度
- **必须使用实际数据值**

## 3. 可视化建议
根据数据特点，建议使用以下图表类型（用代码块标注）：

```chart-suggestion
类型: [折线图/柱状图/饼图/等]
数据: [描述应该可视化的数据]
说明: [为什么选择这个图表类型]
```

（注意：你只需要建议图表类型和说明，不需要实际绘制）

## 4. 数据表

### 查询1: [查询描述]
**数据概览:**
- 行数: [从查询结果摘要中提取]
- 时间范围: [从查询结果摘要中提取]
- 主要维度: [从查询结果摘要中提取]

**数据预览:**
[将"查询结果摘要"中的"数据预览"转换为Markdown表格格式]

**完整数据文件:** `[CSV文件路径]`

（如果有多个查询，重复此结构）

## 5. 业务洞察与建议

### 5.1 关键发现
1. [发现1 - 必须基于实际数据]
2. [发现2 - 必须基于实际数据]
3. [发现3 - 必须基于实际数据]

### 5.2 可能的原因
- [原因分析1]
- [原因分析2]

### 5.3 行动建议
1. [建议1]
2. [建议2]
3. [建议3]

## 6. 附录
- 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 数据来源: 神策数据平台

---

【关键要求 - 必须遵守】
1. **绝对禁止使用"待填充"、"待计算"等占位符** - 必须使用上面"查询结果摘要"中的实际数值
2. **数据预览部分**：将文本格式的数据预览转换为规范的Markdown表格
3. **关键指标部分**：必须填入具体数值，从"数据预览"或"统计摘要"中提取
4. **趋势分析部分**：必须引用实际数据进行对比计算
5. 表格使用标准Markdown格式: | 列1 | 列2 | ... |
6. 使用清晰的业务语言，避免技术术语
7. 突出显示异常值和关键发现
8. 如果"查询结果摘要"中的数据不足以支撑分析，明确说明需要更多数据

现在，请生成完整的Markdown分析报告，**确保所有数据字段都填入实际数值**：
"""

            response = self.model([{"role": "user", "content": synthesis_prompt}])
            report = response.content

            logger.info("[AnalystAgent] 综合分析完成")
            return report

        except Exception as e:
            logger.error(f"[AnalystAgent] 综合分析失败: {e}", exc_info=True)
            return f"综合分析失败: {str(e)}"

    def _extract_results_summary(self, results: List[Dict[str, Any]]) -> str:
        """
        从查询结果中提取摘要信息，避免上下文爆炸

        策略:
        1. 只保留CSV路径和行数
        2. 如果数据≤30行，保留全部数据；否则保留前20行
        3. 提取structured_data中的统计摘要
        4. 移除大段的原始数据

        Args:
            results: 查询结果列表

        Returns:
            结果摘要字符串
        """
        import re
        import json

        summaries = []

        for i, result in enumerate(results, 1):
            summary = {
                "查询序号": i,
                "状态": result.get("status", "unknown")
            }

            if result.get("status") == "success":
                result_text = result.get("result", "")

                # 确保 result_text 是字符串
                if isinstance(result_text, dict):
                    result_text = str(result_text)
                elif not isinstance(result_text, str):
                    result_text = str(result_text)

                # 提取CSV路径
                csv_match = re.search(r'CSV 文件:\s*(.+)', result_text)
                if csv_match:
                    summary["CSV文件"] = csv_match.group(1).strip()

                # 提取行数
                rows_match = re.search(r'行数:\s*(\d+)', result_text)
                rows_count = 0
                if rows_match:
                    rows_count = int(rows_match.group(1))
                    summary["数据行数"] = rows_count

                # 提取列信息
                columns_match = re.search(r'列:\s*\[([^\]]+)\]', result_text)
                if columns_match:
                    summary["列名"] = columns_match.group(1).strip()

                # 提取structured_data中的统计信息
                structured_match = re.search(r'<structured_data>(.*?)</structured_data>', result_text, re.DOTALL)
                if structured_match:
                    try:
                        structured_data = json.loads(structured_match.group(1))

                        # 只保留关键统计信息
                        if "summary_stats" in structured_data:
                            summary["统计摘要"] = structured_data["summary_stats"]

                        if "date_range" in structured_data:
                            summary["日期范围"] = structured_data["date_range"]
                    except:
                        pass

                # 提取数据预览 - 根据数据量动态调整
                preview_match = re.search(r'数据预览.*?:\s*\n-+\n(.*?)(?:\n\.\.\.|=====|\Z)', result_text, re.DOTALL)
                if preview_match:
                    preview_lines = preview_match.group(1).strip().split('\n')

                    # 动态决定保留多少行数据
                    if rows_count > 0 and rows_count <= 30:
                        # 小数据集：保留所有数据
                        summary["数据预览"] = '\n'.join(preview_lines)
                        summary["_数据完整性"] = "完整数据"
                    else:
                        # 大数据集：保留前20行
                        max_preview = 20
                        summary["数据预览"] = '\n'.join(preview_lines[:max_preview])
                        if len(preview_lines) > max_preview:
                            summary["数据预览"] += f"\n... (还有 {len(preview_lines) - max_preview} 行未显示)"
                        summary["_数据完整性"] = f"前{max_preview}行预览"

            else:
                # 失败的查询
                summary["错误"] = result.get("error", "未知错误")

            summaries.append(summary)

        # 格式化输出
        output_lines = []
        for summary in summaries:
            output_lines.append(f"\n查询 {summary['查询序号']}:")
            output_lines.append("-" * 60)
            for key, value in summary.items():
                if key != "查询序号" and not key.startswith("_"):
                    if isinstance(value, dict):
                        output_lines.append(f"  {key}:")
                        for k, v in value.items():
                            output_lines.append(f"    {k}: {v}")
                    else:
                        output_lines.append(f"  {key}: {value}")
            output_lines.append("")

        return '\n'.join(output_lines)

    def _format_instructions(self, instructions: List[Dict[str, Any]]) -> str:
        """
        格式化指令列表，避免冗余信息

        Args:
            instructions: 指令列表

        Returns:
            格式化后的指令字符串
        """
        formatted = []
        for i, inst in enumerate(instructions, 1):
            if isinstance(inst, dict):
                task = inst.get("task", str(inst))
                formatted.append(f"{i}. {task}")
            else:
                formatted.append(f"{i}. {inst}")

        return '\n'.join(formatted)

    def evaluate_and_decide_drilldown(
        self,
        user_question: str,
        initial_results: List[Dict[str, Any]],
        task_type: str = "auto"
    ) -> Dict[str, Any]:
        """
        评估初步查询结果，决定是否需要下钻分析

        Args:
            user_question: 原始用户问题
            initial_results: 初步查询的结果列表
            task_type: 任务类型提示 ("trend", "anomaly", "comparison", "auto")

        Returns:
            决策结果，包含:
            - need_drilldown: bool - 是否需要下钻
            - reasoning: str - 决策理由
            - suggested_dimensions: List[str] - 建议分析的维度
        """
        logger.info("[AnalystAgent] 开始评估是否需要下钻分析...")

        try:
            # 提取结果摘要
            results_summary = self._extract_results_summary(initial_results)

            # 构建评估prompt
            evaluation_prompt = f"""
你是数据分析专家，需要评估初步查询结果，决定是否需要进一步深入分析。

【原始问题】
{user_question}

【初步查询结果】
{results_summary}

【任务】
请分析以上结果，回答以下问题：

1. **结果是否足够回答用户问题？**
   - 如果结果已经清晰回答了问题，返回 NO_DRILLDOWN_NEEDED
   - 如果结果显示有异常/趋势/差异需要进一步解释，返回 DRILLDOWN_NEEDED

2. **如果需要下钻，应该从哪些维度分析？**
   可选维度：
   - channel/source (渠道)
   - category (品类/类别)
   - region/country (地域)
   - user_type (用户类型)
   - device_type (设备类型)

3. **决策理由是什么？**

请按以下JSON格式返回：
```json
{{
    "decision": "DRILLDOWN_NEEDED 或 NO_DRILLDOWN_NEEDED",
    "reasoning": "决策理由（为什么需要或不需要下钻）",
    "suggested_dimensions": ["dimension1", "dimension2"],
    "confidence": 0.8
}}
```

注意：
- 如果用户只是问"最近7天GMV"，且结果已经给出了明确数值 -> NO_DRILLDOWN_NEEDED
- 如果用户问"为什么GMV下降"，且初步结果显示确实下降 -> DRILLDOWN_NEEDED，需要按维度分析原因
- 如果用户问"对比分析"，初步结果只有整体数据 -> DRILLDOWN_NEEDED
"""

            # 调用LLM评估
            response = self.model([{"role": "user", "content": evaluation_prompt}])

            # 处理响应内容 - 可能是字符串或字典
            if hasattr(response, 'content'):
                evaluation_text = response.content
            else:
                evaluation_text = str(response)

            # 确保是字符串
            if isinstance(evaluation_text, dict):
                evaluation_text = json.dumps(evaluation_text, ensure_ascii=False)

            logger.debug(f"[评估结果]\n{evaluation_text}")

            # 解析JSON响应
            import json
            import re

            json_match = re.search(r'```json\s*(\{.*?\})\s*```', evaluation_text, re.DOTALL)
            if json_match:
                decision_data = json.loads(json_match.group(1))
            else:
                # 尝试直接解析整个文本
                try:
                    decision_data = json.loads(evaluation_text)
                except json.JSONDecodeError:
                    # 如果还是失败，尝试提取第一个JSON对象
                    json_obj_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', evaluation_text, re.DOTALL)
                    if json_obj_match:
                        decision_data = json.loads(json_obj_match.group(0))
                    else:
                        raise ValueError(f"无法从响应中解析JSON: {evaluation_text[:200]}")

            need_drilldown = decision_data.get("decision") == "DRILLDOWN_NEEDED"
            reasoning = decision_data.get("reasoning", "未提供理由")
            suggested_dimensions = decision_data.get("suggested_dimensions", [])
            confidence = decision_data.get("confidence", 0.5)

            logger.info(f"[决策结果] {'需要下钻' if need_drilldown else '不需要下钻'} (置信度: {confidence})")
            logger.info(f"[决策理由] {reasoning}")

            if need_drilldown and suggested_dimensions:
                logger.info(f"[建议维度] {', '.join(suggested_dimensions)}")

            return {
                "need_drilldown": need_drilldown,
                "reasoning": reasoning,
                "suggested_dimensions": suggested_dimensions,
                "confidence": confidence
            }

        except Exception as e:
            logger.error(f"[AnalystAgent] 评估下钻决策失败: {e}", exc_info=True)
            # 默认不下钻，避免过度查询
            return {
                "need_drilldown": False,
                "reasoning": f"评估失败: {str(e)}",
                "suggested_dimensions": [],
                "confidence": 0.0
            }

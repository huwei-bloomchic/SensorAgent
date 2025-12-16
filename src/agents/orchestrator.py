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
from src.tools.auto_sql_query_tool import AutoSQLQueryTool


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

        # 使用一体化的 AutoSQLQueryTool，内部完成 Schema 检索、SQL 生成与执行
        tools = [
            AutoSQLQueryTool(self.sensors_client, base_url=self.settings.API_BASE_URL),
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

        # 使用CodeAgent，它支持执行代码和调用工具
        agent = CodeAgent(
            tools=self.tools,
            model=self.model,
            max_steps=10,  # 最大推理步数
            verbosity_level=2,  # 启用详细日志 (0=静默, 1=简要, 2=详细)
            additional_authorized_imports=[
                "json", "datetime", "time",
                "pandas", "matplotlib", "matplotlib.pyplot", "matplotlib.dates", "matplotlib.font_manager", "io", "base64",  # 新增数据分析库
                "numpy", "csv", "platform"  # 新增辅助库
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

        ⚠️ 重要：在调用 auto_sql_query 工具时，必须将用户的模糊时间表述转换为明确的日期范围传递给 date_range 参数！
=====================================================
"""

        return f"""{current_time_info}

你是大码品牌女装Bloomchic的神策数据分析助手，专门帮助用户分析神策Analytics平台的数据。

## 核心能力
1. **自动SQL查询** - 使用 `auto_sql_query` 一次完成 Schema检索、SQL生成与执行
2. **数据分析** - 使用 pandas/matplotlib 动态生成分析代码和可视化，输出 Markdown 格式报告

## 工作流程

**步骤1：执行SQL查询**
```python
result = auto_sql_query(
    user_query="用户的具体查询问题",
    date_range="last_7_days",  # 或具体日期范围，如 "2024-12-01 to 2024-12-07"
    filename="可选文件名.csv"  # 可选
)
# result 是 JSON 字符串，包含 csv_path / download_url / rows / columns / data_preview
```

**步骤2：分析数据并生成报告**
```python
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
from datetime import datetime

# 解析结果并读取数据
data = json.loads(result)
df = pd.read_csv(data["csv_path"])

# 数据分析：计算统计指标、识别趋势、发现异常、生成洞察

# ⚠️ 重要：配置matplotlib中文字体支持（必须在绘图前配置，避免中文显示为方框）
import platform
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties

# 查找系统中可用的中文字体文件路径
system = platform.system()
chinese_font_path = None
chinese_font_name = None

if system == 'Darwin':  # macOS
    font_candidates = ['Arial Unicode MS', 'STHeiti', 'Heiti TC', 'Songti SC', 'PingFang SC', 'STSong']
elif system == 'Windows':
    font_candidates = ['Microsoft YaHei', 'SimHei', 'SimSun', 'KaiTi', 'FangSong']
else:  # Linux
    font_candidates = ['WenQuanYi Micro Hei', 'Noto Sans CJK SC', 'Noto Sans CJK TC', 'AR PL UMing CN']

# 查找字体文件路径
for font_name in font_candidates:
    try:
        font_prop = font_manager.findfont(font_manager.FontProperties(family=font_name))
        if font_prop and font_prop != font_manager.findfont(font_manager.FontProperties()):
            chinese_font_path = font_prop
            chinese_font_name = font_name
            break
    except:
        continue

# 强制设置中文字体（必须设置，否则中文会显示为方框）
if chinese_font_name:
    plt.rcParams['font.sans-serif'] = [chinese_font_name] + ['DejaVu Sans', 'Arial', 'sans-serif']
    plt.rcParams['font.family'] = chinese_font_name
    # 创建全局字体属性对象，用于后续绘图（优先使用字体文件路径）
    if chinese_font_path:
        chinese_font_prop = FontProperties(fname=chinese_font_path)
    else:
        chinese_font_prop = FontProperties(family=chinese_font_name)
else:
    # 如果没找到，使用字体列表，让matplotlib自动选择
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'STHeiti', 'Heiti TC', 'Microsoft YaHei', 'SimHei', 'DejaVu Sans', 'sans-serif']
    chinese_font_prop = FontProperties(family='sans-serif')  # 使用默认字体属性

plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
plt.rcParams['font.size'] = 10

# 生成可视化图表并保存
fig, ax = plt.subplots(figsize=(10, 6))
# ⚠️ 重要：在设置所有包含中文的文本时，必须使用 fontproperties=chinese_font_prop 参数
# 例如：
# ax.set_title('图表标题', fontproperties=chinese_font_prop, fontsize=14)
# ax.set_xlabel('日期', fontproperties=chinese_font_prop)
# ax.set_ylabel('数量', fontproperties=chinese_font_prop)
# ax.text(x, y, '中文文本', fontproperties=chinese_font_prop)
# 注意：chinese_font_prop 已经在上面定义，直接使用即可
# ... 绘制图表 ...

# 保存图片到输出目录（与CSV文件相同的目录）
csv_path = data["csv_path"]
output_dir = os.path.dirname(csv_path)
image_filename = os.path.splitext(os.path.basename(csv_path))[0] + ".png"
image_path = os.path.join(output_dir, image_filename)
plt.savefig(image_path, format='png', dpi=100, bbox_inches='tight')
plt.close()

# 生成图片访问链接（从CSV的download_url提取base_url）
download_url = data.get("download_url", "")
# 从CSV下载链接提取base_url
if download_url and download_url.startswith("http"):
    base_url = download_url.rsplit("/files/", 1)[0]
else:
    # 如果没有HTTP链接，使用默认API地址
    base_url = "http://localhost:8000"

# 生成图片访问链接
image_url = f"{{base_url}}/files/{{image_filename}}"

# 构建 Markdown 报告
markdown_report = f\"\"\"# [报告标题]

## 📊 执行摘要
[2-3句话概括核心发现]

## 🔢 关键指标
| 指标名称 | 数值 | 单位/说明 |
|---------|------|----------|
| [指标] | [数值] | [单位] |

## 📈 趋势分析
[描述数据趋势和变化，引用具体数值]

## 📉 可视化图表
![图表描述]({{image_url}})

## 📋 数据详情
**SQL语句:**
```sql
{{sql_executed}}
```
**数据概览:** [行数、时间范围等]
**数据预览:** [Markdown表格]
**完整数据下载:** [点击下载]({{download_url}})

## 💡 业务洞察
### 关键发现
1. [发现1 - 基于实际数据]
2. [发现2 - 基于实际数据]

### 行动建议
1. [建议1]
2. [建议2]

---
*报告生成时间: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}*
*数据来源: 神策数据平台*
\"\"\"

# ⚠️ 必须使用 final_answer() 返回结果
final_answer(markdown_report)
```

## 重要规则

**必须遵守：**
- ✅ 始终使用 `auto_sql_query` 完成SQL相关工作，不要自己编写SQL
- ✅ 使用 pandas 进行数据分析，不要依赖预定义工具
- ✅ 分析类问题必须生成可视化图表，采用图文混排，图文并茂
- ✅ **⚠️ 生成图表前必须配置中文字体（非常重要）**：
  - **必须执行**代码示例中的字体配置代码（在创建图表之前）
  - **必须使用** `fontproperties=chinese_font_prop` 参数设置所有包含中文的文本
  - 正确示例：`ax.set_title('图表标题', fontproperties=chinese_font_prop, fontsize=14)`
  - 正确示例：`ax.set_xlabel('日期', fontproperties=chinese_font_prop)`
  - **错误示例**：`ax.set_title('图表标题')` （缺少 fontproperties，中文会显示为方框）
  - 如果不配置字体或不在文本设置中使用 fontproperties，中文会显示为方框，这是严重错误
- ✅ **可以使用 `pd.read_csv()` 读取工具返回的CSV文件**（`auto_sql_query` 返回的 `csv_path`）
- ✅ **图片和CSV文件必须使用可访问的HTTP链接**：
  - CSV：使用 `auto_sql_query` 返回的 `download_url`
  - 图片：保存到输出目录后，从CSV的 `download_url` 中提取 `base_url`，然后生成 `{{base_url}}/files/{{image_filename}}` 格式的链接
  - 如果 `download_url` 不是HTTP链接，使用默认的 `http://localhost:8000` 作为 `base_url`
- ✅ 最终输出必须是完整的 Markdown 文档，包含：执行摘要、关键指标、趋势分析、可视化图表、数据详情、业务洞察
- ✅ **必须使用 `final_answer(markdown_report)` 返回结果**


**禁止行为：**
- ❌ 禁止使用 `open()` 或 `with open()` 创建或写入文件（包括读取和写入）
- ❌ 禁止编造数据或数字
- ❌ 禁止假设查询成功并继续分析
- ❌ 禁止仅使用 `print()` 作为最终输出

**注意事项：**
- 对于"日活"、"DAU"等概念，通常使用 `$AppStart` 事件
- `auto_sql_query` 会自动添加性能优化条件
- 如果数据异常，要主动指出并给出可能的原因
- 工具错误会自动抛出异常并中断执行，向用户报告错误并说明原因

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

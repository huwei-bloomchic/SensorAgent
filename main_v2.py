#!/usr/bin/env python3
"""
神策数据分析助手 V2 - 双层架构CLI入口

提供交互式命令行界面，使用双层Agent架构
"""
import sys
import os
import json
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import click
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from loguru import logger

from config.settings import get_settings
from src.agents.orchestrator_v2 import create_agent_v2
from src.utils.logger import setup_logger


# 初始化Rich Console用于美化输出
console = Console()


def print_welcome():
    """打印欢迎信息"""
    welcome_text = """
# 神策数据分析助手 V2 (双层架构)

欢迎使用神策数据分析助手 V2！采用双层Agent架构：

## 🏗️ 架构特点

### 上层: 分析规划Agent (The Analyst)
- ✅ 懂业务逻辑和分析方法
- ✅ 理解用户的模糊问题
- ✅ 制定分析计划和指令
- ❌ 不懂SQL，不直接操作数据

### 下层: SQL执行Agent (The Engineer)
- ✅ 懂SQL和数据库表结构
- ✅ 持有字段白名单，确保安全
- ✅ 强制风控机制
- ❌ 不负责复杂的业务归因

## 📊 我可以帮你

- 分析业务趋势和异常
- 生成多维度数据报告
- 自动化数据查询和可视化
- 提供业务洞察和建议

## 使用示例

```
你: 昨天GMV下降了，帮我分析原因
你: 对比最近7天和上周的用户活跃情况
你: 分析各渠道的转化率
```

## 命令

- `help` - 显示帮助信息
- `reset` - 重置对话
- `exit` / `quit` - 退出程序

---
"""
    console.print(Panel(Markdown(welcome_text), title="🤖 神策数据分析助手 V2", border_style="blue"))


def print_help():
    """打印帮助信息"""
    help_text = """
## 可用命令

- `help` - 显示此帮助信息
- `reset` - 重置对话上下文，开始新的对话
- `clear` - 清空屏幕
- `exit` / `quit` - 退出程序

## 查询示例

### 趋势分析
- "分析最近30天的GMV趋势"
- "对比本月和上月的日活"
- "查看最近7天的订单量变化"

### 异常诊断
- "昨天GMV下降了，帮我找原因"
- "为什么今天的用户数这么少？"
- "分析最近的数据异常"

### 多维度分析
- "按渠道分析最近7天的转化率"
- "各品类的销售额对比"
- "不同地区的用户活跃度"

## 双层架构工作流

1. **上层Agent分析**: 理解你的问题，制定分析计划
2. **下层Agent执行**: 生成并执行SQL查询
3. **上层Agent综合**: 整合结果，生成业务洞察

## 优势

- ✅ 业务理解更准确
- ✅ SQL生成更安全
- ✅ 分析更有深度
- ✅ 多步骤自动执行
"""
    console.print(Panel(Markdown(help_text), title="📖 帮助", border_style="green"))


def check_environment():
    """检查环境配置"""
    settings = get_settings()

    issues = []

    # 检查神策配置
    if not settings.SENSORS_API_KEY or settings.SENSORS_API_KEY == "":
        issues.append("⚠️  神策API密钥未配置 (SENSORS_API_KEY)")

    # 检查LLM配置
    if not settings.LITELLM_API_KEY or settings.LITELLM_API_KEY == "your_api_key_here":
        issues.append("⚠️  LLM API密钥未配置 (LITELLM_API_KEY)")

    if issues:
        console.print("[yellow]配置警告:[/yellow]")
        for issue in issues:
            console.print(f"  {issue}")
        console.print("\n请在 .env 文件中配置相关密钥\n")
        return False

    return True


@click.command()
@click.option('--analyst-model', default=None, help='上层分析Agent模型名称')
@click.option('--engineer-model', default=None, help='下层执行Agent模型名称')
@click.option('--api-key', default=None, help='LLM API密钥')
@click.option('--debug', is_flag=True, help='启用调试模式')
def main(analyst_model: str, engineer_model: str, api_key: str, debug: bool):
    """
    神策数据分析助手 V2 - 双层架构交互式CLI

    使用自然语言查询神策数据，通过双层Agent架构获得智能分析结果。
    """
    # 设置日志级别
    if debug:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG")

    try:
        # 打印欢迎信息
        print_welcome()

        # 检查环境配置
        if not check_environment():
            if not click.confirm("是否继续？", default=True):
                return

        # 创建双层Agent
        console.print("[cyan]正在初始化双层Agent架构...[/cyan]")
        console.print("  ├─ 上层: 分析规划Agent")
        console.print("  └─ 下层: SQL执行Agent")

        agent = create_agent_v2(
            analyst_model_name=analyst_model,
            engineer_model_name=engineer_model,
            api_key=api_key
        )
        console.print("[green]✓ 双层Agent初始化完成[/green]\n")

        # 交互循环
        conversation_count = 0
        while True:
            try:
                # 获取用户输入
                user_input = Prompt.ask("\n[bold blue]你[/bold blue]").strip()

                if not user_input:
                    continue

                # 处理命令
                if user_input.lower() in ['exit', 'quit', 'q']:
                    console.print("\n[yellow]再见！👋[/yellow]")
                    break
                elif user_input.lower() == 'help':
                    print_help()
                    continue
                elif user_input.lower() == 'reset':
                    agent.reset()
                    conversation_count = 0
                    console.print("[green]✓ 对话已重置[/green]")
                    continue
                elif user_input.lower() == 'clear':
                    os.system('clear' if os.name != 'nt' else 'cls')
                    print_welcome()
                    continue

                # 处理查询
                console.print("\n[cyan]🤔 上层Agent正在分析问题...[/cyan]")

                response = agent.query(user_input)

                # 显示结果
                console.print("\n[bold green]助手:[/bold green]")

                # 处理不同类型的返回值
                if isinstance(response, dict):
                    # 如果是字典，将其转换为格式化的字符串
                    response_str = json.dumps(response, ensure_ascii=False, indent=2)
                    console.print(Panel(response_str, border_style="green"))
                elif isinstance(response, str):
                    console.print(Panel(response, border_style="green"))
                else:
                    # 其他类型，转换为字符串
                    console.print(Panel(str(response), border_style="green"))

                conversation_count += 1

            except KeyboardInterrupt:
                console.print("\n\n[yellow]检测到中断。输入 'exit' 退出，或继续提问。[/yellow]")
                continue
            except Exception as e:
                logger.exception("处理查询时发生错误")
                console.print(f"\n[red]错误: {str(e)}[/red]")
                console.print("[yellow]请重试或输入 'help' 查看帮助[/yellow]")

    except Exception as e:
        logger.exception("程序启动失败")
        console.print(f"\n[red]启动失败: {str(e)}[/red]")
        console.print("\n请检查：")
        console.print("1. .env 配置文件是否存在且配置正确")
        console.print("2. 依赖包是否已安装 (pip install -r requirements.txt)")
        console.print("3. Python版本是否 >= 3.9")
        sys.exit(1)
    finally:
        # 清理资源
        try:
            if 'agent' in locals():
                agent.close()
        except:
            pass


if __name__ == "__main__":
    main()

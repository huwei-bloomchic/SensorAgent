#!/usr/bin/env python3
"""
神策数据分析助手 - CLI入口

提供交互式命令行界面，用于与神策数据分析Agent对话
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
from src.agents.orchestrator import create_agent
from src.utils.logger import setup_logger


# 初始化Rich Console用于美化输出
console = Console()


def print_welcome():
    """打印欢迎信息"""
    welcome_text = """
# 神策数据分析助手

欢迎使用神策数据分析助手！我可以帮你：

- 📊 查询事件数据（日活、事件次数等）
- 🔍 分析用户行为和趋势
- 📈 生成数据报告
- 🚨 检测数据异常

## 使用示例

```
你: 最近7天的日活是多少？
你: 分析最近30天的购买事件趋势
你: 查询今天iOS平台的页面浏览数
```

## 命令

- `help` - 显示帮助信息
- `reset` - 重置对话
- `exit` / `quit` - 退出程序

---
"""
    console.print(Panel(Markdown(welcome_text), title="🤖 神策数据分析助手", border_style="blue"))


def print_help():
    """打印帮助信息"""
    help_text = """
## 可用命令

- `help` - 显示此帮助信息
- `reset` - 重置对话上下文，开始新的对话
- `clear` - 清空屏幕
- `exit` / `quit` - 退出程序

## 查询示例

### 事件查询
- "最近7天的日活用户数是多少？"
- "查询昨天的应用启动次数"
- "展示最近30天的购买事件趋势"

### 按维度分组
- "按平台统计最近7天的页面浏览量"
- "查看不同地区的用户分布"

### 时间范围
- "today" - 今天
- "yesterday" - 昨天
- "last_7_days" - 最近7天
- "last_30_days" - 最近30天
- "2024-01-01,2024-01-31" - 指定日期范围

## 常用事件名称

- `$AppStart` - 应用启动
- `$PageView` - 页面浏览
- `purchase` - 购买
- `register` - 注册
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
@click.option('--model', default=None, help='LLM模型名称 (如 gpt-4, claude-3-sonnet)')
@click.option('--api-key', default=None, help='LLM API密钥')
@click.option('--debug', is_flag=True, help='启用调试模式')
def main(model: str, api_key: str, debug: bool):
    """
    神策数据分析助手 - 交互式CLI

    使用自然语言查询神策数据，获得智能分析结果。
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

        # 创建Agent
        console.print("[cyan]正在初始化Agent...[/cyan]")
        agent = create_agent(model_name=model, api_key=api_key)
        console.print("[green]✓ Agent初始化完成[/green]\n")

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
                console.print("\n[cyan]思考中...[/cyan]")

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

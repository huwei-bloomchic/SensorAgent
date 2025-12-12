#!/bin/bash

# 神策数据分析助手 - 安装脚本

set -e

echo "=================================="
echo "神策数据分析助手 - 安装脚本"
echo "=================================="
echo ""

# 检查Python版本
echo "检查Python版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python版本: $python_version"

required_version="3.9"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ 错误: 需要Python 3.9或更高版本"
    exit 1
fi
echo "✓ Python版本符合要求"
echo ""

# 创建虚拟环境
echo "创建虚拟环境..."
if [ -d "venv" ]; then
    echo "虚拟环境已存在，跳过创建"
else
    python3 -m venv venv
    echo "✓ 虚拟环境创建成功"
fi
echo ""

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate
echo "✓ 虚拟环境已激活"
echo ""

# 升级pip
echo "升级pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✓ pip已升级"
echo ""

# 安装依赖
echo "安装依赖包..."
pip install -r requirements.txt
echo "✓ 依赖安装完成"
echo ""

# 复制配置文件
echo "配置环境变量..."
if [ -f ".env" ]; then
    echo ".env 文件已存在，跳过复制"
else
    cp .env.example .env
    echo "✓ 已创建 .env 配置文件"
    echo ""
    echo "⚠️  请编辑 .env 文件，填入你的API密钥："
    echo "   - SENSORS_API_KEY (神策API密钥)"
    echo "   - LITELLM_API_KEY (LLM API密钥)"
fi
echo ""

# 创建日志目录
echo "创建日志目录..."
mkdir -p logs
echo "✓ 日志目录创建完成"
echo ""

echo "=================================="
echo "安装完成！"
echo "=================================="
echo ""
echo "下一步："
echo "1. 编辑 .env 文件，填入API密钥"
echo "2. 运行 'source venv/bin/activate' 激活虚拟环境"
echo "3. 运行 'python main.py' 启动CLI"
echo ""
echo "使用 'python main.py --help' 查看更多选项"
echo ""

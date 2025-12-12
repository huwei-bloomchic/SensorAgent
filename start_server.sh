#!/bin/bash
# 神策数据分析助手 - API服务器启动脚本

echo "========================================="
echo "神策数据分析助手 - API Server"
echo "========================================="
echo ""

# 查找正确的Python解释器
# 优先使用 miniconda3 或 conda 环境中的 Python
if [ -f "$HOME/miniconda3/bin/python" ]; then
    PYTHON_CMD="$HOME/miniconda3/bin/python"
elif [ -f "$HOME/anaconda3/bin/python" ]; then
    PYTHON_CMD="$HOME/anaconda3/bin/python"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo "错误: 未找到Python解释器"
    exit 1
fi

# 检查Python版本
python_version=$($PYTHON_CMD --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+' | head -1)
echo "Python路径: $PYTHON_CMD"
echo "Python版本: $python_version"

# 验证FastAPI是否可用
if ! $PYTHON_CMD -c "import fastapi" 2>/dev/null; then
    echo ""
    echo "错误: FastAPI未安装或不在当前Python环境中"
    echo "请运行: $PYTHON_CMD -m pip install -r requirements.txt"
    exit 1
fi

# 检查.env文件
if [ ! -f .env ]; then
    echo "警告: 未找到.env配置文件"
    echo "请复制.env.example并配置相关参数"
    exit 1
fi

echo ""
echo "正在启动API服务器..."
echo "地址: http://0.0.0.0:8000"
echo "API文档: http://0.0.0.0:8000/docs"
echo ""
echo "按 Ctrl+C 停止服务器"
echo "========================================="
echo ""

# 启动服务器
$PYTHON_CMD api_server.py

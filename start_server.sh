#!/bin/bash
# 神策数据分析助手 - API服务器启动脚本

echo "========================================="
echo "神策数据分析助手 - API Server"
echo "========================================="
echo ""

# 检查Python版本
python_version=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+' | head -1)
echo "Python版本: $python_version"

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
python3 api_server.py

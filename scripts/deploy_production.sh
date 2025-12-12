#!/bin/bash
# 生产环境部署脚本

set -e  # 遇到错误立即退出

echo "=========================================="
echo "神策数据分析Agent - 生产环境部署"
echo "=========================================="
echo ""

# 检查必要的环境变量
check_env_var() {
    if [ -z "${!1}" ]; then
        echo "❌ 错误: 环境变量 $1 未设置"
        echo "请在 .env 文件中配置此变量"
        exit 1
    fi
    echo "✅ $1=${!1}"
}

echo "第1步: 检查环境变量配置"
echo "------------------------------------------"

# 加载.env文件
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ 已加载 .env 文件"
else
    echo "❌ 错误: .env 文件不存在"
    exit 1
fi

# 检查必要的环境变量
check_env_var "SENSORS_API_URL"
check_env_var "SENSORS_API_KEY"
check_env_var "LITELLM_API_KEY"
check_env_var "API_BASE_URL"

echo ""
echo "第2步: 创建必要的目录"
echo "------------------------------------------"

# 创建日志目录
mkdir -p logs
echo "✅ 日志目录: logs/"

# 创建CSV输出目录
CSV_DIR=${SQL_OUTPUT_DIR:-/tmp/sensors_data}
mkdir -p "$CSV_DIR"
echo "✅ CSV目录: $CSV_DIR"

echo ""
echo "第3步: 检查Python依赖"
echo "------------------------------------------"

if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: Python3 未安装"
    exit 1
fi

echo "✅ Python版本: $(python3 --version)"

# 检查必要的包
python3 -c "import fastapi, uvicorn, smolagents" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 错误: 缺少必要的Python包"
    echo "请运行: pip install -r requirements.txt"
    exit 1
fi

echo "✅ Python依赖检查通过"

echo ""
echo "第4步: 测试文件下载端点"
echo "------------------------------------------"

# 启动服务器（后台运行）
echo "启动API服务器..."
python3 api_server.py &
SERVER_PID=$!

# 等待服务器启动
sleep 5

# 测试健康检查
echo "测试健康检查端点..."
HEALTH_CHECK=$(curl -s http://localhost:8000/ | python3 -c "import sys, json; print(json.load(sys.stdin).get('status', 'error'))" || echo "error")

if [ "$HEALTH_CHECK" = "ok" ]; then
    echo "✅ 服务器启动成功"
else
    echo "❌ 服务器健康检查失败"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

# 测试文件列表端点
echo "测试文件列表端点..."
FILES_RESPONSE=$(curl -s http://localhost:8000/files)
if [ $? -eq 0 ]; then
    echo "✅ 文件列表端点正常"
else
    echo "❌ 文件列表端点异常"
fi

# 停止测试服务器
kill $SERVER_PID 2>/dev/null
sleep 2

echo ""
echo "第5步: 配置系统服务（可选）"
echo "------------------------------------------"

cat > sensors-agent.service << EOF
[Unit]
Description=Sensors Analytics Agent API Server
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment="PATH=$PATH"
EnvironmentFile=$(pwd)/.env
ExecStart=/usr/bin/python3 $(pwd)/api_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo "系统服务配置文件已生成: sensors-agent.service"
echo ""
echo "如需设置为系统服务，请运行："
echo "  sudo cp sensors-agent.service /etc/systemd/system/"
echo "  sudo systemctl daemon-reload"
echo "  sudo systemctl enable sensors-agent"
echo "  sudo systemctl start sensors-agent"

echo ""
echo "第6步: 配置Nginx反向代理（可选）"
echo "------------------------------------------"

cat > nginx-sensors-agent.conf << EOF
server {
    listen 80;
    server_name your-domain.com;

    # 文件下载端点
    location /files/ {
        proxy_pass http://localhost:8000/files/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;

        # 增加超时时间（大文件下载）
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
    }

    # API端点
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;

        # WebSocket支持（如需）
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF

echo "Nginx配置文件已生成: nginx-sensors-agent.conf"
echo ""
echo "如需配置Nginx，请运行："
echo "  sudo cp nginx-sensors-agent.conf /etc/nginx/sites-available/sensors-agent"
echo "  sudo ln -s /etc/nginx/sites-available/sensors-agent /etc/nginx/sites-enabled/"
echo "  sudo nginx -t"
echo "  sudo systemctl reload nginx"

echo ""
echo "=========================================="
echo "✅ 部署准备完成！"
echo "=========================================="
echo ""
echo "启动命令："
echo "  python3 api_server.py"
echo ""
echo "或使用系统服务："
echo "  sudo systemctl start sensors-agent"
echo ""
echo "API地址："
echo "  健康检查: http://localhost:8000/"
echo "  文件列表: http://localhost:8000/files"
echo "  文件下载: http://localhost:8000/files/<filename>"
echo ""
echo "配置的下载链接基础URL: $API_BASE_URL"
echo ""
echo "查看日志："
echo "  tail -f logs/sensors_agent.log"
echo ""
echo "运行测试："
echo "  python3 test_file_download.py"
echo ""
echo "=========================================="

@echo off
REM 神策数据分析助手 - Windows安装脚本

echo ==================================
echo 神策数据分析助手 - 安装脚本
echo ==================================
echo.

REM 检查Python
echo 检查Python版本...
python --version
if errorlevel 1 (
    echo ❌ 错误: 未找到Python
    echo 请先安装Python 3.9或更高版本
    pause
    exit /b 1
)
echo ✓ Python已安装
echo.

REM 创建虚拟环境
echo 创建虚拟环境...
if exist venv (
    echo 虚拟环境已存在，跳过创建
) else (
    python -m venv venv
    echo ✓ 虚拟环境创建成功
)
echo.

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat
echo ✓ 虚拟环境已激活
echo.

REM 升级pip
echo 升级pip...
python -m pip install --upgrade pip >nul 2>&1
echo ✓ pip已升级
echo.

REM 安装依赖
echo 安装依赖包...
pip install -r requirements.txt
echo ✓ 依赖安装完成
echo.

REM 复制配置文件
echo 配置环境变量...
if exist .env (
    echo .env 文件已存在，跳过复制
) else (
    copy .env.example .env
    echo ✓ 已创建 .env 配置文件
    echo.
    echo ⚠️  请编辑 .env 文件，填入你的API密钥：
    echo    - SENSORS_API_KEY ^(神策API密钥^)
    echo    - LITELLM_API_KEY ^(LLM API密钥^)
)
echo.

REM 创建日志目录
echo 创建日志目录...
if not exist logs mkdir logs
echo ✓ 日志目录创建完成
echo.

echo ==================================
echo 安装完成！
echo ==================================
echo.
echo 下一步：
echo 1. 编辑 .env 文件，填入API密钥
echo 2. 运行 'venv\Scripts\activate.bat' 激活虚拟环境
echo 3. 运行 'python main.py' 启动CLI
echo.
echo 使用 'python main.py --help' 查看更多选项
echo.
pause

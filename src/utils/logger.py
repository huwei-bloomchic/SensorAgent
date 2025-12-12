"""
日志配置模块
使用 loguru 配置日志
"""
import sys
from pathlib import Path
from loguru import logger
from config.settings import get_settings


def setup_logger():
    """配置日志"""
    settings = get_settings()

    # 移除默认的handler
    logger.remove()

    # 日志格式
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    # 添加控制台输出
    if settings.LOG_TO_CONSOLE:
        logger.add(
            sys.stderr,
            format=log_format,
            level=settings.LOG_LEVEL,
            colorize=True,
            backtrace=True,
            diagnose=True
        )

    # 添加文件输出
    if settings.LOG_FILE:
        log_path = Path(settings.LOG_FILE)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        logger.add(
            settings.LOG_FILE,
            format=log_format,
            level=settings.LOG_LEVEL,
            rotation="10 MB",  # 日志文件达到10MB时轮转
            retention="7 days",  # 保留7天的日志
            compression="zip",  # 压缩旧日志
            backtrace=True,
            diagnose=True,
            encoding="utf-8"
        )

    logger.info(f"日志系统已初始化，级别: {settings.LOG_LEVEL}")

    return logger


# 初始化日志
setup_logger()

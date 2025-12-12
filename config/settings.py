"""
配置管理模块
使用 pydantic-settings 从环境变量加载配置
"""
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置类"""

    # ========== 神策数据分析平台配置 ==========
    SENSORS_API_URL: str = Field(
        default="https://sensorsdata-admin.bloomeverybody.work",
        description="神策API URL"
    )
    SENSORS_PROJECT: str = Field(
        default="production",
        description="神策项目名称"
    )
    SENSORS_API_KEY: str = Field(
        default="",
        description="神策API密钥"
    )

    # ========== LiteLLM 配置 ==========
    LITELLM_MODEL: str = Field(
        default="gpt-4",
        description="LLM模型名称"
    )
    LITELLM_API_KEY: str = Field(
        default="",
        description="LiteLLM API密钥"
    )
    LITELLM_BASE_URL: Optional[str] = Field(
        default=None,
        description="LiteLLM API基础URL（可选）"
    )
    LITELLM_TEMPERATURE: float = Field(
        default=0.1,
        ge=0.0,
        le=2.0,
        description="LLM温度参数"
    )
    LITELLM_MAX_TOKENS: int = Field(
        default=4096,
        gt=0,
        description="LLM最大token数"
    )

    # ========== 异常检测配置 ==========
    ANOMALY_DETECTION_ENABLED: bool = Field(
        default=True,
        description="是否启用异常检测"
    )
    ANOMALY_SENSITIVITY: str = Field(
        default="medium",
        pattern="^(low|medium|high)$",
        description="异常检测敏感度"
    )
    ANOMALY_ZSCORE_THRESHOLD: float = Field(
        default=3.0,
        gt=0,
        description="Z-Score阈值"
    )
    ANOMALY_CHECK_INTERVAL: int = Field(
        default=3600,
        gt=0,
        description="异常检查间隔（秒）"
    )

    # ========== 日志配置 ==========
    LOG_LEVEL: str = Field(
        default="INFO",
        pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$",
        description="日志级别"
    )
    LOG_FILE: str = Field(
        default="logs/sensors_agent.log",
        description="日志文件路径"
    )
    LOG_TO_CONSOLE: bool = Field(
        default=True,
        description="是否输出到控制台"
    )

    # ========== 缓存配置 ==========
    CACHE_ENABLED: bool = Field(
        default=True,
        description="是否启用缓存"
    )
    CACHE_TTL: int = Field(
        default=300,
        gt=0,
        description="缓存过期时间（秒）"
    )

    # ========== SQL生成相关配置 ==========
    SQL_OUTPUT_DIR: str = Field(
        default="/tmp/sensors_data",
        description="CSV输出文件目录"
    )
    SQL_TIMEOUT: int = Field(
        default=60,
        gt=0,
        description="SQL执行超时时间（秒）"
    )
    SQL_MAX_RETRIES: int = Field(
        default=3,
        ge=0,
        description="SQL执行最大重试次数"
    )
    IMPALA_VERSION: str = Field(
        default="4.0.0.4258",
        description="Impala版本（用于SQL生成）"
    )
    CSV_CLEANUP_HOURS: int = Field(
        default=24,
        gt=0,
        description="CSV文件保留时间（小时），超时自动清理"
    )

    # ========== 其他配置 ==========
    REQUEST_TIMEOUT: int = Field(
        default=30,
        gt=0,
        description="API请求超时时间（秒）"
    )
    MAX_RETRIES: int = Field(
        default=3,
        ge=0,
        description="最大重试次数"
    )
    RATE_LIMIT: int = Field(
        default=60,
        gt=0,
        description="速率限制（每分钟最大请求数）"
    )
    API_BASE_URL: str = Field(
        default="http://localhost:8000",
        description="API服务器基础URL，用于生成CSV文件下载链接"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    def get_sensitivity_threshold(self) -> float:
        """根据敏感度返回对应的Z-Score阈值"""
        sensitivity_map = {
            "low": 4.0,
            "medium": 3.0,
            "high": 2.0
        }
        return sensitivity_map.get(self.ANOMALY_SENSITIVITY, 3.0)

    @property
    def sensors_config(self) -> dict:
        """返回神策配置字典"""
        return {
            "api_url": self.SENSORS_API_URL,
            "project": self.SENSORS_PROJECT,
            "api_key": self.SENSORS_API_KEY
        }

    @property
    def llm_config(self) -> dict:
        """返回LLM配置字典"""
        config = {
            "model": self.LITELLM_MODEL,
            "api_key": self.LITELLM_API_KEY,
            "temperature": self.LITELLM_TEMPERATURE,
            "max_tokens": self.LITELLM_MAX_TOKENS
        }
        if self.LITELLM_BASE_URL:
            config["base_url"] = self.LITELLM_BASE_URL
        return config


# 全局配置实例
settings = Settings()


def get_settings() -> Settings:
    """获取配置实例"""
    return settings

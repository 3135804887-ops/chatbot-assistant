"""
配置文件
集中管理项目的所有配置参数，包括API密钥、服务配置等
"""

import os
from typing import Optional


class Config:
    """
    配置类，封装所有配置参数
    """
    
    # 智谱AI配置
    ZHIPUAI_API_KEY: str = os.getenv("ZHIPUAI_API_KEY", "")
    ZHIPUAI_MODEL: str = "glm-5"
    ZHIPUAI_TEMPERATURE: float = 1.0
    ZHIPUAI_MAX_TOKENS: int = 65536
    ZHIPUAI_TIMEOUT: int = 30
    
    # 第三方比价API配置
    # 使用Onebound API进行商品比价
    # 官网：https://open.onebound.cn/
    # API文档：http://open.onebound.cn/test/?api_type=taobao&
    
    # Onebound API基础配置
    PRICE_API_BASE_URL: str = "https://api-gw.onebound.cn"
    PRICE_API_KEY: str = os.getenv("PRICE_API_KEY", "t3110960985")  # 你的API Key
    PRICE_API_SECRET: str = os.getenv("PRICE_API_SECRET", "09856fd4")  # 你的API Secret
    PRICE_API_TIMEOUT: int = 10
    PRICE_MAX_RESULTS: int = 10
    
    # API配置选项
    PRICE_API_CACHE: str = "yes"  # 是否使用缓存：yes/no
    PRICE_API_RESULT_TYPE: str = "json"  # 返回数据格式：json/xml
    PRICE_API_LANG: str = "cn"  # 语言：cn/en/ru
    PRICE_API_VERSION: str = "v1"  # API版本
    
    # 系统配置
    MAX_RETRY_TIMES: int = 3
    RETRY_DELAY: float = 1.0
    CACHE_EXPIRE_SECONDS: int = 3600
    
    # Streamlit配置
    PAGE_TITLE: str = "一个聊天机器人"
    PAGE_ICON: str = "🛍️"
    LAYOUT: str = "wide"
    
    @classmethod
    def validate(cls) -> bool:
        """
        验证必要的配置是否完整
        
        Returns:
            bool: 配置是否有效
        """
        if not cls.ZHIPUAI_API_KEY:
            print("警告：未设置智谱AI API密钥，请在环境变量中设置 ZHIPUAI_API_KEY")
            return False
        return True
    
    @classmethod
    def get_zhipuai_config(cls) -> dict:
        """
        获取智谱AI配置字典
        
        Returns:
            dict: 智谱AI配置参数
        """
        return {
            "api_key": cls.ZHIPUAI_API_KEY,
            "model": cls.ZHIPUAI_MODEL,
            "temperature": cls.ZHIPUAI_TEMPERATURE,
            "max_tokens": cls.ZHIPUAI_MAX_TOKENS,
            "timeout": cls.ZHIPUAI_TIMEOUT
        }
    
    @classmethod
    def get_price_api_config(cls) -> dict:
        """
        获取比价API配置字典
        
        Returns:
            dict: 比价API配置参数
        """
        return {
            "base_url": cls.PRICE_API_BASE_URL,
            "api_key": cls.PRICE_API_KEY,
            "timeout": cls.PRICE_API_TIMEOUT,
            "max_results": cls.PRICE_MAX_RESULTS
        }


# 创建全局配置实例
config = Config()

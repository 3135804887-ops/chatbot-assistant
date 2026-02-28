"""
大模型服务模块
封装智谱AI API调用，提供流式对话功能
"""

from typing import Optional
from dataclasses import dataclass
from zai import ZhipuAiClient
from config import config


@dataclass
class Message:
    """
    消息数据类，用于存储对话消息
    """
    role: str
    content: str


class LLMService:
    """
    大模型服务类，封装智谱AI的所有功能
    """
    
    def __init__(self):
        """
        初始化大模型服务
        """
        self.client = None
        self.conversation_history: list[Message] = []
        self._init_client()
    
    def _init_client(self) -> None:
        """
        初始化智谱AI客户端
        """
        try:
            self.client = ZhipuAiClient(api_key=config.ZHIPUAI_API_KEY)
            print("智谱AI客户端初始化成功")
        except Exception as e:
            print(f"智谱AI客户端初始化失败: {e}")
            raise
    
    def chat_stream(self, user_input: str, system_prompt: Optional[str] = None):
        """
        流式对话，返回生成器用于实时输出
        
        Args:
            user_input: 用户输入
            system_prompt: 系统提示词（可选）
        
        Yields:
            str: 每次生成的内容片段
        """
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": user_input})
            
            response = self.client.chat.completions.create(
                model=config.ZHIPUAI_MODEL,
                messages=messages,
                thinking={"type": "enabled"},
                max_tokens=config.ZHIPUAI_MAX_TOKENS,
                temperature=config.ZHIPUAI_TEMPERATURE,
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        
        except Exception as e:
            print(f"调用智谱AI失败: {e}")
            yield f"抱歉，我遇到了一些问题：{str(e)}"
    
    def chat_with_history(self, user_input: str) -> str:
        """
        带历史记录的对话
        
        Args:
            user_input: 用户输入
        
        Returns:
            str: 大模型的完整回复
        """
        try:
            messages = [
                {"role": "system", "content": "你是一个智能助手，可以帮助用户解答问题、提供建议、进行对话交流。"}
            ]
            
            for msg in self.conversation_history:
                messages.append({"role": msg.role, "content": msg.content})
            
            messages.append({"role": "user", "content": user_input})
            
            response = self.client.chat.completions.create(
                model=config.ZHIPUAI_MODEL,
                messages=messages,
                thinking={"type": "enabled"},
                max_tokens=config.ZHIPUAI_MAX_TOKENS,
                temperature=config.ZHIPUAI_TEMPERATURE
            )
            
            reply = response.choices[0].message.content
            
            self.conversation_history.append(Message(role="user", content=user_input))
            self.conversation_history.append(Message(role="assistant", content=reply))
            
            return reply
        
        except Exception as e:
            print(f"调用智谱AI失败: {e}")
            return f"抱歉，我遇到了一些问题：{str(e)}"
    
    def clear_history(self) -> None:
        """
        清空对话历史
        """
        self.conversation_history = []
        print("对话历史已清空")


# 创建全局大模型服务实例
llm_service = LLMService()

# 智能对话助手

基于Streamlit和智谱AI GLM-5大模型的智能对话助手。

## 项目简介

这是一个支持多轮对话的智能助手应用，采用前后端分离架构，实现了对话历史管理、流式输出和数据持久化功能。

## 技术栈

- **前端**: Streamlit
- **大模型**: 智谱AI GLM-5
- **语言**: Python 3.8+
- **存储**: JSON文件

## 功能特性

- 多轮对话支持
- 对话历史管理
- 流式输出
- 数据持久化
- 多对话并行管理

## 本地运行

### 环境要求

- Python 3.8+
- 智谱AI API密钥

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/chatbot-assistant.git
cd chatbot-assistant

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
export ZHIPUAI_API_KEY="your_api_key_here"

# 运行应用
streamlit run streamlit前端.py
```

## 项目结构

```
chatbot-assistant/
├── streamlit前端.py       # 前端主文件
├── llm_service.py         # 大模型服务
├── config.py              # 配置文件
├── conversations.json     # 数据存储
├── requirements.txt       # 依赖列表
└── README.md              # 项目说明
```

## 使用方法

### 基本对话

在输入框中输入问题即可开始对话，例如：
- "推荐一些技术书籍"
- "解释一下机器学习的概念"
- "帮我写一个Python函数"

### 对话管理

- 点击"新对话"创建新的对话
- 左侧显示所有对话历史
- 点击对话标题切换查看
- 点击"删除"移除对话

## 配置说明

### API密钥配置

在环境变量中设置智谱AI API密钥：

```bash
export ZHIPUAI_API_KEY="your_api_key"
```

获取API密钥：https://open.bigmodel.cn/

### 模型配置

在 `config.py` 中可以调整模型参数：
- `ZHIPUAI_MODEL`: 模型选择
- `ZHIPUAI_TEMPERATURE`: 输出随机性
- `ZHIPUAI_MAX_TOKENS`: 最大输出长度

## 部署

详细部署步骤请查看 [DEPLOYMENT.md](DEPLOYMENT.md)

## 开发计划

- [ ] 添加用户认证系统
- [ ] 支持文档问答
- [ ] 集成更多大模型
- [ ] 添加语音交互

## 技术要点

### 流式输出实现

使用生成器实现流式输出，提升用户体验：

```python
def chat_stream(self, user_input: str):
    response = self.client.chat.completions.create(
        model=self.model,
        messages=messages,
        stream=True
    )
    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
```

### 数据持久化

使用JSON文件存储对话历史，实现数据持久化：

```python
def save_conversations():
    with open('conversations.json', 'w', encoding='utf-8') as f:
        json.dump(conversations, f, ensure_ascii=False, indent=2)
```

## 许可证

MIT License

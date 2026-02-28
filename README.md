# 智能对话助手

基于Streamlit和智谱AI GLM-5大模型的智能对话助手，支持多轮对话、对话历史管理和流式输出。

[![Deploy to Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)

## 项目亮点

- **大模型集成**：使用智谱AI GLM-5模型，支持深度思考和推理
- **流式输出**：实时显示AI回复，提升用户体验
- **对话管理**：支持多对话并行管理，自动命名和持久化
- **数据持久化**：JSON文件存储，刷新页面不丢失数据
- **简洁界面**：无emoji设计，专业简洁的用户界面

## 在线演示

访问在线演示：[智能对话助手](https://share.streamlit.io/)

## 功能特性

- 智能对话：基于智谱AI GLM-5大模型，支持多轮对话
- 上下文理解：能够理解对话历史，进行连续对话
- 知识问答：回答各种问题，提供建议和信息
- 模块化设计：代码结构清晰，易于维护和扩展
- 对话历史管理：类似腾讯元宝、豆包的对话历史记录，支持多对话切换
- 流式输出：实时显示AI回复生成过程，提升用户体验
- 多对话支持：同时管理多个独立对话，随时切换查看

## 技术栈

- **前端框架**：Streamlit 1.28+
- **大模型API**：智谱AI GLM-5 (zai-sdk)
- **编程语言**：Python 3.8+
- **数据存储**：JSON文件

## 快速开始

### 本地运行

1. **克隆仓库**
```bash
git clone https://github.com/YOUR_USERNAME/chatbot-assistant.git
cd chatbot-assistant
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置API密钥**

在环境变量中设置智谱AI API密钥：

**Windows (PowerShell):**
```powershell
$env:ZHIPUAI_API_KEY="your_api_key_here"
```

**Linux/Mac:**
```bash
export ZHIPUAI_API_KEY="your_api_key_here"
```

获取API密钥：https://open.bigmodel.cn/

4. **运行应用**
```bash
streamlit run streamlit前端.py
```

5. **访问应用**

浏览器会自动打开 `http://localhost:8501`

### 云端部署

详细部署步骤请查看 [DEPLOYMENT.md](DEPLOYMENT.md)

## 项目结构

```
chatbot-assistant/
├── streamlit前端.py       # Streamlit前端主文件
├── llm_service.py         # 智谱AI大模型服务模块
├── config.py              # 配置文件
├── conversations.json     # 对话历史数据
├── requirements.txt       # Python依赖包
├── README.md              # 项目说明文档
├── DEPLOYMENT.md          # 部署指南
└── .gitignore            # Git忽略文件
```

## 使用说明

### 基本对话

直接在输入框中输入问题，例如：
- "你好"
- "你能做什么？"
- "推荐一些好书"
- "帮我写一段代码"
- "解释一下什么是人工智能"
- "给我一些建议"

### 对话功能

- **多轮对话**：系统能记住对话历史，进行连续对话
- **新对话**：点击左侧边栏的"新对话"按钮，开始新的对话
- **对话历史**：左侧边栏显示所有对话历史，点击可切换查看
- **删除对话**：点击对话旁边的"删除"按钮删除对话
- **自动命名**：新对话会根据第一条消息自动生成标题

## 扩展建议

### 功能扩展
- 知识库集成（RAG）：添加向量数据库，支持文档问答
- 工具调用：让AI调用外部工具和API
- 多模态支持：支持图片、语音输入输出
- 用户认证：添加登录注册功能

### 技术升级
- 后端API：使用FastAPI构建RESTful API
- 数据库：使用SQLite或PostgreSQL存储数据
- 容器化：使用Docker部署
- 监控：添加日志和性能监控

## 常见问题

**Q: 如何更换大模型？**
A: 在 `config.py` 中修改 `ZHIPUAI_MODEL` 参数。

**Q: 如何调整回复风格？**
A: 修改 `llm_service.py` 中的系统提示词。

**Q: 如何部署到云端？**
A: 查看 [DEPLOYMENT.md](DEPLOYMENT.md) 获取详细步骤。

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎通过以下方式联系：
- 提交GitHub Issue
- 发送邮件

---

如果这个项目对你有帮助，请给一个⭐️Star支持一下！
